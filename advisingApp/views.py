#File: Views.py
#Purpose: To create contexts to be displayed on templates
#		  and render the contexts on the templates. Also
#         carries out all logic implemented on each template.
#Author: Tyler Cline
#Ohio University 2016

from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .models import (Advisor, Departments, Students,
	Degrees, Prerequisites, Courses, takes, chooses, contains
	)
from .forms import StudentForm, TakesForm, ChoosesForm
from django.contrib.auth.models import User
import g
import math
from django.db.models import Q
# Create your views here.

def base(request):
	return render(request, 'home.html', {})

#Function: report
#purpose: to render the report web page and generate the logic behind
#         report generation for the student.
# How it works: First, the studnet pid is obtained from the student
# table utilizing the email in the current logged in account.
# Next, the students degree is obtained by querying the chooses table
# with the students PID. Once the degree is obtained, it is used to gather
# the required courses for that degree by querying the contains table.
# This builds a list of course titles from the contains table.
# Also, a list of taken courses is built using the takes table.
# this lists are compared and set differenced, generating courses the
# student still needs to take to acheive his/her degree
def report(request):
	#gathering the students PID from the student table using user email
	if request.user.is_authenticated() and not request.user.is_anonymous():
		student = Students.objects.filter(Email=request.user.email)
		for pid in student:
			p = pid.PID
	
	#gathering the degree which the student chose via PID
		choose = chooses.objects.filter(PID=p)
		degree = ''
		for d in choose:
			degree = d.DegreeTitle

	#getting the courses taken by the student via PID
		taken = takes.objects.filter(PID=p)
	#getting the courses in the degree which the student chose
		needed = contains.objects.filter(Degree_Title=degree)
		name = Students.objects.filter(PID=p)
	#logic for building the lists of courses taken and courses needed
	#The takes database table has a many to many field, allowing multiple records to be 
	#added to one row in one column. This is very useful in storing multiple courses,
	# but is hard to extract the data. This bit of code extracts that data from the 
	#many to many field. Iterate through the taken dictionary (created by a query above), then
	#iterate through the coures_title record withing that record. Then a list is built with
	#the correct data.
		courses_taken = []
		for obj in taken:
			for Course_Title in obj.Course_Title.all():
				courses_taken.append(str(Course_Title))
	#building a list of needed courses
		courses_needed = []
		for obj in needed:
			courses_needed.append(str(obj.Course_Title))
	#set difference, getting the courses needed
		difference = [item for item in courses_needed if item not in courses_taken]
	
	#calculations to determine student credit hours taken and needed
		course_credits = Courses.objects.all()
		credit = 0
		taken_credit = 0
		genEd_credit = 33
		genEd_left = 0
		for c in course_credits:
			if c.Type == degree:
				credit = credit + int(c.Credits)
			if str(c.TITLE) in courses_taken:
				taken_credit = taken_credit + int(c.Credits)

	#checks each tier requirment to see if fullfilled. If so,
	#add the credit hours to the general education tier credit variable
		for t in taken:
			if t.Tier1comp == True:
				genEd_left = genEd_left + 3
			if t.Tier1qs == True:
				genEd_left = genEd_left + 3
			if t.Tier1jc == True:
				genEd_left = genEd_left + 3
			if t.CrossCulture == True:
				genEd_left = genEd_left + 2
			if t.ScienceMath == True:
				genEd_left = genEd_left + 2
			if t.FineArts == True:
				genEd_left = genEd_left + 2
			if t.Humanities == True:
				genEd_left = genEd_left + 2
			if t.NaturalScience == True:
				genEd_left = genEd_left + 2
			if t.SocialScience == True:
				genEd_left = genEd_left + 2
			if t.FreeElectives == True:
				genEd_left = genEd_left + 9
			if t.Tier3 == True:
				genEd_left = genEd_left + 3

	#These variables are rather self explanatory. They just store credits aquired, credits
	#needed, credits left, years left, and semesters left. These are put in the context varibale
		credit_left = credit - (taken_credit)
		genEd_needed = genEd_credit - genEd_left
		total_credits = credit + genEd_credit
		total_taken_credits = taken_credit + genEd_left
		total_left = total_credits - total_taken_credits
		semesters_left = math.ceil(total_left/15.0)
		years_left = semesters_left / 2

	#all of the querysets used in the template
		context = {
			"advisor_data": taken,
			"courses_needed": needed,
			"student": name,
			"other": difference,
			"credit": credit,
			"taken_credit": taken_credit,
			"credit_left" : credit_left,
			"genEd": genEd_left,
			"genEd_needed": genEd_needed,
			"total": total_credits,
			"total_taken" : total_taken_credits,
			"total_left": total_left,
			"years_left": years_left,
			"semesters_left": semesters_left,
		}
	else:
		context = {}
	return render(request, 'report.html', context)

