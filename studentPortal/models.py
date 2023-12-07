from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    def __str__(self):
        return f"{self.username}, {self.email}"
    

class Student(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student")
    studentFirstName = models.CharField(max_length=200,default=None)
    studentLastName = models.CharField(max_length=200,default=None)
    studentEmail = models.CharField(max_length=200)
    standing = models.CharField(max_length=8)
    
    def __str__(self):
        return f"{self.pk}: {self.studentFirstName}"


class Class(models.Model):
    className = models.CharField(max_length=100)
    classTimings = models.CharField(max_length=100)
    studentLimit = models.PositiveIntegerField()
    studentList = models.ManyToManyField(Student, related_name='students', blank=True)
    
    def __str__(self):
        return f"{self.className}"



