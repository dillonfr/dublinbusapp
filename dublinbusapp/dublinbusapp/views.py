from django.http import HttpResponse
from django.shortcuts import render
#from .models import Bus
from .models import Trips2017
from dict import *

def index(request):
	buslist = makeBusStopDict()
	
	query_results = Trips2017.objects.raw('SELECT * FROM trips2017 LIMIT 20')

	context = {
		'buslist': buslist,
		'query_results': query_results,
	}

	return render(request, 'index.html', context)

def detail(request, route):
	return HttpResponse("<h2>Details for route id: " + str(route) + "</h2>")

