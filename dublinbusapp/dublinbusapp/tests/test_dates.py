from dates import *

Date = "23 July 2018 - 04:30 pm"

def testStripDay():
    ''' Tests that the correct day in integer form is returned for a given datetime '''
    testDay = stripDay(Date)
    assert testDay == 1

def testStripTime():
    ''' Tests that the correct hour in integer form is returned for a given datetime '''
    testTime = stripTime(Date)
    assert testTime == 16

def testIsPeak():
    ''' Tests whether a given datetime is peak/off-peak '''
    testPeak = isPeak(Date)
    assert testPeak == 1

def testUnixTime():
    ''' Tests if the unixtime for a given datetime is correct '''
    testUnix = unixTime(Date)
    assert testUnix == 1532316600

def testGetRouteStops():
    ''' Tests if the stopid: latitude, longitude dictionary is not empty for a give route '''
    testStops = getRouteStops(15)
    assert testStops != None

def testGetStopId():
    ''' Tests if the returned stopid for a given latitude/longitude is correct '''
    route = getRouteStops(15)
    latlong = "53.27423, -6.3312"
    testStopId = getStopId(route, latlong)
    assert testStopId == ('6335', '6283', '6326', '3007')
