from prediction import *

def testGetUserDataFrame():
    ''' Tests whether the dataframe returned has the correct amount of columns and rows '''
    testUserDF = getUserDataFrame([('1160',), ('1161',), ('1162',), ('1163',), ('1164',), ('1165',), ('1166',), ('1167',), ('1168',), ('1169',), ('1170',)], 4, 1, 10, 0, 22)
    assert len(testUserDF.columns) == 6, len(testUserDF.index) == 10
