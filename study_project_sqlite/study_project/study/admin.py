from django.contrib import admin
from study.models import Professor, Subject, Subsection, Lesson, Student, StudentLesson

# Register your models here.

admin.site.register([Professor, Subject, Subsection, Lesson, Student, StudentLesson,])