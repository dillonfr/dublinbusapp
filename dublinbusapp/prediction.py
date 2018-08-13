import numpy
import pandas as pd
from sklearn.externals import joblib

def getUserDataFrame(seqstoplist, dayOfWeek, peak, hourOfDay, rain, temperature):
    ''' Takes in the sequential list of stopids and creates a dataframe of them
    Takes in the user inputted data and creates a dataframe from it
    Concatenates these two dataframes
    Reformats the resulting dataframe for use in the prediction model '''

    # We first turn the stopids into a list
    listOfStops = []
    for i in range(0, len(seqstoplist)):
    	listOfStops.append(seqstoplist[i][0])

    # Create a dataframe out of this list. Consists of one column with a row for each stopid on the journey
    df_list = pd.DataFrame(listOfStops, columns=['stop_point_id'])

    # Create a dictionary that stores the route information we need to pass into the model
    modelData = {'day' : dayOfWeek, 'peak' : peak, 'hour' : hourOfDay, 'rain' : rain, 'temp' : temperature}
    # Create a dataframe out of this information
    df_features = pd.DataFrame(modelData, index=[0])

    # We concatenate the stopids dataframe and the route information dataframes
    df_new = pd.concat([df_features, df_list], axis=1, ignore_index=True)
    df_new = df_new.fillna(method='ffill') # We use this to fill each row in the new dataframe with the route information data

    # Our model works by estimating the time between every stop on a route. We need to create a new column that has the stopid for the next stop
    df_new[6]=df_new[5].shift(-1) # We shift all the data in the stopids column down one place and store this as a new column representing nextstopid
    # We have to reindex the dataframe to fit our model
    columnsTitles=[0, 2, 1, 5, 6, 3, 4]
    df_new = df_new.reindex(columns=columnsTitles)
    # We drop the last row of the dataframe as this has no next stop to go to
    df_new = df_new[:-1]

    # We need to change the data type to int and then category so that our model reads it correctly
    for i in range(0, 7):
    	df_new[i] = df_new[i].astype('int')
    	df_new[i] = df_new[i].astype('category')

    # We drop the temperature column
    df_new = df_new.drop(df_new.columns[6], axis=1)

    # Assign column titles to the new dataframe
    df_new.columns = ['dayofweek', 'peak', 'hour', 'stoppointid', 'nextstop_id', 'rain']

    # Return the combined dataframe
    return df_new

def getCombinedDataFrame(dbroute, df_user):
    ''' Creates an empty dataframe containg all the dummy variables on a given route
    Changes the user dataframe by creating dummy variables for each feature in it
    Combines the empty dataframe and the user dataframe by aligining on matching column names
    Reindexes the resulting dataframe so that it will fit the format expected by our model
    Returns the new dataframe '''

    # Load the empty dataframe for the given route
    dummies = joblib.load(open("C:\\Users\\Emmet\\Documents\\MScComputerScienceConversion\\Summer_Project\\Team14\\Git\\dublinbusapp\\dublinbusapp\\dublinbusapp\\dummies\\route" + dbroute+ "_dummies.sav", 'rb'))

    # Create a dummy variable for each feature in the user dataframe
    df_dum = pd.get_dummies(df_user)

    # Align the user dataframe and empty dataframe by matching column names
    df_x, df_y = dummies.align(df_dum, fill_value=0) # Fill all empty cells with 0

    # Reindex the resulting dataframe to match the format expected by the model
    df_final = df_y.reindex(dummies.columns, axis=1)

    return df_final

