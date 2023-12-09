
from .models import MSRProject, MSRField, FileTransfer, MSRSite, MSRDevice, MSRCable, MSRSymbol,\
    MSRController, MSRModule, MSRIOFunction, DRVClient

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from admin_ordering.admin import OrderableAdmin


class ProjectInline(admin.TabularInline):
    model = MSRProject
    extra = 0


class FieldInline(admin.TabularInline):
    model = MSRField
    extra = 0


class SiteInline(admin.TabularInline):
    model = MSRSite
    extra = 0


class DeviceInline(admin.TabularInline):
    model = MSRDevice
    extra = 0


class CableInline(admin.TabularInline):
    model = MSRCable
    extra = 0


class SymbolInline(admin.TabularInline):
    model = MSRSymbol
    extra = 0


class ControllerInline(admin.TabularInline):
    model = MSRController
    extra = 0


class ModuleInline(admin.TabularInline):
    model = MSRModule
    extra = 0


class IOFunctionInline(admin.TabularInline):
    model = MSRIOFunction
    extra = 0


class DRVClientInline(admin.TabularInline):
    model = DRVClient
    extra = 0


#   Admin-Classes
class UserAdmin(BaseUserAdmin):
    inlines = [ProjectInline]


@admin.register(MSRProject)
class ProjectModelAdmin(admin.ModelAdmin):
    inlines = [FieldInline]
    list_display = ('name', 'project_ID', 'created_at', 'updated_at', 'creator')
    search_fields = ('name', 'creator')
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


@admin.register(FileTransfer)
class FileTransferAdmin(admin.ModelAdmin):
    # inlines = [FieldInline]
    list_display = ('project', 'name', 'filetype', 'uploaded', 'generated', 'created_at', 'updated_at')
    search_fields = ('name', 'filetype')
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


@admin.register(MSRField)
class FieldAdmin(admin.ModelAdmin):
    inlines = [SiteInline, ControllerInline]
    list_display = ('name', 'assigned', 'created_at', 'updated_at', 'creator')
    search_fields = ('creator', 'name')
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


@admin.register(MSRSite)
class SiteAdmin(admin.ModelAdmin):
    inlines = [DeviceInline]
    list_display = ('name', 'assigned', 'created_at', 'updated_at')
    search_fields = ('name',)
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


@admin.register(MSRDevice)
class DeviceAdmin(admin.ModelAdmin):
    inlines = [SymbolInline, CableInline, IOFunctionInline]
    list_display = ('name', 'assigned', 'devFunction', 'created_at', 'updated_at')
    search_fields = ('name', 'devFunction')
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


@admin.register(MSRCable)
class CableAdmin(admin.ModelAdmin):
    list_display = ('name', 'assigned', 'created_at', 'updated_at')
    search_fields = ('name', )
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


@admin.register(MSRSymbol)
class SymbolAdmin(admin.ModelAdmin):
    list_display = ('name', 'device')
    search_fields = ('name', )
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


@admin.register(MSRController)
class ControllerAdmin(admin.ModelAdmin):
    inlines = [ModuleInline, DRVClientInline]
    list_display = ('name', 'assigned', 'created_at', 'updated_at')
    search_fields = ('name', )
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


@admin.register(MSRModule)
class ModuleAdmin(admin.ModelAdmin):
    inlines = [IOFunctionInline]
    list_display = ('name', 'assigned', 'manufacturer', 'manufactureType', 'slot', 'created_at', 'updated_at')
    search_fields = ('name', 'manufacturer', 'manufactureType', )
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


@admin.register(MSRIOFunction)
class IOFunctionAdmin(OrderableAdmin, admin.ModelAdmin):
    # ordering_field = 'address'
    list_display = ('name', 'address', 'assigned', 'msrModule', 'device', 'objFunction', 'created_at', 'updated_at')
    # list_display_links = ('fullname',)
    # list_editable = ('address',)
    search_fields = ('name', 'objFunction')
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


@admin.register(DRVClient)
class DRVClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'drive_type')
    search_fields = ('name', )
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# register
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
