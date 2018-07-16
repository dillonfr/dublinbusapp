from django import forms

class StartForm(forms.Form):
	start_id = forms.CharField(label="Start ID", max_length=50)
	end_id = forms.CharField(label="End ID", max_length=50)	

class NameForm(forms.Form):
	your_name = forms.CharField(label='Your name', max_length=100)
