from django.views.generic.base import TemplateView
from django.http import HttpResponse
from .models import Bus

class HomeView(TemplateView):
	template_name = 'index.html'

def index(request):
	all_buses = Bus.objects.all()
	html = ''

	for bus in all_buses:
		url = str(bus.route) + '/'
		html += '<a href="' + url + '">' + bus.bus_id + '</a><br>'

	return HttpResponse(html)

def detail(request, route):
	return HttpResponse("<h2>Details for route id: " + str(route) + "</h2>")

