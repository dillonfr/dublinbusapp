from django.http import HttpResponse
from django.shortcuts import render
from .models import Bus
from dict import *

def index(request):
	all_buses = Bus.objects.all()
	html = ''

	for bus in all_buses:
		url = str(bus.route) + '/'
		html += '<a href="' + url + '">' + bus.bus_id + '</a><br>'

	#return HttpResponse(html)

	buslist = makeBusStopDict()

	context = {
		'buslist': buslist
	}

	return render(request, 'index.html', context)

def detail(request, route):
	return HttpResponse("<h2>Details for route id: " + str(route) + "</h2>")

