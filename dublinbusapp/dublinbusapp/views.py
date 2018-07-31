from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

from buslist import *
from dates import *
from weather import *
from realtime import *


from django.views.decorators.csrf import csrf_exempt

import pickle
import pandas as pd
from sklearn.externals import joblib



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
		#print(unixTime(dateChosen))
		uTime = unixTime(dateChosen)

		weatherDict = getWeather(uTime)
		print(weatherDict)

		rain = weatherDict['raining']
		temperature = weatherDict['temperature']
		windSpeed = weatherDict['windSpeed']
		weatherNowText = weatherDict['weatherNowText']
		weatherIcon = weatherDict['weatherIcon']

		print(rain)
		print(temperature)
		print(windSpeed)



		routesToTake =[]
		busTime = 0
		isFirstStopId = False

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

			# Get realtime info for the first bus stop id of the journey
			if isFirstStopId == False:
				realTimeInfo = getRealTimeInfo(originId) # Returns a list
				isFirstStopId = True


			# Assume direction for now
			direction = 2

			# Create dataframe
			df = [[dayOfWeek, peak, originId, direction, destinationId, numStops]]





			X_1 = [(5, 1, 12, 1642, 213, 1, 0.2777)]
			X_dummies = pd.get_dummies(X_1)

			# X_2 = [(0.2777)]
			# X_Test = pd.concat([X_dummies, X_2], axis=1)
			df = [[0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0.277487]]


			# start_id_dummies
			# [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

			# end_id_dummies
			# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
			# Pass df into model and get prediction
			loaded_model = joblib.load(open("C:/Users/dillo_000/Desktop/dublinbusapp/dublinbusapp/dublinbusapp/pickles/test_7_LR_pickle_sk.sav", 'rb'))


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
				'walkingTime': walkingTime,
				'totalTime': (busTime/60) + walkingTime,
				'realTimeInfo': realTimeInfo,
				'weatherNowText': weatherNowText,
				'weatherIcon': weatherIcon,
				}

	# Return the result dictionary to AJAX as a response
	return JsonResponse(result, safe=False)
