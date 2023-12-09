
import os
import time
from zipfile import ZipFile
from docxtpl import DocxTemplate
from jinja2 import Template
from .models import MSRProject, FileTransfer
from django.core.files import File


def generate_files():
    """

    :return:
    """
    project = MSRProject.objects.first()
    context = {'project': project}

    files = FileTransfer.objects.filter(filetype='Template')
    for template_file in files:
        # file_name = os.path.splitext(str(template_file.filename()))[0]
        ending = os.path.splitext(str(template_file.filename()))[1]
        new_name = 'NJL-ed@' + time.strftime("%Y%m%d_%H%M%S") + "__" + template_file.filename()
        if ending == '.docx' or ending == '.doc':
            try:
                doc = DocxTemplate('media/' + template_file.filename())
                doc.render(context)
                doc.save(new_name)

                reader = File(open(new_name, 'br'))
                FileTransfer().set_generated_file(template_file.filename(), reader, ending)

                reader.close()
                # os.remove(new_name)

            except Exception as e:
                print('!!!Error docx!!!', e)
        else:   # interpret as a simple text-file
            try:
                t2 = open('media/' + template_file.filename()).read()
                txt_data = Template(t2).render(context)
                writer = File(open(new_name, 'w').write(str(txt_data)))
                # writer.close()

                reader = File(open(new_name, 'br'))
                FileTransfer().set_generated_file(template_file.filename(), reader, ending)

                reader.close()

            except Exception as e:
                print('!!!Error txt!!!', e)
        try:
            os.remove(new_name)
        except Exception as e:
            print('!!Error generating file!!', e)


def generate_zipfile():
    files = FileTransfer.objects.filter(generated=True)
    try:
        with ZipFile('media/NJLed.zip', 'w') as zf:
            for file in files:
                zf.write('media/' + file.filename())
    except Exception as e:
        print('!!Error generating zip-file!!', e)

