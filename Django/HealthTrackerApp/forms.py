from django.forms import ModelForm
from django.forms import ModelForm
from .models import Patient


class PatientForm(ModelForm):
	class Meta:
		model = Patient
		fields = ['RFID','Firstname','Lastname','Cin']
