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
	''' When someone visits our domain name this renders the homepage for them
	Returns index.html '''

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
			conn = connectDB() # Establish a connection to the DB

			allRoutes = json.loads(request.POST["allRoutes"]) # Retrieve all possible journeys
      
			bestRoute = allRoutes[0] # The first journey suggested by google is the best

		  walkingTime = bestRoute[-1]['walkingtime']
		  walkTimeToStop = bestRoute[-1]['walkTimeToStop']
		  totalLuasTime = bestRoute[-1]['totalLuasTime']

			numBusJourneys = len(bestRoute) - 1 # Calulate the number of different buses a user needs to take


			# Retrieve the date chosen by the user
			dateChosen = request.POST["dateChosen"]

			# Use the chosen date to get some of the features we need for the model
			dayOfWeek = stripDay(dateChosen) # Returns integer representation of day of the week (1-7)
			hourOfDay = stripTime(dateChosen) # Returns integer representation of hour of the day (0-23)
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

			print('Rain: \n', rain)

			routesToTake =[] # Initialise the number of different buses a user needs to take to 0
			busTime = 0 # Intialise the time the total journey will take to 0
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

				# Find all of the stopid's on the route
				stopsDictList = getRouteStops(str(route))

				# Find the closest stopid's with the given latitudes/longitudes
				originId = str(getStopId(stopsDictList, originLatLng)[0])
				destinationId = str(getStopId(stopsDictList, destinationLatLng))

				#print("Origin ID: \n", originId)
				#print("Destination ID: \n", destinationId)

				# Get realtime info for the first bus stop id of the journey
				if isFirstStopId == False:
					realTimeInfo = getRealTimeInfo(originId) # Returns a list
					isFirstStopId = True

				try:
					''' We first try and use our main model to predict the time for the route
					The main model only occasionaly fails so we use this most of the time '''

					# Convert data we have into a format that can be used to query the database
					dbroute = route.upper() # Routes are stored in database with capital letters e.g. 7D, 15B, etc.
					gtfsday = getGTFSday(dateChosen) # Day of the week is stored in database in non-integer form
					timeOfDay = getSeconds(dateChosen) # We need to get the time in seconds since midnight

					# Query the database with this data and return best result i.e. a journey that matches our parameters and is closest to the departure time
					tripdata = getStartStop(conn, dbroute, gtfsday, originId, timeOfDay)[0]
					trip_id = tripdata[0] # Store the tripid. We use this in the next query to guarantee we are using the same trip in the timetable
					startnum = tripdata[1] # This is the sequence number for the starting stop
					print('Trip ID:\n', trip_id)
					print('Start Sequence No.:\n', startnum)

					# Query the database with the tripid and destination stopid to get the sequence number for the last stop
					stopnum = getEndStop(conn, trip_id, destinationId)[0][0] # This is the sequence number for the last stop
					print('Stop Sequence No.:\n', stopnum)

					# Query the database for every stopid between the start and stop sequence numbers
					seqstoplist = getStopList(conn, trip_id, startnum, stopnum) # A list of every stop between start and end
					print('List of Stops in Sequential Order:\n', seqstoplist)

					print('-------------------------------------------------------------')

					# Create a dataframe from the user data retrieved from frontend
					df_user = getUserDataFrame(seqstoplist, dayOfWeek, peak, hourOfDay, rain, temperature)
					print('User Data DF: \n', df_user)

					# Create a new dataframe that combines the user one with an empty dataframe containing dummy variables for every route
					df_combo = getCombinedDataFrame(dbroute, df_user)
					#print(df_combo)

					print('-------------------------------------------------------------')

					routeTime = getRouteTime(dbroute, df_combo)
					print('Route Journey Time: \n', routeTime)

					busTime += routeTime

				except:
					try:
						''' This block of code is executed if we can't use our main model
						On rare occasions our main model fails because of issues with accurately determining the user's start stop
						We have a more basic backup model for each route if this occurs '''

						print('---------------------------------------------------------')
						print('******** Backup Model Employed ********')
						print('---------------------------------------------------------')

						# Create a backup dataframe from the user data and information from Google Directions Service API
						df_backup = getBackupDataFrame(dayOfWeek, peak, hourOfDay, numStops, rain)
						print('Backup Dataframe: \n', df_backup)

						print('---------------------------------------------------------')

						df_backupCombo = getBackupCombo(dbroute, df_backup)
						#print('Backup Combined Dataframe: \n', df_backupCombo)

						print('-------------------------------------------------------------')

						routeTime = getBackupRouteTime(dbroute, df_backupCombo)
						print('Route Journey Time: \n', routeTime)

						busTime += routeTime

					except:
						''' If our backup model also fails we use the Google estimation for the route time
						We don't envision this ever happening but it is just a failsafe if something goes wrong '''
						busTime += bestRoute[i]['googleTime']

			print('-------------------------------------------------------------')
			print('Total Journey Time (Sum of All Routes): \n', busTime)

			# Put data from AJAX and the model into dictionary to send back to AJAX as a response
			result = {
					'query': json.loads(request.POST["query"]),
					'dateChosen': request.POST["dateChosen"],
					'lastBusStepPrediction': routeTime/60, # Seconds to minutes
					'routesToTake': routesToTake,
					'busTime': busTime/60, # Seconds to minutes
					'walkingTime': walkingTime,
          'walkTimeToStop': walkTimeToStop,
          'totalLuasTime': totalLuasTime/60, # Seconds to minutes
					'totalTime': (busTime/60) + walkingTime + (totalLuasTime/60),
					'realTimeInfo': realTimeInfo,
					'weatherNowText': weatherNowText,
					'weatherIcon': weatherIcon,
					'temperature': temperature,
					}

		# Return the result dictionary to AJAX as a response
		return JsonResponse(result, safe=False)

	except:
		result = 'Error! Something Has Gone Horribly Wrong! Oh Boy! What a Mess!'
		#print(result)
		return JsonResponse(result, safe=False)