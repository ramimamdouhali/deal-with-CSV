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
from TasksManager.views import index, create_supervisor, create_developer


admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/$', index.Home_page, name="Home_page"),
    url(r'^create-developer$', create_developer.page, name="create_developer"),
    url(r'^create-supervisor$', create_supervisor.page, name="create_supervisor"),
   
    
    url(r'^home/my_profile$', index.update_profile, name="my_profile"),
    

    url(r'^modify_my_file/$', index.modify_my_file, name="modify_my_file"),
    url(r'^modify_my_file/file-details-(?P<pk>\d+)$', index.file_details, name="file_details"),
    url(r'^modify_my_file/modified-file-(?P<pk>\d+)$', index.display_modified_file, name="modified_file"),

    url(r'^manage_my_files/$', index.manage_my_files, name="manage_my_files"),
    url(r'^manage_my_files/add_new/$', index.upload_file, name="Upload_New_File"),
    

    url(r'^accounts/',include('django.contrib.auth.urls')),
       
    
]
