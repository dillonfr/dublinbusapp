import requests

def getRealTimeInfo(stopId):
	''' Function that gets the realtime info on buses and their arrival time for a specific Dublin bus stop id'''

	url = "https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid=" + str(stopId)

	realTimeData = requests.get(url).json()

	results = realTimeData['results']

	numResults = len(realTimeData['results']) # Number of buses coming within the next hour

	# Stores a list of dictionaries, each dictionary holds a route and arrival time as its key:value
	realTimeList = []

	for i in range(0, numResults):
		busArrivalDict = {}

		route = results[i]['route']
		arrivalTime = results[i]['duetime'] # Minutes until the bus is due to arrive

		busArrivalDict[route] = arrivalTime 

		realTimeList.append(busArrivalDict)

	return realTimeList