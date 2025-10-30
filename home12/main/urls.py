from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),
    path("students/", views.students, name="students"),
    path("students/<int:pk>/", views.student_detail, name="student_detail"),
    path("students/add/", views.student_create, name="student_add"),
    path("students/<int:pk>/edit/", views.student_edit, name="student_edit"),
    path("students/<int:pk>/delete/", views.student_delete, name="student_delete"),
    path("courses/", views.courses, name="courses"),
    path("courses/<int:pk>/", views.course_detail, name="course_detail"),
    path("courses/add/", views.course_create, name="course_add"),
    path("courses/<int:pk>/edit/", views.course_edit, name="course_edit"),
    path("courses/<int:pk>/delete/", views.course_delete, name="course_delete"),
    path("journal/", views.journal, name="journal"),
    path("register/", views.register, name="register"),
]

