import time
from weather import *

def testGetWeather():
    ''' Tests if the getWeather function returns an empty object
    Uses current time to test '''
    testTime = int(time.time())
    testWeather = getWeather(testTime)
    assert testWeather != None
