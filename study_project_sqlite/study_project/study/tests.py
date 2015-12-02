from django.test import TestCase
from datetime import datetime
from .models import StudentLesson, Lesson, Student, Professor, Subject, Professor, Subsection

class StudyTests(TestCase):
    def test_add_lesson(self):
        p = Professor(name='Test')
        p.save()
        s = Subject(professor=p, title='Test')
        s.save()
        ss = Subsection(subject=s, title='Test')
        ss.save()
        l = Lesson(subsection=ss, lesson_type=True, date='2000-01-01')
        l.save()
        response = self.client.get('/attendance/' + str(Subject.objects.order_by('id')[0].id))
        self.assertEqual(response.status_code, 200)

    def test_add_student(self):
        p = Professor(name='Test')
        p.save()
        s = Subject(professor=p, title='Test')
        s.save()
        Student(name='Test').save()
        response = self.client.get('/attendance/' + str(Subject.objects.order_by('id')[0].id))
        self.assertEqual(response.status_code, 200)

    def test_amount_of_attended_lessons_counting(self):
        #init db
        p = Professor(name='Test')
        p.save()
        s = Subject(professor=p, title='Test')
        s.save()
        subsections = []
        lessons = []
        for i in range(1, 10):
            ss = Subsection(subject=s, title='TestSubsection' + str(i))
            ss.save()
            subsections.append(ss)
            l = Lesson(subsection=ss, lesson_type=True, date='2000-01-0' + str(i))
            l.save()
            lessons.append(l)
        st = Student(name='Test')
        st.save()
        #add attendance
        student_lesson_list = []
        #[l1, l2, l3, l4]
        for i in range(4):
            sl = StudentLesson(student=st, lesson=lessons[i])
            sl.save()
            student_lesson_list.append(sl)

        #print([sl.lesson.subsection for sl in student_lesson_list])

        #get page with 5 counted tickets
        response = self.client.post('/student/1/1/', {'amount': 5})

        #print(list(response.context['tickets'])) #[l5, l6, l7, l8, l9]

        #[TestSubsection5, TestSubsection6, TestSubsection7>, <Subsection: TestSubsection8>, <Subsection: TestSubsection9>
        self.assertTrue(set(list(response.context['tickets'])).isdisjoint([sl.lesson.subsection for sl in student_lesson_list]))
