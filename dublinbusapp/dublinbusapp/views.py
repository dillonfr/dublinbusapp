from django.http import HttpResponse
from django.http import JsonResponse

from django.shortcuts import render

from .models import Trips2017
from dict import *
from .forms import *
from .dates import *

from django.views.decorators.csrf import csrf_exempt

import pickle
import pandas as pd



@csrf_exempt
def index(request):
	buslist = makeBusStopDict()

	context = {
		'buslist': buslist,
	}
	return render(request, 'index.html', context)


@csrf_exempt
def ajax(request):
	context = {}

	if request.is_ajax():
		print("I got sent some ajax")
		testInput = request.POST['testInput']
		name = request.POST['teamName']

		sampleX = [1, 1, 281, 2, 4, 2]
		sampleY = [41]

		df = pd.DataFrame(data=[sampleX])

		loaded_model = pickle.load(open("C:/Users/dillo_000/Desktop/dublinbusapp/dublinbusapp/dublinbusapp/test_7D_pickle.sav", 'rb'))

		newResult = loaded_model.predict(df)
		newResult = newResult.tolist()
		print(newResult[0])
		print(type(newResult[0]))

		context['result'] = newResult[0]

	return render(request, 'name.html', context)

@csrf_exempt
def journey(request):
	if request.method == "POST":

		allRoutes = json.loads(request.POST["allRoutes"])
		print("BEST ROUTE:")
		bestRoute = allRoutes[0] #the first journey suggested by google is the best
		print(bestRoute)

		numBusJourneys = len(bestRoute) - 1

		# Initialise times that our model will add minutes to
		busTime = 0
		walkingTime = bestRoute[-1]['walkingtime']

		# Reformat date chosen into format that can be passed into model
		dateChosen = request.POST["dateChosen"]
		dayOfWeek = stripDay(dateChosen)
		peak = isPeak(dateChosen)


		# Go through each bus leg and get a prediction on journey time for that leg
		for i in range(0, numBusJourneys):
			route = bestRoute[i]['route']
			originLatLng = bestRoute[i]['departurelatlng']
			destinationLatLng = bestRoute[i]['arrivallatlng']
			numStops = bestRoute[i]['numstops']


			stopsDictList = getRouteStops(route)

			originId = getStopId(stopsDictList, departureLatLng)
			destinationId = getStopId(stopsDictList, arrivalLatLng)
			direction = 2

			df = [dayOfWeek, peak, originId, direction, destinationId, numStops]

			loaded_model = pickle.load(open("C:/Users/dillo_000/Desktop/dublinbusapp/dublinbusapp/dublinbusapp/test_7D_pickle.sav", 'rb'))

			journeyTimePrediction = loaded_model.predict(df)
			journeyTimePrediction = journeyTimePrediction.tolist()
			journeyTimePrediction = journeyTimePrediction[0]

			busTime += journeyTimePrediction


		print("New bustime")
		print(busTime)
		# Getting a sample result from a sample pickle file

		#dayofweek, peak, originid, direction, destinationid, numofstops 
		sampleX = [1, 1, 281, 2, 4, 2]
		sampleY = [41]

		df = pd.DataFrame(data=[sampleX])

		loaded_model = pickle.load(open("C:/Users/dillo_000/Desktop/dublinbusapp/dublinbusapp/dublinbusapp/test_7D_pickle.sav", 'rb'))


		journeyTimePrediction = loaded_model.predict(df)
		journeyTimePrediction = journeyTimePrediction.tolist()
		journeyTimePrediction = journeyTimePrediction[0]

		# Parsing data received from AJAX
		result=json.loads(request.POST["query"]) #result is a list

		result.append(request.POST["testInput"])
		result.append(request.POST["origin"])
		result.append(request.POST["destination"])
		result.append(journeyTimePrediction)
		result.append(request.POST["dateChosen"])

		print(type(request.POST["dateChosen"]))
		print(request.POST["dateChosen"])

	return JsonResponse(result, safe=False)



@csrf_exempt
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


	