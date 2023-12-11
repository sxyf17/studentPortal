from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from .models import *
#todo 

def catalog(request, userID):
    classes = Class.objects.all()
    user = User.objects.get(pk=userID)
    student = Student.objects.get(student=user)
    
    classData = []
    for classObj in classes:
        enrolled = False
        currentStudentCount = classObj.studentList.count()
        if student in classObj.studentList.all():
            enrolled = True
        
        classData.append({
            "classObj": classObj,
            "currentStudentCount": currentStudentCount,
            "enrolled": enrolled
        })
    
    return render(request, "studentPortal/catalog.html", {
        "classData": classData,
    })


def enroll(request, classID, userID):
    user = User.objects.get(pk=userID)
    course = Class.objects.get(pk=classID)
    student = Student.objects.get(student=user)
    classes = Class.objects.all()
    
    #only add if class not filled already
    currentStudentCount = course.studentList.count()
    if currentStudentCount < course.studentLimit:
        student.classes.add(course)
        course.studentList.add(student)
        student.save()
        course.save()
    
    else:
        return render(request, "studentPortal/catalog.html", {
            "message": "Class limit reached",
            "classes": classes,
            "currentStudentCount": currentStudentCount
        })
    
    return render(request, "studentPortal/catalog.html", {
        "message": "Class added successfully",
        "classes": classes,
        "currentStudentCount": currentStudentCount
    })
    

def unenroll(request, classID, userID):
    user = User.objects.get(pk=userID)
    course = Class.objects.get(pk=classID)
    student = Student.objects.get(student=user)
    classes = Class.objects.all()
    
    
    student.classes.remove(course)
    course.studentList.remove(student)
    student.save()
    course.save()
    
    return render(request, "studentPortal/catalog.html", {
        "message": "Class removed successfully",
        "classes": classes,
    })


def index(request):
    
    return render(request, "studentPortal/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("profile", user.id)
        else:
            return render(request, "studentPortal/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "studentPortal/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def profile(request, userID):
    
    user = User.objects.get(pk=userID)
    student = Student.objects.get(student=user)
    classes = student.classes.all()
    classData = []
    for classObj in classes:
        currentStudentCount = classObj.studentList.count()
        classData.append({
            "classObj": classObj,
            "currentStudentCount": currentStudentCount,
        })
    
    return render(request, "studentPortal/profile.html", {
        "classData": classData,
    })


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "studentPortal/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "studentPortal/register.html", {
                "message": "Username already taken."
            })
        
        #attempt to create student if student was chosen
        if request.POST['userType'] == 'Student':
            firstName = request.POST["firstname"]
            lastName = request.POST["lastname"]
            standing = request.POST["standing"]
            
            student = Student.objects.create(student=user,studentFirstName=firstName,studentLastName=lastName,studentEmail=email,standing=standing)
            student.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
            
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "studentPortal/register.html")
