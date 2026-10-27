# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 15:21:28 2026

@author: s.akter
"""

# write "%matplotlib qt" command in console panal to get interactive plot
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


# Importing processed MIRA EGR data
MIS = pd.read_csv(r"D:\Data\Data_3rd_chapter\Outputs\MIS_EGR_processed.csv", header = 0, parse_dates= [0], index_col=0)
print(MIS.index)
# Drop unnecessary columns
#MIS = MIS.drop(MIS.columns[0:6], axis=1)

## Function for averaging
def mean_when_11non_nan(x):
    non_nulls = x.notnull()
    if non_nulls.sum() > 10: # calculate mean when at least 9 hrs data are available
        return x[non_nulls].mean()
    return np.nan
MIS_daily = MIS.resample('D').apply(mean_when_11non_nan)
MIS_daily = MIS_daily.rolling('3D', center=True, closed='both').mean()

# Merging MIS data with an independent time index which has all timestamp from the start to end period 
# Creating a dataframe with customized date time index
time_index = pd.date_range(start ='2024/02/01 00:00:00', end ='2024/12/31 00:00:00', freq ='D')
print(time_index)
df = pd.DataFrame(time_index, columns =['date']) # Creating a dataframe, making the time index a column named as date
df['data'] = np.random.randint(0, 100, size =(len(time_index)))  # Creating a new column with random numbers 
df['datetime'] = pd.to_datetime(df['date'], utc=True, format= '%Y-%m-%dT%H:%M:%S.%f%z')
df = df.set_index('datetime')
df.drop(['date'], axis = 1, inplace = True)
#df = df.drop(df.index[0:139], axis=0) # Removing the unnecessary rows
# Merging SM_cb with the customized datetime index data to avoid error during interpolation
MIS = pd.merge(df, MIS_daily, how = 'left', left_index = True, right_index = True )
MIS.drop(['data'], axis = 1, inplace = True)


## Importing SM data
SM = pd.read_csv(r"D:\Data\Data_3rd_chapter\Outputs\selhausen_ref_SM_with_add_SoilNet_data.csv", header = 0, parse_dates= [0], index_col=0)
#SM_hourly = SM.resample('h').mean()
SM_daily = SM.resample('D').apply(mean_when_11non_nan)
## Merging with the MIS data
MIS_SM = pd.merge(MIS, SM_daily, how = 'left', left_index = True, right_index = True )
MIS_SM_weekly = MIS_SM.resample('W').mean()
MIS_SM = MIS_SM['2024/02/02 00:00:00':'2024/12/30 00:00:00']
print(MIS_SM[['Corrected EGR for short-term SCR variability', 'SM_av_dw']].corr(method='pearson'))


## Importing biomass data
B = pd.read_excel(r"D:\Data\Data_3rd_chapter\Input_data\Selhausen_2024\Biomass_data_cleaned.xlsx", header = 0, parse_dates= [0], index_col=0)
print(B.index)
B.index = pd.to_datetime(B.index, utc= True, format= '%Y-%m-%dT%H:%M:%S.%f%z')
### Joining data
Data = pd.merge(MIS_SM, B, how = 'left', left_index = True, right_index = True )
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
Data.to_csv("D:\Data\Data_3rd_chapter\Outputs\MIRA_EGR_ref_SM_Biomass.csv", header=True, index = True)







