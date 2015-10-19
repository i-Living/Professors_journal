from django.shortcuts import get_object_or_404, render
from django.template.defaulttags import register
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from .models import Student, StudentLesson, Lesson, Subsection

def __get_student_lessons_dict(students_list):
    student_lesson_list = StudentLesson.objects.order_by('student')
    result = {}
    for student in students_list:
        result[student] = []
        for student_lesson in student_lesson_list:
            if student_lesson.student == student:
                result[student].append(student_lesson.lesson)
    return result

def attendance(request):
    lessons_list = Lesson.objects.order_by('date')
    students_list = Student.objects.order_by('name')
    context = {'result_dict': __get_student_lessons_dict(students_list), 'lessons_list': lessons_list, 'students_list': students_list}
    return render(request, 'study/attendance.html', context)

def home(request):
    return render(request, 'study/index.html')

def student(request, student_id):
    student = Student.objects.get(id=student_id)
    student_info = {}
    lessons_dict = __get_student_lessons_dict(Student.objects.order_by('name'))
    for subsection in Subsection.objects.order_by('id'):
        counter = 0
        for lesson in lessons_dict[student]:
            if lesson.subsection == subsection:
                counter += 1
        student_info[subsection] = counter
    lessons_info = {}
    context = {'student_info': student_info, 'student': student}
    return render(request, 'study/student.html', context)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def check_item(li, value):
    return value in li

def confirm_visit(request, student_id, lesson_id):
    student_lesson_list = StudentLesson.objects.order_by('id')
    is_contain = False
    for student_lesson in student_lesson_list:
        if int(student_lesson.student.id) == int(student_id) and int(student_lesson.lesson.id) == int(lesson_id):
            is_contain = True
            student_lesson.delete()
            break
    if not is_contain:
        new_rec = StudentLesson(student=Student.objects.get(id=student_id), lesson=Lesson.objects.get(id=lesson_id))
        new_rec.save()

    return HttpResponseRedirect(reverse('study:attendance'))