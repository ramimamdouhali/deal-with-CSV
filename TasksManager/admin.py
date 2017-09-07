from django.contrib import admin
from TasksManager.models import UserProfile, Project, Task, Supervisor, Developer, Uploadedfiles


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Supervisor)
admin.site.register(Developer)
admin.site.register(Uploadedfiles)
