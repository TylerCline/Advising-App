from django.shortcuts import render
from django.http import HttpResponse
from .models import (Advisor, Departments, Students,
	Degrees, Prerequisites, Courses, takes, chooses, contains
	)
# Create your views here.
def home(request):
	return render(request, 'home.html', {})
	
def advisor(request):
	queryset = Advisor.objects.all()
	context = {
		"advisor_data": queryset,
	}
	return render(request, 'advisor.html', context)

def student(request):
	queryset = Students.objects.all()
	context = {
		"student_data": queryset,
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
	queryset = takes.objects.all()
	context = {
		"takes_data": queryset,
	}
	return render(request, 'takes.html', context)

def Contains(request):
	queryset = contains.objects.all()
	context = {
		"contains_data": queryset,
	}
	return render(request, 'contains.html', context)

def Chooses(request):
	queryset = chooses.objects.all()
	context = {
		"chooses_data": queryset,
	}
	return render(request, 'chooses.html', context)