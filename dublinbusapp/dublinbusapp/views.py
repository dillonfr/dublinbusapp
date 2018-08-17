# Django modules
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Data analytics modules
from sklearn.externals import joblib
import pickle
import numpy
import pandas as pd

# Modules containing various functions needed
from dates import *
from weather import *
from realtime import *
from routedb import *
from prediction import *


@csrf_exempt
def index(request):
	''' When someone visits our domain name this renders the homepage for them'''
	return render(request, 'index.html')


@csrf_exempt
def journey(request):
	''' Main function for our web app
	Takes in the user information from the frontend
	Passes this information into our model to generate an estimation for the journey time
	Queries the database containing information on the route timetables to ensure our provided time is valid
	Returns a dictionary containing all of the information for the user
	Dictionary is used to populate the pop-up window '''


	try:
		if request.method == "POST":
			conn = connectDB()

			allRoutes = json.loads(request.POST["allRoutes"]) # Retrieve all possible journeys suggested by Google

			bestRoute = allRoutes[0] # The first journey suggested by Google is the best

			walkingTime = bestRoute[-1]['walkingtime']
			walkTimeToStop = bestRoute[-1]['walkTimeToStop']
			totalLuasTime = bestRoute[-1]['totalLuasTime']

			numBusJourneys = len(bestRoute) - 1 # Calulate the number of different buses a user needs to take

			# Retrieve date chosen by the user
			dateChosen = request.POST["dateChosen"]

			# Error check date chosen received from datetime picker, make sure date chosen is a string
			if isinstance(dateChosen, str) == False:
				dateChosen = ""

			# Use the chosen date to get some of the features we need for the model
			dayOfWeek = stripDay(dateChosen) # Returns integer representation of day of the week (1-7)
			hourOfDay = stripTime(dateChosen) # Returns integer representation of hour of the day (0-23)

			if hourOfDay < 6:
				result = "<h3>Shhh the buses are sleeping...</h3><h6>(Dublin Bus service not available until 6am)</h6>"
				return JsonResponse(result, safe=False)

			peak = isPeak(dateChosen) # Returns 1 if chosen time is during peak travle times, 0 otherwise

			# Get a weather forecast for the chosen date so we can pass this into the model
			uTime = unixTime(dateChosen) # Need to get the chosen datetime in unix time

			weatherDict = getWeather(uTime) # Create a dictionary of weather details

			# Some basic error handling for the weather
			if weatherDict != None: # If our API request to DarkSky is successful we proceed with the returned information
				rain = weatherDict['raining']
				temperature = weatherDict['temperature']
				weatherNowText = weatherDict['weatherNowText']
				weatherIcon = weatherDict['weatherIcon']
			else:
				rain = 0 # If no forecast weather returns we default to 0 (not raining). We care about rain as this is used in the model

			routesToTake =[] # Bus routes needed to complete the journey
			busTime = 0 # Time spent on bus
			isFirstStopId = True

			#Go through each bus leg and get a prediction on journey time for that leg
			for i in range(0, numBusJourneys):
				# Add each route to list of routes to take
				route = bestRoute[i]['route']
				routesToTake.append(route)

				# Extract data needed to pass into model
				originLatLng = bestRoute[i]['departureLatLng']
				destinationLatLng = bestRoute[i]['arrivalLatLng']
				numStops = bestRoute[i]['numStops']

				try:
					# Find all of the stopid's on the route
					stopsDictList = getRouteStops(str(route))

					# Find the closest stopid's with the given latitudes/longitudes
					originId = str(getStopId(stopsDictList, originLatLng)[0])
					destinationId = str(getStopId(stopsDictList, destinationLatLng))

				except Exception as e:
					print(str(e))
					if i == 0:
						realTimeInfo =[]
						isFirstStopId = False
					busTime += bestRoute[i]['googleTime']
					continue

				# Get realtime info for the first bus stop id of the journey
				if isFirstStopId == True:
					realTimeInfo = getRealTimeInfo(originId) # Returns a list
					isFirstStopId = False

				try:
					''' Use main model to predict the time for the route'''

					# Convert data we have into a format that can be used to query the database
					dbroute = route.upper() # Change letters to uppercase e.g. 15B
					gtfsday = getGTFSday(dateChosen) # Day of the week is stored in database in non-integer form
					timeOfDay = getSeconds(dateChosen) # Seconds since midnight

					# Query the database with this data and return best result i.e. a journey that matches our parameters and is closest to the departure time
					tripdata = getStartStop(conn, dbroute, gtfsday, originId, timeOfDay)[0]
					trip_id = tripdata[0] # Store the tripid. We use this in the next query to guarantee we are using the same trip in the timetable
					startnum = tripdata[1] # This is the sequence number for the starting stop

					# Query the database with the tripid and destination stopid to get the sequence number for the last stop
					stopnum = getEndStop(conn, trip_id, destinationId)[0][0] # This is the sequence number for the last stop

					# Query the database for every stopid between the start and stop sequence numbers
					seqstoplist = getStopList(conn, trip_id, startnum, stopnum) # A list of every stop between start and end

					# Create a dataframe from the user data retrieved from frontend
					df_user = getUserDataFrame(seqstoplist, dayOfWeek, peak, hourOfDay, rain, temperature)

					# Create a new dataframe that combines the user one with an empty dataframe containing dummy variables for every route
					df_combo = getCombinedDataFrame(dbroute, df_user)

					routeTime = getRouteTime(dbroute, df_combo)

					busTime += routeTime

				except Exception as e:
					print(str(e))
					try:
						''' This block of code is executed if we can't use our main model
						On rare occasions our main model fails because of issues with accurately determining the user's start stop
						We have a more basic backup model for each route if this occurs '''

						# Create a backup dataframe from the user data and information from Google Directions Service API
						df_backup = getBackupDataFrame(dayOfWeek, peak, hourOfDay, numStops, rain)

						df_backupCombo = getBackupCombo(dbroute, df_backup)

						routeTime = getBackupRouteTime(dbroute, df_backupCombo)

						if routeTime > 20000:
							raise Exception("Dataframe Error. Backup model valuation invalid")

						busTime += routeTime

					except Exception as e:
						''' If our backup model also fails we use the Google estimation for the route time
						We don't envision this ever happening but it is just a failsafe if something goes wrong '''
						print(str(e))
						busTime += bestRoute[i]['googleTime']

			# Put data from AJAX and the model into dictionary to send back to AJAX as a response
			result = {
					'query': json.loads(request.POST["query"]),
					'dateChosen': request.POST["dateChosen"],
					'routesToTake': routesToTake,
					'busTime': busTime//60, # Seconds to minutes
					'walkingTime': walkingTime,
	      			'walkTimeToStop': walkTimeToStop,
	      			'totalLuasTime': totalLuasTime//60, # Seconds to minutes
					'totalTime': (busTime//60) + walkingTime + (totalLuasTime//60),
					'realTimeInfo': realTimeInfo,
					'weatherNowText': weatherNowText,
					'weatherIcon': weatherIcon,
					'temperature': temperature,
					}

		# Return the result dictionary to AJAX as a response
		return JsonResponse(result, safe=False)


	except Exception as e:
		print(str(e))
		result = "<h3>Error! Something Has Gone Horribly Wrong! Oh Boy! What a Mess!</h3>"
		return JsonResponse(result, safe=False)
