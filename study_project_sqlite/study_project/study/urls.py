from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^get_first_subject', views.get_first_subject, name='get_first_subject'),
    url(r'^attendance/(?P<subject_id>[0-9]+)', views.attendance, name='attendance'),
    url(r'^student/(?P<subject_id>[0-9]+)/(?P<student_id>[0-9]+)', views.student, name='student'),
    url(r'^confirm_visit/(?P<subject_id>[0-9]+)/(?P<student_id>[0-9]+)/(?P<lesson_id>[0-9]+)/$', views.confirm_visit, name='confirm_visit'),
]