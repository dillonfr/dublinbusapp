# Import the necessary Django packages
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Import the data analytics packages
from sklearn.externals import joblib
import pickle
import numpy
import pandas as pd

# Import the packages containing the functions we need
from buslist import *
from dates import *
from weather import *
from realtime import *
from routedb import *


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

		conn = connectDB()

		allRoutes = json.loads(request.POST["allRoutes"])

		bestRoute = allRoutes[0] # The first journey suggested by google is the best

		numBusJourneys = len(bestRoute) - 1

		walkingTime = bestRoute[-1]['walkingtime']

		# Reformat date chosen into format that can be passed into model
		dateChosen = request.POST["dateChosen"]
		dayOfWeek = stripDay(dateChosen)
		hourOfDay = stripTime(dateChosen)
		peak = isPeak(dateChosen)
		uTime = unixTime(dateChosen)
		weatherDict = getWeather(uTime)

		rain = weatherDict['raining']
		temperature = weatherDict['temperature']
		windSpeed = weatherDict['windSpeed']
		weatherNowText = weatherDict['weatherNowText']
		weatherIcon = weatherDict['weatherIcon']

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
			originId = str(getStopId(stopsDictList, originLatLng))
			destinationId = str(getStopId(stopsDictList, destinationLatLng))

			# Get realtime info for the first bus stop id of the journey
			if isFirstStopId == False:
				realTimeInfo = getRealTimeInfo(originId) # Returns a list
				isFirstStopId = True

			# DB queries
			dbroute = route.upper()
			gtfsday = getGTFSday(dateChosen)
			timeOfDay = getSeconds(dateChosen)

			tripdata = getStartStop(conn, dbroute, gtfsday, originId, timeOfDay)[0]
			trip_id = tripdata[0]
			startnum = tripdata[1]
			print(trip_id)
			print(startnum)

			stopnum = getEndStop(conn, trip_id, destinationId)[0][0]
			print(stopnum)

			seqstoplist = getStopList(conn, trip_id, startnum, stopnum)
			# for i in range(0, len(seqstoplist), 1):
			# 	print(seqstoplist[i][0])

			# df created using DB
			listOfStops = []
			for i in range(0, len(seqstoplist)):
				listOfStops.append(seqstoplist[i][0])

			df_list = pd.DataFrame(listOfStops, columns=['stop_point_id'])

			modelData = {'day' : dayOfWeek, 'peak' : peak, 'hour' : hourOfDay, 'rain' : rain, 'temp' : temperature}
			df_features = pd.DataFrame(modelData, index=[0])
			# print(df_features)

			df_new = pd.concat([df_features, df_list], axis=1, ignore_index=True)
			df_new = df_new.fillna(method='ffill')

			df_new[6]=df_new[5].shift(-1)
			columnsTitles=[0, 2, 1, 5, 6, 3, 4]
			df_new = df_new.reindex(columns=columnsTitles)
			df_new = df_new[:-1]

			for i in range(0, 7):
				df_new[i] = df_new[i].astype('int')
				df_new[i] = df_new[i].astype('category')

			df_new = df_new.drop(df_new.columns[6], axis=1)

			df_new.columns = ['dayofweek', 'peak', 'hour', 'stoppointid', 'nextstop_id', 'rain']

			print(df_new)

			# Create dataframe
			# df = [[dayOfWeek, peak, originId, direction, destinationId, numStops]]
			# Pass df into model and get prediction

			dummies = joblib.load(open("C:\\Users\\Emmet\\Documents\\MScComputerScienceConversion\\Summer_Project\\Team14\\Git\\dublinbusapp\\dublinbusapp\\dublinbusapp\\dummies\\route" + dbroute+ "_dummies.sav", 'rb'))

			loaded_model = joblib.load(open("C:\\Users\\Emmet\\Documents\\MScComputerScienceConversion\\Summer_Project\\Team14\\Git\\dublinbusapp\\dublinbusapp\\dublinbusapp\\pickles\\route" + dbroute + "_model.sav", 'rb'))

			print(dummies)

			df_dum = pd.get_dummies(df_new)
			print("df_dum \n ", df_dum)

			df_x, df_y = dummies.align(df_dum, fill_value=0)

			print("df_y \n", df_y)

			df_final = df_y.reindex(dummies.columns, axis=1)
			print("df_final \n", df_final)


			journeyTimePrediction = loaded_model.predict(df_final)
			print(journeyTimePrediction)
			journeyTimePrediction = journeyTimePrediction.tolist()
			# print(journeyTimePrediction)
			# journeyTimePrediction = journeyTimePrediction[0]

			print('------------------------------------------')
			totalTrips = len(journeyTimePrediction)
			errorCount = 0
			total = 0
			for i in range(0, len(journeyTimePrediction)):
				if journeyTimePrediction[i] > 500 or journeyTimePrediction[i] < -500:
					errorCount += 1
				else:
					total += int(journeyTimePrediction[i])
			print(errorCount)
			print(total)
			avgStopTime = total // (totalTrips - errorCount)
			errorTime = avgStopTime * errorCount
			total += errorTime
			print(total)

			busTime += total


		# Put data from AJAX and the model into dictionary to send back to AJAX as a response
		result = {
				'query': json.loads(request.POST["query"]),
				'origin': request.POST["origin"],
				'destination': request.POST["destination"],
				'dateChosen': request.POST["dateChosen"],
				'lastBusStepPrediction': total/60, # Seconds to minutes
				'routesToTake': routesToTake,
				'busTime': busTime/60, # Seconds to minutes
				'walkingTime': walkingTime,
				'totalTime': (busTime/60) + walkingTime,
				'realTimeInfo': realTimeInfo,
				'weatherNowText': weatherNowText,
				'weatherIcon': weatherIcon,
				'temperature': temperature,
				}

	# Return the result dictionary to AJAX as a response
	return JsonResponse(result, safe=False)
