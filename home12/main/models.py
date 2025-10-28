from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Student(models.Model):
    name = models.CharField(max_length=30, verbose_name="Имя")
    surname = models.CharField(max_length=30, verbose_name="Фамилия")
    age = models.SmallIntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(100)],
        verbose_name="Возраст"
    )
    sex = models.CharField(
        max_length=10,
        choices=[('m', 'Мужчина'), ('f', 'Женщина')],
        verbose_name="Пол"
    )
    active = models.BooleanField(default=True, verbose_name="Активный")

    course = models.ManyToManyField("Course", blank=True, verbose_name="Курсы")

    def __str__(self):
        return f"{self.surname} {self.name}"


class Course(models.Model):
    langs = [
        ('py', 'Python'),
        ('js', 'JavaScript'),
        ('c', 'C++'),
        ('an', 'Android'),
    ]
    name = models.CharField(choices=langs, max_length=20, verbose_name="Курс")
    course_num = models.SmallIntegerField(default=1, verbose_name="Номер курса")
    start_date = models.DateField(null=True, verbose_name="Начало курса")
    end_date = models.DateField(null=True, verbose_name="Окончание курса")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return f"{self.get_name_display()}-{self.course_num}"


class Grade(models.Model):
    person = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="grades")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    grade = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Оценка"
    )
    date = models.DateField(null=True, verbose_name="Дата оценки")
    date_add = models.DateField(auto_now_add=True)
    date_update = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.person} - {self.course}: {self.grade}"
