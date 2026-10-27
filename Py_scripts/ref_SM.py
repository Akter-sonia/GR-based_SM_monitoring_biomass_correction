# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 11:27:07 2026

@author: s.akter
"""

import pandas as pd # library for data management
import numpy as np
import matplotlib
import matplotlib.pyplot as plt #Library for plotting
import matplotlib.cm
import matplotlib.dates as mdates
from matplotlib import gridspec
#from datetime import date, datetime, time, timedelta
#import pytz 
#from pytz import timezone
# Handle date time conversions between pandas and matplotlib
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import glob
import scipy.signal as ss



### Importing raw reference soil moisture data and making them clean for the analysis

# For location 01 
# Define folder directory to look for all the files
files = glob.glob(r"D:\Data\Data_3rd_chapter\Input_data\Selhausen_2024\selhausen_soil_moisture_ICOS\DE-RuS_BM*_L01_F01.csv") # Making a list of files
# make a list of all files
list_ = []
# Looping through each files
for i in files:
   df = pd.read_csv(i, header = None)  
   list_.append(df)  ## Appending all files as an element of the list
## stack each file on top of the other and make one single dataframe   
stack = pd.concat(list_, axis = 0)
## Set first row as column header
stack.columns = stack.iloc[0]   # copied the first row and set as column header
stack = stack[1:]   # delete the first row
# Keeping only necessary columns
stack = stack[["TIMESTAMP", "soilwatercontent_1_1_1", "SWC_1_2_1", "SWC_1_3_1", "SWC_1_4_1", "SWC_1_5_1"]]
# SWC at 0, 5, 10, 20 and 50 cm depth for location 1
# Save the output
stack.to_csv("D:\Data\Data_3rd_chapter\Outputs\selhausen_ref_SM_L1.csv", index = False)

## For L2
files = glob.glob(r"D:\Data\Data_3rd_chapter\Input_data\Selhausen_2024\selhausen_soil_moisture_ICOS\DE-RuS_BM*_L02_F01.csv")
# make a list of all files
list_ = []
# Looping through each files
for i in files:
   df = pd.read_csv(i, header = None)  
   list_.append(df)  ## Appending all files as an element of the list
## stack each file on top of the other and make one single dataframe   
stack = pd.concat(list_, axis = 0)
## Set first row as column header
stack.columns = stack.iloc[0]   # copied the first row and set as column header
stack = stack[1:]   # delete the first row
# Keeping only necessary columns
stack = stack[["TIMESTAMP", "soilwatercontent_2_1_1", "SWC_2_2_1", "SWC_2_3_1", "SWC_2_4_1", "SWC_2_5_1"]]
# Save the output
stack.to_csv("D:\Data\Data_3rd_chapter\Outputs\selhausen_ref_SM_L2.csv", index = False)

## For L3
files = glob.glob(r"D:\Data\Data_3rd_chapter\Input_data\Selhausen_2024\selhausen_soil_moisture_ICOS\DE-RuS_BM*_L03_F01.csv")
# make a list of all files
list_ = []
# Looping through each files
for i in files:
   df = pd.read_csv(i, header = None)  
   list_.append(df)  ## Appending all files as an element of the list
## stack each file on top of the other and make one single dataframe   
stack = pd.concat(list_, axis = 0) 
## Set first row as column header
stack.columns = stack.iloc[0]   # copied the first row and set as column header
stack = stack[1:]   # delete the first row
# Keeping only necessary columns
stack = stack[["TIMESTAMP", "soilwatercontent_3_1_1", "SWC_3_2_1", "SWC_3_3_1", "SWC_3_4_1", "SWC_3_5_1"]]
# Save the output
stack.to_csv("D:\Data\Data_3rd_chapter\Outputs\selhausen_ref_SM_L3.csv", index = False)

# For L4 
# Define folder directory to look for all the files
files = glob.glob(r"D:\Data\Data_3rd_chapter\Input_data\Selhausen_2024\selhausen_soil_moisture_ICOS\DE-RuS_BM*_L04_F01.csv") # Making a list of files
# make a list of all files
list_ = []
# Looping through each files
for i in files:
   df = pd.read_csv(i, header = None)  
   list_.append(df)  ## Appending all files as an element of the list
## stack each file on top of the other and make one single dataframe   
stack = pd.concat(list_, axis = 0)
## Set first row as column header
stack.columns = stack.iloc[0]   # copied the first row and set as column header
stack = stack[1:]   # delete the first row
# Keeping only necessary columns
stack = stack[["TIMESTAMP", "soilwatercontent_4_1_1", "SWC_4_2_1", "SWC_4_3_1", "SWC_4_4_1", "SWC_4_5_1"]]
# Save the output
stack.to_csv("D:\Data\Data_3rd_chapter\Outputs\selhausen_ref_SM_L4.csv", index = False)

# For L5 
# Define folder directory to look for all the files
files = glob.glob(r"D:\Data\Data_3rd_chapter\Input_data\Selhausen_2024\selhausen_soil_moisture_ICOS\DE-RuS_BM*_L05_F01.csv") # Making a list of files
# make a list of all files
list_ = []
# Looping through each files
for i in files:
   df = pd.read_csv(i, header = None)  
   list_.append(df)  ## Appending all files as an element of the list
## stack each file on top of the other and make one single dataframe   
stack = pd.concat(list_, axis = 0)
## Set first row as column header
stack.columns = stack.iloc[0]   # copied the first row and set as column header
stack = stack[1:]   # delete the first row
# Keeping only necessary columns
stack = stack[["TIMESTAMP", "soilwatercontent_5_1_1", "SWC_5_2_1", "SWC_5_3_1", "SWC_5_4_1", "SWC_5_5_1"]]
# Save the output
stack.to_csv("D:\Data\Data_3rd_chapter\Outputs\selhausen_ref_SM_L5.csv", index = False)



### Importing the clean reference soil moisture data and visualize
#L1
ref_SM_L1 = pd.read_csv(r"D:\Data\Data_3rd_chapter\Outputs\selhausen_ref_SM_L1.csv", index_col=0, parse_dates = True, header = 0)
print(ref_SM_L1.index)
# Making pandas datetime to be UTC aware
ref_SM_L1.index = pd.to_datetime(ref_SM_L1.index, utc=True, format= '%Y-%m-%dT%H:%M:%S.%f%z')  
print(ref_SM_L1.index)
# check for duplicated indexes 
duplicated_indexes = ref_SM_L1.index.duplicated(keep=False) ## True when duplicate timestamp is found
duplicated_rows = ref_SM_L1[duplicated_indexes]             #showing the rows for duplicate timestamp
## Duplicate timestamps are present
ref_SM_L1 = ref_SM_L1.groupby(ref_SM_L1.index).first()  # filtering duplicate timestamp
#ref_SM_L1 = ref_SM_L1.groupby(ref_SM_L1.index).mean()  ## or marging duplicate timestamp by taking mean values
# Renaming the columns
ref_SM_L1.rename(columns = {'soilwatercontent_1_1_1':'SM_0cm', 'SWC_1_2_1':'SM_5cm', 'SWC_1_3_1':'SM_10cm',
                              'SWC_1_4_1':'SM_20cm','SWC_1_5_1':'SM_50cm'}, inplace = True)
print(ref_SM_L1.columns)
## disregarding all the erronious zero values if any
ref_SM_L1.isnull().sum()                         # counting nan values
ref_SM_L1.replace(0, np.nan, inplace=True)       # replacing zero with nan
# changing entire row with nan values if a single column has nan
#ref_SM_L1.loc[ref_SM_L1.isna().any(1)] = np.nan  # finding if a row has nan, masking for that row and making all cells of that row nan
## or interpolate the missing values, need to have all timestamps for better interpolation
# Merging L1 data with an independent time index which has all timestamp from the start to end period 
ref_SM_L1.tail(10)
# Creating a dataframe with customized date time index
time_index = pd.date_range(start ='2024/02/01 00:01:00', end ='2025/01/01 00:00:00', freq =' 1 Min')
print(time_index)
df = pd.DataFrame(time_index, columns =['date']) # Creating a dataframe, making the time index a column named as date
df['data'] = np.random.randint(0, 100, size =(len(time_index)))  # Creating a new column with random numbers 
df['datetime'] = pd.to_datetime(df['date'], utc=True, format= '%Y-%m-%dT%H:%M:%S.%f%z')
df = df.set_index('datetime')
df.drop(['date'], axis = 1, inplace = True)
#df = df.drop(df.index[0:139], axis=0) # Removing the unnecessary rows
# Merging L1 with the customized datetime index data
ref_SM_L1 = pd.merge(df, ref_SM_L1, how = 'left', left_index = True, right_index = True )
ref_SM_L1.drop(['data'], axis = 1, inplace = True)
## interpolating the missing values
#ref_SM_L1 = ref_SM_L1['2023-02-01 00:01:00':'2023-11-20 00:00:00']
ref_SM_L1.interpolate(method = 'time', limit= 2000, limit_direction='both', inplace = True)
ref_SM_L1['SM_0cm'] = ss.medfilt(ref_SM_L1['SM_0cm'], kernel_size=551)  ## removing the spikes using median filter
#ref_SM_L1 = ref_SM_L1['2023-02-01 00:01:00':'2023-11-20 00:00:00']
ref_SM_L1 = ref_SM_L1.resample('10min').mean()
ref_SM_L1[ref_SM_L1.isnull().any(axis=1)]  ## finding the rows with nan
# Average soil moisture through the entire depth (0-50 cm)
#ref_SM_L1['SM_1'] = ref_SM_L1[['SM_0cm', 'SM_5cm', 'SM_10cm','SM_20cm', 'SM_50cm']].mean(axis=1)
# alternative ref_SM_L1['SM_1'] = ref_SM_L1.iloc[:, 0:5].mean(axis=1) ## 0:5 means start from column 0 and end before 5 (not including 5)
#as datetime is set as index, first column (SM_0cm) is counted as 0.
# Save the output
ref_SM_L1.to_csv("D:\Data\Data_3rd_chapter\Outputs\selhausen_ref_SM_L1_processed.csv")


#L2
ref_SM_L2 = pd.read_csv(r"D:\Data\Data_3rd_chapter\Outputs\selhausen_ref_SM_L2.csv", index_col=0, parse_dates = True, header = 0)
print(ref_SM_L2.index)
# Making pandas datetime to be UTC aware
ref_SM_L2.index = pd.to_datetime(ref_SM_L2.index, utc=True, format= '%Y-%m-%dT%H:%M:%S.%f%z')  
print(ref_SM_L2.index)
# check for duplicated indexes 
duplicated_indexes = ref_SM_L2.index.duplicated(keep=False) ## True when duplicate timestamp is found
duplicated_rows = ref_SM_L2[duplicated_indexes]             #showing the rows for duplicate timestamp
## Duplicate timestamps are present
ref_SM_L2 = ref_SM_L2.groupby(ref_SM_L2.index).first()  # filtering duplicate timestamp
# Renaming the columns
ref_SM_L2.rename(columns = {'soilwatercontent_2_1_1':'SM_0cm', 'SWC_2_2_1':'SM_5cm', 'SWC_2_3_1':'SM_10cm',
                              'SWC_2_4_1':'SM_20cm','SWC_2_5_1':'SM_50cm'}, inplace = True)
## disregarding all the erronious zero values
ref_SM_L2.isnull().sum()                         # counting nan values
ref_SM_L2.replace(0, np.nan, inplace=True)       # replacing zero with nan
# changing entire row with nan values if a single column has nan
#ref_SM_L2.loc[ref_SM_L2.isna().any(1)] = np.nan  # finding if a row has nan, masking for that row and making all cells of that row nan
## or interpolate the missing values
# Merging L2 with the customized datetime index data to avoid error during interpolation
ref_SM_L2 = pd.merge(df, ref_SM_L2, how = 'left', left_index = True, right_index = True )
ref_SM_L2.drop(['data'], axis = 1, inplace = True)
ref_SM_L2.interpolate(method = 'time', limit = 2000, limit_direction='both', inplace = True) ## limiting the no of nan values to be filled, to avoid large data gap
ref_SM_L2['SM_0cm'] = ss.medfilt(ref_SM_L2['SM_0cm'], kernel_size=551)  ## removing the spikes using median filter
ref_SM_L2['SM_5cm'] = ss.medfilt(ref_SM_L2['SM_5cm'], kernel_size=551)
#ref_SM_L2 = ref_SM_L2['2023-02-01 00:01:00':'2023-07-20 00:00:00']
ref_SM_L2 = ref_SM_L2.resample('10min').mean()
# Average soil moisture through the entire depth (0-50 cm)
#ref_SM_L2['SM_2'] = ref_SM_L2[['SM_0cm', 'SM_5cm', 'SM_10cm','SM_20cm', 'SM_50cm']].mean(axis=1)


#L3
ref_SM_L3 = pd.read_csv(r"D:\Data\Data_3rd_chapter\Outputs\selhausen_ref_SM_L3.csv", index_col=0, parse_dates = True, header = 0)
print(ref_SM_L3.index)
# Making pandas datetime to be UTC aware
ref_SM_L3.index = pd.to_datetime(ref_SM_L3.index, utc=True, format= '%Y-%m-%dT%H:%M:%S.%f%z')  
print(ref_SM_L3.index)
# check for duplicated indexes 
duplicated_indexes = ref_SM_L3.index.duplicated(keep=False) ## True when duplicate timestamp is found
duplicated_rows = ref_SM_L3[duplicated_indexes]             #showing the rows for duplicate timestamp
## Duplicate timestamps are present
ref_SM_L3 = ref_SM_L3.groupby(ref_SM_L3.index).first()  # filtering duplicate timestamp
# Renaming the columns
ref_SM_L3.rename(columns = {'soilwatercontent_3_1_1':'SM_0cm', 'SWC_3_2_1':'SM_5cm', 'SWC_3_3_1':'SM_10cm',
                              'SWC_3_4_1':'SM_20cm','SWC_3_5_1':'SM_50cm'}, inplace = True)
## disregarding all the erronious zero values
ref_SM_L3.isnull().sum()                         # counting nan values
#ref_SM_L3.replace(0, np.nan, inplace=True)      # unvalid code because soil surface has valid 0 SM for that location 
cols = ['SM_5cm', 'SM_10cm', 'SM_20cm', 'SM_50cm']
ref_SM_L3[cols] = ref_SM_L3[cols].replace(0, np.nan)
# changing entire row with nan values if a single column has nan
#ref_SM_L3.loc[ref_SM_L3.isna().any(1)] = np.nan  # finding if a row has nan, masking for that row and making all cells of that row nan
## or interpolate the missing values
# Merging L3 with the customized datetime index data to avoid error during interpolation
ref_SM_L3 = pd.merge(df, ref_SM_L3, how = 'left', left_index = True, right_index = True )
ref_SM_L3.drop(['data'], axis = 1, inplace = True)
ref_SM_L3.interpolate(method = 'time', limit= 2000, limit_direction='both', inplace = True)
ref_SM_L3['SM_0cm'] = ss.medfilt(ref_SM_L3['SM_0cm'], kernel_size=551)  ## removing the spikes using median filter
#ref_SM_L3 = ref_SM_L3['2023-02-01 00:01:00':'2023-07-20 00:00:00']
ref_SM_L3 = ref_SM_L3.resample('10min').mean() 
# Average soil moisture through the entire depth (0-50 cm)
#ref_SM_L3['SM_3'] = ref_SM_L3[['SM_0cm', 'SM_5cm', 'SM_10cm','SM_20cm', 'SM_50cm']].mean(axis=1)

#L4
ref_SM_L4 = pd.read_csv(r"D:\Data\Data_3rd_chapter\Outputs\selhausen_ref_SM_L4.csv", index_col=0, parse_dates = True, header = 0)
print(ref_SM_L4.index)
# Making pandas datetime to be UTC aware
ref_SM_L4.index = pd.to_datetime(ref_SM_L4.index, utc=True, format= '%Y-%m-%dT%H:%M:%S.%f%z')  
print(ref_SM_L4.index)
# check for duplicated indexes 
duplicated_indexes = ref_SM_L4.index.duplicated(keep=False) ## True when duplicate timestamp is found
duplicated_rows = ref_SM_L4[duplicated_indexes]             #showing the rows for duplicate timestamp
## Duplicate timestamps are present
ref_SM_L4 = ref_SM_L4.groupby(ref_SM_L4.index).first()  # filtering duplicate timestamp
# Renaming the columns
ref_SM_L4.rename(columns = {'soilwatercontent_4_1_1':'SM_0cm', 'SWC_4_2_1':'SM_5cm', 'SWC_4_3_1':'SM_10cm',
                              'SWC_4_4_1':'SM_20cm','SWC_4_5_1':'SM_50cm'}, inplace = True)
## disregarding all the erronious zero values
ref_SM_L4.isnull().sum()                         # counting nan values
ref_SM_L4.replace(0, np.nan, inplace=True)       # replacing zero with nan
# changing entire row with nan values if a single column has nan
#ref_SM_L4.loc[ref_SM_L4.isna().any(1)] = np.nan  # finding if a row has nan, masking for that row and making all cells of that row nan
## or interpolate the missing values
# Merging L4 with the customized datetime index data to avoid error during interpolation
ref_SM_L4 = pd.merge(df, ref_SM_L4, how = 'left', left_index = True, right_index = True )
ref_SM_L4.drop(['data'], axis = 1, inplace = True)
ref_SM_L4.interpolate(method = 'time', limit = 2000, limit_direction='both', inplace = True) 
#ref_SM_L4['SM_10cm'].interpolate(method = 'time', limit = 5000, limit_direction='forward',  inplace = True)
#ref_SM_L4['SM_20cm'].interpolate(method = 'time', limit = 5000, limit_direction='forward', inplace = True)
ref_SM_L4['SM_0cm'] = ss.medfilt(ref_SM_L4['SM_0cm'], kernel_size=551)  ## removing the spikes using median filter
ref_SM_L4['SM_5cm'] = ss.medfilt(ref_SM_L4['SM_5cm'], kernel_size=551)
#ref_SM_L4 = ref_SM_L4['2023-02-01 00:01:00':'2023-07-20 00:00:00']
ref_SM_L4 = ref_SM_L4.resample('10min').mean()
# Average soil moisture through the entire depth (0-50 cm)
#ref_SM_L4['SM_4'] = ref_SM_L4[['SM_0cm', 'SM_5cm', 'SM_10cm','SM_20cm', 'SM_50cm']].mean(axis=1)

#L5
ref_SM_L5 = pd.read_csv(r"D:\Data\Data_3rd_chapter\Outputs\selhausen_ref_SM_L5.csv", header = 0)
print(ref_SM_L5['TIMESTAMP'].dtype)
ref_SM_L5['TIMESTAMP'] = pd.to_datetime(ref_SM_L5['TIMESTAMP'], utc=True, format= '%Y%m%d%H%M')
ref_SM_L5 = ref_SM_L5.set_index('TIMESTAMP')  
print(ref_SM_L5.index)
# check for duplicated indexes 
duplicated_indexes = ref_SM_L5.index.duplicated(keep=False) ## True when duplicate timestamp is found
duplicated_rows = ref_SM_L5[duplicated_indexes]             #showing the rows for duplicate timestamp
## Duplicate timestamps are present
ref_SM_L5 = ref_SM_L5.groupby(ref_SM_L5.index).first()  # filtering duplicate timestamp

# Renaming the columns
ref_SM_L5.rename(columns = {'soilwatercontent_5_1_1':'SM_0cm', 'SWC_5_2_1':'SM_5cm', 'SWC_5_3_1':'SM_10cm',
                              'SWC_5_4_1':'SM_20cm','SWC_5_5_1':'SM_50cm'}, inplace = True)
## disregarding all the erronious zero values
ref_SM_L5.isnull().sum()                         # counting nan values
#ref_SM_L5.replace(0, np.nan, inplace=True)      # unvalid code because soil surface has valid 0 SM for that location 
cols = ['SM_0cm', 'SM_5cm', 'SM_10cm', 'SM_20cm']
ref_SM_L5[cols] = ref_SM_L5[cols].replace(0, np.nan)
# changing entire row with nan values if a single column has nan
#ref_SM_L5.loc[ref_SM_L5.isna().any(1)] = np.nan  # finding if a row has nan, masking for that row and making all cells of that row nan
## or interpolate the missing values
# Merging L5 with the customized datetime index data to avoid error during interpolation
ref_SM_L5 = pd.merge(df, ref_SM_L5, how = 'left', left_index = True, right_index = True )
ref_SM_L5.drop(['data'], axis = 1, inplace = True)
## Still some peaks left
ref_SM_L5.loc['2024-09-13 09:20:00+00:00':'2024-09-17 00:00:00+00:00'] = np.nan
#ref_SM_L5.loc['2023-09-10 08:00:00+00:00':'2023-10-10 08:20:00+00:00','SM_5cm'] = np.nan
#ref_SM_L5.loc['2023-10-05 08:20:00+00:00':'2023-10-05 08:25:00+00:00','SM_0cm'] = np.nan
ref_SM_L5.interpolate(method = 'time', limit = 3000, limit_direction='forward', inplace = True) 
ref_SM_L5['SM_0cm'] = ss.medfilt(ref_SM_L5['SM_0cm'], kernel_size=551)  ## removing the spikes using median filter
ref_SM_L5['SM_5cm'] = ss.medfilt(ref_SM_L5['SM_5cm'], kernel_size=551)
#ref_SM_L5 = ref_SM_L5['2023-02-01 00:01:00':'2023-07-20 00:00:00']
#ref_SM_L5.loc['2023-07-24 09:30:00+00:00':'2023-08-24 09:50:00+00:00'] = np.nan
ref_SM_L5 = ref_SM_L5.resample('10min').mean()
# Average soil moisture through the entire depth (0-50 cm)
#ref_SM_L5['SM_5'] = ref_SM_L5[['SM_0cm', 'SM_5cm', 'SM_10cm','SM_20cm', 'SM_50cm']].mean(axis=1)


# Importing precipitation data
prc = pd.read_excel(r"D:\Data\Data_3rd_chapter\Input_data\Selhausen_2024\SE_EC_precipitation.xlsx", header = 0, parse_dates= [0], index_col=0, na_values=['noData', '99999', '-9999'])
prc.columns = ['Feature', 'Precipitation','Data quality']
print(prc.head())
prc.info()
prc.isnull().sum()  # counting nan values
print(prc.index)
prc.index = pd.to_datetime(prc.index, utc= True, format= '%Y-%m-%dT%H:%M:%S.%f%z')
print(prc['Data quality'].unique())
prc.drop(['Feature', 'Data quality'], axis=1, inplace=True)
prc["Precipitation"] = prc["Precipitation"].round(decimals=5)
print(prc.index)
prc.describe()
prc['Precipitation'].sum(axis = 0, skipna = True)
##plotting
fig, ax = plt.subplots(figsize=(10, 7))
# Add x-axis and y-axis, to plot scatter plot use ax.scatter() command 
ax.plot (prc.index, prc['Precipitation'])
# Set title and labels for axes
ax.set_xlabel("Date", fontsize = 30)
ax.set_ylabel("Precipitation (mm)", fontsize = 30)
#ax.set_title("GR1", fontsize = 35)
plt.xticks(fontsize = 22)
plt.yticks(fontsize = 22)
plt.tight_layout()
plt.savefig("D:\Data\Data_3rd_chapter\Figures\prcipitation_selhausen2024.png")
plt.show()


## Ploting precipitation with soil moisture data for each location
fig, ax = plt.subplots(figsize=(25.5, 19.7), sharex=False, sharey=False, constrained_layout = True, dpi = 50) # No axis sharing
plt.axis('off')   # Turning the general axis off in order to create individual axis for each subplot
gs = gridspec.GridSpec(2, 1, height_ratios=[0.5, 1.2], wspace=0, hspace=0) # no of row 2, column 1 and no space bet. subplots
rain = plt.subplot(gs[0])
SM = plt.subplot(gs[1]) # add_subplot command adds each plot in fig 
# add_subplot(total no of row, total no of column, position of this subplot)
#plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)
matplotlib.rc('xtick', labelsize=24) # defining the xtick fontsize for all subplots
matplotlib.rc('ytick', labelsize=24)
#plt.tick_params(axis='both', which='major', labelsize=14) for one specific subplot
matplotlib.rcParams['xtick.major.pad']='13'
matplotlib.rcParams['ytick.major.pad']='13'

rain.bar (prc.index, prc['Precipitation'])
#rain.set_xlabel("Date", fontsize = 30)
rain.set_ylabel("Precipitation (mm)", fontsize = 46)
rain.set_ylim(0, 13)
rain.set_xlim([pd.to_datetime('2024-01-23 00:01', format = '%Y-%m-%d %H:%M'),
             pd.to_datetime('2025-01-01 00:01', format = '%Y-%m-%d %H:%M')])
rain.set_xticks([])
rain.invert_yaxis()
# fig.add_subplot(111) works for arranging subgraphs within this graph.
SM.plot(ref_SM_L5.index.values, ref_SM_L5['SM_0cm'], label = "2 cm", linewidth =2, color = 'C0')
SM.plot(ref_SM_L5.index.values, ref_SM_L5['SM_5cm'], label = "5 cm", linewidth =2, color = 'C1')
SM.plot(ref_SM_L5.index.values, ref_SM_L5['SM_10cm'], label = "10 cm", linewidth =2, color = 'C2')
SM.plot(ref_SM_L5.index.values, ref_SM_L5['SM_20cm'], label = "20 cm", linewidth =2, color = 'C3')
#SM.plot(ref_SM_L5.index.values, ref_SM_L5['SM_5'], label = "Mean", linewidth =4, color= 'black')
# Setting axes's limit
SM.set_xlim([pd.to_datetime('2024-01-23 00:01', format = '%Y-%m-%d %H:%M'),
             pd.to_datetime('2025-01-01 00:01', format = '%Y-%m-%d %H:%M')])
#SM.set_ylim(0, 42)
# Set title and labels for axes
SM.set_xlabel('Date', fontsize=46)
SM.set_ylabel('Reference SM (vol. %)', fontsize=46)
#plt.title('Gamma dose rate of GR1', fontsize=37)
SM.legend(ncol=1, loc='lower left', fontsize=40, frameon=False)
plt.tight_layout()
plt.savefig("D:\Data\Data_3rd_chapter\Figures\Sel_L5_preprocessed.png")
plt.show()


### Exploring SM data recorded by Campbellsci sensor at EC selhausen station
SM_cb = pd.read_excel(r"D:\Data\Data_3rd_chapter\Input_data\Selhausen_2024\Ref_SM_EC.xlsx", header = 0, parse_dates= [0], index_col=0, na_values=['noData', 'nan'])
SM_cb.columns = ['SM sensor1', 'sensor1 quality', 'SM sensor2', 'sensor2 quality']
print(SM_cb.head())
SM_cb.info()
## changing the sensor data type from object to float64
#SM_cb["SM sensor1"] = pd.to_numeric(SM_cb['SM sensor1'].str.replace('noData', ''))
#SM_cb["SM sensor2"] = pd.to_numeric(SM_cb["SM sensor2"])
print(SM_cb.index)
SM_cb.index = pd.to_datetime(SM_cb.index, utc= True, format= '%Y-%m-%dT%H:%M:%S.%f%z')
print(SM_cb['sensor2 quality'].unique())
SM_cb.loc[SM_cb['sensor1 quality'].isin(['4_4018','noData','4_4011']), 'SM sensor1'] = np.nan
#SM_cb['SM sensor1'] = np.where(SM_cb['sensor1 quality'] == '4_4018', np.nan, SM_cb['SM sensor1']) ## alternative, does not work when setting nan based on multiple sensor quality values
#SM_cb.loc[SM_cb['sensor1 quality'] == '4_4018', 'SM sensor1'] = np.nan  ## alternative, does not work when setting nan based on multiple sensor quality values
#SM_cb[SM_cb['sensor1 quality'] == 'noData'] = np.nan ## to make all cells in a row nan
SM_cb.loc[SM_cb['sensor2 quality'].isin(['4_4018','noData','4_4011']), 'SM sensor2'] = np.nan
# changing entire row with nan values if a single column has nan
#SM_cb.loc[SM_cb.isna().any(1)] = np.nan
## or interpolate the missing values
SM_cb.drop(['sensor1 quality', 'sensor2 quality'], axis=1, inplace=True)
#SM_cb.interpolate(method = 'time', limit_direction='forward', limit = 1000, inplace = True) 
# Merging L1 data with an independent time index which has all timestamp from the start to end period 
# Creating a dataframe with customized date time index
time_index = pd.date_range(start ='2024/2/01 00:10:00', end ='2025/01/01 00:00:00', freq =' 10 Min')
print(time_index)
df = pd.DataFrame(time_index, columns =['date']) # Creating a dataframe, making the time index a column named as date
df['data'] = np.random.randint(0, 100, size =(len(time_index)))  # Creating a new column with random numbers 
df['datetime'] = pd.to_datetime(df['date'], utc=True, format= '%Y-%m-%dT%H:%M:%S.%f%z')
df = df.set_index('datetime')
df.drop(['date'], axis = 1, inplace = True)
#df = df.drop(df.index[0:139], axis=0) # Removing the unnecessary rows
# Merging SM_cb with the customized datetime index data to avoid error during interpolation
SM_cb = pd.merge(df, SM_cb, how = 'left', left_index = True, right_index = True )
SM_cb.drop(['data'], axis = 1, inplace = True)
SM_cb.interpolate(method = 'time', limit_direction='forward', limit = 1000, inplace = True) 
# Average soil moisture for two sensors
SM_cb['SM_EC'] = SM_cb[['SM sensor1', 'SM sensor2']].mean(axis=1)
#SM_cb.loc['2023-07-24 09:30:00+00:00':'2023-08-24 09:50:00+00:00'] = np.nan
#SM_cb.loc['2023-11-02 01:00:00+00:00':'2023-11-14 09:50:00+00:00'] = np.nan
#SM_cb.loc['2024-01-08 09:30':'2024-01-22 09:50'] = np.nan  ## snow-fall event


## Ploting precipitation with EC soil moisture data
fig, ax = plt.subplots(figsize=(25.5, 19.7), sharex=False, sharey=False, constrained_layout = True, dpi = 50) # No axis sharing
plt.axis('off')   # Turning the general axis off in order to create individual axis for each subplot
gs = gridspec.GridSpec(2, 1, height_ratios=[0.5, 1.2], wspace=0, hspace=0) # no of row 2, column 1 and no space bet. subplots
rain = plt.subplot(gs[0])
SM = plt.subplot(gs[1]) # add_subplot command adds each plot in fig 
# add_subplot(total no of row, total no of column, position of this subplot)
#plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)
matplotlib.rc('xtick', labelsize=24) # defining the xtick fontsize for all subplots
matplotlib.rc('ytick', labelsize=24)
#plt.tick_params(axis='both', which='major', labelsize=14) for one specific subplot
matplotlib.rcParams['xtick.major.pad']='13'
matplotlib.rcParams['ytick.major.pad']='13'

rain.bar (prc.index, prc['Precipitation'])
#rain.set_xlabel("Date", fontsize = 30)
rain.set_ylabel("Precipitation (mm)", fontsize = 46)
rain.set_ylim(0, 13)
rain.set_xlim('2024-02-01 00:00', '2025-01-01 00:00')
rain.set_xticks([])
rain.invert_yaxis()
# fig.add_subplot(111) works for arranging subgraphs within this graph.
SM.plot(SM_cb.index.values, SM_cb['SM sensor1'], label = "sensor 1", linewidth =2, color = 'C0')
SM.plot(SM_cb.index.values, SM_cb['SM sensor2'], label = "sensor 2", linewidth =2, color = 'C1')
#SM.plot(SM_cb.index.values, SM_cb['SM_EC'], label = "Mean", linewidth =4, color= 'black')
# Setting axes's limit
SM.set_xlim('2024-02-01 00:00', '2025-01-01 00:00')
#SM.set_ylim(0, 42)
# Set title and labels for axes
SM.set_xlabel('Date', fontsize=46)
SM.set_ylabel('Ref. vol. SM (%)', fontsize=46)
#plt.title('Gamma dose rate of GR1', fontsize=37)
SM.legend(ncol=1, loc='lower left', fontsize=40, frameon=False)
plt.tight_layout()
plt.savefig("D:\Data\Data_3rd_chapter\Figures\Sel_EC_SM_preprocessed.png")
plt.show()





## Horizontal average of soil moisture for each depth
ref_SM_0 = pd.concat([ref_SM_L1['SM_0cm'], ref_SM_L2['SM_0cm'],ref_SM_L3['SM_0cm'],ref_SM_L4['SM_0cm'],ref_SM_L5['SM_0cm'], SM_cb['SM_EC']], axis=1, keys=['ref_SM_L1', 'ref_SM_L2', 'ref_SM_L3','ref_SM_L4','ref_SM_L5','SM_cb'])
ref_SM_0.columns = ['L1', 'L2', 'L3', 'L4', 'L5', 'EC']
#ref_SM_0 = pd.concat([ref_SM_L1['SM_0cm'], ref_SM_L2['SM_0cm'], ref_SM_L3['SM_0cm'], ref_SM_L4['SM_0cm'], ref_SM_L5['SM_0cm']], axis=1, keys=['ref_SM_L1', 'ref_SM_L2', 'ref_SM_L3','ref_SM_L4','ref_SM_L5'])
#ref_SM_0.columns = ['L1', 'L2', 'L3', 'L4', 'L5']
#ref_SM_0 = pd.concat([ref_SM_L1['SM_0cm'], ref_SM_L2['SM_0cm'], ref_SM_L5['SM_0cm']], axis=1, keys=['ref_SM_L1', 'ref_SM_L2','ref_SM_L5'])
#ref_SM_0.columns = ['L1', 'L2', 'L5']
# counting nan values
ref_SM_0.isnull().sum()
# calling rows which has nan (at least in a single cell)
#ref_SM_0.loc[ref_SM_0.isna().any(1)]
#changing entire row with nan values if a single cell has nan
ref_SM_0.loc[ref_SM_0.isna().any(axis=1)] = np.nan
ref_SM_0['SM_0cm'] = ref_SM_0[['L1', 'L2', 'L3', 'L4','L5','EC']].mean(axis=1)
#ref_SM_0['SM_0cm'] = ref_SM_0[['L1', 'L2', 'L3', 'L4','L5']].mean(axis=1)
#ref_SM_0['SM_0cm'] = ref_SM_0[['L1', 'L2', 'L5']].mean(axis=1)

ref_SM_5 = pd.concat([ref_SM_L1['SM_5cm'], ref_SM_L2['SM_5cm'],ref_SM_L3['SM_5cm'], ref_SM_L4['SM_5cm'], ref_SM_L5['SM_5cm']], axis=1, keys=['ref_SM_L1', 'ref_SM_L2', 'ref_SM_L3', 'ref_SM_L4','ref_SM_L5'])
ref_SM_5.columns = ['L1', 'L2', 'L3', 'L4', 'L5']
#ref_SM_5 = pd.concat([ref_SM_L1['SM_5cm'], ref_SM_L3['SM_5cm'], ref_SM_L4['SM_5cm']], axis=1, keys=['ref_SM_L1', 'ref_SM_L2', 'ref_SM_L3', 'ref_SM_L4','ref_SM_L5'])
#ref_SM_5.columns = ['L1', 'L3', 'L4']
# counting nan values
ref_SM_5.isnull().sum()
ref_SM_5.loc[ref_SM_5.isna().any(axis=1)] = np.nan
ref_SM_5['SM_5cm'] = ref_SM_5[['L1', 'L2', 'L3','L4', 'L5']].mean(axis=1)
#ref_SM_5['SM_5cm'] = ref_SM_5[['L1', 'L3','L4']].mean(axis=1)


ref_SM_10 = pd.concat([ref_SM_L1['SM_10cm'], ref_SM_L2['SM_10cm'],ref_SM_L3['SM_10cm'],ref_SM_L4['SM_10cm'],ref_SM_L5['SM_10cm']], axis=1, keys=['ref_SM_L1', 'ref_SM_L2', 'ref_SM_L3', 'ref_SM_L4','ref_SM_L5'])
ref_SM_10.columns = ['L1', 'L2', 'L3', 'L4', 'L5']
# counting nan values
ref_SM_10.isnull().sum()
ref_SM_10.loc[ref_SM_10.isna().any(axis=1)] = np.nan
ref_SM_10['SM_10cm'] = ref_SM_10[['L1', 'L2', 'L3','L4','L5']].mean(axis=1)

ref_SM_20 = pd.concat([ref_SM_L1['SM_20cm'], ref_SM_L2['SM_20cm'],ref_SM_L3['SM_20cm'],ref_SM_L4['SM_20cm'],ref_SM_L5['SM_20cm']], axis=1, keys=['ref_SM_L1', 'ref_SM_L2', 'ref_SM_L3', 'ref_SM_L4','ref_SM_L5'])
ref_SM_20.columns = ['L1', 'L2', 'L3', 'L4', 'L5']
# counting nan values
ref_SM_20.isnull().sum()
ref_SM_20.loc[ref_SM_20.isna().any(axis=1)] = np.nan
ref_SM_20['SM_20cm'] = ref_SM_20[['L1', 'L2', 'L3', 'L4', 'L5']].mean(axis=1)

## Combining soil moisture data for each depth
ref_SM = pd.concat([ref_SM_0['SM_0cm'], ref_SM_5['SM_5cm'],ref_SM_10['SM_10cm'],ref_SM_20['SM_20cm']], axis=1, keys=['ref_SM_0', 'ref_SM_5', 'ref_SM_10','ref_SM_20'])
ref_SM.columns = ['SM_0cm', 'SM_5cm', 'SM_10cm', 'SM_20cm']
ref_SM.rename(columns={'SM_0cm': 'SM_2cm'}, inplace=True)
ref_SM.interpolate(method = 'time', limit_direction='forward', limit = 500, inplace = True)
### Calculating hourly and daily average 
# defining function to calculate hourly mean when 50% data points are available 
def mean_when_3non_nan(x):
    non_nulls = x.notnull()
    if non_nulls.sum() > 2: # Among 6 datapoints, calculate mean when 3 datapoints are available
        return x[non_nulls].mean()
    return np.nan
ref_SM_hourly = ref_SM.resample('h').apply(mean_when_3non_nan)

## Adding additional SoilNet data for the summer 2024
# Before adding, slicing the ICOS ref Sm data
ref_SM_1 = ref_SM_hourly.loc['2024-02-01 00:00':'2024-05-29 00:00']
ref_SM_2 = ref_SM_hourly.loc['2024-05-29 01:00':'2024-09-13 00:00']
ref_SM_3 = ref_SM_hourly.loc['2024-09-13 01:00':'2025-01-01 00:00']
## importing processed additional SoilNet data
add = pd.read_csv(r"D:\Data\Data_3rd_chapter\Outputs\Add_SoilNet_2024.csv", index_col=0, parse_dates = True, header = 0)

# Average corresponding columns from two dataframes
ref_SM_summer = (ref_SM_2 + add) / 2
## Adding one dataset after another to get a continuous time-series
ref_SM = pd.concat([ref_SM_1, ref_SM_summer, ref_SM_3])

ref_SM.loc[ref_SM.isna().any(axis=1)] = np.nan
#ref_SM.loc['2023-07-22 09:30:00+00:00':'2023-08-24 09:50:00+00:00'] = np.nan
#ref_SM.loc['2023-11-02 01:00:00+00:00':'2023-11-14 09:50:00+00:00'] = np.nan
#ref_SM.loc['2023-02-06 01:00:00+00:00':'2023-02-10 09:50:00+00:00'] = np.nan
# Average soil moisture through the entire depth (0-50 cm)
#ref_SM['SM_av'] = ref_SM[['SM_0cm', 'SM_5cm', 'SM_10cm','SM_20cm']].mean(axis=1)
ref_SM['SM_av_dw'] = ((ref_SM['SM_2cm']*3.5)+ (ref_SM['SM_5cm']*4) + (ref_SM['SM_10cm']*7.5) + (ref_SM['SM_20cm']*10))/25
ref_SM['SM_av_sw'] = (ref_SM['SM_2cm']*0.47 + ref_SM['SM_5cm']*0.22 + ref_SM['SM_10cm']*0.17 + ref_SM['SM_20cm']*0.14)
## saving the output
ref_SM.to_csv("D:\Data\Data_3rd_chapter\Outputs\selhausen_ref_SM_with_add_SoilNet_data.csv")


### Calculating daily average 
ref_SM_daily = ref_SM.resample('D').mean()

## Ploting 
fig, ax = plt.subplots(figsize=(25.5, 19.7), sharex=False, sharey=False, constrained_layout = True, dpi = 50) # No axis sharing
plt.axis('off')   # Turning the general axis off in order to create individual axis for each subplot
gs = gridspec.GridSpec(2, 1, height_ratios=[0.5, 1.2], wspace=0, hspace=0) # no of row 2, column 1 and no space bet. subplots
rain = plt.subplot(gs[0])
SM = plt.subplot(gs[1]) # add_subplot command adds each plot in fig 
# add_subplot(total no of row, total no of column, position of this subplot)
#plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)
matplotlib.rc('xtick', labelsize=23) # defining the xtick fontsize for all subplots
matplotlib.rc('ytick', labelsize=23)
#plt.tick_params(axis='both', which='major', labelsize=14) for one specific subplot
matplotlib.rcParams['xtick.major.pad']='13'
matplotlib.rcParams['ytick.major.pad']='13'

rain.bar (prc.index, prc['Precipitation'])
#rain.set_xlabel("Date", fontsize = 30)
rain.set_ylabel("Precipitation (mm)", fontsize = 44)
rain.set_ylim(0, 13)
rain.set_xlim([pd.to_datetime('2024-01-23 00:00', format = '%Y-%m-%d %H:%M'),
             pd.to_datetime('2025-01-01 00:00', format = '%Y-%m-%d %H:%M')])
rain.set_xticks([])
rain.invert_yaxis()
# fig.add_subplot(111) works for arranging subgraphs within this graph.
SM.plot(ref_SM_daily.index.values, ref_SM_daily['SM_2cm'], label = "2 cm", linewidth =2)
SM.plot(ref_SM_daily.index.values, ref_SM_daily['SM_5cm'], label = "5 cm", linewidth =2)
SM.plot(ref_SM_daily.index.values, ref_SM_daily['SM_10cm'], label = "10 cm", linewidth =2)
SM.plot(ref_SM_daily.index.values, ref_SM_daily['SM_20cm'], label = "20 cm", linewidth =2)
SM.plot(ref_SM_daily.index.values, ref_SM_daily['SM_av_dw'], label = "Mean", linewidth =4, color= 'black')
# Setting axes's limit
SM.set_xlim([pd.to_datetime('2024-01-23 00:00', format = '%Y-%m-%d %H:%M'),
             pd.to_datetime('2025-01-01 00:00', format = '%Y-%m-%d %H:%M')])
#SM.set_ylim(0, 42)
# Set title and labels for axes
SM.set_xlabel('Date', fontsize=42)
SM.set_ylabel('Ref. vol. SM (%)', fontsize=42)
#plt.title('Gamma dose rate of GR1', fontsize=37)
SM.legend(ncol=1, loc='lower left', fontsize=39, frameon=False)
plt.tight_layout()
plt.savefig("D:\Data\Data_3rd_chapter\Figures\Sel_ref_SM_daily_add_SoilNet.png")
plt.show()





