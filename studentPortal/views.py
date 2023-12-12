from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from .models import *
#todo waitlist

def catalog(request, userID):
    
    user = User.objects.get(pk=userID)
    student = Student.objects.filter(student=user).first()
    
    classes = Class.objects.all()
    classData = []

    if student:
        # If the user is a student
        for classObj in classes:
            enrolled = student in classObj.studentList.all()
            currentStudentCount = classObj.studentList.count()
            waitlistCount = classObj.studentWaitlist.count()

            classData.append({
                "classObj": classObj,
                "currentStudentCount": currentStudentCount,
                "enrolled": enrolled,
                "waitlistCount": waitlistCount
            })
    else:
        # If the user is not a student (instructor)
        for classObj in classes:
            currentStudentCount = classObj.studentList.count()
            waitlistCount = classObj.studentWaitlist.count()

            classData.append({
                "classObj": classObj,
                "currentStudentCount": currentStudentCount,
                "waitlistCount": waitlistCount
            })
        
        return render(request, "studentPortal/instrCatalog.html", {
        "classData": classData,
    })

    return render(request, "studentPortal/catalog.html", {
        "classData": classData,
    })


def createClass(request, userID):
    
    user = User.objects.get(pk=userID)
    
    if request.method == 'POST':
        # Process the form submission to create a new class
        className = request.POST.get('className')
        classNumber = request.POST.get('classNumber')
        classTimings = request.POST.get('classTimings')
        studentLimit = request.POST.get('studentLimit')
        
        # Create a new class
        newClass = Class.objects.create(className=className,classNumber=classNumber,classTimings=classTimings,studentLimit=studentLimit)
        # Add the instructor to the class
        instructor = Instructor.objects.get(instructor=user)
        newClass.instructorClasses.add(instructor)

        # Save the new class
        newClass.save()
        return HttpResponse("Class successfully added")


def createPage(request):
    return render(request, "studentPortal/createPage.html")


def enroll(request, classID, userID):
    user = User.objects.get(pk=userID)
    course = Class.objects.get(pk=classID)
    student = Student.objects.get(student=user)
    classes = Class.objects.all()
    
    #get list of user's classes, check if this course has same time as another in the list
    userClasses = student.classes.all()
    timeConflict = False
    for classObj in userClasses:
        if classObj.classTimings == course.classTimings:
            timeConflict = True
            break
        
    #only add if class not filled already and doesnt conflict with enrolled class times
    currentStudentCount = course.studentList.count()
    if currentStudentCount < course.studentLimit and not timeConflict:
        student.classes.add(course)
        course.studentList.add(student)
        student.save()
        course.save()
    
    else:
        return render(request, "studentPortal/catalog.html", {
            "message": "Unable to enroll: Please check class limit and/or any class time conflicts",
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
    
    #check if students on waitlist, enroll first student if so
    if course.studentWaitlist.count() > 0:
        waitlistStudent = course.studentWaitlist.first() 
        #enroll the student, remove from waitlist
        course.studentList.add(waitlistStudent)
        waitlistStudent.classes.add(course)
        waitlistStudent.classWaitlist.remove(course)
        course.studentWaitlist.remove(waitlistStudent)
        
        course.save()
        waitlistStudent.save()
    
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
            
            #check if user is instructor
            is_instructor = Instructor.objects.filter(instructor=user).exists()

            if is_instructor:
                # Render a template for instructors
                return render(request, "studentPortal/instructor.html", {
                        
                })
            
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
        
        #create student if student was chosen
        if request.POST['userType'] == 'Student':
            firstName = request.POST["firstname"]
            lastName = request.POST["lastname"]
            standing = request.POST["standing"]
            
            student = Student.objects.create(student=user,studentFirstName=firstName,studentLastName=lastName,studentEmail=email,standing=standing)
            student.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        #create instructor if chosen
        if request.POST['userType'] == 'Instructor':
            firstName = request.POST["firstname"]
            lastName = request.POST["lastname"]
            
            instructor = Instructor.objects.create(instructor=user,instructorFirstName=firstName,instructorLastName=lastName,instructorEmail=email)
            instructor.save()
            login(request, user)
            isInstructor = True
            return render(request, "studentPortal/layout.html", {
                "isInstructor": isInstructor
            })
            
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "studentPortal/register.html")
    
    
def viewWaitlist(request, userID):
    user = User.objects.get(pk=userID)
    student = Student.objects.get(student=user)
    studentWaitlist = student.classWaitlist.all()
    
    return render(request, "studentPortal/viewWaitlist.html", {
        "waitlist": studentWaitlist
    })

    
    
def waitlist(request, classID, userID):
    user = User.objects.get(pk=userID)
    course = Class.objects.get(pk=classID)
    student = Student.objects.get(student=user)
    classes = Class.objects.all()
    
    course.studentWaitlist.add(student)
    student.classWaitlist.add(course)
    student.save()
    course.save()
    
    return render(request, "studentPortal/catalog.html", {
        "classes": classes,
        "message": "Class added to waitlist"
    })
    
    
