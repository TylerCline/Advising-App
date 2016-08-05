#File: urls.py
#Purpose: To create urls for the website. 
#Author: Tyler Cline
#Ohio University 2016
from django.conf.urls import url, include
from django.contrib import admin
from .views import (
	base,
	report,
	student,
	degree,
	courses,
	Takes,
	takes_update,
	Chooses
	)

urlpatterns = [
    url(r'^report/$', report, name='report'),
    url(r'^student/$', student, name='student'),
    url(r'^degree/$', degree, name='degree'),
    url(r'^courses/$', courses, name='courses'),
    url(r'^Takes/$', Takes, name='Takes'),
    url(r'^Chooses/$', Chooses, name='Chooses'),
    url(r'^base/$', base, name='base'),
    url(r'^takes_update/$', takes_update, name='takes_update')
    # url(r'^accounts/', include('registration.backends.simple.urls'), name='accounts/register'),

]