# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 15:24:24 2026

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


### Importing the reference SoilNet data for summer 2024
#L1
ref_SM_L1 = pd.read_csv(r"D:\Data\Data_3rd_chapter\Input_data\Selhausen_2024\SoilNet_ADD_2024\sn_001.csv", index_col=0, parse_dates = True, header = 0)
## removing unnecessary TS (soil temperature) columns
ref_SM_L1 = ref_SM_L1.drop(columns=[col for col in ref_SM_L1.columns if col.startswith('TS')])
## in case the column name has issue with case (TS or ts)
#ref_SM_L1 = ref_SM_L1.drop(columns=[col for col in ref_SM_L1.columns if col.upper().startswith('TS')])
# Making pandas datetime to be UTC aware
ref_SM_L1.index = pd.to_datetime(ref_SM_L1.index, utc=True, format= '%Y-%m-%dT%H:%M:%S.%f%z')  
print(ref_SM_L1.index)
ref_SM_L1['SM_2cm'] = ref_SM_L1[['SWC_1[vol%]', 'SWC_2[vol%]']].mean(axis=1)
ref_SM_L1['SM_5cm'] = ref_SM_L1[['SWC_3[vol%]', 'SWC_4[vol%]']].mean(axis=1)
ref_SM_L1['SM_10cm'] = ref_SM_L1[['SWC_5[vol%]', 'SWC_6[vol%]']].mean(axis=1)
ref_SM_L1['SM_20cm'] = ref_SM_L1[['SWC_7[vol%]', 'SWC_8[vol%]']].mean(axis=1)

#L2
ref_SM_L2 = pd.read_csv(r"D:\Data\Data_3rd_chapter\Input_data\Selhausen_2024\SoilNet_ADD_2024\sn_002.csv", index_col=0, parse_dates = True, header = 0)
## removing unnecessary TS (soil temperature) columns
ref_SM_L2 = ref_SM_L2.drop(columns=[col for col in ref_SM_L2.columns if col.startswith('TS')])
ref_SM_L2.index = pd.to_datetime(ref_SM_L2.index, utc=True, format= '%Y-%m-%dT%H:%M:%S.%f%z')  
print(ref_SM_L2.index)
ref_SM_L2['SM_2cm'] = ref_SM_L2[['SWC_1[vol%]', 'SWC_2[vol%]']].mean(axis=1)
ref_SM_L2['SM_5cm'] = ref_SM_L2[['SWC_3[vol%]', 'SWC_4[vol%]']].mean(axis=1)
ref_SM_L2['SM_10cm'] = ref_SM_L2[['SWC_5[vol%]', 'SWC_6[vol%]']].mean(axis=1)
ref_SM_L2['SM_20cm'] = ref_SM_L2[['SWC_7[vol%]', 'SWC_8[vol%]']].mean(axis=1)


#L3
ref_SM_L3 = pd.read_csv(r"D:\Data\Data_3rd_chapter\Input_data\Selhausen_2024\SoilNet_ADD_2024\sn_003.csv", index_col=0, parse_dates = True, header = 0)
## removing unnecessary TS (soil temperature) columns
ref_SM_L3 = ref_SM_L3.drop(columns=[col for col in ref_SM_L3.columns if col.startswith('TS')])
ref_SM_L3.index = pd.to_datetime(ref_SM_L3.index, utc=True, format= '%Y-%m-%dT%H:%M:%S.%f%z')  
print(ref_SM_L3.index)
ref_SM_L3['SM_2cm'] = ref_SM_L3[['SWC_1[vol%]', 'SWC_2[vol%]']].mean(axis=1)
ref_SM_L3['SM_5cm'] = ref_SM_L3[['SWC_3[vol%]', 'SWC_4[vol%]']].mean(axis=1)
ref_SM_L3['SM_10cm'] = ref_SM_L3[['SWC_5[vol%]', 'SWC_6[vol%]']].mean(axis=1)
ref_SM_L3['SM_20cm'] = ref_SM_L3[['SWC_7[vol%]', 'SWC_8[vol%]']].mean(axis=1)


