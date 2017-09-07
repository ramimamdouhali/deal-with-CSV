from django.shortcuts import render
from django.http import HttpResponse
from TasksManager.models import Supervisor, Developer
from django import forms
from django.contrib.auth.models import User
# This line imports the Django forms package


class Form_inscription(forms.Form):
# This line creates the form with four fields. It is an object that
#inherits from forms.Form. It contains attributes that define the form
#fields.
    name = forms.CharField(label="Name", max_length=30)
    login = forms.CharField(label="Login", max_length=30)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    supervisor = forms.ModelChoiceField(label="Supervisor",queryset=Supervisor.objects.all())



def page(request):
    if request.POST:
        form = Form_inscription(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']
            
            supervisor = form.cleaned_data['supervisor']
            
            new_user = User.objects.create_user(username = login, password=password)
            new_user.is_active = True
            new_user.last_name=name
            new_user.save()
            
            new_developer = Developer(user_auth = new_user, supervisor_name=supervisor)
            new_developer.save()
            return HttpResponse("Developer added")
        else:
            return render(request, 'TasksManager/create_developer.html', {'form' : form})
    else:
        form = Form_inscription()
        return render(request, 'TasksManager/create_developer.html', {'form' : form})