#Function: Student
#purpose: to render the student template for sign ups
#How it works: First, the user is checked for authentication. Then
# ths users email address is used to prefill the email field via the
# 'initial' parameter in the form constructor. The form is checked to see if
# the user is posting data, then the data is saved to the database.
def student(request):
	#gathering the user's email, and saving it in a variable called
	# em
	em = ''
	if request.user.is_authenticated:
		student = Students.objects.filter(Email=request.user.email)
		for stud in student:
			em = stud.Email
	else:
		em = ''

	#if the users email is equal to a student email, then the user already created
	#a student profile, and the takes table needed updated, not initially put in. So, this code
	# redirects the user to an update page to update the coures he took.
	if request.user.email == em:
		return HttpResponseRedirect('/advisingApp/takes_update/')

	#form constructr. This is the form the student uses to input his information as a student.
	form = StudentForm(request.POST or None, initial={'Email': request.user.email})
	#This code saves the input from the form
	if request.method == 'POST':
		if form.is_valid():
			pid = form.cleaned_data['PID']
			email = form.cleaned_data['Email']
			instance = form.save(commit=False)
			instance.save()
			return HttpResponseRedirect('/advisingApp/Chooses/')
	context = {
		"form": form,
		"em" : em,
	}
	return render(request, 'student.html', context)

#Function: degree
#Purpose: To add searching capabilities for degrees,
#so the student can browse the degree offerings.
def degree(request):
	queryset_list = Degrees.objects.all()
	#querys the database with the information entered on the form. The query string
	#is stored in the variable 'q'. This variable is named in the degree.html template
	query = request.GET.get('q')
	#Utilizes Q, which allows for the creartion of multiple searches.
	#using the filter method, Q uses the model fields followed by __icontains
	#to search the field to see if the query matches any string in that field.
	#This instance searches all fields for the query.
	if query:
		queryset_list = queryset_list.filter(
			Q(TITLE__icontains=query) |
			Q(About__icontains=query) |
			Q(Deparment_Name__icontains=query)
			).distinct()
	context = {
		"degree_data": queryset_list,
	}
	return render(request, 'degree.html', context)

#operates exactly the same as the degree function.
def courses(request):
	queryset_list = Courses.objects.all()
	query = request.GET.get('q')
	if query:
		queryset_list = queryset_list.filter(
			Q(TITLE__icontains=query) |
			Q(Type__icontains=query) |
			Q(Name__icontains=query) |
			Q(Tier__icontains=query) |
			Q(discription__icontains=query)
			).distinct()
	queryset = Courses.objects.filter(Tier='CS-Requirement')
	context = {
		"course_data": queryset_list,
	}
	return render(request, 'courses.html', context)

#Function: Takes
#Purpose: To render the takes template, so the student can input courses
# and requirments he/she has taken.
#How it works: The students PID is gathered by using the users email.
# once the PID is aquired, it is used to prefill the form for takes, so the 
# student can't arbitrarily type a PID. the form is renderd and saved.
def Takes(request):
	#gathering the pid using user email
	p = ''
	student = Students.objects.filter(Email=request.user.email)
	for pid in student:
		p = pid.PID
	g.user_email = request.user.email
	#initializing the takes form for student course input
	form = TakesForm(request.POST or None, initial={'PID':p})
	if request.method== 'POST':
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			form.save_m2m()
			return HttpResponseRedirect('/advisingApp/base/')
	context = {
		"form": form,
	}
	return render(request, 'takes.html', context)

#same as the Takes class, except it prefills the form with
#data the student already has in his takes record in the database.
#This allows for the student to continue where he left of, or update
#courses he/she took.
def takes_update(request, id=None):
	#gathering the pid using user email
	p = ''
	student = Students.objects.filter(Email=request.user.email)
	for pid in student:
		p = pid.PID
	g.user_email = request.user.email
	#initializing the takes form for student course input
	instance = get_object_or_404(takes, PID=p)
	form = TakesForm(request.POST or None, instance=instance)
	if request.method== 'POST':
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			form.save_m2m()
			return HttpResponseRedirect('/advisingApp/base/')
	context = {
		"form": form,
	}
	return render(request, 'takes_update.html', context)


#function: Chooses
#Purpose: To render the chooses page for students to choose a degree
#How it works: The user is checked for authentication and the pid is gathered
# by using user email. This pid variable is used to prefill the form's PID
#section so students can't arbitrarily choose PIDs. The Form is them rendered and
# saved.
def Chooses(request):
	#checking if the user is authenticated. if he is, get the student
	#else, do not.
	if request.user.is_authenticated:
		student = Students.objects.filter(Email=request.user.email)
	else:
		student = ''
	#gather the students pid to use for prefill
	p = ''
	student = Students.objects.filter(Email=request.user.email)
	for pid in student:
		p = pid.PID
	#initializing the form constructor and initializing the PID
	form = ChoosesForm(request.POST or None, initial={'PID':p})
	if request.method== 'POST':
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			return HttpResponseRedirect('/advisingApp/Takes/')
	context = {
		"form": form,
		"p" : p,
	}
	return render(request, 'chooses.html', context)