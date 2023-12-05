from django.contrib import admin
from app1.models import Teacher, Student
# Register your models here.

admin.site.register([Student, Teacher])