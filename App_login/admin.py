from django.contrib import admin
from .models import Task, UserSignUp

# Register your models here.
admin.site.register(Task)
admin.site.register(UserSignUp)