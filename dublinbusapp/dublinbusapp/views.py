from django.http import HttpResponse
from django.http import JsonResponse

from django.shortcuts import render

from .models import Trips2017
from dict import *
from .forms import *
from dates import *

from django.views.decorators.csrf import csrf_exempt

import pickle
import pandas as pd


#TODO Put these into dates.py and import
# import urllib.request
# import json
# import geopy
# from geopy import distance
# from geopy.distance import vincenty
# import datetime

# def StripDay(date):
#    if date == "":
#        DayInt = datetime.datetime.today().weekday()
#    elif date[-2] == 'p':
#        DayInt = datetime.datetime.strptime(date, '%d %B %Y - %H:%M pm').strftime('%w')
#    elif date[-2] == 'a':
#        DayInt = datetime.datetime.strptime(date, '%d %B %Y - %H:%M am').strftime('%w')
#    return int(DayInt) + 2


# def stripTime(date):
#    if date == "":
#        return datetime.datetime.today().hour
#    elif date[-2] == 'a':
#        return int(datetime.datetime.strptime(date, '%d %B %Y - %H:%M am').strftime('%H'))
#    elif date[-2] == 'p':
#        return int(datetime.datetime.strptime(date, '%d %B %Y - %H:%M pm').strftime('%H')) + 12

# def IsPeak(date):
#    if date == "":
#        HourInt = datetime.datetime.today().hour
#        if HourInt >= 7 and HourInt <= 10 or HourInt >= 16 and HourInt <= 19:
#            return 2
#        else:
#            return 1
#    elif date[-2] == 'a':
#        HourInt = int(datetime.datetime.strptime(date, '%d %B %Y - %H:%M am').strftime('%H'))
#        if HourInt >= 7 and HourInt <= 10:
#            return 2
#        else:
#            return 1
#    elif date[-2] == 'p':
#        HourInt = int(datetime.datetime.strptime(date, '%d %B %Y - %H:%M pm').strftime('%H'))
#        if HourInt >= 4 and HourInt <= 7:
#            return 2
#        else:
#            return 1

# def getRouteStops(routeNumber):
#    ''' Function that returns the latitude and longitude of each bus stopid in a given route
#    Takes a route number as an argument
#    A dictionary is returned: key is stopid and associated value is latitude/longitude '''
   
#    # Initialise the empty dictionary
#    stopidDict = {}
   
#    # Scrape all available data on the given route
#    url = "https://data.dublinked.ie/cgi-bin/rtpi/routeinformation?routeid=" + str(routeNumber) + "&operator=bac&format=json"
#    with urllib.request.urlopen(url) as req:
#        Stops = json.loads(req.read().decode("utf-8"))
       
#    for chosenRoute in Stops["results"]:
#            for stop in chosenRoute["stops"]:
#                stopID = stop["stopid"]
#                lat = float(stop["latitude"])
#                lng = float(stop['longitude'])
#                stopidDict[stopID] ={"lat":lat, "lng": lng} # We only care about the stopids and their lat/long
   
#    return stopidDict


# def getStopId(dictlist, lat_lng):
# 	for key in dictlist.keys():
# 		dictlist[key].update({"distance": geopy.distance.vincenty([dictlist[key]["lat"], dictlist[key]["lng"]], lat_lng).km})

# 	sortedDict = sorted(dictlist.items(), key = lambda x_y: x_y[1]["distance"])

# 	return sortedDict[0][0]


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
		dayOfWeek = StripDay(dateChosen)
		peak = IsPeak(dateChosen)
		routesToTake =[]

		#Go through each bus leg and get a prediction on journey time for that leg
		for i in range(0, numBusJourneys):
			route = bestRoute[i]['route']
			routesToTake.append(route)
			originLatLng = bestRoute[i]['departurelatlng']
			destinationLatLng = bestRoute[i]['arrivallatlng']
			numStops = bestRoute[i]['numstops']


			stopsDictList = getRouteStops(str(route))
			print("Made this dictlist")
			print(stopsDictList)

			originId = int(getStopId(stopsDictList, originLatLng))
			destinationId = int(getStopId(stopsDictList, destinationLatLng))
			direction = 2

			df = [[dayOfWeek, peak, originId, direction, destinationId, numStops]]
			#df.append(dayOfWeek)

			print("OUR DF")
			print(df)


			loaded_model = pickle.load(open("C:/Users/dillo_000/Desktop/dublinbusapp/dublinbusapp/dublinbusapp/test_7D_pickle.sav", 'rb'))



			journeyTimePrediction = loaded_model.predict(df)
			journeyTimePrediction = journeyTimePrediction.tolist()
			journeyTimePrediction = journeyTimePrediction[0]

			busTime += journeyTimePrediction
			print(route)
			print(busTime)


		print("New bustime")
		print(busTime)
		# Getting a sample result from a sample pickle file


		# Parsing data received from AJAX
		result=json.loads(request.POST["query"]) #result is a list

		result.append(request.POST["testInput"])
		result.append(request.POST["origin"])
		result.append(request.POST["destination"])
		result.append(journeyTimePrediction)
		result.append(request.POST["dateChosen"])
		result.append(routesToTake)
		result.append(busTime/60)

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


	

