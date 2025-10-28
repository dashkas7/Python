from django.shortcuts import render, get_object_or_404
from .models import Student, Course


def home(request):
    return render(request, "home.html")


def students(request):
    return render(request, "students/students_list.html", {"students": Student.objects.all()})


def student_detail(request, pk):
    student = get_object_or_404(Student.objects.prefetch_related("grades__course"), pk=pk)
    return render(request, "students/student_detail.html", {"student": student})


def courses(request):
    return render(request, "courses/courses_list.html", {"courses": Course.objects.all()})


def course_detail(request, pk):
    course = get_object_or_404(Course.objects.prefetch_related("student_set"), pk=pk)
    return render(request, "courses/course_detail.html", {"course": course})


def journal(request):
    students = Student.objects.prefetch_related("grades__course")
    return render(request, "journal.html", {"students": students})
