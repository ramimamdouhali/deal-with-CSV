from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from TasksManager.forms import Form_upload_file,Form_Developers, Form_User,Form_Profile

from TasksManager.models import Project, Uploadedfiles, Developer, Task,UserProfile
from Work_manager import settings
import csv
from django import forms
import calendar
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json


        

def Home_page(request):    
    return render(request, 'TasksManager/home.html')


@login_required
def update_profile(request):
    currentuser = request.user
    currentdeveloper=Developer.objects.get(user_auth=currentuser)
    my_uploaded_files=Uploadedfiles.objects.filter(app_user=currentdeveloper).order_by("id")

    if request.method=='POST':
        user_form=Form_User(request.POST,instance=request.user)
        profile_form=Form_Profile(request.POST,instance=Developer.objects.get(user_auth=request.user))
        
        if profile_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponse('profile updated successfully')
        else:
            user_form=Form_User(instance=request.user)
            profile_form=Form_Profile(instance=Developer.objects.get(user_auth=request.user))
            return render(request,'TasksManager/my_profile.html',{"user_form":user_form,"profile_form":profile_form, "my_uploaded_files":my_uploaded_files})
    else:
        user_form=Form_User(instance=request.user)
        profile_form=Form_Profile(instance=Developer.objects.get(user_auth=request.user))
        return render(request,'TasksManager/my_profile.html',{"user_form":user_form,"profile_form":profile_form, "my_uploaded_files":my_uploaded_files})

            

@login_required
def manage_my_files(request):
    error=False
    currentuser = request.user
    currentdeveloper=Developer.objects.get(user_auth=currentuser)
    my_uploaded_files=Uploadedfiles.objects.filter(app_user=currentdeveloper).order_by("id")
    action = ""
    if request.method=='POST':
        if 'deletrow' in request.POST:
            selected_rows = request.POST.getlist('deletrow')
        else:
            error = True
        if not error:
            for id in selected_rows:
                row=my_uploaded_files.get(id=id)
                #row=Uploadedfiles.objects.get(id=id)
                row.delete()
            #all_uploaded_files=Uploadedfiles.objects.all()
            action='Files Deleted successfully.'
            return render(request,'TasksManager/manage_my_files.html',{"action":action,"my_uploaded_files":my_uploaded_files})
        else:
            action='You did not select any file'
            return render(request,'TasksManager/manage_my_files.html',{"action":action,"my_uploaded_files":my_uploaded_files})
    else:
        action='Select files to be deleted:'
        return render(request,'TasksManager/manage_my_files.html',{"action":action,"my_uploaded_files":my_uploaded_files})

@login_required
def modify_my_file(request):
    currentuser = request.user
    currentdeveloper=Developer.objects.get(user_auth=currentuser)
    my_uploaded_files = Uploadedfiles.objects.filter(app_user=currentdeveloper).order_by("id")

    if len(my_uploaded_files) >0:
        first_file=my_uploaded_files.first()
        return HttpResponseRedirect('/modify_my_file/file-details-'+ str(first_file.id))
    else:
        action="Start uploading your files"
        return render(request, 'TasksManager/modify_my_file.html', {"action": action, "my_uploaded_files": my_uploaded_files})
        

