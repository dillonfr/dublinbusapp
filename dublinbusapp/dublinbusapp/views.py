from django.http import HttpResponse
from django.shortcuts import render
from .models import Trips2017
from dict import *
from .forms import *

def index(request):
	buslist = makeBusStopDict()

	#context is a dictionary that will contain anything we want to send to the frontend
	context = {
		'buslist': buslist,
	}

	
	#if user clicks the find route button on the frontend, this sends a post request to django
	if request.method == 'POST':
		form = StartForm(request.POST)
		
		#start_id = form.cleaned_data['start_id']
		
		#context['start_id'] = start_id
		
		#checks the info input into the form to make sure it is legal (security check, checks theres no SQL injection etc.)
		if form.is_valid():
			start_id = form.cleaned_data['start_id']
			#end_id = form.cleaned_data['end_id']
			print("Start: ", start_id)
			#print("End: ", end_id)	
			context['start_id'] = start_id
			#context['end_id'] = end_id
			return render(request, 'index.html', context)
	
	else:
		form = StartForm()
	
	#how to query database: (add query_results to context to send to frontend)
	#query_results = Trips2017.objects.raw('SELECT * FROM trips2017 LIMIT 20')

	#context = {
		#'buslist': buslist,
		#'query_results': query_results,
		#'form': form,
	#}
	print("fell through")
	return render(request, 'index.html', context)

def detail(request, route):
	if request.method == 'POST':
		form = NameForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['your_name']
			
			context = {
				'name': name,
			}
			return render(request, 'name.html', context)
	else:
		form = NameForm()

	return render(request, 'index.html', {'form': form})
