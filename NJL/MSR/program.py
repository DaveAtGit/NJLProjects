import math

from .models import MSRProject, MSRField, FileTransfer, MSRSite, MSRDevice, MSRCable,\
    MSRController, MSRModule, MSRIOFunction, DRVClient
from .program_constants import *

import pandas as pd
import numpy as np


"""
global vars
"""
gMasterList = FileTransfer()
gProject = MSRProject()
gField = MSRField()
gSite = MSRSite()
gDevice = MSRDevice()
gAddress = 0
gAutoAddress = False


# todo: analyse xls-file, raise error if format is not correct
def set_matrix_from_xls(file):
    """
    read a excel-file, to set the matrix
    """
    global gMasterList, gProject
    # clear old MasterList and Matrix
    Matrix.clear()

    master_file = FileTransfer(name='MasterFile', file=file, filetype='Master.xls', uploaded=True)
    master_file.name = master_file.filename()
    master_file.save()

    cnt_tabs = 0
    for tab in TAB_XLS:
        data = pd.read_excel(file,
                             index_col=0,
                             sheet_name=TAB_XLS[cnt_tabs])
        # ..fill up
        Matrix.update(data)
        cnt_tabs += 1

    gMasterList = master_file
    return Matrix


def set_new_template(file):
    """
    read any file and set as template
    """
    template_file = FileTransfer(name=template_filetype, file=file, filetype='Template', uploaded=True)
    template_file.save()


def init_models():
    """
    assign model's keywords from matrix
    """
    global gAddress, gAutoAddress

    if Matrix:
        MSRIOFunction.init_name(Matrix[PRJ_1][prjAE], Matrix[PRJ_1][prjAA], Matrix[PRJ_1][prjDE1], Matrix[PRJ_1][prjDA])
        gAddress = Matrix[ADR_1][adrHardware]
        if Matrix[ADR_1][adrAuto] == 'JA'.casefold():
            gAutoAddress = True
        else:
            gAutoAddress = False


def build_site_field_from_matrix(creator):
    """
    First build-function (SiteField)
    set models of site-field into db by reading the matrix
    """
    global gMasterList, gProject, gField, gSite, gDevice

    if Matrix:
        #   set project
        project_name = Matrix[PRJ_1][prjName]
        project_number = Matrix[PRJ_1][prjNumber]
        gProject = MSRProject().set_object(project_name, project_number, creator)
        gMasterList.project = gProject
        gMasterList.save()

        #   set field and assign project
        field_name = Matrix[PRJ_1][prjField]
        gField = MSRField().set_object(field_name, gProject, creator)

        #   dummy-site and dummy-device for all unassigned objects
        gSite = MSRSite().set_object('Reserve_Site', gField)
        gDevice = MSRDevice().set_object('', 'Reserve_Device', gSite, '', '', '')

        #   declare site, device
        site = None
        device = None

        #   declare keys for old values
        key1_old = ''  # prev site
        key2_old = ''  # prev device
        key3_old = ''  # prev function

        #   counters
        cnt_site_field = 0
        cnt_site = 0
        cnt_device = 0
        cnt_device_fkt = 0

        #   start forming the "site-field"
        i = 1
        for key1 in Matrix[MST_Site]:
            if not pd.isna(key1):    # str(key1).isnumeric():
                key2 = Matrix[MST_Device][i]
                key3 = Matrix[MST_DeviceDivision][i]

                #   first row -> set new site
                if i == 1:
                    site_name = Matrix[MST_Site][i]
                    site = MSRSite().set_object(site_name, gField)

                    device = set_device_from_matrix(i, site)
                    io_function = set_io_from_matrix(i, device)

                    cnt_site_field += 1
                    cnt_site += 1
                    cnt_device += 1
                    cnt_device_fkt += 1
                #   following rows..
                else:
                    #   new site
                    if key1 != key1_old:
                        site_name = Matrix[MST_Site][i]
                        site = MSRSite().set_object(site_name, gField)

                        device = set_device_from_matrix(i, site)
                        io_function = set_io_from_matrix(i, device)

                        cnt_site += 1
                        cnt_device += 1
                        cnt_device_fkt += 1
                    #   old site
                    else:
                        key2 = Matrix[MST_Device][i]
                        # new device
                        if key2 != key2_old:
                            device = set_device_from_matrix(i, site)
                            io_function = set_io_from_matrix(i, device)

                            cnt_device += 1
                            cnt_device_fkt += 1
                        #   old device
                        else:
                            key3 = Matrix[MST_DeviceDivision][i]
                            #   new deviceFunction
                            if key3 != key3_old:
                                io_function = set_io_from_matrix(i, device)

                                cnt_device_fkt += 1
                            #   old deviceFunction
                            else:
                                io_function = set_io_from_matrix(i, device)

                key1_old = key1
                key2_old = key2
                key3_old = key3

                #   end of loop
                i += 1


