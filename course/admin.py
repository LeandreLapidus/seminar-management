from django.contrib import admin

from course.forms import CourseChangeForm, CourseCreateForm, TrainerForm
from course.models import Course, Trainer

# Register your models here.
@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "subjects", "email")
    form = TrainerForm

@admin.register(Course)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "location", "subject", "date_scheduled", "trainer")
    add_form = CourseCreateForm
    form = CourseChangeForm