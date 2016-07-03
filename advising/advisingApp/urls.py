from django.conf.urls import url
from django.contrib import admin
from .views import (
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
    url(r'^advisor/$', advisor),
    url(r'^student/$', student),
    url(r'^degree/$', degree),
    url(r'^courses/$', courses),
    url(r'^departments/$', departments),
    url(r'^prerequisites/$', prerequisites),
    url(r'^Takes/$', Takes),
    url(r'^Contains/$', Contains),
    url(r'^Chooses/$', Chooses),

]