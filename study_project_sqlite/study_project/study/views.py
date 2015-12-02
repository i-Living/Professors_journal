from django.shortcuts import get_object_or_404, render
from django.template.defaulttags import register
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from .models import Student, StudentLesson, Lesson, Subsection, Subject

#return dictionary "student: list of attended lessons"
def __get_student_lessons_dict(student_lesson_list, students_list):
    result = {}
    for student in students_list:
        result[student] = []
        for student_lesson in student_lesson_list:
            if student_lesson.student == student:
                result[student].append(student_lesson.lesson)
    return result

#return dictionary "subsection: amount of attendance" for the student
def __get_student_info(lessons_dict, subsections_list, student):
    student_info = {}
    for subsection in subsections_list:
        counter = 0
        for lesson in lessons_dict[student]:
            if lesson.subsection == subsection:
                counter += 1
        student_info[subsection] = counter
    return student_info

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

def student(request, subject_id, student_id):
    student = Student.objects.get(id=student_id)
    subject = Subject.objects.get(id=subject_id)
    student_lessons = []
    lessons_dict = __get_student_lessons_dict(StudentLesson.objects.order_by('student'), Student.objects.order_by('name'))
    subsections_list = Subsection.objects.filter(subject=subject)
    student_info = __get_student_info(lessons_dict, subsections_list, student)
    lessons_info = {}
    for subsection in subsections_list:
        counter = 0
        for lesson in Lesson.objects.order_by('id'):
            if lesson.subsection == subsection:
                counter += 1
        lessons_info[subsection] = counter
    #subsection: percentage 4 student
    student_percentage = {}
    for subsection in subsections_list:
        student_percentage[subsection] = int(student_info[subsection] * 100 / (lessons_info[subsection] if lessons_info[subsection] > 0 else 1))
    amount = 0
    tickets = []
    try:
        amount = int(request.POST['amount'])
        import operator
        tickets = [item[0] for item in sorted(student_percentage.items(), key=operator.itemgetter(1))[0:amount]]
    except:
        pass
    context = {
        'student_info': student_info,
        'lessons_info': lessons_info,
        'student': student,
        'subjects_list': Subject.objects.order_by('title'),
        'student_percentage': student_percentage,
        'tickets': tickets
        }
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