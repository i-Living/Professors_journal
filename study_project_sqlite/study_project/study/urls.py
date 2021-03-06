from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^get_first_subject_attendance', views.get_first_subject_attendance, name='get_first_subject_attendance'),
    url(r'^get_first_subject_tickets', views.get_first_subject_tickets, name='get_first_subject_tickets'),
    url(r'^attendance/(?P<subject_id>[0-9]+)', views.attendance, name='attendance'),
    url(r'^tickets/(?P<subject_id>[0-9]+)', views.tickets, name='tickets'),
    url(r'^student/(?P<subject_id>[0-9]+)/(?P<student_id>[0-9]+)', views.student, name='student'),
    url(r'^confirm_visit/(?P<subject_id>[0-9]+)/(?P<student_id>[0-9]+)/(?P<lesson_id>[0-9]+)/$', views.confirm_visit, name='confirm_visit'),
]