def build_control_field_from_matrix():
    """
    Second build-function (ControlField)
    set models of control-field into db by reading the matrix
    """

    global gProject, gField, gAutoAddress

    if Matrix:
        controller_ip = str(Matrix[STG_2][stgIP])
        controller_name = Matrix[STG_2][stgName]
        controller_desc = Matrix[STG_2][stgType1]
        controller_manu = Matrix[STG_2][stgManufacturer]
        controller_manu_type = Matrix[STG_2][stgType2]
        controller = MSRController().set_object(controller_ip, controller_name, gField,
                                                controller_desc, controller_manu, controller_manu_type)

        set_cables_from_matrix(gAutoAddress, gProject, gField)
        identify_modules(gAutoAddress, controller)


#   called from: build_control_field_from_matrix()
def set_cables_from_matrix(auto_address, project, field):
    dev_cab_list = [APP_Cable1, APP_Cable2, APP_Cable3, APP_Cable4, APP_Cable5, APP_Cable6]
    pin_list = [CAB_1, CAB_2, CAB_3, CAB_4, CAB_5, CAB_6]

    # desc = ''
    # sect = 0
    actual_page = Matrix[PRJ_1][prjESchemaStart]

    if auto_address:
        sites = MSRSite.objects.filter(field__project__name=project.name). \
            filter(field__name=field.name).order_by('created_at')
        for site in sites:
            devices = MSRDevice.objects.filter(site__name=site.name).order_by('created_at')

            for device in devices:
                # check device-function
                dev_function = device.devFunction
                if dev_function != '':
                    for key in dev_cab_list:
                        if pd.isna(key):
                            pass
                        else:
                            a_cable = Matrix[key][dev_function]
                            cond = pd.isna(a_cable)
                            if not cond:
                                name = Matrix[key][appCabType]
                                desc = Matrix[CAB_Text][a_cable]
                                sect = Matrix[CAB_0][a_cable]
                                actual_page_path = Matrix[key][appPath]
                                MSRCable().set_object(device, name, sect, desc, actual_page, actual_page_path)
                                actual_page += Matrix[PRJ_2][prjESchemaDiff]

    else:
        pass


#   todo; called from: build_site_field_from_matrix()
def set_site_from_matrix(i, field):
    pass


#   called from: build_site_field_from_matrix()
def set_device_from_matrix(i, site):
    """
    sets and returns a device-object filled with data from matrix by index 'i'
    """
    device_function = Matrix[MST_DeviceFunction][i]
    device_name = Matrix[MST_Device][i]
    device_desc = Matrix[MST_DeviceName][i]
    device_man = Matrix[MST_DeviceManufacturer][i]
    device_man_type = Matrix[MST_DeviceType][i]
    device = MSRDevice().set_object(device_function, device_name, site, device_desc, device_man, device_man_type)
    return device


#   called from: build_site_field_from_matrix()
def set_io_from_matrix(i, device):
    """
    sets and returns an io-object filled with data from matrix by index 'i'
    """
    dev_func = str(Matrix[MST_DeviceFunction][i]) + ':' + str(Matrix[MST_DeviceDivision][i])
    io_name = Matrix[MST_DPName][i]
    io_func = Matrix[MST_DPFunction][i]
    io_address = Matrix[MST_DPAddress][i]
    io_comment = Matrix[MST_DPComment][i]
    io_unit = Matrix[MST_DPUnit][i]
    io_ctrl_func = Matrix[MST_DPControlFunction][i]

    j = 1
    io_desc = Matrix[DPT_1][j]
    for key in Matrix[DPT_2]:
        # search/fill in text from DatapointProperties
        if key == Matrix[MST_DPFunction][i][0:3]:
            io_desc = Matrix[DPT_1][j]
        # end of loop
        j += 1

    io_object = MSRIOFunction().set_object(io_name, device, dev_func,
                                           io_func, io_address, io_comment, io_desc, io_unit, io_ctrl_func)

    return io_object


