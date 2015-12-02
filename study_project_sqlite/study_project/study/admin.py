from django.contrib import admin
from study.models import *


class LessonAdmin(admin.ModelAdmin):
    list_display = ('subsection', 'date', 'lesson_type')

admin.site.register(Lesson, LessonAdmin)
admin.site.register([Professor, Subject, Subsection, Student, StudentLesson])