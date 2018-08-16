import pandas as pd
import mysql.connector
import numpy as np
import time

# //================== Clean Trips ====================//
def cleanTrips(result):
	'''
		after we observed the trips data, we chose some columns,like
		['dayofservice','tripid','lineid','direction'], which maybe useful in the next processes
		and decided to drop some unnecessary columns
	'''
	df = pd.DataFrame(result) 
	# check for duplicate rows and columns
	print('Duplicate rows:', df.duplicated()[df.duplicated() == True].shape[0])
	print('Duplicate columns:',df.columns.size - df.columns.unique(  ).size)

	#  set columns name
	df.columns = ['dayofservice','tripid','lineid','direction']

	# transfer the "dayofservice" into datetime
	df['dayofservice'] = pd.to_datetime(df['dayofservice'])

	# save the cleaned data in to new file
	df.to_csv('trips_2017_cleaned.csv', index=False)
	return df

# //================== Clean leavetimes ====================//
def cleanLeavetimes(filename):
	'''
		because the size of leavetimes files are larger than the trips, after test, 
		we decided to use bash to split data instead of getting data into database
		Command: split -l 5000000 rt_leavetimes_2017_I_DB.txt leavetime2017_      
	'''
	
	# get the dayofweek from dayofservice
	df_day = pd.read_csv(filename,sep=';',header=None,usecols=[1])
	df_day.columns = ['dayofservice']
	df_day['dayofservice'] = pd.to_datetime(df_day['dayofservice'],format='%d-%b-%y %H:%M:%S')
	df_day ['dayofweek'] = df_day['dayofservice'] .dt.weekday_name
	df_day ['dayofweek'] = df_day ['dayofweek'].astype('category')

	#  deal with other columns-
	df_data = pd.read_csv(filename,sep=';',header=None,usecols=[2,3,4,5,6,7,8,9])
	df_data.columns = ['tripid','progrnumber','stoppointid','plannedtime_arr','plannedtime_dep','actualtime_arr','actualtime_dep','vehicleid']
	df_data['tripid'] = df_data['tripid'].astype('int')
	df_data['progrnumber'] = df_data['progrnumber'].astype('int')
	df_data['stoppointid'] = df_data['stoppointid'].astype('int')
	df_data['plannedtime_arr'] = df_data['plannedtime_arr'].astype('int')
	df_data['plannedtime_dep'] = df_data['plannedtime_dep'].astype('int')
	df_data['actualtime_arr'] = df_data['actualtime_arr'].astype('int')
	df_data['actualtime_dep'] = df_data['actualtime_dep'].astype('int')
	df_data['vehicleid'] = df_data['vehicleid'].astype('int')

	# concat the dayofweek and the other columns
	df = pd.concat([df_day,df_data],axis=1)
	# save the new dataframe into csv file
	# df.to_csv(filename+'_cleaned.csv', index=False)
	return df 



# //================== Clean weather ====================//
def cleanWeather(filename):
	'''
		we got the data from open resource and clean the data.
	'''
	df_w =  pd.read_csv(filename,  keep_default_na=True, sep='\t', delimiter='\t', skipinitialspace=True)
	df_w = df_w[['date','rain','temp','vis']]
	df_w['day'] = pd.to_datetime(df_w['date']).dt.date
	df_w['hour'] = pd.to_datetime(df_w['date']).dt.hour
	df_w = df_w.drop('date',1)
	df_w['day'] = pd.to_datetime(df_w['day'])
	return df_w


# //================== split into routes ====================//
def splitIntoRoutes(df):
	'''
		First, we get the route list from the real-time bus routes resources,
		and then split the data into different routes and save to csv file.
	'''
	route_list = ['1', '4', '7', '9', '11', '13', '14', '15', '16', '17', '18', '25', '26', '27', '31',
                 '32', '33', '37', '38', '39', '40', '41', '42', '43', '44', '47', '49', '53', '59',
                 '61', '63', '65', '66', '67', '68', '69', '70', '75', '76', '79', '83', '84', '102',
                 '104', '111', '114', '116', '118', '120', '122', '123', '130', '140', '142', '145',
                 '150', '151', '161', '184', '185', '220', '236', '238', '239', '270', '747', '757',
                 '1C', '7A', '7B', '7D', '14C', '15A', '15B', '15D', '16C', '17A', '25A', '25B', '25D',
                 '25X', '27A', '27B', '27X', '29A', '31A', '31B', '31D', '32X', '33A', '33B', '33D',
                 '33X', '38A', '38B', '38D', '39A', '39X', '40B', '40D', '41A', '41B', '41C', '41X',
                 '42D', '44B', '45A', '46A', '46E', '51D', '51X', '54A', '56A', '65B', '66A', '66B',
                 '66X', '67X', '68A', '68X', '69X', '70D', '76A', '77A', '77X', '79A', '83A', '84A',
                '84X']
    for route in route_list:
    	df_route = df.loc[df['routeid'] == route]
    	name='route'+route+'.csv'
    	df_route.to_csv(name, index=False, mode='a', header=None)
    # print(name+' is finished!')
    return df_route



# //================== main function ====================//
def run():
	#  connect to database
	conn = mysql.connector.connect(user='root', password='Team14', database='dublinbus')
	cursor = conn.cursor()
	#  get columns from trips table
	query1= ("select day_of_service, tripid, lineid,direction from trips2016;")
	query2= ("select day_of_service, tripid, lineid,direction from trips2017;")
	cursor.execute(query1)
	columns1=cursor.column_names
	result1=cursor.fetchall()
	cursor.execute(query2)
	columns2=cursor.column_names
	result2=cursor.fetchall()
	conn.commit()
	cursor.close()
	conn.close()

	# call cleanTrips function to clean the data of trips
	df_2016 = cleanTrips(result1)
	df_2017 = cleanTrips(result2)
	df_trips = pd.concat([df_2017,df_2017])

	# call cleanWeather function to clean weather data
	df_w = 	cleanWeather('weather.csv')

	# call cleanLeavetime function to clean the data of leavetimes
	tablelist = ['aa','ab','ac','ad','ae','af','ag','ah','ai','aj','ak','al']
	year = ['2016','2017']
	for y in year:
		for i in tablelist:
			filename = '/data_resource/leavetime'+y+'_'+i
			df_cleaned = cleanLeavetimes(filename)

			# Merge trips and leavetimes 
			df = pd.merge(df_cleaned, df_trips, left_on=['dayofservice','tripid'], right_on=['dayofservice','tripid'])
			df.to_csv('output_'+y+'_'+i+'.csv',mode='a',header=False) # mode='a' means append to "filename"

			# split data into different routes
			splitIntoRoutes(df)


run()











