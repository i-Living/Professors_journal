from django.contrib import admin
from study.models import Professor, Subject, Subsection, Lesson, Student, StudentLesson

# Register your models here.

class LessonAdmin(admin.ModelAdmin):
    list_display = ('subsection_subject', 'subsection', 'date', 'lesson_type')
    list_filter = ['subsection']

admin.site.register(Lesson, LessonAdmin)
admin.site.register([Professor, Subject, Subsection, Student, StudentLesson])