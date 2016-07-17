from django.conf.urls import url, include
from django.contrib import admin
from .views import (
	base,
	report,
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
    url(r'^report/$', report, name='report'),
    url(r'^student/$', student, name='student'),
    url(r'^degree/$', degree, name='degree'),
    url(r'^courses/$', courses, name='courses'),
    url(r'^departments/$', departments, name='departments'),
    url(r'^prerequisites/$', prerequisites, name='prerequisites'),
    url(r'^Takes/$', Takes, name='Takes'),
    url(r'^Contains/$', Contains, name='Contains'),
    url(r'^Chooses/$', Chooses, name='Chooses'),
    url(r'^base/$', base, name='base'),
    url(r'^accounts/', include('registration.backends.simple.urls'), name='accounts/register'),

]