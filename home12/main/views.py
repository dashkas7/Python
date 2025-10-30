from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, StudentForm, CourseForm
from .models import Student, Course

def home(request):
    return render(request, "home.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("main:home")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


def students(request):
    students = Student.objects.all()
    return render(request, "students/students_list.html", {"students": students})

def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, "students/student_detail.html", {"student": student})


@login_required
def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("main:students")
    else:
        form = StudentForm()
    return render(request, "students/student_form.html", {"form": form})

@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect("main:students")
    else:
        form = StudentForm(instance=student)
    return render(request, "students/student_form.html", {"form": form})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect("main:students")


def courses(request):
    courses = Course.objects.all()
    return render(request, "courses/courses_list.html", {"courses": courses})

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, "courses/course_detail.html", {"course": course})

@login_required
def course_create(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("main:courses")
    else:
        form = CourseForm()
    return render(request, "courses/course_form.html", {"form": form})

@login_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect("main:courses")
    else:
        form = CourseForm(instance=course)
    return render(request, "courses/course_form.html", {"form": form})

@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    return redirect("main:courses")


def journal(request):
    students = Student.objects.prefetch_related("grades__course").all()
    return render(request, "journal.html", {"students": students})