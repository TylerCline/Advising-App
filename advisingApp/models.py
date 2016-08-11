#File: models.py
#Purpose: To implement the database schema through models.
#Author: Tyler Cline
#Ohio University 2016

from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# Create your models here.

#Naming convention validator. This makes sure that the title
#of courses stays consistent

#All validators written using django documentation: https://docs.djangoproject.com/en/1.9/ref/validators/
def validate_Cname(title):
	names = ['CS', 'EE', 'CE', 'ET', 'ME', 'CHE', 'ETM', 'ISE'
	         'CHEM', 'EMGT', 'ENGT', 'MATH', 'PHYS', 'BIOS', 'GEOL',
	         'NO_Match']
	matched = False
	for i in range(0, len(names)):
		if i < 5:
			if title.startswith(names[i], 0, 1):
				matched = True
		elif i >= 5 and i < 8:
			if title.startswith(names[i], 0, 2):
				matched = True
		elif i >= 8 and i < len(names):
			if title.startswith(names[i], 0, 3):
				matched = True
		elif i == len(names) and matched == False:
			 raise ValidationError(
            _('%(title)s is not named correctly. Example: EE1024'),
            params={'title': title},
        )


#*******************************
#Server Side input validate.
#*******************************
def validate_Dname(title):
	names = ['Computer Science', 'Electrical Engineering', 
	         'Computer Engineering', 'Chemical Engineering',
	         'Civil Engineering', 'Mechanical Engineering',
	         'Industrial and Systems Engineering', 
	         'Engineering Technology and Management', 'Aviation Flight']
	if title not in names:
		raise ValidationError(
            _('%(title)s is not a degree offered by Russ College. Choices are Computer Science, Electrical Engineering, Computer Engineering, Chemical Engineering, Civil Engineering, Mechanical Engineering, Industrial and Systems Engineering, Engineering Technology and Management, Aviation Flight'),
            params={'title': title},
        )

def validate_PID(PID):
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

def validate_Grade(grade):
	grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-',
	          'D+', 'D', 'D-', 'F', 'Null']
	matched = False
	for i in range(0, len(grades)):
		if grade == grades[i]:
			matched = True
		elif i == len(grades) and matched == False:
			raise ValidationError(
            _('%(grade)s is not a valid grade'),
            params={'grade': grade},
        )

def validate_credits(credit):
	matched = False
	for i in range(0, 11):
		if credit == i and i < 10:
			matched = True
		elif i == 10 and matched == False:
			raise ValidationError(
            _('no class is worth %(credit)s credits. Must be a value between 1-9'),
            params={'credit': credit},
        )
#*****************************************
#Beginning of the model implementations.
#These are the database table implementations in 
#the schema diagram. These will be updated and 
#created when the programmer runser "python manage.py makemigrations"
#then "python manage.py migrate"
#*****************************************

#database table for advisor information
class Advisor(models.Model):
	EMAIL = models.EmailField(max_length=100, primary_key=True, unique=True)
	Fname = models.CharField(max_length=50)
	Lname = models.CharField(max_length=50)
	Title = models.CharField(max_length=50)
	def __unicode__(self):
		return self.Fname + " " + self.Lname

#database table for departments in russ college
class Departments(models.Model):
	Name = models.TextField(max_length=100)
	DEPT_NUM = models.IntegerField(primary_key=True)
	Building = models.CharField(max_length=100)
	def __unicode__(self):
		return self.Name

#Database table to hold all student information
class Students(models.Model):
	PID = models.CharField(max_length=9, primary_key=True, validators=[validate_PID])
	Email = models.EmailField(max_length=100)
	Fname = models.CharField(max_length=50)
	Lname = models.CharField(max_length=50)
	Years_To_Completion = models.DecimalField(max_digits=5, decimal_places=2)
	AdvisorEmail = models.ForeignKey('Advisor', on_delete=models.CASCADE)
	def __unicode__(self):
		return self.PID

#Database table to hold all degree information.
class Degrees(models.Model):
	TITLE = models.CharField(max_length=50, primary_key=True, 
							validators=[validate_Dname])
	About = models.TextField()
	Requiured_Credits = models.IntegerField()
	Deparment_Name = models.ForeignKey('Departments', on_delete=models.CASCADE)
	def __unicode__(self):
		return self.TITLE

#Database table to hold course prerequisites
class Prerequisites(models.Model):
	TITLE = models.CharField(max_length=10, primary_key=True)
	Course = models.ForeignKey('Courses', on_delete=models.CASCADE)

#Database table to hold individual course information
class Courses (models.Model):
	TITLE = models.CharField(max_length=40, primary_key=True, validators=[validate_Cname])
	Type = models.CharField(max_length=100)
	Name = models.CharField(max_length=100)
	Grade_Needed = models.CharField(max_length=10, validators=[validate_Grade])
	Credits = models.IntegerField(validators=[validate_credits])
	Tier = models.CharField(max_length=20)
	discription = models.TextField(blank=True)
	def __unicode__(self):
		return self.TITLE

#database table to hold all information about what a student has
#taken and requiremtns he has fulfilled
class takes (models.Model):
	PID = models.CharField(max_length=9, primary_key=True)
	Course_Title = models.ManyToManyField(Courses, related_name='Course_Title')
	Grade_Received = models.CharField(blank = True, max_length=3, validators=[validate_Grade])
	Enrolled = models.BooleanField(blank=True)
	Tier1comp = models.BooleanField(blank=True, default=False)
	Tier1qs = models.BooleanField(blank=True, default=False)
	Tier1jc = models.BooleanField(blank=True, default=False)
	Tier2 = models.DecimalField(max_digits=5, decimal_places=1, default=0.0)
	CrossCulture = models.BooleanField(blank=True, default=False)
	ScienceMath = models.BooleanField(blank=True, default=False)
	FineArts = models.BooleanField(blank=True, default=False)
	Humanities = models.BooleanField(blank=True, default=False)
	NaturalScience = models.BooleanField(blank=True, default=False)
	SocialScience = models.BooleanField(blank=True, default=False)
	FreeElectives = models.BooleanField(blank=True, default=False)
	Tier3 = models.BooleanField(blank=True, default=False)

#database table to hold what degree a student chose
class chooses(models.Model):
	PID = models.CharField(max_length=9, primary_key=True)
	DegreeTitle = models.CharField(max_length=100)

#database table to hold what courses a degree contains.
class contains(models.Model):
	Course_Title = models.CharField(max_length=100)
	Degree_Title = models.CharField(max_length=100, validators=[validate_Dname])