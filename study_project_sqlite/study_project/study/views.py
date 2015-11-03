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

def to_attendance(request):
    return HttpResponseRedirect('/attendance/' + str(Subject.objects.order_by('id')[0].id))

def to_best_students(request):
    return HttpResponseRedirect('/best_students/' + str(Subject.objects.order_by('id')[0].id))

def to_student(request, student_id):
    return HttpResponseRedirect('/student/' + str(Subject.objects.order_by('id')[0].id) + '/' + str(student_id))

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

def student(request, student_id, subject_id):
    subject = Subject.objects.get(id=subject_id)
    student = Student.objects.get(id=student_id)
    student_info = {}
    subsections = [subsection for subsection in Subsection.objects.order_by('id') if subsection.subject == subject]
    lessons_dict = __get_student_lessons_dict(
        [student_lesson for student_lesson in StudentLesson.objects.order_by('lesson') if student_lesson.lesson.subsection.subject == subject],
        Student.objects.order_by('name'))
    for subsection in subsections:
        counter = 0
        for lesson in lessons_dict[student]:
            if lesson.subsection == subsection:
                counter += 1
        student_info[subsection] = counter
    lessons_info = {}

    lessons = [lesson for lesson in Lesson.objects.order_by('id') if lesson.subsection.subject == subject]
    for subsection in subsections:
        counter = 0
        for lesson in lessons:
            if lesson.subsection == subsection:
                counter += 1
        lessons_info[subsection] = counter
    context = {
        'student_info': student_info,
        'lessons_info': lessons_info,
        'student': student,
        'subject': subject,
        'subjects_list': Subject.objects.order_by('title'),
    }
    return render(request, 'study/student.html', context)

def best_students(request, subject_id):
    result = []
    subject = Subject.objects.get(id=subject_id)
    lessons_list_length = len([lesson for lesson in Lesson.objects.order_by('subsection') if lesson.subsection.subject == subject])
    lessons_dict = __get_student_lessons_dict(
        [student_lesson for student_lesson in StudentLesson.objects.order_by('lesson') if student_lesson.lesson.subsection.subject == subject],
        Student.objects.order_by('name'))
    for student in lessons_dict.keys():
        if len(lessons_dict[student]) == lessons_list_length:
            result.append(student)
    context = {
        'best_students': result,
        'subjects_list': Subject.objects.order_by('title'),
        'subject': subject,
        }
    return render(request, 'study/best_students.html', context)

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