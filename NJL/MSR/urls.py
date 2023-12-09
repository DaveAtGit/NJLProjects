
# from django.conf.urls import url
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
# from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('', views.go_home, name='home'),
    path('MSR/selector/', views.selector, name='selector'),
    path('MSR/selector/<int:project_id>/', views.selector, name='selector'),
    path('MSR/selector/generator/<int:project_id>/', views.generator, name='generator'),
    path('MSR/selector/transmit/<int:project_id>/', views.transmitter, name='transmit'),
    path('MSR/erase_project/<int:project_id>/', views.erase_specific_project, name='erase_project'),
    path('MSR/uploader', views.uploader, name='uploader'),
    path('MSR/downloader', views.downloader, name='downloader'),
    path('MSR/eraser/<int:erase_id>/', views.eraser, name='eraser'),

    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),

    path('project', views.project_api, name='project_api'),

    # url(r'^department$', views.departmentApi),
    # url(r'^department/([0-9]+)$', views.departmentApi),
    # url(r'^employee$', views.employeeApi),
    # url(r'^employee/([0-9]+)$', views.employeeApi),
    # url(r'^employee/savefile', views.SaveFile)

]