#   called from: build_control_field_from_matrix()
def identify_modules(auto_address, controller):
    """
    analyse which io-functions can be handled by the modules
    """
    global gProject

    modules = {}                # nested dict for all modules!
    MSRModule.index = 1
    module_name_index = []      # list for modules name
    i = 0
    for key1, key2 in zip(Matrix[STG_1][STG_START_INDEX:], Matrix[STG_2][STG_START_INDEX:]):
        index_pos_list = [i for i in range(len(Matrix[STG_2][STG_START_INDEX:]))
                          if Matrix[STG_2][STG_START_INDEX:][i] == str(key2)]
        if index_pos_list:
            module_name_index.append(index_pos_list)
        splitter = str(key1).split()
        rows = []
        j = 0
        for key3 in splitter:
            if MSRIOFunction.objects. \
                    filter(objFunction=key3).\
                    filter(device__site__field__project__project_ID=gProject.project_ID):

                rows.append([Matrix[STG_2][i + STG_START_INDEX],
                             MSRModule.index, key3, Matrix[STG_3][i + STG_START_INDEX]])

                MSRModule.index += 1
            j += 1
        i += 1
        for row in rows:
            modules.setdefault(row[0], {}).setdefault(row[1], {}).setdefault(row[2], row[3])
    MSRModule.index = 0

    """
    When auto-addressing is ordered, set control-modules and address io's.
    Else do nothing.
    """
    if auto_address:
        # print(modules)
        module_interface = {}
        for key, value in modules.items():
            # print("\nModule:", key)
            i = 1
            module_name = key
            io_type_old = ''
            #   empty ios_old
            ios_old = MSRIOFunction.objects.filter(objFunction='')
            value2_old = ''
            if type(value) is dict:
                for key1, value1 in value.items():
                    # print(key1, value1)
                    if type(value1) is dict:
                        for key2, value2 in value1.items():
                            ios = MSRIOFunction.objects.filter(objFunction=key2).\
                                filter(device__site__field__name=gField.name).\
                                filter(device__site__field__project__name=gProject.name)
                            if not ios_old:
                                ios_old = ios
                            io_type = ios.first().objType
                            if io_type == io_type_old:
                                ios |= ios_old
                                # print('union_IOs')
                            else:
                                ios = MSRIOFunction.objects.filter(objFunction=key2).\
                                    filter(device__site__field__name=gField.name).\
                                    filter(device__site__field__project__name=gProject.name)
                                # print('single_IO')
                                if io_type_old:
                                    # print('add different IOs')
                                    module_interface.update({i: {'IOs': ios_old, 'max_IOs': value2_old}})
                                    i += 1
                            ios_old = ios
                            io_type_old = io_type
                            value2_old = value2
            """
            set the module-interface
            """
            # print('setModule!')
            module_interface.update({i: {'IOs': ios_old, 'max_IOs': value2_old}})
            set_modules_auto_addressing(module_interface, module_name, controller)
            module_interface = {}
    else:
        pass
        # print('!controller-modules must be set manually!')


