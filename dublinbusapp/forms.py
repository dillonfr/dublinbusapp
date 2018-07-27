from django import forms

class StartForm(forms.Form):
	start_id = forms.CharField(label="Start ID", max_length=50)
	end_id = forms.CharField(label="End ID", max_length=50)	

class JourneyForm(forms.Form):
	start = forms.CharField(label="Start Address", max_length=200)
	end = forms.CharField(label="End Address", max_length=200)
	test = forms.CharField(label="Test", max_length=200)

class NameForm(forms.Form):
	your_name = forms.CharField(label='Your name', max_length=100)
