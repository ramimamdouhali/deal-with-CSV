from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from TasksManager.models import Supervisor, Developer
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
# This line imports the Django forms package


class Form_inscription(forms.Form):
# This line creates the form with four fields. It is an object that
#inherits from forms.Form. It contains attributes that define the form
#fields.
    name = forms.CharField(label="Name", max_length=30)
    username = forms.CharField(label="User Name", max_length=30)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    #supervisor = forms.ModelChoiceField(label="Supervisor",queryset=Supervisor.objects.all())
    email = forms.EmailField(label = "Email")


def page(request):
    if request.POST:
        form = Form_inscription(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            
            #supervisor = form.cleaned_data['supervisor']
            
            new_user = User.objects.create_user(username = username, password=password,email=email)
            new_user.is_active = True
            new_user.last_name=name
            new_user.save()
            
            new_developer = Developer(user_auth = new_user)#, supervisor_name=supervisor
            new_developer.save()
            messages.info(request,"Thanks for registering. Now you are logging in")
            new_user= authenticate(username=username, password=password)
            login(request, new_user)

            return HttpResponseRedirect('/modify_my_file')
        else:
            return render(request, 'TasksManager/create_developer.html', {'form' : form})
    else:
        form = Form_inscription()
        return render(request, 'TasksManager/create_developer.html', {'form' : form})