#   called from: identify_modules(...)
def set_modules_auto_addressing(module_interface, module_name, controller):
    """
    set the modules and addresses v2
    """
    global gAddress
    cnt_io = 0
    cnt_modules = 0
    cnt_modules_max = 0
    max_ios_list = []
    io_obj_list = []
    cnt_io_list = []
    module_parts = []
    io_set = []
    for key, value in module_interface.items():
        # print(key, 'Teil-Modul')
        if type(value) is dict:
            for key1, value1 in value.items():
                # print(key1, value1)
                if key1 == 'IOs':
                    # print(value1)
                    ios = value1
                    io_obj_list.append(value1)
                    cnt_io = ios.count()
                    cnt_io_list.append(cnt_io)
                    io_set.append({key: value1})
                if key1 == 'max_IOs':
                    max_io_on_module = value1
                    max_ios_list.append(value1)
                    cnt_modules = MSRModule.cnt_modules(cnt_io, max_io_on_module)
                    module_parts.append({key: value1})
                if cnt_modules > cnt_modules_max:
                    cnt_modules_max = cnt_modules

    # print('io_obj_list: ', io_obj_list)
    nested_list = []
    for i in range(len(module_parts)):
        nested_list.append([])
    i = 0
    for key in io_obj_list:
        for key1 in key:
            nested_list[i].append(key1)
        i += 1
    # nested_list.ordered_by('fullname')
    i = 0
    while i < cnt_modules_max:

        msr_module = MSRModule().set_object(module_name, controller)
        j = 0
        # print('module_part: ', module_parts)
        for keyNumbers in module_parts:
            ind_max_ios = 0
            # print('keyNumbers: ', keyNumbers)
            m_key = 0
            for keyNo in keyNumbers:
                m_key = keyNo

            # print('nested_list: ', nested_list)
            nested_list[0].sort(key=lambda x: x.created_at, reverse=False)
            # sorted(nested_list, key=lambda e: e[1][0], reverse=False)
            # print('nested_list: ', nested_list)

            for key in nested_list[m_key-1][:max_ios_list[j]]:
                io_actual = key
                if io_actual.assigned:
                    pass
                else:
                    io_actual.address = gAddress
                    # print(io_actual)
                    io_actual.update_module(msr_module)
                    nested_list[m_key-1].remove(key)

                    gAddress += 1
                    ind_max_ios += 1

            # print('liste nach schleife: ', nested_list)  # io_obj_list_dummy)

            while ind_max_ios < max_ios_list[j]:
                io_actual = MSRIOFunction().set_object('Res' + str(gAddress), gDevice, '', '', gAddress, '', '', '', '')
                io_actual.update_module(msr_module)
                gAddress += 1
                ind_max_ios += 1

                # print('-> Reserve: ', io_actual.fullname)
            j += 1
        i += 1


def erase_field(project_name, field_name):
    """
    erase all objects from a specific field in a specific project

    :param project_name: name of specified project
    :param field_name: field to erase
    :return:
    """
    MSRIOFunction.objects.filter(device__site__field__project__name=project_name).\
        filter(device__site__field__name=field_name).delete()
    MSRDevice.objects.filter(site__field__project__name=project_name).\
        filter(site__field__name=field_name).delete()
    MSRSite.objects.filter(field__project__name=project_name).\
        filter(field__name=field_name).delete()
    MSRField.objects.filter(project__name=project_name).\
        filter(name=field_name).delete()
    MSRModule.objects.filter(controller__field__project__name=project_name).\
        filter(controller__field__name=field_name).delete()
    MSRController.objects.filter(field__project__name=project_name).\
        filter(field__name=field_name).delete()

    DRVClient.objects.filter(controller__field__project__name=project_name).\
        filter(controller__field__name=field_name).delete()


def erase_project(project_name):
    """
    erase all objects from a specific project

    :param project_name: project to erase
    :return:
    """
    MSRIOFunction.objects.filter(device__site__field__project__name=project_name).delete()
    MSRDevice.objects.filter(site__field__project__name=project_name).delete()
    MSRSite.objects.filter(field__project__name=project_name).delete()
    MSRField.objects.filter(project__name=project_name).delete()
    MSRModule.objects.filter(controller__field__project__name=project_name).delete()
    MSRController.objects.filter(field__project__name=project_name).delete()
    MSRProject.objects.filter(name=project_name).delete()

    FileTransfer.objects.filter(project__name=project_name).delete()

    DRVClient.objects.filter(controller__field__project__name=project_name).delete()


def erase_template_files():
    FileTransfer.objects.filter(filetype=template_filetype).delete()


def erase_templates_from_project(project_name):
    FileTransfer.objects.filter(filetype=template_filetype).filter(project=project_name).delete()


#   !!!for staff only!!!
def erase_all_objects():
    """
    erase all modules from db!
    """
    global gAddress
    gAddress = 0

    MSRIOFunction.objects.all().delete()
    MSRDevice.objects.all().delete()
    MSRCable.objects.all().delete()
    MSRSite.objects.all().delete()
    MSRField.objects.all().delete()
    MSRModule.objects.all().delete()
    MSRController.objects.all().delete()
    MSRProject.objects.all().delete()

    FileTransfer.objects.all().delete()

    DRVClient.objects.all().delete()
    print('!!!all objects deleted!!!')
