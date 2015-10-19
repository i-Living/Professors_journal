from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^attendance', views.attendance, name='attendance'),
    url(r'^student/(?P<student_id>[0-9]+)', views.student, name='student'),
    url(r'^confirm_visit/(?P<student_id>[0-9]+)/(?P<lesson_id>[0-9]+)/$', views.confirm_visit, name='confirm_visit'),
]