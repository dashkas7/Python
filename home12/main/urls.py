from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),
    path("students/", views.students, name="students"),
    path("students/<int:pk>/", views.student_detail, name="student_detail"),
    path("courses/", views.courses, name="courses"),
    path("courses/<int:pk>/", views.course_detail, name="course_detail"),
    path("journal/", views.journal, name="journal"),
]
