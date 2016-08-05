#File: forms.py
#purpose: To create forms for user input on various pages
#Author: Tyler Cline
#Ohio University 2016

from django import forms
from django.forms import CheckboxSelectMultiple, Textarea, CheckboxInput
from .models import Students, takes, chooses, Courses, contains
from django.contrib.auth.models import User
from itertools import chain
import g

#Class: StudentForm
#Purpose: Creates a input form for the student model.
#		  Students input all of there information into text boxes
#		  on he student.html web page. The inputs can be seen in the
#         fields list.
class StudentForm(forms.ModelForm): 
	class Meta:
		model = Students
		fields = [
			"PID",
			"Email",
			"Fname",
			"Lname",
			"Years_To_Completion",
			"AdvisorEmail"
		]
	#Input validation for the email. If the user does not use an ohio.edu email, an
	#error will be raised.
	def clean_email(self):
		email = self.cleaned_data.get('Email')
		base, provider = email.split("@")
		domain, extension = provider.split(".")
		if not extension == "edu" and not domain == "ohio":
			raise forms.ValidationError("Please Use your Ohio email")
		return email
	#input validation for the student PID. Follows the same notion of the above function.
	#It checks to see if the student added the P and weather it is 9 characters long.
	def clean_PID(self):
		PID = self.cleaned_data.get("PID")
		if PID[0] == 'P':
			raise ValidationError(
				_('%(PID)s Omitt the P'),
            	params={'PID': PID},
            )
		elif len(PID) != 9:
			raise ValidationError(
            	_('%(PID)s Is not long enough. Must have length 9. (P followed by 9 numbers'),
            	params={'PID': PID},
        	)
        	return PID

#Class: TakesForm
#Purpose: Creates form inputs for students to enter all of the course requirments
#		  he/she has taken towards their degree. This is rendered in the takes.html
#		  template
class TakesForm(forms.ModelForm):
	class Meta:
		model = takes
		fields = [
			"PID",
			"Tier1comp",
			"Tier1qs",
			"Tier1jc",
			"CrossCulture",
			"ScienceMath",
			"FineArts",
			"Humanities",
			"NaturalScience", 
			"SocialScience",
			"FreeElectives",
			"Tier3",
			"Course_Title",
			"Enrolled",
		]
	#This function overides the default rendering of the form by django. This allows
	#for me to customize how the form will look, including the data that is displayed for the user
	#with checkboxes. This bit of code can be found on the django documentation under custom forms.
	def __init__ (self, *args, **kwargs):
		#This logic here grabs the student PID from the student model using the current users email.
		#The email variable is stored in a global variable in the file g.py. This global variable will
		#always hold the current user's email address.
		p = ''
		email = g.user_email
		student = Students.objects.filter(Email=email)
		for pid in student:
			p = pid.PID
		chooseSet = chooses.objects.filter(PID=p)
		deg = ''
		for degree in chooseSet:
			deg = degree.DegreeTitle
		#this overrides the default form and allows for customization
		super(TakesForm, self).__init__(*args, **kwargs)
		self.fields["Course_Title"].widget=forms.widgets.CheckboxSelectMultiple()
		self.fields["Course_Title"].help_text=''
		self.fields["Course_Title"].queryset=Courses.objects.filter(Type=deg)

#Class: ChooseForm
#Purpose: To create a input form for the student to choose a degree before he/she
#		  can choose courses they have taken.
class ChoosesForm(forms.ModelForm):
	class Meta:
		model = chooses
		fields = [
			"PID",
			"DegreeTitle",
		]