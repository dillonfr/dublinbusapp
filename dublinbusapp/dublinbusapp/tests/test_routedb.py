from routedb import *

Date = "23 July 2018 - 04:30 pm"

def testGetGTFSDay():
    testDay = getGTFSday(Date)
    assert testDay == '"y102v", "y1022", "y1023"'

def testGetSeconds():
    testSeconds = getSeconds(Date)
    assert testSeconds == 59400

# def testGetStartStop():
#     conn = connectDB()
#     testStart = getStartStop(conn, '15', '"y102v", "y1022", "y1023"', '1160', 59400)
#     assert testStart == [('4773.y1022.60-15-b12-1.194.I', 16)]

def testGetEndStop():
    conn = connectDB()
    testStop = getEndStop(conn, '4773.y1022.60-15-b12-1.194.I', '1072')
    assert testStop == 12