@login_required
def file_details(request, pk):
    currentuser = request.user
    currentdeveloper=Developer.objects.get(user_auth=currentuser)
    my_uploaded_files = Uploadedfiles.objects.filter(app_user=currentdeveloper)
    #instance_uploaded_file = Uploadedfiles.objects.filter(app_user=currentdeveloper)
    #if len(instance_uploaded_file)<1:
        #return HttpResponseRedirect(reverse('modify_my_file'))

    instance_uploaded_file=my_uploaded_files.get(id=pk)
    path = '{0}/{1}'.format(settings.MEDIA_URL, instance_uploaded_file.files.name)

    csv_file = csv.reader(open(path))

    #csv_file2 = csv.reader(open(instance_uploaded_file.modified_file.name))

    action = "File details: "
    header = next(csv_file)
    column_num = len(header)
    
    original_headers = [(str(i+1), header[i])for i in range(0, column_num)]
    #return HttpResponse(original_headers)
    instance_uploaded_file.orginal_headers = json.dumps(original_headers)
    instance_uploaded_file.save()

    error = False
    #selected_headers=[]
    if request.method == "POST":
        if 'col' in request.POST:
            selected_headers = request.POST.getlist('col')

        else:
            error = True

        if not error:
            
            instance_uploaded_file.selected_headers =json.dumps(selected_headers)
            instance_uploaded_file.save()

            mylist = []
            directory = '{0}/modifiedfiles/user_{1}'.format(settings.MEDIA_URL, instance_uploaded_file.app_user)
            if not os.path.exists(directory):
                os.makedirs(directory)
            path_modified = '{0}/{1}.{2}'.format(directory, instance_uploaded_file.title, 'csv')
            new_csv_file = open(path_modified, 'w')
           
            for row in csv_file:
                mylist.append([row[int(i)-1] for i in selected_headers])
                #line = ""
                #for j in selected_headers:
                    #line += row[int(j)] + ","
                #line += "\n"
                line=", ".join ([row[int(i)-1] for i in selected_headers])
                line+="\n"
                new_csv_file.write(line)
                
            
            instance_uploaded_file.modified_file = path_modified
            instance_uploaded_file.save()
           
            return HttpResponseRedirect('/modify_my_file/modified-file-'+ str(instance_uploaded_file.id))
            #return render(request, 'TasksManager/display_modified_file.html',
                          #{"selected_headers": selected_headers, "original_headers": original_headers,
                           #"file": instance_uploaded_file, "new_csv_file": mylist,"my_uploaded_files":my_uploaded_files})
        else:
            
            return render(request, 'TasksManager/files_details.html',
                          {"action": action, "file_details": instance_uploaded_file, "header": header,
                           "original_headers": original_headers, "csv_file": csv_file,"my_uploaded_files":my_uploaded_files})

    else:
        return render(request, 'TasksManager/files_details.html',
                      {"action": action, "file_details": instance_uploaded_file, "header": header,
                      "original_headers": original_headers,"csv_file": csv_file,"my_uploaded_files":my_uploaded_files})




@login_required
def upload_file(request):
    currentuser = request.user
    currentdeveloper=Developer.objects.get(user_auth=currentuser)
    my_uploaded_files=Uploadedfiles.objects.filter(app_user=currentdeveloper).order_by("id")

    if request.method == 'POST':
        new_file = Uploadedfiles(app_user = currentdeveloper)
        form = Form_upload_file(request.POST, request.FILES,instance=new_file)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/modify_my_file/file-details-'+ str(new_file.id))
            #return HttpResponseRedirect('/modify_my_file/file-details-'+ str({{new_file.id}}))
        else:
            return render(request, 'TasksManager/Upload_File.html', {'form': form,"my_uploaded_files":my_uploaded_files})
    else:
        form = Form_upload_file()
        return render(request, 'TasksManager/Upload_File.html', {'form': form,"my_uploaded_files":my_uploaded_files})

@login_required
def display_modified_file(request,pk):
    currentuser = request.user
    currentdeveloper=Developer.objects.get(user_auth=currentuser)

    action = "display modified file"
    my_uploaded_files = Uploadedfiles.objects.filter(app_user=currentdeveloper)
    instance_uploaded_file = my_uploaded_files.get(id=pk)
    #instance_uploaded_file = Uploadedfiles.objects.get(id=pk)
    path = '{0}'.format(instance_uploaded_file.modified_file.name)
    csv_file = csv.reader(open(path))
    #jsonDec=json.decoder.JSONDecoder()
    
    original_headers = json.loads(instance_uploaded_file.orginal_headers)
    selected_headers= json.loads(instance_uploaded_file.selected_headers)


    return render(request, 'TasksManager/display_modified_file.html',
                          {"original_headers": original_headers,"selected_headers":selected_headers,
                           "file": instance_uploaded_file, "new_csv_file": csv_file,"my_uploaded_files":my_uploaded_files})


