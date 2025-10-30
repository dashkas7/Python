from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student, Course

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["name", "surname", "age", "sex", "active", "photo", "course"]

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name", "course_num", "start_date", "end_date", "description"]