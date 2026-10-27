# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 15:19:35 2026

@author: s.akter
"""

# write "%matplotlib qt" command in console panal to get interactive plot
# then run the command for plotting
import matplotlib
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


#### Importing daily GR data
# Importing SARA K-40 Selhausen data for the year of 2023 and 2024
K = pd.read_csv(r"D:\Data\Data_3rd_chapter\Outputs\K_SM_2023_2024.csv", header = 0, parse_dates= [0], index_col=0)

# Importing MIRA Selhausen data for the year of 2023 and 2024
MIS = pd.read_csv(r"D:\Data\Data_3rd_chapter\Outputs\MIS_SM_2023_2024.csv", header = 0, parse_dates= [0], index_col=0)
print(MIS.index)
# drop unnecessary columns
MIS = MIS.drop(MIS.columns[1:13], axis=1)
MIS.rename(columns={"Corrected EGR for short-term SCR variability": "EGR"}, inplace=True)

#Joining with K-40 data
Data = pd.merge(K, MIS, how = 'left', left_index = True, right_index = True )
Data = Data.drop(Data.columns[1:5], axis=1)
# Merging the data with an independent time index which has all timestamp from the start to end period 
# Creating a dataframe with customized date time index
time_index = pd.date_range(start ='2023/02/05 00:00:00', end ='2024/12/31 00:00:00', freq ='D')
print(time_index)
df = pd.DataFrame(time_index, columns =['date']) # Creating a dataframe, making the time index a column named as date
df['data'] = np.random.randint(0, 100, size =(len(time_index)))  # Creating a new column with random numbers 
df['datetime'] = pd.to_datetime(df['date'], utc=True, format= '%Y-%m-%dT%H:%M:%S.%f%z')
df = df.set_index('datetime')
df.drop(['date'], axis = 1, inplace = True)
# Merging data with the customized datetime index data to avoid joining line when there is no data
Data = pd.merge(df, Data, how = 'left', left_index = True, right_index = True )
Data.drop(['data'], axis = 1, inplace = True)
Data.iloc[:, 5:9] = Data.iloc[:, 5:9].replace(0, np.nan)  ## to improve visualization
# save the GR data
#Data.to_csv("D:\Data\Data_3rd_chapter\Outputs\GR_time_series.csv", header=True, index = True)



# Importing precipitation data
#2024
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
prc = prc['2024/02/01 00:00:00':'2024/12/31 00:00:00']


#2023
# Importing precipitation data
prc1 = pd.read_excel(r"D:\Data\Data_2nd_paper\Raw_data_2nd_paper\SE_BDK_precp_nearby_field.xlsx",  header=None, parse_dates= [0], index_col=0, na_values=['noData', '99999'])
prc1.columns = ['Feature', 'Precipitation','Data quality']
print(prc1.head())
prc1.info()
print(prc1.index)
prc1.index = pd.to_datetime(prc1.index, utc= True, format= '%Y-%m-%dT%H:%M:%S.%f%z')
print(prc1['Data quality'].unique())
prc1.drop(['Feature', 'Data quality'], axis=1, inplace=True)
prc1["Precipitation"] = prc1["Precipitation"].round(decimals=5)
prc1 = prc1['2023/02/05 00:00:00':'2024/01/31 00:00:00']

## Stacking the 2023 data with the 2024 data
df = pd.concat([prc1, prc], axis=0)
print(df)



### Plotting
end_date = Data.index.max()

plt.rcParams["font.family"] = "Calibri"
fig = plt.subplots(figsize=(22, 16), sharex=False, sharey=False, constrained_layout = True, dpi=350) # No axis sharing
plt.axis('off')   # Turning the general axis off in order to create individual axis for each subplot
gs = gridspec.GridSpec(5, 1, height_ratios=[0.8, 1, 1, 1, 1.2], wspace=0, hspace=0)

R = plt.subplot(gs[0])
W = plt.subplot(gs[1])
K = plt.subplot(gs[2])
M = plt.subplot(gs[3])
B = plt.subplot(gs[4])

# add_subplot(total no of row, total no of column, position of this subplot)
#plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)
matplotlib.rc('xtick', labelsize=20) # defining the xtick fontsize for all subplots
matplotlib.rc('ytick', labelsize=20)
#plt.tick_params(axis='both', which='major', labelsize=14) for one specific subplot
matplotlib.rcParams['xtick.major.pad']='18'
matplotlib.rcParams['ytick.major.pad']='18'

R.plot(df.index, df['Precipitation'], color= 'black', linewidth = 2)
R.set_xlim([pd.to_datetime('2023-02-05 00:00', format = '%Y-%m-%d %H:%M'),
             pd.to_datetime('2024-12-31 00:00', format = '%Y-%m-%d %H:%M')])
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
R.set_ylim(0, 8)
R.set_ylabel("Precipitation\n[mm]", fontsize = 34)
R.set_xticks([])

W.plot(Data.index, Data['SM_av_dw'], color= 'black', linewidth = 2)
W.set_xlim([pd.to_datetime('2023-02-05 00:00', format = '%Y-%m-%d %H:%M'),
             pd.to_datetime('2024-12-31 00:00', format = '%Y-%m-%d %H:%M')])
W.axvspan (pd.to_datetime('2023-03-13 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2023-04-09 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
W.axvspan (pd.to_datetime('2023-04-10 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2023-07-26 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'darkgreen', fill=True, alpha=.3)
W.axvspan (pd.to_datetime('2023-07-27 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2023-08-20 00:00', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
W.axvspan (pd.to_datetime('2023-10-20 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2024-01-10 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
W.axvspan (pd.to_datetime('2024-05-24 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2024-07-01 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
W.axvspan (pd.to_datetime('2024-07-02 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2024-09-15 00:00', format = '%Y-%m-%d %H:%M'), 
         color= 'darkgreen', fill=True, alpha=.3)
W.set_ylim(10, 45)
W.set_ylabel("Ref SM\n[vol%]", fontsize = 34)
W.set_xticks([])

K.plot(Data.index, Data['K'], color= 'black', linewidth = 2)
# Setting axes's limit
K.set_xlim([pd.to_datetime('2023-02-05 00:00', format = '%Y-%m-%d %H:%M'),
             pd.to_datetime('2024-12-31 00:00', format = '%Y-%m-%d %H:%M')])
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
K.set_xticks([])
K.set_ylim(9.01, 12.5)
K.set_ylabel("$^{40}$K GR\n[nSv $\mathregular{h^{-1}]}$", fontsize = 34)


M.plot(Data.index, Data['EGR'], color= 'black', label = "MIRA", linewidth = 2)
# Setting axes's limit
M.set_xlim([pd.to_datetime('2023-02-05 00:00', format = '%Y-%m-%d %H:%M'),
             pd.to_datetime('2024-12-31 00:00', format = '%Y-%m-%d %H:%M')])
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
M.set_xticks([])
M.set_ylabel("EGR\n[nSv $\mathregular{h^{-1}]}$", fontsize = 34)


B.plot(Data.index, Data['FB_AG (mm)'], color= 'green', label = r'AGB$_{\mathrm{fresh}}$', linewidth = 3) 
B.plot(Data.index, Data['FB_BG (mm)'], color= 'green', label = r'BGB$_{\mathrm{fresh}}$', linewidth = 3, linestyle = 'dashed')
B.plot(Data.index, Data['BWC_AG (mm)'], color= 'blue', label = r'AGB$_{\mathrm{WC}}$', linewidth = 3, linestyle = 'dashdot')
B.plot(Data.index, Data['BWC_BG (mm)'], color= 'blue', label = r'BGB$_{\mathrm{WC}}$', linewidth = 3, linestyle = 'dotted')
B.set_xlabel('Date', fontsize=40)
B.set_ylim(0, 14)
B.legend(ncol=2, loc='lower center', fontsize=30, frameon=False)
B.set_ylabel("Biomass\n[kg $\mathregular{m^{-2}]}$", fontsize = 34)
B.set_xlim([pd.to_datetime('2023-02-05 00:00', format = '%Y-%m-%d %H:%M'),
             pd.to_datetime('2024-12-31 00:00', format = '%Y-%m-%d %H:%M')])
B.axvspan (pd.to_datetime('2023-03-13 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2023-04-09 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
B.axvspan (pd.to_datetime('2023-04-10 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2023-07-26 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'darkgreen', fill=True, alpha=.3)
B.axvspan (pd.to_datetime('2023-07-27 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2023-08-20 00:00', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
B.axvspan (pd.to_datetime('2023-10-20 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2024-01-10 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
B.axvspan (pd.to_datetime('2024-05-24 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2024-07-01 23:59', format = '%Y-%m-%d %H:%M'), 
         color= 'limegreen', fill=True, alpha=.3)
B.axvspan (pd.to_datetime('2024-07-02 00:00', format = '%Y-%m-%d %H:%M'), pd.to_datetime('2024-09-15 00:00', format = '%Y-%m-%d %H:%M'), 
         color= 'darkgreen', fill=True, alpha=.3)
B.text('2023-04-13 00:00', 11.5, 'Winter wheat', fontsize = 32, color = 'black')
B.text('2023-10-22 00:00', 11.5, 'Catch crop', fontsize = 32, color = 'black')
B.text('2024-06-10 00:00', 11.5, 'Sugar beet', fontsize = 32, color = 'black')



# add labels
props = dict(boxstyle='square', facecolor='gray', alpha=0.5, pad=.1)
R.text(Data.index.max()-pd.Timedelta('35Hours'), 6.71, 'a', fontsize=30, fontweight='bold', bbox=props, ha='right', c='k')
W.text(Data.index.max()-pd.Timedelta('35Hours'), 40.3, 'b', fontsize=30, fontweight='bold', bbox=props, ha='right', c='k')
K.text(Data.index.max()-pd.Timedelta('35Hours'), 12.04, 'c', fontsize=30, fontweight='bold', bbox=props, ha='right', c='k')
M.text(Data.index.max()-pd.Timedelta('35Hours'), 98.1, 'd', fontsize=30, fontweight='bold', bbox=props, ha='right', c='k')
B.text(Data.index.max()-pd.Timedelta('35Hours'), 12.495, 'e', fontsize=30, fontweight='bold', bbox=props, ha='right', c='k')

plt.savefig(r"D:\Data\Data_3rd_chapter\Figures\Time_series.png")
plt.show()
