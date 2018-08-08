from weather import *

def testGetWeather():
    testWeather = getWeather(1532316600)
    assert testWeather != None
