from django.shortcuts import get_object_or_404, render
from django.template.defaulttags import register
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from .models import Student, StudentLesson, Lesson, Subsection, Subject

def __get_student_lessons_dict(student_lesson_list, students_list):
    result = {}
    for student in students_list:
        result[student] = []
        for student_lesson in student_lesson_list:
            if student_lesson.student == student:
                result[student].append(student_lesson.lesson)
    return result

def __get_student_lessons_dict2(student_lesson_list, students_list):
    result = {}
    for student in students_list:
        result[student] = []
        for student_lesson in student_lesson_list:
            if student_lesson.student == student:
                result[student].append(student_lesson.lesson)
    return result

def get_first_subject(request):
    return HttpResponseRedirect('/attendance/' + str(Subject.objects.order_by('id')[0].id))

def attendance(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    student_lesson_list = StudentLesson.objects.order_by("student")
    lessons_list = [lesson for lesson in Lesson.objects.order_by('date') if lesson.subsection.subject == subject]
    students_list = Student.objects.order_by('name')
    context = {
        'result_dict': __get_student_lessons_dict(student_lesson_list, students_list),
        'lessons_list': lessons_list,
        'students_list': students_list,
        'subject': subject,
        'subjects_list': Subject.objects.order_by('title'),
    }
    return render(request, 'study/attendance.html', context)

def home(request):
    return render(request, 'study/index.html')

def student(request, student_id):
    student = Student.objects.get(id=student_id)
    student_info = {}
    lessons_dict = __get_student_lessons_dict(StudentLesson.objects.order_by('student'), Student.objects.order_by('name'))
    for subsection in Subsection.objects.order_by('id'):
        counter = 0
        for lesson in lessons_dict[student]:
            if lesson.subsection == subsection:
                counter += 1
        student_info[subsection] = counter
    lessons_info = {}
    for subsection in Subsection.objects.order_by('id'):
        counter = 0
        for lesson in Lesson.objects.order_by('id'):
            if lesson.subsection == subsection:
                counter += 1
        lessons_info[subsection] = counter


    context = {'student_info': student_info, 'lessons_info': lessons_info, 'student': student}
    return render(request, 'study/student.html', context)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def check_item(li, value):
    return value in li

def confirm_visit(request, subject_id, student_id, lesson_id):
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
    return HttpResponseRedirect(reverse('study:attendance', args=[subject_id]))