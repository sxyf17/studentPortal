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
    classes = models.ManyToManyField('Class', related_name="classes", blank=True)
    classWaitlist = models.ManyToManyField('Class', related_name="classWaitlist", blank=True)
    
    def __str__(self):
        return f"{self.pk}: {self.studentFirstName} {self.studentLastName}"


class Class(models.Model):
    className = models.CharField(max_length=100)
    classNumber = models.CharField(max_length=8, default=None)
    classTimings = models.CharField(max_length=100)
    studentLimit = models.PositiveIntegerField()
    studentList = models.ManyToManyField(Student, related_name='students', blank=True)
    studentWaitlist = models.ManyToManyField(Student, related_name='studentWaitlist', blank=True)
    
    def __str__(self):
        return f"{self.classNumber} - {self.className}"
    
    
class Instructor(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="instructor")
    instructorFirstName = models.CharField(max_length=200,default=None)
    instructorLastName = models.CharField(max_length=200,default=None)
    instructorEmail = models.CharField(max_length=200)
    classes = models.ManyToManyField('Class', related_name="instructorClasses", blank=True)
    
    def __str__(self):
         return f"{self.pk}: Professor {self.instructorFirstName} {self.instructorLastName}"



