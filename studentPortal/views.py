from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from .models import *
#todo

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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "studentPortal/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
            student.save
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
            
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "studentPortal/register.html")
