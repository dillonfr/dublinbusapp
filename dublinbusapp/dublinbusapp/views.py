from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

from buslist import *
from dates import *
from weather import *
from realtime import *
from routedb import *


from django.views.decorators.csrf import csrf_exempt

import pickle
import numpy
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

		conn = connectDB()

		allRoutes = json.loads(request.POST["allRoutes"])

		bestRoute = allRoutes[0] # The first journey suggested by google is the best

		numBusJourneys = len(bestRoute) - 1

		walkingTime = bestRoute[-1]['walkingtime']

		# Initialise times that our model will add minutes to


		# Reformat date chosen into format that can be passed into model
		dateChosen = request.POST["dateChosen"]
		dayOfWeek = stripDay(dateChosen)
		hourOfDay = stripTime(dateChosen)
		peak = isPeak(dateChosen)

		# Check weather conditions
		#print(unixTime(dateChosen))
		uTime = unixTime(dateChosen)

		weatherDict = getWeather(uTime)
		#print(weatherDict)

		rain = weatherDict['raining']
		temperature = weatherDict['temperature']
		windSpeed = weatherDict['windSpeed']
		weatherNowText = weatherDict['weatherNowText']
		weatherIcon = weatherDict['weatherIcon']

		# print(rain)
		# print(temperature)
		# print(windSpeed)


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
			# print(dbroute)
			gtfsday = getGTFSday(dateChosen)
			print(gtfsday)
			timeOfDay = getSeconds(dateChosen)
			print(timeOfDay)

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

			df_new[0] = df_new[0].astype('int')
			df_new[1] = df_new[1].astype('int')
			df_new[2] = df_new[2].astype('int')
			df_new[3] = df_new[3].astype('int')
			df_new[4] = df_new[4].astype('int')
			df_new[5] = df_new[5].astype('int')
			df_new[6] = df_new[6].astype('float')

			df_new[0] = df_new[0].astype('category')
			df_new[1] = df_new[1].astype('category')
			df_new[2] = df_new[2].astype('category')
			df_new[3] = df_new[3].astype('category')
			df_new[4] = df_new[4].astype('category')
			df_new[5] = df_new[5].astype('category')
			df_new[6] = df_new[6].astype('category')

			# print(df_new.dtypes)
			print(df_new)
			# print(df_new.dtypes)

			df_new = df_new.drop(df_new.columns[6], axis=1)

			df_new.columns = ['dayofweek', 'peak', 'hour', 'stoppointid', 'nextstop_id', 'rain']

			# df_dumvars = pd.get_dummies(df_new)

			print(df_new)
			# print(df_dumvars)
			# Create dataframe
			# df = [[dayOfWeek, peak, originId, direction, destinationId, numStops]]

			# Pass df into model and get prediction

			dummies = joblib.load(open("C:\\Users\\Emmet\\Documents\\MScComputerScienceConversion\\Summer_Project\\Team14\\Git\\dublinbusapp\\dublinbusapp\\dublinbusapp\\pickles\\route1_dummies_final.sav", 'rb'))

			loaded_model = joblib.load(open("C:\\Users\\Emmet\\Documents\\MScComputerScienceConversion\\Summer_Project\\Team14\\Git\\dublinbusapp\\dublinbusapp\\dublinbusapp\\pickles\\test_1_LR_dummi.sav", 'rb'))

			#df_empty = df_new.reindex(columns = dummies.columns, fill_value=0)
			df_dum = pd.get_dummies(df_new)
			# print("df_dum \n ", df_dum)

			df_x, df_y = dummies.align(df_dum, fill_value=0)

			df_final = df_y.reindex(dummies.columns, axis=1)
			print("df_final \n", df_final)
			# print("df_empty \n", df_empty)

			# print("df_y \n", df_y)

			journeyTimePrediction = loaded_model.predict(df_final)
			#print(journeyTimePrediction)
			journeyTimePrediction = journeyTimePrediction.tolist()
			# print(journeyTimePrediction)
			# journeyTimePrediction = journeyTimePrediction[0]

			print('------------------------------------------')
			totalTrips = len(journeyTimePrediction)
			errorCount = 0
			total = 0
			for i in range(0, len(journeyTimePrediction)):
				if journeyTimePrediction[i] > 500:
					errorCount += 1
				else:
					total += int(journeyTimePrediction[i])
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
