from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^to_attendance', views.to_attendance, name='to_attendance'),
    url(r'^to_best_students', views.to_best_students, name='to_best_students'),
    url(r'^to_student/(?P<student_id>[0-9]+)', views.to_student, name='to_student'),
    url(r'^attendance/(?P<subject_id>[0-9]+)', views.attendance, name='attendance'),
    url(r'^student/(?P<subject_id>[0-9]+)/(?P<student_id>[0-9]+)', views.student, name='student'),
    url(r'^best_students/(?P<subject_id>[0-9]+)', views.best_students, name='best_students'),
    url(r'^confirm_visit/(?P<subject_id>[0-9]+)/(?P<student_id>[0-9]+)/(?P<lesson_id>[0-9]+)/$', views.confirm_visit, name='confirm_visit'),
]