#L4
ref_SM_L4 = pd.read_csv(r"D:\Data\Data_3rd_chapter\Input_data\Selhausen_2024\SoilNet_ADD_2024\sn_004.csv", index_col=0, parse_dates = True, header = 0)
## removing unnecessary TS (soil temperature) columns
ref_SM_L4 = ref_SM_L4.drop(columns=[col for col in ref_SM_L4.columns if col.startswith('TS')])
ref_SM_L4.index = pd.to_datetime(ref_SM_L4.index, utc=True, format= '%Y-%m-%dT%H:%M:%S.%f%z')  
print(ref_SM_L4.index)
ref_SM_L4['SM_2cm'] = ref_SM_L4[['SWC_1[vol%]', 'SWC_2[vol%]']].mean(axis=1)
ref_SM_L4['SM_5cm'] = ref_SM_L4[['SWC_3[vol%]', 'SWC_4[vol%]']].mean(axis=1)
ref_SM_L4['SM_10cm'] = ref_SM_L4[['SWC_5[vol%]', 'SWC_6[vol%]']].mean(axis=1)
ref_SM_L4['SM_20cm'] = ref_SM_L4[['SWC_7[vol%]', 'SWC_8[vol%]']].mean(axis=1)

## Horizontal average of soil moisture for each depth
ref_SM_2 = pd.concat([ref_SM_L1['SM_2cm'], ref_SM_L2['SM_2cm'],ref_SM_L3['SM_2cm'],ref_SM_L4['SM_2cm']], axis=1, keys=['ref_SM_L1', 'ref_SM_L2', 'ref_SM_L3','ref_SM_L4'])
ref_SM_2.columns = ['L1', 'L2', 'L3', 'L4']
# counting nan values
ref_SM_2.isnull().sum()
# calling rows which has nan (at least in a single cell)
#ref_SM_0.loc[ref_SM_0.isna().any(1)]
#changing entire row with nan values if a single cell has nan
ref_SM_2.loc[ref_SM_2.isna().any(axis=1)] = np.nan
ref_SM_2['SM_2cm'] = ref_SM_2[['L1', 'L2', 'L3', 'L4']].mean(axis=1)

ref_SM_5 = pd.concat([ref_SM_L1['SM_5cm'], ref_SM_L2['SM_5cm'],ref_SM_L3['SM_5cm'], ref_SM_L4['SM_5cm']], axis=1, keys=['ref_SM_L1', 'ref_SM_L2', 'ref_SM_L3', 'ref_SM_L4'])
ref_SM_5.columns = ['L1', 'L2', 'L3', 'L4']
# counting nan values
ref_SM_5.isnull().sum()
ref_SM_5.loc[ref_SM_5.isna().any(axis=1)] = np.nan
ref_SM_5['SM_5cm'] = ref_SM_5[['L1', 'L2', 'L3','L4']].mean(axis=1)

ref_SM_10 = pd.concat([ref_SM_L1['SM_10cm'], ref_SM_L2['SM_10cm'],ref_SM_L3['SM_10cm'],ref_SM_L4['SM_10cm']], axis=1, keys=['ref_SM_L1', 'ref_SM_L2', 'ref_SM_L3', 'ref_SM_L4'])
ref_SM_10.columns = ['L1', 'L2', 'L3', 'L4']
# counting nan values
ref_SM_10.isnull().sum()
ref_SM_10.loc[ref_SM_10.isna().any(axis=1)] = np.nan
ref_SM_10['SM_10cm'] = ref_SM_10[['L1', 'L2', 'L3','L4']].mean(axis=1)

ref_SM_20 = pd.concat([ref_SM_L1['SM_20cm'], ref_SM_L2['SM_20cm'],ref_SM_L3['SM_20cm'],ref_SM_L4['SM_20cm']], axis=1, keys=['ref_SM_L1', 'ref_SM_L2', 'ref_SM_L3', 'ref_SM_L4'])
ref_SM_20.columns = ['L1', 'L2', 'L3', 'L4']
# counting nan values
ref_SM_20.isnull().sum()
ref_SM_20.loc[ref_SM_20.isna().any(axis=1)] = np.nan
ref_SM_20['SM_20cm'] = ref_SM_20[['L1', 'L2', 'L3', 'L4']].mean(axis=1)


## Combining soil moisture data for each depth
ref_SM = pd.concat([ref_SM_2['SM_2cm'], ref_SM_5['SM_5cm'],ref_SM_10['SM_10cm'],ref_SM_20['SM_20cm']], axis=1, keys=['ref_SM_0', 'ref_SM_5', 'ref_SM_10','ref_SM_20'])
ref_SM.columns = ['SM_2cm', 'SM_5cm', 'SM_10cm', 'SM_20cm']
ref_SM.loc[ref_SM.isna().any(axis=1)] = np.nan
ref_SM.interpolate(method = 'time', limit_direction='forward', limit = 500, inplace = True)
## saving the output
ref_SM.to_csv("D:\Data\Data_3rd_chapter\Outputs\Add_SoilNet_2024.csv")
