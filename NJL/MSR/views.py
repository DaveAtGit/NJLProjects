import os
import time
from zipfile import ZipFile
from django.core.files.storage import default_storage
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import MSRProjectSerializer, MSRFieldSerializer
from docxtpl import DocxTemplate
from jinja2 import Template, TemplateError
from django.core.files import File
from .models import MSRProject, FileTransfer, DRVClient
from .program import set_matrix_from_xls, set_new_template, init_models, \
    build_site_field_from_matrix, build_control_field_from_matrix, \
    erase_all_objects, erase_project, erase_template_files
from .forms import FileUploadForm, RegistrationForm, AccountAuthenticationForm

from .gen_files import generate_files, generate_zipfile
# from .serializers import MasterDPLSerializer

# from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout


# from rest_framework.views import APIView
# from rest_framework.response import Response


def go_home(request):
    """
    :param request:
    :return: home.html
    """
    projects = MSRProject.objects.all()
    # session-tests...
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    if request.user.get_username() == 'ravey':
        request.session['name'] = 'Ravey-Session!'
    else:
        request.session['name'] = 'Any-Session!'
    #

    return render(request, 'home.html', {
        'projects': projects,  # !required in base.html!
    })


def uploader(request):
    """
    :param request:
    sets the matrix or a new template
    :return: uploader.html
    """
    projects = MSRProject.objects.all()
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        for filename, file in request.FILES.items():
            # name = request.FILES[filename].name
            if filename == 'mstList':
                file = request.FILES['mstList']
                matrix = set_matrix_from_xls(file)

                # user who upload masterList
                user = request.user

                #   set models
                init_models()
                build_site_field_from_matrix(user)
                build_control_field_from_matrix()

                return render(request, 'uploader.html', {
                    'matrix': matrix,
                    'projects': projects,
                })
            elif filename == 'newTemplate':
                file = request.FILES['newTemplate']
                set_new_template(file)

    return render(request, 'uploader.html', {
        'projects': projects,  # !required in base.html!
    })


def downloader(request):
    """
    :param request:
    generates files with the available templates
    :return: downloader.html
    """
    projects = MSRProject.objects.all()
    try:
        generate_files()
        generate_zipfile()
        return render(request, 'downloader.html', {
            'projects': projects,  # !required in base.html!
        })
    except ValueError:
        go_home(request)


def eraser(request, erase_id):
    """
    :param request:
    erases specific objects
    :return: erase_all.html
    """
    projects = MSRProject.objects.all()
    if request.method == 'POST':
        if erase_id == 1:
            erase_all_objects()
        if erase_id == 2:
            erase_template_files()
    # return redirect("/")
    return render(request, 'eraser.html', {
        'projects': projects,  # !required in base.html!
    })


def selector(request, project_id):
    """
    :param request:
    :return: home.html
    """
    projects = MSRProject.objects.all()
    the_project = MSRProject.objects.filter(project_ID=str(project_id))[0]
    # myvar = request.GET['myvar']
    # print(myvar)

    return render(request, 'selector.html', {
        'projects': projects,  # !required in base.html!
        'the_project': the_project,
    })


def generator(request, project_id):
    """
    :param request:
    :return: home.html
    """
    projects = MSRProject.objects.all()
    the_project = MSRProject.objects.filter(project_ID=str(project_id))[0]

    context = {'project': the_project}

    files = FileTransfer.objects.filter(filetype='Template')
    for template_file in files:
        ending = os.path.splitext(str(template_file.filename()))[1]
        new_name = 'NJLed_at_' + time.strftime("%YY%mM%dD%Hh%Mm%Ss") + "__" + template_file.filename()
        if ending == '.docx' or ending == '.doc':
            try:
                doc = DocxTemplate('media/' + template_file.filename())
                doc.render(context)
                doc.save(new_name)

                reader = File(open(new_name, 'br'))
                FileTransfer().set_project_generated_file(the_project, template_file.filename(), reader, ending)

                reader.close()
                # os.remove(new_name)

            except Exception as e:
                print('!!!Error docx!!!', e)
        else:  # interpret as a simple text-file
            try:
                t2 = open('media/' + template_file.filename()).read()
                txt_data = Template(t2).render(context)
                writer = File(open(new_name, 'w').write(str(txt_data)))
                # writer.close()

                reader = File(open(new_name, 'br'))
                FileTransfer().set_project_generated_file(the_project, template_file.filename(), reader, ending)

                reader.close()

            except Exception as e:
                print('!!!Error txt!!!', e)
        try:
            os.remove(new_name)
        except Exception as e:
            print('!!Error FileAccess!!', e)

    return render(request, 'selector.html', {
        'projects': projects,  # !required in base.html!
        'the_project': the_project,
    })


