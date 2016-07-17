from django import forms
from django.forms import CheckboxSelectMultiple, Textarea, CheckboxInput
from .models import Students, takes, chooses

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

	def clean_email(self):
		email = self.cleaned_data.get('Email')
		base, provider = email.split("@")
		domain, extension = provider.split(".")
		if not extension == "edu" and not domain == "ohio":
			raise forms.ValidationError("Please Use your Ohio email")
		return email

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

class TakesForm(forms.ModelForm):
	class Meta:
		model = takes
		fields = [
			"PID",
			"Course_Title",
			"Enrolled"
		]
		widgets = {
		 	"Course_Title": CheckboxSelectMultiple
		 }

class ChoosesForm(forms.ModelForm):
	class Meta:
		model = chooses
		fields = [
			"PID",
			"DegreeTitle"
		]