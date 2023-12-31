from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:userID>/", views.profile, name="profile"),
    path("catalog/<int:userID>/", views.catalog, name="catalog"),
    path("enroll/<int:classID>/<int:userID>", views.enroll, name="enroll"),
    path("unenroll/<int:classID>/<int:userID>", views.unenroll, name="unenroll"),
    path("waitlist/<int:classID>/<int:userID>", views.waitlist, name="waitlist"),
    path("viewWaitlist/<int:userID>", views.viewWaitlist, name="viewWaitlist"),
    path("createClass/<int:userID>", views.createClass, name="createClass"),
    path("createPage", views.createPage, name="createPage")

]