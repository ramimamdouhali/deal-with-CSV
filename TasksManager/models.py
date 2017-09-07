from django.db import models
from django.contrib.auth.models import User

# Create your models here.
error_name = {
'required': 'You must type a name !',
'invalid': 'Wrong format.'
}

class UserProfile(models.Model):
    user_auth = models.OneToOneField(User, primary_key=True)
    phone = models.CharField(max_length=20, verbose_name="Phone number", null=True, default=None, blank=True)
    born_date = models.DateField(verbose_name="Born date", null=True, default=None, blank=True)
    last_connection = models.DateTimeField(verbose_name="Date of last connection", null=True, default=None, blank=True)
    years_seniority = models.IntegerField(verbose_name="Seniority", default=0)
    
    def __str__(self):
        return self.user_auth.username
        
    

class Project(models.Model):
    title = models.CharField(max_length=50, verbose_name="Title")
    description = models.CharField(max_length=1000, verbose_name="Description")
    client_name = models.CharField(max_length=1000, verbose_name="Client name")

    def __str__(self):
        return self.title


class Supervisor(UserProfile):
    specialisation = models.CharField(max_length=50, verbose_name="Specialisation")


class Developer(UserProfile):
    supervisor_name = models.ForeignKey(Supervisor, verbose_name="Supervisor")


class Task(models.Model):
    title = models.CharField(max_length=50, verbose_name="Title")
    description = models.CharField(max_length=1000, verbose_name="Description")
    time_elapsed = models.IntegerField(verbose_name="Elapsed time", null=True, default=None, blank=True)
    importance = models.IntegerField(verbose_name="Importance")
    project = models.ForeignKey(Project, verbose_name="Project", null=True, default=None, blank=True)
    app_user = models.ForeignKey(Developer, verbose_name="User")


def user_directory_bath(instance,filename):
    return 'uploadedfiles/user_{0}/{1}'.format(instance.app_user.user_auth,filename)

def user_directory_bathmodified(instance, modifiedfilename):
    return 'modifiedfiles/user_{0}/{1}'.format(instance.app_user.user_auth,modifiedfilename)


# upload_to='uploadedfiles/%y-%m-%d'
class Uploadedfiles(models.Model):
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    YEAR_IN_SCHOOL_CHOICES = (
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
    )

    files = models.FileField(verbose_name="Files", upload_to=user_directory_bath)
    title = models.CharField(max_length=50, verbose_name="File Title")
    description = models.CharField(max_length=1000, verbose_name="Description")
    orginal_headers = models.CharField(max_length=3, choices=YEAR_IN_SCHOOL_CHOICES, default=FRESHMAN)
    selected_headers = models.CharField(max_length=3, default='1')
    modified_file = models.FileField(verbose_name="modified", upload_to=user_directory_bathmodified,null=True)

    app_user = models.ForeignKey(Developer, verbose_name="User")
    