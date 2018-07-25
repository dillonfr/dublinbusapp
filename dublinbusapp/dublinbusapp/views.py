from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

from buslist import *
from dates import *
from weather import *


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
def journey(request):
	if request.method == "POST":


		allRoutes = json.loads(request.POST["allRoutes"])

		bestRoute = allRoutes[0] # The first journey suggested by google is the best

		numBusJourneys = len(bestRoute) - 1

		walkingTime = bestRoute[-1]['walkingtime']

		# Initialise times that our model will add minutes to


		# Reformat date chosen into format that can be passed into model
		dateChosen = request.POST["dateChosen"]
		dayOfWeek = stripDay(dateChosen)
		peak = isPeak(dateChosen)

		# Check weather conditions
		print(unixTime(dateChosen))
		uTime = unixTime(dateChosen)

		weatherDict = getWeather(uTime)

		rain = weatherDict['raining']
		temperature = weatherDict['temperature']
		windSpeed = weatherDict['windSpeed']
		print(rain)
		print(temperature)
		print(windSpeed)


		routesToTake =[]
		busTime = 0

		#Go through each bus leg and get a prediction on journey time for that leg
		for i in range(0, numBusJourneys):
			# Add each route to list of routes to take
			route = bestRoute[i]['route']
			routesToTake.append(route)

			# Extract data needed to pass into model
			originLatLng = bestRoute[i]['departureLatLng']
			destinationLatLng = bestRoute[i]['arrivalLatLng']
			numStops = bestRoute[i]['numStops']

			# Find all the stopid's on the route
			stopsDictList = getRouteStops(str(route))

			# Find the closest stopid's with the given latitudes/longitudes
			originId = int(getStopId(stopsDictList, originLatLng))
			destinationId = int(getStopId(stopsDictList, destinationLatLng))

			# Assume direction for now
			direction = 2

			# Create dataframe
			df = [[dayOfWeek, peak, originId, direction, destinationId, numStops]]

			# Pass df into model and get prediction
			loaded_model = pickle.load(open("/home/student/dublinbusapp/dublinbusapp/test_7D_pickle.sav", 'rb'))

			journeyTimePrediction = loaded_model.predict(df)
			journeyTimePrediction = journeyTimePrediction.tolist()
			journeyTimePrediction = journeyTimePrediction[0]

			busTime += journeyTimePrediction

		# Put data from AJAX and the model into dictionary to send back to AJAX as a response
		result = {
				'query': json.loads(request.POST["query"]),
				'origin': request.POST["origin"],
				'destination': request.POST["destination"],
				'dateChosen': request.POST["dateChosen"],
				'lastBusStepPrediction': journeyTimePrediction/60, # Seconds to minutes
				'routesToTake': routesToTake,
				'busTime': busTime/60, # Seconds to minutes
				}

	# Return the result dictionary to AJAX as a response
	return JsonResponse(result, safe=False)
