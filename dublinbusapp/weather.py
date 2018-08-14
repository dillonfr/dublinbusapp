import requests


def getWeather(unixTime):
	'''Gets the weather conditions at a given time from DarkSky API'''


	# Make request with time specified
	url = "https://api.darksky.net/forecast/677b0825944f34372369ece7b0a8bc46/53.2049,6.1531," + str(unixTime) + "?units=si"

	weatherData = requests.get(url).json()

	# Load the current weather at that time
	currentWeather = weatherData['currently']

	# Decide if it is likely raining or not based on probability of precipiation
	chanceOfRain = currentWeather['precipProbability']

	if chanceOfRain > 0.5:
		rain = 1
	else:
		rain = 0

	# Add info needed to dict
	weatherDict = {
		'rainProbability': currentWeather['precipProbability'], # Decimal probability of precipiation (rain, snow..)
		'raining': rain, # 1 for raining, 0 for not raining
		'temperature': currentWeather['temperature'], # Celsius
		'windSpeed': currentWeather['windSpeed'], # Metres per Second
		'visibility': currentWeather['visibility'], # Kilometers
		'weatherNowText': currentWeather['summary'],
		'weatherIcon': currentWeather['icon'],
	}

	return weatherDict
	