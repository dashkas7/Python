from django.contrib import admin
from django.db.models import Avg
from .models import Student, Course, Grade


class GradeInline(admin.TabularInline):
    model = Grade
    extra = 1
    fields = ("course", "grade", "date")
    ordering = ("-date",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("surname", "name", "sex", "short_name", "avg_grade", "courses_list")
    list_display_links = ("surname", "name")
    search_fields = ("surname", "name")
    list_filter = ("sex", "active")
    filter_horizontal = ("course",)
    inlines = [GradeInline]

    def short_name(self, obj):
        return f"{obj.surname} {obj.name[0]}."

    def avg_grade(self, obj):
        res = obj.grades.aggregate(avg=Avg("grade"))
        return round(res["avg"], 2) if res["avg"] else "—"

    def courses_list(self, obj):
        return ", ".join(str(c) for c in obj.course.all())


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "course_num", "start_date", "end_date")
    list_filter = ("name", "course_num")
    search_fields = ("description",)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("person", "course", "grade", "date")
    list_filter = ("course", "grade", "date")
    search_fields = ("person__surname", "person__name")
