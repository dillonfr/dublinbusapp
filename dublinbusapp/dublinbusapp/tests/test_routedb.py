from routedb import *

Date = "23 July 2018 - 04:30 pm"

def testGetGTFSDay():
    ''' Tests if the date from the user is translated correctly into the format used in the database '''
    testDay = getGTFSday(Date)
    assert testDay == '"y102v", "y1022", "y1023"'

def testGetSeconds():
    ''' Tests if the time from the user is translated correctly into the format used in the database '''
    testSeconds = getSeconds(Date)
    assert testSeconds == 59400

def testGetStartStop():
    ''' Tests the database query that returns the trip ID and sequence number for the starting stop '''
    conn = connectDB()
    testStart = getStartStop(conn, '15', '"y102v", "y1022", "y1023"', '1160', 59400)
    assert testStart == [('4773.y1022.60-15-b12-1.194.I', 16)]

def testGetEndStop():
    ''' Tests the database query that returns the sequence number for the desitination stop '''
    conn = connectDB()
    testStop = getEndStop(conn, '4773.y1022.60-15-b12-1.194.I', '("1170")')
    assert testStop[0][0] == 26

def testGetStopList():
    ''' Tests the database query that return the sequential list of stops between the start and end stop '''
    conn = connectDB()
    testList = getStopList(conn, '4773.y1022.60-15-b12-1.194.I', 16, 26)
    assert testList == [('1160',), ('1161',), ('1162',), ('1163',), ('1164',), ('1165',), ('1166',), ('1167',), ('1168',), ('1169',), ('1170',)]
