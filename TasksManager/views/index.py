from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from TasksManager.forms import Form_upload_file,Form_Developers
from TasksManager.models import Project, Uploadedfiles, Developer, Task
from Work_manager import settings
import csv
from django import forms
import calendar
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def page(request):    
    action = 'Display all project'
    all_projects = Project.objects.all()
    projects_to_me = Project.objects.filter(client_name="me")
    return render(request, 'TasksManager/index.html', {"action": action, "all_projects": all_projects, "projects_to_me": projects_to_me})

@login_required
def project_details(request,pk):
    action = "display certain project"
    project = Project.objects.get(id=pk)
    return render(request, 'TasksManager/project_details.html', {"action": action, "project_details": project})
@login_required
def manage_my_files(request):
    error=False
    all_uploaded_files=Uploadedfiles.objects.all()
    action = ""
    if request.method=='POST':
        if 'deletrow' in request.POST:
            selected_rows = request.POST.getlist('deletrow')
        else:
            error = True
        if not error:
            for id in selected_rows:
                row=Uploadedfiles.objects.get(id=id)
                row.delete()
            all_uploaded_files=Uploadedfiles.objects.all()
            action='Files Deleted successfully'
            return render(request,'TasksManager/manage_my_files.html',{"action":action,"all_uploaded_files":all_uploaded_files})
        else:
            action='Please select one file atleast'
            return render(request,'TasksManager/manage_my_files.html',{"action":action,"all_uploaded_files":all_uploaded_files})
    else:
        action='Select files to be deleted'
        return render(request,'TasksManager/manage_my_files.html',{"action":action,"all_uploaded_files":all_uploaded_files})

@login_required
def modify_my_file(request):
    all_uploaded_files = Uploadedfiles.objects.all()
    action="Select your file and start modifing"
    return render(request, 'TasksManager/modify_my_file.html', {"action": action, "all_uploaded_files": all_uploaded_files})

@login_required
def file_details(request, pk):
    all_uploaded_files = Uploadedfiles.objects.all()
    instance_uploaded_file = Uploadedfiles.objects.get(id=pk)
    path = '{0}/{1}'.format(settings.MEDIA_URL, instance_uploaded_file.files.name)

    csv_file = csv.reader(open(path))

    #csv_file2 = csv.reader(open(instance_uploaded_file.modified_file.name))

    action = "File details: "
    header = next(csv_file)
    column_num = len(header)
    original_headers = [(str(i), header[i])for i in range(0, column_num)]

    instance_uploaded_file.orginal_headers = original_headers
    instance_uploaded_file.save()

    error = False
    selected_headers=[]
    if request.method == "POST":
        if 'col' in request.POST:
            selected_headers = request.POST.getlist('col')

        else:
            error = True

        if not error:
            instance_uploaded_file.selected_headers = selected_headers
            instance_uploaded_file.save()

            mylist = []
            directory = '{0}/modifiedfiles/user_{1}'.format(settings.MEDIA_URL, instance_uploaded_file.app_user)
            if not os.path.exists(directory):
                os.makedirs(directory)
            path_modified = '{0}/{1}.{2}'.format(directory, instance_uploaded_file.title, 'csv')
            new_csv_file = open(path_modified, 'w')

            for row in csv_file:
                mylist.append([row[int(i)] for i in selected_headers])
                line = ""
                for j in selected_headers:
                    line += row[int(j)] + ","
                line += "\n"
                new_csv_file.write(line)
            instance_uploaded_file.modified_file = path_modified
            instance_uploaded_file.save()

            return render(request, 'TasksManager/display_modified_file.html',
                          {"selected_headers": selected_headers, "original_headers": original_headers,
                           "file": instance_uploaded_file, "new_csv_file": mylist,"all_uploaded_files":all_uploaded_files})
        else:
            return render(request, 'TasksManager/files_details.html',
                          {"action": action, "file_details": instance_uploaded_file, "header": header,
                           "original_headers": original_headers, "csv_file": csv_file,"all_uploaded_files":all_uploaded_files})

    else:
        return render(request, 'TasksManager/files_details.html',
                      {"action": action, "file_details": instance_uploaded_file, "header": header,
                      "original_headers": original_headers,"csv_file": csv_file,"all_uploaded_files":all_uploaded_files})

@login_required
def user_details(request,pk):
    action = "display user details"
    user = Developer.objects.get(id=pk)
    return render(request, 'TasksManager/user_Details.html', {"action": action, "user_details": user})


def add_user(request):
    action = "display user"
    
    if request.method=='POST':
        form = Form_Developers(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse('modify_my_file'))
        else:
            return render(request, 'TasksManager/Upload_File.html', {'form': form})
    else:
        form=Form_Developers()
        return render(request, 'TasksManager/Upload_File.html', {'form': form})

@login_required
def upload_file(request):
    currentuser = request.user
    currentdeveloper=Developer.objects.get(user_auth=currentuser)

    if request.method == 'POST':
        new_file = Uploadedfiles(app_user = currentdeveloper)
        form = Form_upload_file(request.POST, request.FILES,instance=new_file)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse('modify_my_file'))
        else:
            return render(request, 'TasksManager/Upload_File.html', {'form': form})
    else:
        form = Form_upload_file()
        return render(request, 'TasksManager/Upload_File.html', {'form': form})

@login_required
def display_modified_file(request,pk):

    action = "display modified file"
    all_uploaded_files = Uploadedfiles.objects.all()
    instance_uploaded_file = Uploadedfiles.objects.get(id=pk)
    path = '{0}'.format(instance_uploaded_file.modified_file.name)
    csv_file = csv.reader(open(path))

    original_headers = instance_uploaded_file.orginal_headers
    selected_headers=instance_uploaded_file.selected_headers

    return render(request, 'TasksManager/display_modified_file.html',
                          {"original_headers": original_headers,"selected_headers":selected_headers,
                           "file": instance_uploaded_file, "new_csv_file": csv_file,"all_uploaded_files":all_uploaded_files})


