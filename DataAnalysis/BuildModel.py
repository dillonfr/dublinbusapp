# Import pandas, numpy and sklearn
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.externals import joblib
from pandas.core.frame import DataFrame




# //========================================================//
def time(x):
    '''get the time  '''
    m, s = divmod(x, 60)
    h, m = divmod(m, 60)
    return ("%02d:%02d:%02d" % (h, m, s))

def peaktime(x):
    '''generate 'peak' column as a descriptive feature,
        if the departure time is between 7am ~ 10am or 16pm ~ 20pm, it will be marked as peak(1),
        otherwise, it will be marked as not in peak(0)
     '''
    if x>'07:00:00'and x<'10:00:00':
        return 1
    elif x>'16:00:00' and x<'20:00:00':
        return 1
    else:
        return 0

def isRain(x):
    '''if the rainfall capacity is more than 0, it will be marked as rain(1)
        or it will be marked as not rain(0)
    '''
    if x>0:
        return 1
    else:
        return 0

# //================== split into routes ====================//
def prepareRoutes(df):
    '''
        generate columns like nextprogrnumber, nextstop_id, stopsnumber,hour and peak
        and journeytime (as the target feature), 
        then prepare the data, replace the dayofweek with number 
    '''

    # generate columns like nextprogrnumber, nextstop_id, stopsnumber,
    # and journeytime (as the target feature)
    df = df.sort_values(['dayofservice','tripid'], ascending=True)
    df['dayofservice'] = pd.to_datetime(df['dayofservice'])
    df['tripid'] = df['tripid'].astype('category')
    df_1 = df[['dayofservice','tripid','progrnumber','stoppointid','actualtime_arr','routeid','direction']]
    df_sorted = df_1.groupby(["dayofservice","tripid"]).apply(lambda x: x.sort_values(["progrnumber"], ascending = True)).reset_index(drop=True)
    df_sorted['nextprogrnumber']=df_sorted.groupby(["dayofservice","tripid"])["progrnumber"].shift(-1)
    df_sorted['nextstop_arr']=df_sorted.groupby(["dayofservice","tripid"])['actualtime_arr'].shift(-1)
    df_sorted['nextstop_id']=df_sorted.groupby(["dayofservice","tripid"])['stoppointid'].shift(-1)
    df_sorted['stopsnumber'] = df_sorted['nextprogrnumber'] - df_sorted['progrnumber']
    df_sorted['journeytime_arr'] = df_sorted['nextstop_arr'] - df_sorted['actualtime_arr']

    # check the null values and drop these rows
    df_sorted.isnull().sum()
    df_sorted = df_sorted.dropna(axis=0)
    
    # merge the origin df with the generated columns
    df_end = pd.merge(df, df_sorted,how='outer',left_on=['dayofservice','tripid','progrnumber','stoppointid','actualtime_arr','routeid','direction'], right_on=['dayofservice','tripid','progrnumber','stoppointid','actualtime_arr','routeid','direction'])
    
    # generate 'hour' column from the 'actualtime_dep_time' column
    df_end['actualtime_dep_time'] = df_end['actualtime_dep'].apply(lambda x: time(x))
    df_end['hour'] = pd.to_timedelta(df_end['actualtime_dep_time'])
    df_end['hour'] = pd.to_datetime(df_end['hour'])
    df_end['hour'] = df_end['hour'].dt.hour

    # generate 'peak' column from 'actualtime_dep_time' by call peaktime function
    df_end['peak'] = df_end['actualtime_dep_time'].apply(lambda x: peaktime(x))

    # transfer 'dayofweek' into number
    df_end = df_end.replace('Monday',1)
    df_end = df_end.replace('Tuesday',2)
    df_end = df_end.replace('Wednesday',3)
    df_end = df_end.replace('Thursday',4)
    df_end = df_end.replace('Friday',5)
    df_end = df_end.replace('Saturday',6)
    df_end = df_end.replace('Sunday',7)
    return df_end

# //================== add weather data ====================//
def addWeather(df):
    '''
        add weather information into different routes
    '''
     
    df_w = pd.read_csv('weather_end.csv',  keep_default_na=True, sep=',\s+', delimiter=',', skipinitialspace=True)
    df_w['day'] = pd.to_datetime(df_w['day'])
    
    # merge weather info with the dataframe 
    
    df_finished = pd.merge(df,df_w,how='left',left_on=['dayofservice','hour'],right_on=['day','hour'])
    # drop unnecessary columns
    df_finished = df_finished_end.drop('id',1)
    df_finished = df_finished.drop('actualtime_dep_time',1)
    df_finished = df_finished.drop('vehicleid',1)
    df_finished = df_finished.drop('plannedtime_dep',1)
    df_finished = df_finished.drop('plannedtime_arr',1)
    df_finished = df_finished.drop('nextprogrnumber',1)
    # 
    df_finished['rain'] = df_finished['rain'].apply(lambda x: isRain(x))
    return df_finished


