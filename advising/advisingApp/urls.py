from django.conf.urls import url
from django.contrib import admin
from .views import (
	home,
	advisor,
	student,
	degree,
	courses,
	departments,
	prerequisites,
	Takes,
	Contains,
	Chooses
	)

urlpatterns = [
    url(r'^advisor/$', advisor, name='advisor'),
    url(r'^student/$', student, name='student'),
    url(r'^degree/$', degree, name='degree'),
    url(r'^courses/$', courses, name='courses'),
    url(r'^departments/$', departments, name='departments'),
    url(r'^prerequisites/$', prerequisites, name='prerequisites'),
    url(r'^Takes/$', Takes, name='Takes'),
    url(r'^Contains/$', Contains, name='Contains'),
    url(r'^Chooses/$', Chooses, name='Chooses'),
    url(r'^home/$', home, name='home'),

]