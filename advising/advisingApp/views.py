from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .models import (Advisor, Departments, Students,
	Degrees, Prerequisites, Courses, takes, chooses, contains
	)
from .forms import StudentForm, TakesForm, ChoosesForm
# Create your views here.
def base(request):
	return render(request, 'home.html', {})
	
def report(request):
	queryset = Advisor.objects.all()
	context = {
		"advisor_data": queryset,
	}
	return render(request, 'report.html', context)

def student(request):
	form = StudentForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			PID = form.cleaned_data['PID']
			instance = form.save(commit=False)
			instance.save()
			return HttpResponseRedirect('/advisingApp/Chooses/')
	context = {
		"form": form,
	}
	return render(request, 'student.html', context)

def degree(request):
	queryset = Degrees.objects.all()
	context = {
		"degree_data": queryset,
	}
	return render(request, 'degree.html', context)

def courses(request):
	queryset = Courses.objects.all()
	context = {
		"course_data": queryset,
	}
	return render(request, 'courses.html', context)

def departments(request):
	queryset = Departments.objects.all()
	context = {
		"Department_data": queryset,
	}
	return render(request, 'department.html', context)

def prerequisites(request):
	queryset = Prerequisites.objects.all()
	context = {
		"prereq_data": queryset,
	}
	return render(request, 'prerequisites.html', context)

def Takes(request):
	form = TakesForm(request.POST or None)
	if request.method== 'POST':
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			return HttpResponseRedirect('/advisingApp/base/')
	context = {
		"form": form,
	}
	return render(request, 'takes.html', context)

def Contains(request):
	queryset = contains.objects.all()
	context = {
		"contains_data": queryset,
	}
	return render(request, 'contains.html', context)

def Chooses(request):
	form = ChoosesForm(request.POST or None)
	if request.method== 'POST':
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			return HttpResponseRedirect('/advisingApp/Takes/')
	context = {
		"form": form,
	}
	return render(request, 'chooses.html', context)