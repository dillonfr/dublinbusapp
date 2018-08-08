from realtime import *

def testGetRealTimeInfo():
    testRTI = getRealTimeInfo(1024)
    assert testRTI != None
