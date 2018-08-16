import urllib.request
import json
import time
import datetime
import geopy
from geopy import distance
from geopy.distance import vincenty

def stripDay(date):
	''' Takes in specific datetime format and returns the weekday as an int
	Sample input: "23 July 2018 - 04:30 pm"
	'''
	if date == "":
		DayInt = int(datetime.datetime.today().weekday()) + 1
	elif date[-2] == 'p':
		DayInt = int(datetime.datetime.strptime(date, '%d %B %Y - %H:%M pm').strftime('%w'))
	elif date[-2] == 'a':
		DayInt = int(datetime.datetime.strptime(date, '%d %B %Y - %H:%M am').strftime('%w'))

	if DayInt == 0:
		return 7
	else:
		return DayInt

def stripTime(date):
	''' Takes in specific datetime format and returns the hour as an int between 0 and 23'''

	if date == "":
		return datetime.datetime.today().hour
	elif date[-2] == 'a': # Check if time is AM
		return int(datetime.datetime.strptime(date, '%d %B %Y - %H:%M am').strftime('%H'))
	elif date[-2] == 'p': # Check if time is PM
		time = int(datetime.datetime.strptime(date, '%d %B %Y - %H:%M pm').strftime('%H')) + 12

	if time > 23: # Error check for midday
		time = 12

	return time

def isPeak(date):
	''' Function that checks if a specific datetime format is within peak hours
	Peak hours are between 7-10am and 4-7pm
	'''
	if date == "":
		HourInt = datetime.datetime.today().hour
		if HourInt >= 7 and HourInt <= 10 or HourInt >= 16 and HourInt <= 19:
			return 1 # Within peak hours
		else:
			return 0 # Not within peak hours
	elif date[-2] == 'a':
		HourInt = int(datetime.datetime.strptime(date, '%d %B %Y - %H:%M am').strftime('%H'))
		if HourInt >= 7 and HourInt <= 10:
			return 1
		else:
			return 0
	elif date[-2] == 'p':
		HourInt = int(datetime.datetime.strptime(date, '%d %B %Y - %H:%M pm').strftime('%H'))
		if HourInt >= 4 and HourInt <= 7:
			return 1
		else:
			return 0

def unixTime(date):
	''' Converts the given date into Unix time to get the weather forecast information '''

	if date == "":
	    uTime = int(time.time())
	elif date[-2] == 'p':
	    uTime = int(time.mktime(datetime.datetime.strptime(date, '%d %B %Y - %H:%M pm').timetuple())) + 43200
	elif date[-2] == 'a':
	    uTime = int(time.mktime(datetime.datetime.strptime(date, '%d %B %Y - %H:%M am').timetuple()))


	limit = int(time.time()) + 604800 # Limit is current time + 7 days

	if uTime > limit:
	    return int(time.time())
	else:
	    return int(uTime)


def getRouteStops(routeNumber):
	''' Function that returns the latitude and longitude of each bus stopid in a given route
	A dictionary is returned: key is stopid and associated value is latitude/longitude '''

	stopidDict = {}


	jsonFile = "C:\\Users\\dillo_000\\Desktop\\dublinbusapp\\dublinbusapp\\static\\all_stops_on_routes\\" + str(routeNumber) + ".json"
	#jsonFile = "/Users/yulia/Desktop/prefinal/dublinbusapp/static/all_stops_on_routes/" + str(routeNumber) + ".json"


	with open(jsonFile, encoding='utf-8') as data_file:
	    Stops = json.loads(data_file.read())


	for chosenRoute in Stops["results"]:
		for stop in chosenRoute["stops"]:
			stopID = stop["stopid"]
			lat = float(stop["latitude"])
			lng = float(stop["longitude"])
			stopidDict[stopID] = {"lat":lat, "lng":lng} # We only care about the stopids and their lat/long

	return stopidDict



def getStopId(dictlist, lat_lng):
	''' Function that returns the stopid's for the closest stops to the given lat/long
	The Google Directions Service returns lat/long for each stop that is slightly different to Dublin Bus lat/long for the same stop
	Finds the closest matching latitude and longtude to the inputted one and returns the corresponding stopid
	Takes a dictionary of stopid: lat/long and a target lat/long as arguments '''

	# Calculate the distance between each stopid in a route and the inputted lat/long
	for key in dictlist.keys():
		dictlist[key].update({"distance": geopy.distance.vincenty([dictlist[key]["lat"], dictlist[key]["lng"]], lat_lng).km})

	# Sort the dictionary by the shortest distance
	sortedDict = sorted(dictlist.items(), key = lambda x_y: x_y[1]["distance"]) 

	# Return the 4 closest stop id's to the given lat_lng
	needed_stops = sortedDict[0][0], sortedDict[1][0], sortedDict[2][0], sortedDict[3][0]
	return needed_stops 