# //================== build Linear Regressionmodel ====================//
def buildLinearRegressionModel(df):
    '''
        take 'dayofweek','peak','hour', 'stoppointid','nextstop_id','rain'] as the descriptive features
        to build linear regression model, chooce sklearn package to train the model and 
        use get_dummies function to transfer the category features

    '''
    df = df.loc[df['dayofservice'] > '2017-02-01']
    df = df.loc[df['stopsnumber'] == 1]
    df = df.loc[df['journeytime_arr'] > 5]
    # clean data
    df['dayofweek'] = df['dayofweek'].astype('category')
    df['stoppointid'] = df['stoppointid'].astype('category')
    df['routeid'] = df['routeid'].astype('category')
    df['direction'] = df['direction'].astype('category')
    df['nextstop_id'] = df['nextstop_id'].astype('int')
    df['nextstop_id'] = df['nextstop_id'].astype('category')
    df['nextstop_arr'] = df['nextstop_arr'].astype('int')
    df['journeytime_arr'] = df['journeytime_arr'].astype('int')
    df['peak'] = df['peak'].astype('category')
    df['hour'] = df['hour'].astype('category')
    df['rain'] = df['rain'].apply(lambda x: isRain(x))
    df['rain'] = df['rain'].astype('category')

    X_train = pd.DataFrame(df[['dayofweek','peak','hour', 'stoppointid','nextstop_id','rain']])
    y_train = df.journeytime_arr

    X_1 = pd.DataFrame(X_train[['dayofweek','peak','hour', 'stoppointid','nextstop_id','rain']])
    X_dummies = pd.get_dummies(X_1)
    
    # save dummies for historical data
    dummies = X_dummies.iloc[0:0]

    
    # save model for each route
    lr=LinearRegression(fit_intercept=True,normalize=True)
    lr.fit(X_dummies,y_train)


    return dummies,lr


# //================== build Linear Regressionmodel ====================//
def buildBackUpModel(df):
    '''
        build back-up models if cannot get the stopid, it can take stopnumbers as the feature 
        to predict the journey time
    '''

    df = df.loc[df['dayofservice'] > '2017-02-01']

    df = pd.DataFrame(df[['dayofweek','peak','hour', 'stopsnumber','rain','journeytime_arr']])
    df = df.loc[df['journeytime_arr'] > 5]

    # clean data
    df['dayofweek'] = df['dayofweek'].astype('category')
    df['journeytime_arr'] = df['journeytime_arr'].astype('int')
    df['peak'] = df['peak'].astype('category')
    df['hour'] = df['hour'].astype('category')
    df['stopsnumber'] = df['stopsnumber'].astype('int')
    df['rain'] = df['rain'].apply(lambda x: isRain(x))
    df['rain'] = df['rain'].astype('category')

    X_train = pd.DataFrame(df[['dayofweek','peak','hour','rain','stopsnumber']])
    y_train = df.journeytime_arr

    X_1 = pd.DataFrame(X_train[['dayofweek','peak','hour','rain']])
    X_dummies = pd.get_dummies(X_1)
    X_2 = pd.DataFrame(X_train[['stopsnumber']])
    X_end = pd.concat([X_dummies,X_2],axis=1)

    # save dummies for historical data
    dummies = X_end.iloc[0:0]

    # save model for each route
    lr=LinearRegression(fit_intercept=True,normalize=True)
    lr.fit(X_end,y_train)
    return dummies,lr




# //================== main function ====================//

def run():
	route_list = [	'4', '7', '9', '11', '13', '14', '15', '16', '17', '18', '25', '26', '27', '31',
                	'32', '33', '37', '38', '39', '40', '41', '42', '43', '44', '47', '49', '53', '59',
					'61', '63', '65', '66', '67', '68', '69', '70', '75', '76', '79', '83', '84', '102',
                	'104', '111', '114', '116', '118', '120', '122', '123', '130', '140', '142', '145',
                	'150', '151', '161', '184', '185', '220', '236', '238', '239', '270','747','757','1C',
             		'7A', '7B', '7D', '14C', '15A', '15B', '15D', '16C', '17A', '25A', '25B', '25D',
                	'25X', '27A', '27B', '27X', '29A', '31A', '31B', '31D', '32X', '33A', '33B', '33D',
                	'33X', '38A', '38B', '38D', '39A', '39X', '40B', '40D', '41A', '41B', '41C', '41X',
 					'42D', '44B', '45A', '46A', '46E', '51D', '51X', '54A', '56A', '65B', '66A', '66B'
					'66X', '67X', '68A', '68X', '69X', '70D', '76A', '77A', '77X', '79A', '83A', '84A',
					'84X' ]
    for i in route_list:
        name='route'+route+'.csv'
        df = pd.read_csv(name,  keep_default_na=True, sep=',\s+', delimiter=',', skipinitialspace=True)
        df_new = prepareRoutes(df)
        df_finished = addWeather(df_new)
        # save into csv file
        savename = "route_"+i+"_addweather.csv"
        df_finished.to_csv(savename, index=False)
        
        # get the dummies and model
        dummies,lr = buildLinearRegressionModel(df_finished)
        # save into pickle file
        dummiesname = 'route'+i+'_dummies.sav'
        with open(dummiesname,'wb') as f:
            joblib.dump(dummies, f, compress=4)

        lrfilename = 'route'+i+'_model.sav'
        with open(lrfilename,'wb') as f:
            joblib.dump(lr, f)

        # build back-up model
        basicdummies,basiclr = buildBackUpModel(df_finished)
        basicdummiesname = '/Users/yuyang/Documents/Dataclean/each_route_data/BasicDummies/basic_route'+i+'_dummies.sav'
        with open(basicdummiesname,'wb') as f:
            joblib.dump(basicdummies, f, compress=4)

        basiclr = '/Users/yuyang/Documents/Dataclean/each_route_data/BasicModel/basic_route'+i+'_model.sav'
        with open(basiclrfilename,'wb') as f:
            joblib.dump(basiclr, f)




run()








