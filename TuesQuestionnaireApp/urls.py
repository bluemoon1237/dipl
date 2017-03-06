from django.conf.urls import url

import TuesQuestionnaireApp.views as views

urlpatterns = [
    url(r'^$', views.home.index, name="index"),
    url(r'^chooseRole$', views.home.choose_role, name="choose_role"),
    url(r'^teacher/$', views.home.admin_index, name="admin_index"),

    url(r'^courses/$', views.course.index, name="course_index"),
    url(r'^courses/enroll/(?P<course_id>[0-9]+)$', views.course.enroll, name="course_enroll"),
    url(r'^courses/(?P<course_id>[0-9]+)$', views.course.details, name="course_details"),

    url(r'^assignments/(?P<assignment_id>[0-9]+)$', views.assignment.details, name="assignment_details"),
    url(r'^assignments/results/(?P<assignment_id>[0-9]+)$', views.assignment.results, name="assignment_results"),

    url(r'^attempt/(?P<assignment_id>[0-9]+)$', views.attempt.start_attempt, name="start_attempt"),
    url(r'^attempt/answers$', views.attempt.submit_answers, name="submit_answers"),
    url(r'^attempt/finish/(?P<attempt_id>[0-9]+)$', views.attempt.finish_attempt, name="finish_attempt"),
    url(r'^attempt/results/(?P<attempt_id>[0-9]+)$', views.attempt.results, name="attempt_results"),

]