def getRouteTime(dbroute, df_combo):
    '''We use GTFS data from July 2018
    The data our model is trained on is from 2016 and the first half of 2017
    Dublin Bus often changes the routes of their buses
    Means we have discrepancies between our timetable data and our historical data
    Some of the stopids we get back for a route from the database may not exist in the historical data
    When this happens, our model returns a wild esitmation of the journey time (billions of seconds)
    To account for this, we set the maximum time limit between stops to 10 seconds
    If any stop-to-stop journey exceeds this limit, we instead use the average time travelling between stops on that particular route takes
    Takes in the route and combined dataframe
    Uses a linear regression model to predict journey time on a stop-by-stop basis
    Sums all of these journey times
    If any journey takes longer than 10 minutes, we instead use the average journey time between stops and move on to the next stop '''

    # Load the linear regression model for the given route
    loaded_model = joblib.load(open("C:\\Users\\Emmet\\Documents\\MScComputerScienceConversion\\Summer_Project\\Team14\\Git\\dublinbusapp\\dublinbusapp\\dublinbusapp\\pickles\\route" + dbroute + "_model.sav", 'rb'))

    # Use the loaded model to make a prediction of the journey time
    journeyTimePrediction = loaded_model.predict(df_combo)

    # Print the journey time for each stop and convert to a list format
    print('Journey Time Prediction for Each Stop: \n', journeyTimePrediction)
    journeyTimePrediction = journeyTimePrediction.tolist()

    # Error handling for any stop-to-stop journey time > 10 minutes
    totalTrips = len(journeyTimePrediction)
    errorCount = 0
    total = 0

    for i in range(0, len(journeyTimePrediction)):
    	if journeyTimePrediction[i] > 600 or journeyTimePrediction[i] < 0:
    		errorCount += 1
    	else:
    		total += int(journeyTimePrediction[i])

    avgStopTime = total // (totalTrips - errorCount)
    errorTime = avgStopTime * errorCount
    total += errorTime

    # Return the route journey time
    return total

def getBackupDataFrame(dayOfWeek, peak, hourOfDay, numStops, rain):

    # Create a dictionary that stores the route information we need to pass into the model
    backupData = {'dayofweek' : dayOfWeek, 'peak' : peak, 'hour' : hourOfDay, 'stopsnumber' : numStops, 'rain' : rain}
    # Create a dataframe out of this information
    df_backup = pd.DataFrame(backupData, index=[0])

    df_backup = df_backup[['dayofweek', 'peak', 'hour', 'stopsnumber', 'rain']]

    df_backup['dayofweek'] = df_backup['dayofweek'].astype('category')
    df_backup['peak'] = df_backup['peak'].astype('category')
    df_backup['hour'] = df_backup['hour'].astype('category')
    df_backup['rain'] = df_backup['rain'].astype('category')

    return df_backup

def getBackupCombo(dbroute, df_user):
    ''' Creates an empty dataframe containg all the dummy variables on a given route, except for the continuous feature stopsnumber
    Changes the user dataframe by creating dummy variables for each catgeorical feature in it
    Combines the empty dataframe and the user dataframe by aligining on matching column names
    Reindexes the resulting dataframe so that it will fit the format expected by our model
    Returns the new dataframe '''

    # Load the empty dataframe for the given route
    dummies = joblib.load(open("C:\\Users\\Emmet\\Documents\\MScComputerScienceConversion\\Summer_Project\\Team14\\Git\\dublinbusapp\\dublinbusapp\\dublinbusapp\\dummies\\basic_route" + dbroute+ "_dummies.sav", 'rb'))
    print(dummies)

    # Create a dummy variable for each feature in the user dataframe
    df_dum = pd.get_dummies(df_user)

    # Align the user dataframe and empty dataframe by matching column names
    df_x, df_y = dummies.align(df_dum, fill_value=0) # Fill all empty cells with 0

    # Reindex the resulting dataframe to match the format expected by the model
    df_final = df_y.reindex(dummies.columns, axis=1)

    return df_final

def getBackupRouteTime(dbroute, df_backupCombo):

    # Load the linear regression model for the given route
    loaded_model = joblib.load(open("C:\\Users\\Emmet\\Documents\\MScComputerScienceConversion\\Summer_Project\\Team14\\Git\\dublinbusapp\\dublinbusapp\\dublinbusapp\\pickles\\basic_route" + dbroute + "_model.sav", 'rb'))

    # Use the loaded model to make a prediction of the journey time
    journeyTimePrediction = loaded_model.predict(df_backupCombo)

    # Print the journey time for each stop and convert to a list format
    print('Journey Time Prediction: \n', journeyTimePrediction)
    journeyTimePrediction = journeyTimePrediction.tolist()

    return journeyTimePrediction[0]
