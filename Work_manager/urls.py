"""Work_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from TasksManager.views import index, connection, create_supervisor, create_developer,create_project


admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/$', index.page, name="public_index"),
    url(r'^connection/$', connection.page, name="public_connection"),
    url(r'^home/project-detail-(?P<pk>\d+)$', index.project_details, name="project_detail"),
    
    url(r'^uploaded_files/user-details-(?P<pk>\d+)$', index.user_details, name="user_details"),
    url(r'^create-developer$', create_developer.page, name="create_developer"),
    url(r'^create-supervisor$', create_supervisor.page, name="create_supervisor"),
    url(r'^create_project$', create_project.page, name='create_project'),

    url(r'^modify_my_file/$', index.modify_my_file, name="modify_my_file"),
    url(r'^modify_my_file/file-details-(?P<pk>\d+)$', index.file_details, name="file_details"),
    url(r'^modify_my_file/modified-file-(?P<pk>\d+)$', index.display_modified_file, name="modified_file"),

    url(r'^manage_my_files/$', index.manage_my_files, name="manage_my_files"),
    url(r'^manage_my_files/add_new/$', index.upload_file, name="Upload_New_File"),
    #url(r'^manage_my_files/file-details-(?P<pk>\d+)$', index.file_details, name="file_details2"),
    #url(r'^manage_my_files/modified-file-(?P<pk>\d+)$', index.display_modified_file, name="modified_file2"),

    url(r'^accounts/',include('django.contrib.auth.urls')),
       
    
]
