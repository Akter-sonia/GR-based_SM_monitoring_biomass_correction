# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 15:50:49 2026

@author: s.akter
"""

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



###Visualizing biomass correction effect on soil moisture time series

## Precipitation time series
# Importing 2023 precipitation data
prc_23 = pd.read_excel(r"D:\Data\Data_2nd_paper\Raw_data_2nd_paper\SE_BDK_precp_nearby_field.xlsx", header = None, parse_dates= [0], index_col=0, na_values=['noData', '99999'])
prc_23.columns = ['Feature', 'Precipitation','Data quality']
print(prc_23.head())
prc_23.index = pd.to_datetime(prc_23.index, utc= True, format= '%Y-%m-%dT%H:%M:%S.%f%z')
prc_23.drop(['Feature', 'Data quality'], axis=1, inplace=True)
prc_23["Precipitation"] = prc_23["Precipitation"].round(decimals=5)
prc_23 = prc_23['2023/02/05 00:00:00':'2024/01/31 00:00:00']

# Importing precipitation 2024 data
prc_24 = pd.read_excel(r"D:\Data\Data_3rd_chapter\Input_data\Selhausen_2024\SE_EC_precipitation.xlsx", header = 0, parse_dates= [0], index_col=0, na_values=['noData', '99999', '-9999'])
prc_24.columns = ['Feature', 'Precipitation','Data quality']
print(prc_24.head())
prc_24.index = pd.to_datetime(prc_24.index, utc= True, format= '%Y-%m-%dT%H:%M:%S.%f%z')
prc_24.drop(['Feature', 'Data quality'], axis=1, inplace=True)
prc_24["Precipitation"] = prc_24["Precipitation"].round(decimals=5)
prc_24 = prc_24['2024/02/01 00:00:00':'2024/12/31 00:00:00']

## Stacking the 2023 data with the 2024 data
prc = pd.concat([prc_23, prc_24], axis=0)



## Soil moisture time series
# Importing SARA K-40 data for 2023 for Selhausen
K_SM_23 = pd.read_excel(r"D:\Data\Data_3rd_chapter\Biomass_correction_Selhausen\Biomass_correction_2023\Output\K_dwSM_Fresh_AGB.xlsx", sheet_name=1, header = 0, parse_dates= [0], index_col=0)

### Importing K_SM 2024 data
K_SM_24 = pd.read_excel(r"D:\Data\Data_3rd_chapter\Biomass_correction_Selhausen\Biomass_correction_2024\Output\K_dwSM_Fresh_AGB.xlsx", sheet_name=1, header = 0, parse_dates= [0], index_col=0)

## Stacking the 2023 data with the 2024 data
K_SM = pd.concat([K_SM_23, K_SM_24], axis=0)
# Merging the data with an independent time index which has all timestamp from the start to end period 
# Creating a dataframe with customized date time index
time_index = pd.date_range(start ='2023/02/05 00:00:00', end ='2024/12/31 00:00:00', freq ='D')
df = pd.DataFrame(time_index, columns =['date']) # Creating a dataframe, making the time index a column named as date
df['data'] = np.random.randint(0, 100, size =(len(time_index)))  # Creating a new column with random numbers 
df['datetime'] = pd.to_datetime(df['date'], utc=True, format= '%Y-%m-%dT%H:%M:%S.%f%z')
df = df.set_index('datetime')
df.drop(['date'], axis = 1, inplace = True)
# Merging data with the customized datetime index data to avoid joining line when there is no data
K_SM= pd.merge(df, K_SM, how = 'left', left_index = True, right_index = True )
K_SM.drop(['data'], axis = 1, inplace = True)


# Importing MIRA 2023 data 
MIS_SM_23 = pd.read_excel(r"D:\Data\Data_3rd_chapter\Biomass_correction_Selhausen\Biomass_correction_2023\Output\MIRA_dwSM_Fresh_AGB.xlsx", sheet_name=1, header = 0, parse_dates= [0], index_col=0)

### Importing MIRA 2024 data
MIS_SM_24 = pd.read_excel(r"D:\Data\Data_3rd_chapter\Biomass_correction_Selhausen\Biomass_correction_2024\Output\MIRA_dwSM_Fresh_AGB.xlsx", sheet_name=1, header = 0, parse_dates= [0], index_col=0)

## Stacking the 2023 data with the 2024 data
MIS_SM = pd.concat([MIS_SM_23, MIS_SM_24], axis=0)
# Merging data with the customized datetime index data to avoid joining line when there is no data
MIS_SM= pd.merge(df, MIS_SM, how = 'left', left_index = True, right_index = True )
MIS_SM.drop(['data'], axis = 1, inplace = True)




## Plotting

fig = plt.figure(figsize=(18, 12.6), dpi=350)

# Three rows, one column
gs = gridspec.GridSpec(3, 1, figure=fig, height_ratios=[0.2, 0.4, 0.4], hspace=0)

# Create subplots
R = fig.add_subplot(gs[0])   # Precipitation 
K = fig.add_subplot(gs[1])   # K-40
M = fig.add_subplot(gs[2])   # EGR

# --------------------------------------------------
# 1. Precipitation
# --------------------------------------------------
R.plot(prc.index,prc['Precipitation'],color='black',linewidth=2)

R.axvspan (pd.to_datetime('2023-03-13 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2023-04-09 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
R.axvspan (pd.to_datetime('2023-04-10 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2023-07-26 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'darkgreen', fill=True, alpha=.3)
R.axvspan (pd.to_datetime('2023-07-27 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2023-08-20 00:00', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
R.axvspan (pd.to_datetime('2023-10-20 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2024-01-10 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
R.axvspan (pd.to_datetime('2024-05-24 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2024-07-01 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
R.axvspan (pd.to_datetime('2024-07-02 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2024-09-15 00:00', format = '%Y-%m-%d %H:%M'), 
         color= 'darkgreen', fill=True, alpha=.3)
R.set_ylim(0, 11)
R.set_ylabel("Precipitation\n[mm]", fontsize=25)
R.set_xticks([])
R.text('2023-04-10 00:00', 8, 'Winter wheat', fontsize = 23, color = 'black')
R.text('2023-10-19 00:00', 8, 'Catch crop', fontsize = 23, color = 'black')
R.text('2024-06-06 00:00', 8, 'Sugar beet', fontsize = 23, color = 'black')


# --------------------------------------------------
# 2. K-40 GR
# --------------------------------------------------
K.plot(K_SM.index, K_SM['SM_ref'], color= 'black', linewidth = 2, label = "reference")
K.plot(K_SM.index, K_SM['SM_predicted_beta0'], color= 'red', linewidth = 2, label = "uncorrected")
K.plot(K_SM.index, K_SM['SM_predicted_beta0.01'], color= 'gray', linewidth = 3, label = "corrected")

K.axvspan (pd.to_datetime('2023-03-13 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2023-04-09 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
K.axvspan (pd.to_datetime('2023-04-10 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2023-07-26 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'darkgreen', fill=True, alpha=.3)
K.axvspan (pd.to_datetime('2023-07-27 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2023-08-20 00:00', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
K.axvspan (pd.to_datetime('2023-10-20 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2024-01-10 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
K.axvspan (pd.to_datetime('2024-05-24 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2024-07-01 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
K.axvspan (pd.to_datetime('2024-07-02 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2024-09-15 00:00', format = '%Y-%m-%d %H:%M'), 
         color= 'darkgreen', fill=True, alpha=.3)
K.legend(loc='lower center', fontsize=23, frameon=False,borderpad=0.2)
K.set_xticks([])
K.set_ylim(0, 54)
K.set_ylabel("SM \n[vol.%]", fontsize=25)

# --------------------------------------------------
# 3. MIRA EGR
# --------------------------------------------------
M.plot(MIS_SM.index, MIS_SM['SM_ref'], color= 'black', linewidth = 2, label = "reference")
M.plot(MIS_SM.index, MIS_SM['SM_predicted_beta0'], color= 'red', linewidth = 2, label = "uncorrected")
M.plot(MIS_SM.index, MIS_SM['SM_predicted_beta0.01'], color= 'gray', linewidth = 3, label = "corrected")

M.axvspan (pd.to_datetime('2023-03-13 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2023-04-09 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
M.axvspan (pd.to_datetime('2023-04-10 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2023-07-26 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'darkgreen', fill=True, alpha=.3)
M.axvspan (pd.to_datetime('2023-07-27 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2023-08-20 00:00', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
M.axvspan (pd.to_datetime('2023-10-20 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2024-01-10 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
M.axvspan (pd.to_datetime('2024-05-24 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2024-07-01 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
M.axvspan (pd.to_datetime('2024-07-02 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2024-09-15 00:00', format = '%Y-%m-%d %H:%M'), 
         color= 'darkgreen', fill=True, alpha=.3)
#M.legend(loc='lower left', fontsize=24, frameon=False)
M.set_xlabel("Date", fontsize=25)
M.set_ylim(0, 54)
M.set_ylabel("SM\n[vol.%]", fontsize=25)

# Common x-axis limits
start_date = pd.to_datetime('2023-02-05')
end_date = pd.to_datetime('2024-12-31')

for ax in [R, K, M]:
    ax.set_xlim(start_date, end_date)

# Tick size
for ax in [R, K, M]:
    ax.tick_params(axis='both', labelsize=15)
    
# add labels
props = dict(boxstyle='square', facecolor='gray', alpha=0.5, pad=.1)
R.text(prc.index.max()-pd.Timedelta('35Hours'), 9.5, 'a', fontsize=22, fontweight='bold', bbox=props, ha='right', c='k')
K.text(K_SM.index.max()-pd.Timedelta('35Hours'), 50.27, 'b', fontsize=22, fontweight='bold', bbox=props, ha='right', c='k')
M.text(MIS_SM.index.max()-pd.Timedelta('35Hours'), 50.27, 'c', fontsize=22, fontweight='bold', bbox=props, ha='right', c='k')


plt.savefig(r"D:\Data\Data_3rd_chapter\Figures\SM_series_visu_biomass_corr.png",dpi=300,bbox_inches='tight')
plt.show()












###Visualizing biomass correction effect on soil moisture time series, adding a line for fixed alpha obtained from biomass-exclusion cali model

## Precipitation time series
# Importing 2023 precipitation data
prc_23 = pd.read_excel(r"D:\Data\Data_2nd_paper\Raw_data_2nd_paper\SE_BDK_precp_nearby_field.xlsx", header = None, parse_dates= [0], index_col=0, na_values=['noData', '99999'])
prc_23.columns = ['Feature', 'Precipitation','Data quality']
print(prc_23.head())
prc_23.index = pd.to_datetime(prc_23.index, utc= True, format= '%Y-%m-%dT%H:%M:%S.%f%z')
prc_23.drop(['Feature', 'Data quality'], axis=1, inplace=True)
prc_23["Precipitation"] = prc_23["Precipitation"].round(decimals=5)
prc_23 = prc_23['2023/02/05 00:00:00':'2024/01/31 00:00:00']

# Importing precipitation 2024 data
prc_24 = pd.read_excel(r"D:\Data\Data_3rd_chapter\Input_data\Selhausen_2024\SE_EC_precipitation.xlsx", header = 0, parse_dates= [0], index_col=0, na_values=['noData', '99999', '-9999'])
prc_24.columns = ['Feature', 'Precipitation','Data quality']
print(prc_24.head())
prc_24.index = pd.to_datetime(prc_24.index, utc= True, format= '%Y-%m-%dT%H:%M:%S.%f%z')
prc_24.drop(['Feature', 'Data quality'], axis=1, inplace=True)
prc_24["Precipitation"] = prc_24["Precipitation"].round(decimals=5)
prc_24 = prc_24['2024/02/01 00:00:00':'2024/12/31 00:00:00']

## Stacking the 2023 data with the 2024 data
prc = pd.concat([prc_23, prc_24], axis=0)



## Soil moisture time series
# Importing SARA K-40 data for 2023 for Selhausen
K_SM_23 = pd.read_excel(r"D:\Data\Data_3rd_chapter\Biomass_correction_Selhausen\Biomass_correction_2023\Output\K_dwSM_Fresh_AGB.xlsx", sheet_name=1, header = 0, parse_dates= [0], index_col=0)

### Importing K_SM 2024 data
K_SM_24 = pd.read_excel(r"D:\Data\Data_3rd_chapter\Biomass_correction_Selhausen\Biomass_correction_2024\Output\K_dwSM_Fresh_AGB.xlsx", sheet_name=1, header = 0, parse_dates= [0], index_col=0)

## Stacking the 2023 data with the 2024 data
K_SM = pd.concat([K_SM_23, K_SM_24], axis=0)
# Merging the data with an independent time index which has all timestamp from the start to end period 
# Creating a dataframe with customized date time index
time_index = pd.date_range(start ='2023/02/05 00:00:00', end ='2024/12/31 00:00:00', freq ='D')
df = pd.DataFrame(time_index, columns =['date']) # Creating a dataframe, making the time index a column named as date
df['data'] = np.random.randint(0, 100, size =(len(time_index)))  # Creating a new column with random numbers 
df['datetime'] = pd.to_datetime(df['date'], utc=True, format= '%Y-%m-%dT%H:%M:%S.%f%z')
df = df.set_index('datetime')
df.drop(['date'], axis = 1, inplace = True)
# Merging data with the customized datetime index data to avoid joining line when there is no data
K_SM= pd.merge(df, K_SM, how = 'left', left_index = True, right_index = True )
K_SM.drop(['data'], axis = 1, inplace = True)


# Importing MIRA 2023 data 
MIS_SM_23 = pd.read_excel(r"D:\Data\Data_3rd_chapter\Biomass_correction_Selhausen\Biomass_correction_2023\Output\MIRA_dwSM_Fresh_AGB.xlsx", sheet_name=1, header = 0, parse_dates= [0], index_col=0)

### Importing MIRA 2024 data
MIS_SM_24 = pd.read_excel(r"D:\Data\Data_3rd_chapter\Biomass_correction_Selhausen\Biomass_correction_2024\Output\MIRA_dwSM_Fresh_AGB.xlsx", sheet_name=1, header = 0, parse_dates= [0], index_col=0)

## Stacking the 2023 data with the 2024 data
MIS_SM = pd.concat([MIS_SM_23, MIS_SM_24], axis=0)
# Merging data with the customized datetime index data to avoid joining line when there is no data
MIS_SM= pd.merge(df, MIS_SM, how = 'left', left_index = True, right_index = True )
MIS_SM.drop(['data'], axis = 1, inplace = True)


## Soil moisture time series for fixed alpha
# Importing SARA K-40 data for 2023 for Selhausen
K_SM_23_fa = pd.read_excel(r"D:\Data\Data_3rd_chapter\Biomass_correction_Selhausen\Biomass_correction_2023\Output\K_dwSM_Fresh_AGB_fixed_alpha.xlsx", sheet_name=1, header = 0, parse_dates= [0], index_col=0)

### Importing K_SM 2024 data
K_SM_24_fa = pd.read_excel(r"D:\Data\Data_3rd_chapter\Biomass_correction_Selhausen\Biomass_correction_2024\Output\K_dwSM_Fresh_AGB_fixed_alpha.xlsx", sheet_name=1, header = 0, parse_dates= [0], index_col=0)

## Stacking the 2023 data with the 2024 data
K_SM_fa = pd.concat([K_SM_23_fa, K_SM_24_fa], axis=0)
# Merging the data with an independent time index which has all timestamp from the start to end period 
# Creating a dataframe with customized date time index
time_index = pd.date_range(start ='2023/02/05 00:00:00', end ='2024/12/31 00:00:00', freq ='D')
df = pd.DataFrame(time_index, columns =['date']) # Creating a dataframe, making the time index a column named as date
df['data'] = np.random.randint(0, 100, size =(len(time_index)))  # Creating a new column with random numbers 
df['datetime'] = pd.to_datetime(df['date'], utc=True, format= '%Y-%m-%dT%H:%M:%S.%f%z')
df = df.set_index('datetime')
df.drop(['date'], axis = 1, inplace = True)
# Merging data with the customized datetime index data to avoid joining line when there is no data
K_SM_fa= pd.merge(df, K_SM_fa, how = 'left', left_index = True, right_index = True )
K_SM_fa.drop(['data'], axis = 1, inplace = True)


# Importing MIRA 2023 data 
MIS_SM_23_fa = pd.read_excel(r"D:\Data\Data_3rd_chapter\Biomass_correction_Selhausen\Biomass_correction_2023\Output\MIRA_dwSM_Fresh_AGB_fixed_alpha.xlsx", sheet_name=1, header = 0, parse_dates= [0], index_col=0)

### Importing MIRA 2024 data
MIS_SM_24_fa = pd.read_excel(r"D:\Data\Data_3rd_chapter\Biomass_correction_Selhausen\Biomass_correction_2024\Output\MIRA_dwSM_Fresh_AGB_fixed_alpha.xlsx", sheet_name=1, header = 0, parse_dates= [0], index_col=0)

## Stacking the 2023 data with the 2024 data
MIS_SM_fa = pd.concat([MIS_SM_23_fa, MIS_SM_24_fa], axis=0)
# Merging data with the customized datetime index data to avoid joining line when there is no data
MIS_SM_fa= pd.merge(df, MIS_SM_fa, how = 'left', left_index = True, right_index = True )
MIS_SM_fa.drop(['data'], axis = 1, inplace = True)


## Plotting

fig = plt.figure(figsize=(18, 12.6), dpi=350)

# Three rows, one column
gs = gridspec.GridSpec(3, 1, figure=fig, height_ratios=[0.2, 0.4, 0.4], hspace=0)

# Create subplots
R = fig.add_subplot(gs[0])   # Precipitation 
K = fig.add_subplot(gs[1])   # K-40
M = fig.add_subplot(gs[2])   # EGR

# --------------------------------------------------
# 1. Precipitation
# --------------------------------------------------
R.plot(prc.index,prc['Precipitation'],color='black',linewidth=2)

R.axvspan (pd.to_datetime('2023-03-13 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2023-04-09 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
R.axvspan (pd.to_datetime('2023-04-10 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2023-07-26 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'darkgreen', fill=True, alpha=.3)
R.axvspan (pd.to_datetime('2023-07-27 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2023-08-20 00:00', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
R.axvspan (pd.to_datetime('2023-10-20 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2024-01-10 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
R.axvspan (pd.to_datetime('2024-05-24 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2024-07-01 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
R.axvspan (pd.to_datetime('2024-07-02 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2024-09-15 00:00', format = '%Y-%m-%d %H:%M'), 
         color= 'darkgreen', fill=True, alpha=.3)
R.set_ylim(0, 11)
R.set_ylabel("Precipitation\n[mm]", fontsize=25)
R.set_xticks([])
R.text('2023-04-10 00:00', 8, 'Winter wheat', fontsize = 23, color = 'black')
R.text('2023-10-19 00:00', 8, 'Catch crop', fontsize = 23, color = 'black')
R.text('2024-06-06 00:00', 8, 'Sugar beet', fontsize = 23, color = 'black')


# --------------------------------------------------
# 2. K-40 GR
# --------------------------------------------------
K.plot(K_SM.index, K_SM['SM_ref'], color= 'black', linewidth = 2, label = "reference")
K.plot(K_SM.index, K_SM['SM_predicted_beta0'], color= 'red', linewidth = 2, label = "uncorrected")
K.plot(K_SM_fa.index, K_SM_fa['SM_predicted_beta0'], color= 'gray', linewidth = 3, label = r'$\alpha$ (bare soil)')
K.plot(K_SM.index, K_SM['SM_predicted_beta0.01'], color= 'blue', linewidth = 2, label = 'biomass corrected')
#K.plot(K_SM_fa.index, K_SM_fa['SM_predicted_beta0'], color= 'gray', linewidth = 2, label = r'$\alpha_{^{40}K}$ corrected')
#K.plot(K_SM.index, K_SM['SM_predicted_beta0.01'], color= 'blue', linewidth = 2, label = r'$\alpha_{^{40}K}$ + biomass corrected')


K.axvspan (pd.to_datetime('2023-03-13 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2023-04-09 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
K.axvspan (pd.to_datetime('2023-04-10 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2023-07-26 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'darkgreen', fill=True, alpha=.3)
K.axvspan (pd.to_datetime('2023-07-27 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2023-08-20 00:00', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
K.axvspan (pd.to_datetime('2023-10-20 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2024-01-10 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
K.axvspan (pd.to_datetime('2024-05-24 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2024-07-01 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
K.axvspan (pd.to_datetime('2024-07-02 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2024-09-15 00:00', format = '%Y-%m-%d %H:%M'), 
         color= 'darkgreen', fill=True, alpha=.3)
K.legend(loc='lower center', fontsize=21, frameon=False,borderpad=0.2, ncol = 4)
K.set_xticks([])
K.set_ylim(0, 54)
K.set_ylabel("SM \n[vol.%]", fontsize=25)

# --------------------------------------------------
# 3. MIRA EGR
# --------------------------------------------------
M.plot(MIS_SM.index, MIS_SM['SM_ref'], color= 'black', linewidth = 2, label = "reference")
M.plot(MIS_SM.index, MIS_SM['SM_predicted_beta0'], color= 'red', linewidth = 2, label = "uncorrected")
M.plot(MIS_SM_fa.index, MIS_SM_fa['SM_predicted_beta0'], color= 'gray', linewidth = 3, label = r'$\alpha_{EGR}$ corrected')
M.plot(MIS_SM.index, MIS_SM['SM_predicted_beta0.01'], color= 'blue', linewidth = 2, label = 'biomass corrected')


M.axvspan (pd.to_datetime('2023-03-13 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2023-04-09 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
M.axvspan (pd.to_datetime('2023-04-10 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2023-07-26 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'darkgreen', fill=True, alpha=.3)
M.axvspan (pd.to_datetime('2023-07-27 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2023-08-20 00:00', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
M.axvspan (pd.to_datetime('2023-10-20 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2024-01-10 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
M.axvspan (pd.to_datetime('2024-05-24 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2024-07-01 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
M.axvspan (pd.to_datetime('2024-07-02 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2024-09-15 00:00', format = '%Y-%m-%d %H:%M'), 
         color= 'darkgreen', fill=True, alpha=.3)
#M.legend(loc='lower left', fontsize=24, frameon=False)
#M.legend(loc='lower center', fontsize=20, frameon=False,borderpad=0.2, ncol = 4)
M.set_xlabel("Date", fontsize=25)
M.set_ylim(0, 54)
M.set_ylabel("SM\n[vol.%]", fontsize=25)

# Common x-axis limits
start_date = pd.to_datetime('2023-02-05')
end_date = pd.to_datetime('2024-12-31')

for ax in [R, K, M]:
    ax.set_xlim(start_date, end_date)

# Tick size
for ax in [R, K, M]:
    ax.tick_params(axis='both', labelsize=15)
    
# add labels
props = dict(boxstyle='square', facecolor='gray', alpha=0.5, pad=.1)
R.text(prc.index.max()-pd.Timedelta('35Hours'), 9.5, 'a', fontsize=22, fontweight='bold', bbox=props, ha='right', c='k')
K.text(K_SM.index.max()-pd.Timedelta('35Hours'), 50.27, 'b', fontsize=22, fontweight='bold', bbox=props, ha='right', c='k')
M.text(MIS_SM.index.max()-pd.Timedelta('35Hours'), 50.27, 'c', fontsize=22, fontweight='bold', bbox=props, ha='right', c='k')


plt.savefig(r"D:\Data\Data_3rd_chapter\Figures\SM_series_visu_biomass_corr_adding_fixed_alpha_results.png",dpi=300,bbox_inches='tight')
plt.show()
