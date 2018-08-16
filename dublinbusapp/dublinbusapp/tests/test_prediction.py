from prediction import *

def testGetUserDataFrame():
    ''' Tests whether the user dataframe returned has the correct amount of columns and rows
    Need a row for every stop on the trip '''
    testUserDF = getUserDataFrame([('1160',), ('1161',), ('1162',), ('1163',), ('1164',), ('1165',), ('1166',), ('1167',), ('1168',), ('1169',), ('1170',)], 4, 1, 10, 0, 22)
    assert len(testUserDF.columns) == 6, len(testUserDF.index) == 10

def testGetCombinedDataFrame():
    ''' Tests whether the combined dataframe contains the correct amount of columns and rows
    Uses getUserDataFrame() so reliant on that function working properly '''
    testUserDF = getUserDataFrame([('1160',), ('1161',), ('1162',), ('1163',), ('1164',), ('1165',), ('1166',), ('1167',), ('1168',), ('1169',), ('1170',)], 4, 1, 10, 0, 22)
    testComboDF = getCombinedDataFrame('15', testUserDF)
    assert len(testComboDF.columns) == 313, len(testComboDF.index) == 10

def testGetRouteTime():
    ''' Tests that the estimated journey time in seconds returned by the main model is correct
    Uses getUserDataFrame() so reliant on that function working properly
    Uses getCombinedDataFrame() so reliant on that function working properly '''
    testUserDF = getUserDataFrame([('1160',), ('1161',), ('1162',), ('1163',), ('1164',), ('1165',), ('1166',), ('1167',), ('1168',), ('1169',), ('1170',)], 4, 1, 10, 0, 22)
    testComboDF = getCombinedDataFrame('15', testUserDF)
    testJourneyTime = getRouteTime('15', testComboDF)
    assert testJourneyTime == 791

def testGetBackupDataFrame():
    ''' Tests whether the backup user dataframe returned has the correct amount of columns and rows
    Consists of only one row '''
    testBackupUserDF = getBackupDataFrame(5, 0, 16, 20, 0)
    assert len(testBackupUserDF.columns) == 5, len(testBackupUserDF.index) == 1

def testGetBackpCombo():
    ''' Tests whether the backup combined dataframe contains the correct amount of columns and rows
    Uses getBackupDataFrame() so reliant on that function working properly '''
    testBackupUserDF = getBackupDataFrame(5, 0, 16, 20, 0)
    testBackupComboDF = getBackupCombo('15', testBackupUserDF)
    assert len(testBackupComboDF.columns) == 32, len(testBackupComboDF.index) == 1

def testGetBackupRouteTime():
    ''' Tests that the estimated journey time in seconds returned by the backup model is correct
    Uses getBackupDataFrame() so reliant on that function working properly
    Uses getBackupCombo() so reliant on that function working properly '''
    testBackupUserDF = getBackupDataFrame(5, 0, 16, 20, 0)
    testBackupComboDF = getBackupCombo('15', testBackupUserDF)
    testBackupJourneyTime = getBackupRouteTime('15', testBackupComboDF)
    assert int(testBackupJourneyTime) == 1583
