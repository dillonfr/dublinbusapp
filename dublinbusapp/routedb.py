import sqlite3
import time
import datetime

def connectDB():
    ''' Connects to the sqlite database
    Raises an exception if connection cannot be made'''
    try:
        conn = sqlite3.connect('mydatabase')
        print('-----------------------------------------------------------------')
        print('Successfully connected to DB')
        return conn
    except Error as e:
        print(e)
    return None

def getGTFSday(date):
    ''' Takes in specific datetime format and returns a day in GTFS format for querying DB'''

    if date == "":
        DayInt = datetime.datetime.today().weekday()
    elif date[-2] == 'p':
        DayInt = int(datetime.datetime.strptime(date, '%d %B %Y - %H:%M pm').strftime('%w'))
    elif date[-2] == 'a':
        DayInt = int(datetime.datetime.strptime(date, '%d %B %Y - %H:%M am').strftime('%w'))

    if DayInt >= 0 and DayInt <= 4:
        gtfsday = '"y102v", "y1022", "y1023"'
    elif DayInt == 5:
        gtfsday = '"y1024", "y102w", "y1022", "y1023"'
    elif DayInt == 6:
        gtfsday = '"y102x", "y1022", "y1023"'

    return str(gtfsday)

def getSeconds(date):
    ''' Takes in specific datetime format and returns the time in seconds since midnight'''

    now = datetime.datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)

    if date == "":
        seconds = (now - midnight).seconds
    elif date[-2] == 'a':
        time = datetime.datetime.strptime(date, '%d %B %Y - %H:%M am').strftime('%H:%M:%S')
        h, m, s = time.split(':')
        seconds = int(h) * 3600 + int(m) * 60 + int(s)
    elif date[-2] =='p':
        time = datetime.datetime.strptime(date, '%d %B %Y - %H:%M pm').strftime('%H:%M:%S')
        h, m, s = time.split(':')
        seconds = int(h) * 3600 + int(m) * 60 + int(s) + 43200

    return int(seconds)

def getStartStop(conn, route, dayOfWeek, originID, timeOfDay):
    ''' Takes in route, day of the week, stopid of first stop and time of day
    The database contains the timetable for every stop and every route for the month of August
    Searches database for trips that fit the given parameters
    timeOfDay is in seconds from midnight. We return the trip with a departure time from the stop that is closest to the user's chosen one
    Returns the unique tripid for the chosen trip and the sequence number for the starting stop '''

    c = conn.cursor()

    print("---------------------------------------------------------------------")
    print('Start Query: \nSELECT trip_id, stop_sequence FROM routestops WHERE route_number = "'+route+'" AND day IN ('+dayOfWeek+') AND stop_id IN ('+originID+') AND departure_time >= "+timeOfDay+" ORDER BY departure_time LIMIT 1')

    response = c.execute('SELECT trip_id, stop_sequence FROM routestops WHERE route_number = "'+route+'" AND day IN ('+dayOfWeek+') AND stop_id = "'+originID+'" AND departure_time >= ? ORDER BY departure_time LIMIT 1;', [timeOfDay])

    rows = c.fetchall()

    return rows

def getEndStop(conn, trip_id, destinationId):
    ''' Takes in a unique tripid and the 4 possible stopids for the last stop in the route
    Only searches entries in the database that have the same tripid. Guarantees that we are using the same trip from the first query
    Returns the sequence number for the last stop '''

    c = conn.cursor()

    print("---------------------------------------------------------------------")
    print('End Query: \nSELECT stop_sequence FROM routestops WHERE trip_id = "'+trip_id+'" AND stop_id IN '+destinationId+'')

    response = c.execute('SELECT stop_sequence FROM routestops WHERE trip_id = "'+trip_id+'" AND stop_id IN '+destinationId+';')

    rows = c.fetchall()

    return rows

def getStopList(conn, trip_id, startnum, stopnum):
    ''' Takes in a unique tripid and the sequence number of the first and last stop in the route
    Only searches entries in the database that have the same tripid. Guarantees that we are using the same trip from previous queries
    Returns the stopid for every stop between the starting and end stop '''

    c = conn.cursor()

    print("---------------------------------------------------------------------")
    print('Stoplist Query: \nSELECT stop_id FROM routestops WHERE trip_id = "'+trip_id+'" AND stop_sequence BETWEEN "+startnum+" AND "+stopnum+"')

    if startnum < stopnum:
        response = c.execute('SELECT stop_id FROM routestops WHERE trip_id = "'+trip_id+'" AND stop_sequence BETWEEN ? AND ?;', (startnum, stopnum))
    else:
        response = c.execute('SELECT stop_id FROM routestops WHERE trip_id = "'+trip_id+'" AND stop_sequence BETWEEN ? AND ?;', (stopnum, startnum))

    rows = c.fetchall()

    return rows