def erase_specific_project(request, project_id):
    projects = MSRProject.objects.all()
    the_project = MSRProject.objects.filter(project_ID=str(project_id))[0]
    if request.method == 'POST':
        erase_project(the_project)
    # return redirect("/")
    return render(request, 'home.html', {
        'projects': projects,  # !required in base.html!
    })


#   not in use!
def register(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('/')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'register.html', context)


#   not in use!
def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('/')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('/')

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')


def transmitter(request, project_id):
    """
    scan given project for controllers.
    :param request:
    :param project_id:
    :return:
    """
    projects = MSRProject.objects.all()
    the_project = MSRProject.objects.filter(project_ID=str(project_id))[0]

    for field in the_project.Field.all():
        print(field.name)
        for controller in field.Controller.all():
            print(controller.name)
            for driver in controller.Driver.all():
                print(driver.name)
                try:
                    client = driver.set_client()
                    if client:
                        ## todo: check for connection success
                        client.connect()
                        print(controller.fullname, "is connected")
                        ## single command
                        # DRVClient.read_modbus(driver, client)
                        # client.close()

                        # thread
                        dt = DRVClient.poll_modbus_thread(driver, client, controller)
                        dt.daemon = True
                        dt.start()
                        #dt.join()
                        print(controller.fullname, "thread started")

                except Exception as e:
                    print('!!Error Driver!!', e)

    # context = {'project': the_project}

    return render(request, 'selector.html', {
        'projects': projects,
        'the_project': the_project,
    })


'''
!!Serializers!!
'''


@csrf_exempt
def project_api(request, ident=0):
    if request.method == 'GET':
        projects = MSRProject.objects.all()
        projects_serializer = MSRProjectSerializer(projects, many=True)
        return JsonResponse(projects_serializer.data, safe=False)
    elif request.method == 'POST':
        project_data = JSONParser().parse(request)
        projects_serializer = MSRProjectSerializer(data=project_data)
        if projects_serializer.is_valid():
            projects_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == 'PUT':
        project_data = JSONParser().parse(request)
        project = MSRProject.objects.get(project_ID=project_data['project_ID'])
        projects_serializer = MSRProjectSerializer(project, data=project_data)
        if projects_serializer.is_valid():
            projects_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update")
    elif request.method == 'DELETE':
        project = MSRProject.objects.get(project_ID=ident)
        project.delete()
        return JsonResponse("Deleted Successfully", safe=False)

# @csrf_exempt
# def departmentApi(request,id=0):
#     if request.method=='GET':
#         departments = Departments.objects.all()
#         departments_serializer=DepartmentSerializer(departments,many=True)
#         return JsonResponse(departments_serializer.data,safe=False)
#     elif request.method=='POST':
#         department_data=JSONParser().parse(request)
#         departments_serializer=DepartmentSerializer(data=department_data)
#         if departments_serializer.is_valid():
#             departments_serializer.save()
#             return JsonResponse("Added Successfully",safe=False)
#         return JsonResponse("Failed to Add",safe=False)
#     elif request.method=='PUT':
#         department_data=JSONParser().parse(request)
#         department=Departments.objects.get(DepartmentId=department_data['DepartmentId'])
#         departments_serializer=DepartmentSerializer(department,data=department_data)
#         if departments_serializer.is_valid():
#             departments_serializer.save()
#             return JsonResponse("Updated Successfully",safe=False)
#         return JsonResponse("Failed to Update")
#     elif request.method=='DELETE':
#         department=Departments.objects.get(DepartmentId=id)
#         department.delete()
#         return JsonResponse("Deleted Successfully",safe=False)
#
# @csrf_exempt
# def employeeApi(request,id=0):
#     if request.method=='GET':
#         employees = Employees.objects.all()
#         employees_serializer=EmployeeSerializer(employees,many=True)
#         return JsonResponse(employees_serializer.data,safe=False)
#     elif request.method=='POST':
#         employee_data=JSONParser().parse(request)
#         employees_serializer=EmployeeSerializer(data=employee_data)
#         if employees_serializer.is_valid():
#             employees_serializer.save()
#             return JsonResponse("Added Successfully",safe=False)
#         return JsonResponse("Failed to Add",safe=False)
#     elif request.method=='PUT':
#         employee_data=JSONParser().parse(request)
#         employee=Employees.objects.get(EmployeeId=employee_data['EmployeeId'])
#         employees_serializer=EmployeeSerializer(employee,data=employee_data)
#         if employees_serializer.is_valid():
#             employees_serializer.save()
#             return JsonResponse("Updated Successfully",safe=False)
#         return JsonResponse("Failed to Update")
#     elif request.method=='DELETE':
#         employee=Employees.objects.get(EmployeeId=id)
#         employee.delete()
#         return JsonResponse("Deleted Successfully",safe=False)
#
# @csrf_exempt
# def SaveFile(request):
#     file=request.FILES['file']
#     file_name=default_storage.save(file.name,file)
#     return JsonResponse(file_name,safe=False)