# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 12:25:26 2026

@author: s.akter
"""
# write "%matplotlib qt" command in console panel to get interactive plot
# then run the command for plotting
import pandas as pd # library for data management
import numpy as np
import matplotlib
import matplotlib.pyplot as plt #Library for plotting
import matplotlib.cm
import matplotlib.dates as mdates
import time
from matplotlib import gridspec
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


#### Importing SARA K40 2024 data
# Importing SARA K-40 data for the Selhausen
K = pd.read_csv(r"D:\Data\Data_3rd_chapter\Input_data\Selhausen_2024\SARA_K40.csv", header = 0, parse_dates= [0], index_col=0)
K.columns = ['K', 'K status', 'K detailed status']
print(K['K status'].unique())
# counting nan values
K.isnull().sum()
K.loc[K['K status'] == 'UNCERTAIN', 'K'] = np.nan
K.drop(K.columns[[1,2]], axis=1, inplace=True)
print(K.head())
K.info()
print(K.index)
K.index = pd.to_datetime(K.index, utc= True, format= '%Y-%m-%dT%H:%M:%S.%f%z')
print(K.index)
K.describe()
K = K.sort_index()  # Dataframe is sorted in ascending order by date
K['K'] = np.where(K['K'] < 4, np.nan, K['K'])
K_hourly = K.resample('h').mean()

## Function for averaging
def mean_when_11non_nan(x):
    non_nulls = x.notnull()
    if non_nulls.sum() > 10: # calculate mean when at least 11 hrs data are available
        return x[non_nulls].mean()
    return np.nan
K_daily = K.resample('D').apply(mean_when_11non_nan)
K_daily = K_daily.rolling('3D', center=True, closed='both').mean()

# Merging K-40 data with an independent time index which has all timestamp from the start to end period 
# Creating a dataframe with customized date time index
time_index = pd.date_range(start ='2024/2/01 00:00:00', end ='2025/01/01 00:00:00', freq ='D')
print(time_index)
df = pd.DataFrame(time_index, columns =['date']) # Creating a dataframe, making the time index a column named as date
df['data'] = np.random.randint(0, 100, size =(len(time_index)))  # Creating a new column with random numbers 
df['datetime'] = pd.to_datetime(df['date'], utc=True, format= '%Y-%m-%dT%H:%M:%S.%f%z')
df = df.set_index('datetime')
df.drop(['date'], axis = 1, inplace = True)
# Merging K40 data with the customized datetime index data to avoid error during interpolation
K = pd.merge(df, K_daily, how = 'left', left_index = True, right_index = True )
K.drop(['data'], axis = 1, inplace = True)
 

## Importing SM data
SM = pd.read_csv(r"D:\Data\Data_3rd_chapter\Outputs\selhausen_ref_SM_with_add_SoilNet_data.csv", header = 0, parse_dates= [0], index_col=0)
#SM_hourly = SM.resample('h').mean()
SM_daily = SM.resample('D').apply(mean_when_11non_nan)
## Merging with the MIS data
K_SM = pd.merge(K, SM_daily, how = 'left', left_index = True, right_index = True )

## Calculating depth weighted SM
K_SM['SM_0to7.5cm'] = (K_SM['SM_2cm']*3.5 + K_SM['SM_5cm']*4)/7.5          #for 0-7.5 cm depth
K_SM['SM_0to15cm'] = (K_SM['SM_2cm']*3.5 + K_SM['SM_5cm']*4 + K_SM['SM_10cm']*7.5)/15      #for 0-15 cm depth
#K_SM = K_SM.dropna(how='any')
print(K_SM[['K', 'SM_av_dw']].corr(method='pearson'))

## Importing biomass data
B = pd.read_excel(r"D:\Data\Data_3rd_chapter\Input_data\Selhausen_2024\Biomass_data_cleaned.xlsx", header = 0, parse_dates= [0], index_col=0)
print(B.index)
B.index = pd.to_datetime(B.index, utc= True, format= '%Y-%m-%dT%H:%M:%S.%f%z')
### Joining data
Data = pd.merge(K_SM, B, how = 'left', left_index = True, right_index = True )
## Interpolating 
# Define the growing period
season_start = '2024-05-01'
season_end   = '2024-09-15'
## Create a mask for the growing season
season_mask = Data.index.to_series().between(season_start, season_end)
# Columns to interpolate
biomass_cols = ['FB_AG (mm)', 'FB_BG (mm)', 'BWC_AG (mm)', 'BWC_BG (mm)']   # Above-ground and Below-ground biomass

## Interpolation: Values are interpolated only between measured biomass points. Outside the season remains NaN
Data.loc[season_mask, biomass_cols] = (
    Data.loc[season_mask, biomass_cols]
        .interpolate(method='time')
)

# save the file
Data.to_csv("D:\Data\Data_3rd_chapter\Outputs\K_ref_SM_Biomass.csv", header=True, index = True)























