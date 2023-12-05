from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Teacher(models.Model):
    name = models.CharField(max_length=50)
    students = models.ManyToManyField(Student, related_name='teachers')

    def __str__(self):
        return self.name
