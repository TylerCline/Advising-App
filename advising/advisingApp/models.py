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
#Degree name validator
#*******************************
def validate_Dname(title):
	names = ['Computer Science', 'Electical Engineering', 
	         'Computer Engineeriexng', 'Chemical Engineering',
	         'Civil Engineering', 'Mechanical Engineering',
	         'Industrial Systems Engineering', 
	         'Engineering Technology Management', 'NULL']
	matched = False
	for i in range(0, len(names)):
		if title == names[i]:
			matched = True
		elif i == len(i) and matched == False:
			raise ValidationError(
            _('%(title)s is not a degree offered by Russ College'),
            params={'title': title},
        )

def validate_PID(PID):
	if PID[0] != 'P':
		raise ValidationError(
			_('%(PID)s must begin with a P'),
            params={'PID': PID},
            )
	elif len(PID) != 10:
		raise ValidationError(
            _('%(PID)s Is not long enough. Must have length 10. (P followed by 9 numbers'),
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
#Beginning of the model implementations
#*****************************************
class Advisor(models.Model):
	EMAIL = models.EmailField(max_length=100, primary_key=True, unique=True)
	Fname = models.CharField(max_length=50)
	Lname = models.CharField(max_length=50)
	Title = models.CharField(max_length=50)


class Departments(models.Model):
	Name = models.TextField(max_length=100)
	DEPT_NUM = models.IntegerField(primary_key=True)
	Building = models.CharField(max_length=100)

class Students(models.Model):
	PID = models.CharField(max_length=9, primary_key=True, validators=[validate_PID])
	Email = models.EmailField(max_length=100)
	Fname = models.CharField(max_length=50)
	Lname = models.CharField(max_length=50)
	Years_To_Completion = models.IntegerField()
	AdvisorEmail = models.ForeignKey('Advisor', on_delete=models.CASCADE)

class Degrees(models.Model):
	TITLE = models.CharField(max_length=50, primary_key=True, 
							validators=[validate_Dname])
	About = models.TextField()
	Requiured_Credits = models.IntegerField()
	Deparment_Name = models.ForeignKey('Departments', on_delete=models.CASCADE)

#Ask professor. The algorithm calls for creating a 1 to many relationship
# for multi valued attributes, which is what prerequisite is.
# it was an attribute for courses.
class Prerequisites(models.Model):
	TITLE = models.CharField(max_length=10, primary_key=True, validators=[validate_Cname])
	Course = models.ForeignKey('Courses', on_delete=models.CASCADE)

class Courses (models.Model):
	TITLE = models.CharField(max_length=10, primary_key=True, 
							validators=[validate_Cname])
	Type = models.CharField(max_length=20)
	Code = models.CharField(max_length=20)
	Grade_Needed = models.CharField(max_length=10, validators=[validate_Grade])
	Credits = models.IntegerField(validators=validate_credits)

#****************************
#The following models need composite keys made from the
#combination of foreign keys, but are not supported in django. Need to
#find a workaround, or database redesign.
#
#Possible Workaround: Meta class
# Utilizing the Meta class within the model, you can declare a 
# variable called unique_together and have a tuple containing the
# variables needed to create your primary key. Django will still
# create a primary key however.
#
# Credit:http://stackoverflow.com/questions/28712848/composite-primary-key-in-django
#*****************************
class takes (models.Model):
	class Meta:
		unique_together = (('PID', 'Course_Title'),)

	PID = models.ForeignKey('Students', on_delete=models.CASCADE)
	Course_Title = models.ForeignKey('Courses', on_delete=models.CASCADE)
	Grade_Received = models.CharField(max_length=3, validators=[validate_Grade])
	Enrolled = models.BooleanField()

class chooses(models.Model):
	class Meta:
		unique_together = (('PID', 'Department_Title'),)

	PID = models.ForeignKey('Students', on_delete=models.CASCADE)
	Department_Title = models.ForeignKey('Departments', on_delete=models.CASCADE)

class contains(models.Model):
	class Meta:
		unique_together = (('Course_Title', 'Degree_Title'),)

	Course_Title = models.ForeignKey('Courses', on_delete=models.CASCADE)
	Degree_Title = models.ForeignKey('Degrees', on_delete=models.CASCADE)