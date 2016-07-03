from django.contrib import admin
from .models import Advisor
from .models import Departments
from .models import Students
from .models import Degrees
from .models import Prerequisites
from .models import Courses
from .models import takes
from .models import chooses
from .models import contains
# Register your models here.

class AdvisorAdmin(admin.ModelAdmin):
	list_display = ['EMAIL', 'Fname', 'Lname', 'Title']
	list_display_links = ["EMAIL"]
	list_filter = ["Lname"]
	search_fields = ["Fname", "Lname"]
	class Meta:
		model = Advisor

class DepartmentAdmin(admin.ModelAdmin):
	list_display = ['Name', 'DEPT_NUM', 'Building']
	list_display_links = ['DEPT_NUM']
	list_filter = ['Name']
	search_fields = ['Name', 'Building']
	class Meta:
		model = Departments

class StudentAdmin(admin.ModelAdmin):
	list_display = ['PID', 'Email', 'Fname', 'Lname', 'Years_To_Completion', 'AdvisorEmail']
	list_display_links = ['PID', 'Email']
	list_filter = ['Lname', 'Fname']
	search_fields = ['Lname', 'Fname']
	class Meta:
		model = Students

class DegreeAdmin(admin.ModelAdmin):
	list_display = ['TITLE', 'About', 'Requiured_Credits', 'Deparment_Name']
	list_display_links = ['TITLE']
	list_filter = ['TITLE', 'Deparment_Name']
	search_fields = ['TITLE']
	class Meta:
		model = Degrees

class PrereqAdmin(admin.ModelAdmin):
	list_display = ['TITLE', 'Course']
	list_display_links = ['TITLE']
	list_filter = ['TITLE']
	search_fields = ['TITLE']
	class Meta:
		model = Prerequisites

class CourseAdmin(admin.ModelAdmin):
	list_display = ['TITLE', 'Type', 'Code', 'Grade_Needed', 'Credits']
	list_display_links = ['TITLE']
	list_filter = ['TITLE']
	search_fields = ['TITLE']
	class Meta:
		model = Courses

class TakeAdmin(admin.ModelAdmin):
	list_display = ['PID', 'Course_Title', 'Grade_Received', 'Enrolled']
	list_display_links = ['PID']
	list_filter = ['PID', 'Course_Title']
	search_fields = ['PID', 'Course_Title']
	class Meta:
		model = takes

class ChooseAdmin(admin.ModelAdmin):
	list_display = ['PID', 'Department_Title']
	list_display_links = ['PID']
	list_filter = ['PID']
	search_fields = ['PID']
	class Meta:
		model = chooses

class ContainAdmin(admin.ModelAdmin):
	list_display = ['Course_Title', 'Degree_Title']
	list_display_links = ['Course_Title', 'Degree_Title']
	list_filter = ['Course_Title', 'Degree_Title']
	search_fields = ['Course_Title', 'Degree_Title']
	class Meta:
		model = contains

admin.site.register(Advisor, AdvisorAdmin)
admin.site.register(Departments, DepartmentAdmin)
admin.site.register(Students, StudentAdmin)
admin.site.register(Degrees, DegreeAdmin)
admin.site.register(Prerequisites, PrereqAdmin)
admin.site.register(Courses, CourseAdmin)
admin.site.register(takes, TakeAdmin)
admin.site.register(chooses, ChooseAdmin)
admin.site.register(contains, ContainAdmin)