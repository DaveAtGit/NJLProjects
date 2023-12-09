
import os
import time

from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import User, AbstractUser, Group
from django.core.validators import FileExtensionValidator

from pymodbus3.client.sync import ModbusTcpClient as ModbusClient


class BaseMSR(models.Model):
    """
    abstract BaseClass for most MSR-objects: top of inheritance
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    assigned = models.BooleanField(default=False)
    autoName = models.BooleanField(default=True)
    name = models.CharField(max_length=128, default='set Name')  # required
    nickname = models.CharField(max_length=32, default='', blank=True)

    sep = ':'
    dummyName = 'setName!'

    class Meta:
        abstract = True


class MSRProject(models.Model):
    """
    Project:
    """
    objects = None
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=128, default='set Name')  # required
    project_ID = models.CharField(max_length=32)  # required
    users = models.ManyToManyField(Group)
    creator = models.ForeignKey(User, related_name='Project', verbose_name='Creator', default='',
                                on_delete=models.SET_NULL, null=True)
    photo = models.ImageField(upload_to='pics', default='', blank=True)

    class Meta:
        verbose_name = 'A1 Project'
        verbose_name_plural = 'A1 Projects'

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def set_object(self, name, project_id, creator):
        existing_project = MSRProject.objects.filter(project_ID=project_id)
        if not existing_project:
            the_project = self
            the_project.name = name
            the_project.project_ID = project_id
            the_project.creator = creator
            the_project.save()
            print('new Project created')
        else:
            the_project = existing_project.first()
            print('!wanted Project already exists!')
        return the_project

    def update_object(self):
        pass

    def get_fields(self):
        return self.Field.all()

    def get_users(self):
        return self.users.all()


@receiver(pre_save, sender=MSRProject)
def set_project_object(sender, instance, **kwargs):
    instance.update_object()


class FileTransfer(models.Model):
    """
    Files:
    """
    objects = None
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(MSRProject, related_name='File', verbose_name='Project', default='',
                                on_delete=models.SET_NULL, null=True, blank=True)
    path = ''
    name = models.CharField(max_length=128, default=BaseMSR.dummyName)  # required
    file = models.FileField(upload_to=path)
    filetype = models.CharField(max_length=16, blank=True)
    uploaded = models.BooleanField(default=False)
    generated = models.BooleanField(default=False)

    class Meta:
        verbose_name = '0 Transfer file'
        verbose_name_plural = '0 Transfer files'

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def filename(self):
        return os.path.basename(self.file.name)

    def set_upload_file(self, name, file, filetype):
        self.path = 'upload'
        self.uploaded = True
        self.name = name
        self.filetype = filetype
        self.file = file
        return self

    def set_generated_file(self, name, file, filetype):
        self.path = 'download'
        self.generated = True
        self.name = name
        self.filetype = filetype
        self.file = file
        self.save()
        return self

    def set_project_generated_file(self, project, name, file, filetype):
        self.project = project
        self.path = 'download'
        self.generated = True
        self.name = name
        self.filetype = filetype
        self.file = file
        self.save()
        return self

    def set_path(self, path):
        pass


@receiver(pre_delete, sender=FileTransfer)
def delete_file_upload(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)


class MSRField(models.Model):
    """
    Field:
    """
    objects = None
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    assigned = models.BooleanField(default=False)
    autoName = models.BooleanField(default=True)
    name = models.CharField(max_length=128, default='set Name')
    nickname = models.CharField(max_length=128, default='', blank=True)
    creator = models.ForeignKey(User, related_name='Field', verbose_name='Creator', default='',
                                on_delete=models.SET_NULL, null=True)
    photo = models.ImageField(upload_to='pics', default='', blank=True)
    project = models.ForeignKey(MSRProject, related_name='Field', verbose_name='Project', default='',
                                on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'A2 Field'
        verbose_name_plural = 'A2 Fields'

    def __str__(self):
        return self.nickname

    def __repr__(self):
        return self.name

    def set_object(self, nickname, project, creator):
        existing_site_field = MSRField.objects.\
            filter(project__name=project.name).\
            filter(nickname=nickname)
        if not existing_site_field:
            the_field = self
            the_field.project = project
            the_field.nickname = nickname
            the_field.creator = creator
            the_field.save()
            print('new Field created')
        else:
            the_field = existing_site_field.first()
            print('!wanted Field already exists!')
        return the_field

    def update_object(self):
        if self.autoName:
            if self.project:
                self.assigned = True
                self.name = self.project.name + BaseMSR.sep + self.nickname
            else:
                self.assigned = False

    def get_sites(self):
        return self.Site.all()

    def get_controllers(self):
        return self.Controller.all()


@receiver(pre_save, sender=MSRField)
def set_field_object(sender, instance, **kwargs):
    instance.update_object()


class MSRSite(BaseMSR):
    """
    Site:
    """
    objects = None

    desc = models.CharField(max_length=64, default='', blank=True)
    field = models.ForeignKey(MSRField, related_name='Site', verbose_name='Field', default='',
                              on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'B1 Site'
        verbose_name_plural = 'B1 Sites'

    def __str__(self):
        return self.nickname

    def __repr__(self):
        return self.name

    def set_object(self, nickname, field):
        existing_site = MSRSite.objects. \
            filter(field__name=field.name). \
            filter(nickname=nickname)

        if not existing_site:
            the_site = self
            the_site.field = field
            the_site.nickname = nickname
            the_site.save()
            print('new Site created')
        else:
            the_site = existing_site.first()
            print('!wanted Site already exists!')
        return the_site

    def update_object(self):
        if self.autoName:
            if self.field:
                self.assigned = True
                if self.nickname:
                    self.name = self.field.name + self.sep + self.nickname
                    # self.fullname = self.field.fullname + self.sep + self.nickname
                else:
                    self.name = self.field.name + self.dummyName
                    # self.fullname = self.field.fullname
            else:
                self.assigned = False

    def get_devices(self):
        return self.Device.all()


@receiver(pre_save, sender=MSRSite)
def set_site_object(sender, instance, **kwargs):
    instance.update_object()


class MSRDevice(BaseMSR):
    """
    Device:
    """
    objects = None

    devFunction = models.CharField(max_length=64, default='', verbose_name='Function', blank=True)
    desc = models.CharField(max_length=64, default='', blank=True)
    manufacturer = models.CharField(max_length=64, default='', verbose_name='Manufacturer', blank=True)
    manufactureType = models.CharField(max_length=64, default='', verbose_name='Type', blank=True)
    photo = models.FileField(upload_to='pics/device', validators=[FileExtensionValidator(allowed_extensions=['svg'])],
                             default='', blank=True)
    site = models.ForeignKey(MSRSite, related_name='Device', verbose_name='Site', default='',
                             on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'B2 Device'
        verbose_name_plural = 'B2 Devices'

    def __str__(self):
        return self.nickname

    def __repr__(self):
        return self.name

    def set_object(self, function, nickname, site, desc, manufacturer, manufacturer_type):
        existing_device = MSRDevice.objects. \
            filter(site__name=site.name). \
            filter(nickname=nickname)

        if not existing_device:
            the_device = self
            the_device.site = site
            the_device.nickname = nickname
            the_device.desc = desc
            the_device.manufacturer = manufacturer
            the_device.manufactureType = manufacturer_type
            the_device.devFunction = function
            the_device.save()
            print('new Device created')
        else:
            the_device = existing_device.first()
            print('!wanted Device already exists!')
        return the_device

    def update_object(self):
        if self.autoName:
            if self.site:
                self.assigned = True
                if self.nickname:
                    # self.nickname = self.site.nickname + self.sep + self.nickname
                    self.name = self.site.name + self.sep + self.nickname
                else:
                    self.name = self.site.nickname + self.dummyName
                    # self.fullname = self.site.fullname
            else:
                self.assigned = False

    def get_ios(self):
        return self.IOFunction_D.all()

    def set_cables(self):
        pass

    def get_cables(self):
        return self.Cable.all()


@receiver(pre_save, sender=MSRDevice)
def set_device_object(sender, instance, **kwargs):
    instance.update_object()


class MSRCable(BaseMSR):
    """
    Cable:
    """
    objects = None

    page = models.IntegerField(default=0, verbose_name='Page', blank=True)
    page_path = models.IntegerField(default=0, verbose_name='Page-Path', blank=True)
    description = models.CharField(max_length=64, default='', verbose_name='Description', blank=True)
    crossSection = models.DecimalField(default=0, verbose_name='Cross Section', max_digits=5, decimal_places=2, blank=True)
    device = models.ForeignKey(MSRDevice, related_name='Cable', verbose_name='Device', default='',
                               on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'B2.1 Cable'
        verbose_name_plural = 'B2.1 Cables'

    def __str__(self):
        return self.nickname

    def __repr__(self):
        return self.name

    def set_object(self, device, nickname, cross_section, description, page, page_path):
        existing_cable = MSRCable.objects. \
            filter(device__name=device.name). \
            filter(nickname=nickname)

        if not existing_cable:
            self.device = device
            self.nickname = nickname
            self.crossSection = cross_section
            self.description = description
            self.page = page
            self.page_path = page_path
            the_cable = self
            self.save()
            print('new Cable created')
        else:
            the_cable = existing_cable.first()
            print('!wanted Cable already exists!')
        return the_cable

    def update_object(self):
        if self.autoName:
            if self.device:
                self.assigned = True
                if self.nickname:
                    self.name = self.device.name + self.sep + self.nickname
                else:
                    self.name = self.device.name + self.sep + self.dummyName
            else:
                self.assigned = False


@receiver(pre_save, sender=MSRCable)
def set_cable_object(sender, instance, **kwargs):
    instance.update_object()


#
class MSRSymbol(models.Model):

    class SymbolType(models.TextChoices):
        ANY_BUS = '000', 'not defined'
        SENSOR = '001', 'Sensor'
        PUMP = '002', 'Pump'
        VALVE_2W = '003', 'Valve 2-way'
        VALVE_3W = '004', 'Valve 3-way'

    symbol_type = models.CharField(max_length=3, choices=SymbolType.choices, default='000')

    name = models.CharField(max_length=128, default='symbols name')
    symbol = models.FileField(upload_to='pics/symbol', validators=[FileExtensionValidator(allowed_extensions=['svg'])],
                             default='', blank=True)
    device = models.ForeignKey(MSRDevice, related_name='Symbol', verbose_name='Device', default='',
                               on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'B2.2 Symbol'
        verbose_name_plural = 'B2.2 Symbols'

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class MSRController(BaseMSR):
    """
    Controller:
    """
    objects = None

    desc = models.CharField(max_length=64, default='', blank=True)
    ipaddress = models.CharField(max_length=15, default='', blank=True)
    manufacturer = models.CharField(max_length=64, default='', verbose_name='Manufacturer', blank=True)
    manufactureType = models.CharField(max_length=64, default='', verbose_name='Type', blank=True)
    photo = models.ImageField(upload_to='pics/controller', default='', blank=True)
    field = models.ForeignKey(MSRField, related_name='Controller', verbose_name='C_Field', default='',
                              on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'C1 Controller'
        verbose_name_plural = 'C1 Controllers'

    def __str__(self):
        return self.nickname

    def __repr__(self):
        return self.name

    def set_object(self, ip_address, nickname, field, desc, manufacturer, manufacturer_type):
        existing_controller = MSRController.objects.\
            filter(field__name=field.name).\
            filter(nickname=nickname)
        if not existing_controller:
            the_controller = self
            the_controller.ipaddress = ip_address
            the_controller.field = field
            the_controller.desc = desc
            the_controller.manufacturer = manufacturer
            the_controller.manufactureType = manufacturer_type
            the_controller.nickname = nickname
            the_controller.save()
            print('new Controller created')
        else:
            the_controller = existing_controller.first()
            print('!wanted Controller already exists!')
        return the_controller

    def update_object(self):
        if self.autoName:
            if self.field:
                self.assigned = True
                if self.nickname:
                    self.name = self.field.name + self.sep + self.nickname
                else:
                    self.name = self.field.name + self.sep + self.dummyName
            else:
                self.assigned = False

    def get_modules(self):
        return self.Module.all()


@receiver(pre_save, sender=MSRController)
def set_controller_object(sender, instance, **kwargs):
    instance.update_object()


class MSRModule(BaseMSR):
    """
    Module:
    """
    objects = None
    MAX_IO = 'max_IO'
    IO_TYPE = 'IO_Type'
    NAME = 'name'
    index = 0       # module-index, is added to nickname
    ioCounter = 0
    max_io = 0
    typeCounter = 0
    setOfModules = []

    slot = models.IntegerField(default=0, blank=True)
    desc = models.CharField(max_length=64, default='', blank=True)
    manufacturer = models.CharField(max_length=64, default='', verbose_name='Manufacturer', blank=True)
    manufactureType = models.CharField(max_length=64, default='', verbose_name='Type', blank=True)
    photo = models.ImageField(upload_to='pics/module', default='', blank=True)
    controller = models.ForeignKey(MSRController, related_name='Module', verbose_name='Controller', default='',
                                   on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'C2 Module'
        verbose_name_plural = 'C2 Modules'

    def __str__(self):
        return self.nickname

    def __repr__(self):
        return self.name

    def set_object(self, nickname, controller):
        existing_module = MSRModule.objects.\
            filter(controller__name=controller.name).\
            filter(nickname=nickname)
        if not existing_module:
            MSRModule.index += 1
            the_module = self
            the_module.slot = MSRModule.index
            the_module.typeCounter += 1
            the_module.controller = controller
            the_module.nickname = nickname + '_' + str(self.slot)
            the_module.save()
            print('new Module created')
        else:
            the_module = existing_module.first()
            print('!wanted Module already exists!')
        return the_module

    def update_object(self):
        if self.autoName:
            if self.controller:
                self.assigned = True
                if self.nickname:
                    self.name = self.controller.name + self.sep + self.nickname
                else:
                    self.name = self.controller.name + self.sep + self.dummyName
            else:
                self.assigned = False

    def get_ios(self):
        return self.IOFunction_M.all()

    @staticmethod
    def cnt_modules(cnt, max_io_on_module):
        if max_io_on_module > 0:
            if cnt % max_io_on_module:
                cnt_modules = cnt // max_io_on_module + 1
            else:
                cnt_modules = cnt // max_io_on_module
            return cnt_modules
        else:
            return 0


@receiver(pre_save, sender=MSRModule)
def save_module_object(sender, instance, **kwargs):
    instance.update_object()


class MSRIOFunction(BaseMSR):
    """
    IO's:
    """
    objects = None
    NONE = 'None'
    AE = 'AE'
    AA = 'AA'
    DE = 'DE'
    DA = 'DA'

    address = models.IntegerField(default=0, blank=True)
    objType = models.CharField(max_length=16, default=NONE)  # required
    comment = models.CharField(max_length=64, default='', blank=True)
    objFunction = models.CharField(max_length=16, default=NONE)  # required
    hardware = models.BooleanField(default=True, blank=True)
    desc = models.CharField(max_length=64, default='', blank=True)
    control = models.CharField(max_length=8, verbose_name='logic-parameter', default='', blank=True)
    value = models.IntegerField(default=0, blank=True)
    unit = models.CharField(max_length=8, default='', blank=True)
    msrModule = models.ForeignKey(MSRModule, related_name='IOFunction_M', verbose_name='Module',
                                  on_delete=models.CASCADE, null=True, blank=True)
    device = models.ForeignKey(MSRDevice, related_name='IOFunction_D', verbose_name='Device', default='',
                               on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'D IOFunction'
        verbose_name_plural = 'D IOFunctions'

    def __str__(self):
        return self.nickname

    def __repr__(self):
        return self.name

    @classmethod
    def init_name(cls, ae_name, aa_name, de_name, da_name):
        cls.AE = ae_name
        cls.AA = aa_name
        cls.DE = de_name
        cls.DA = da_name

    #   todo: dev_func...?
    def set_object(self, nickname, device, dev_func,
                   io_func, io_address, io_comment, io_desc, io_unit, io_ctrl_func):
        existing_io = MSRIOFunction.objects.\
            filter(device__name=device.name).\
            filter(nickname=nickname)
        if not existing_io:
            the_io = self
            the_io.device = device
            the_io.address = io_address
            the_io.comment = io_comment
            the_io.desc = io_desc
            the_io.unit = io_unit
            the_io.control = io_ctrl_func
            the_io.objFunction = io_func[0:3]
            if io_func[0:2] == the_io.AE[0:2]:
                the_io.objType = 'AE'
            elif io_func[0:2] == the_io.AA[0:2]:
                the_io.objType = 'AA'
            elif io_func[1:2] == the_io.DE[1:2]:
                the_io.objType = 'DE'
            elif io_func[0:2] == the_io.DA[0:2]:
                the_io.objType = 'DA'
            else:
                the_io.objType = the_io.NONE
            the_io.nickname = nickname
            the_io.save()
            print('new IO created')
        else:
            the_io = existing_io.first()
            print('!wanted IO already exists!')
        return the_io

    def update_module(self, msr_module):
        the_io = self
        the_io.msrModule = msr_module
        the_io.save()
        if the_io.assigned:
            pass
        else:
            the_io.msrModule = msr_module
            the_io.save()
        print('IO assigned to module')

    def update_object(self):
        if self.autoName:
            if self.device and self.msrModule:
                self.assigned = True
            else:
                self.assigned = False
            if self.nickname:
                self.name = self.device.name + self.sep + self.nickname
            else:
                self.name = self.device.name + self.sep + self.dummyName


@receiver(pre_save, sender=MSRIOFunction)
def save_io_function_object(sender, instance, **kwargs):
    instance.update_object()


# todo: Modbus deactivated

class DRVClient(models.Model):

    class DRVType(models.TextChoices):
        ANY_BUS = 'A', 'not defined'
        MODBUS_TCP = 'B', 'Modbus TCP'
        MODBUS_RTU = 'C', 'Modbus RTU'
        BACNET = 'D', 'BACnet'

    drive_type = models.CharField(max_length=2, choices=DRVType.choices, default='A')

    name = models.CharField(max_length=128, default='clients name')
    controller = models.ForeignKey(MSRController, related_name='Driver', verbose_name='Controller', default='',
                                   on_delete=models.SET_NULL, null=True, blank=True)

    def set_drive_type(self, drive_type):
        self.drive_type = drive_type

    def set_name(self, name):
        self.name = name

    class Meta:
        verbose_name = 'Z01 Driver-Client'
        verbose_name_plural = 'Z01 Driver-Clients'

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def set_client(self):
        ip_adr = self.controller.ipaddress
        if self.drive_type == self.DRVType.MODBUS_TCP:
            port_nr = 502   # ModbusTCP
            client = ModbusClient(ip_adr, port_nr)
        else:
            client = -1
        return client

    def read_modbus(self, client):
        for mod in self.controller.Module.all():
            for ioFunc in mod.IOFunction_M.all():
                if ioFunc.objType[0:1] == 'A':    # 'Analog':
                    print("read_modbus: start reading:", ioFunc.address)
                    rr = client.read_holding_registers(ioFunc.address + 1, 1, unit=0)
                    assert (rr.function_code < 0x80)  # test that we are not an error
                    print("read_modbus: Zuweisung")
                    ioFunc.value = rr.registers[0]
                    ioFunc.save()
                if ioFunc.objType[0:1] == 'D':     # 'Digital':
                    rc = client.read_coils(ioFunc.address + 1, 1, unit=1)
                    assert (rc.function_code < 0x80)  # test that we are not an error
                    ioFunc.value = rc.bits[0]
                    ioFunc.save()

                #print(ioFunc.address)

    def poll_modbus_thread(self, client, controller):
        while True:
            for mod in controller.Module.all():
                for ioFunc in mod.IOFunction_M.all():
                    if ioFunc.objType[0:1] == 'A':  # 'Analog':
                        rr = client.read_holding_registers(ioFunc.address + 1, 1, unit=0)
                        assert (rr.function_code < 0x80)  # test that we are not an error
                        ioFunc.value = rr.registers[0]
                        ioFunc.save()
                    if ioFunc.objType[0:1] == 'D':  # 'Digital':
                        rc = client.read_coils(ioFunc.address + 1, 1, unit=1)
                        assert (rc.function_code < 0x80)  # test that we are not an error
                        ioFunc.value = rc.bits[0]
                        ioFunc.save()
            print(controller.fullname, "Thread alive")
            time.sleep(2)


"""
Tests
"""
