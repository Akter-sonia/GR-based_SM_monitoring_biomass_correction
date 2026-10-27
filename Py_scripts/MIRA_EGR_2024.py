# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 14:04:57 2026

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



### Importing MIRA sensor data for the Selhausen site
MIS = pd.read_csv(r"D:\Data\Data_3rd_chapter\Input_data\Selhausen_2024\MIRA_EGR.csv", header = 0, parse_dates= [0], index_col=0)
MIS.columns = ['Dose rate', 'Status','Detailed status']
print(MIS.head())
MIS.info()
print(MIS['Status'].unique())
print(MIS['Detailed status'].unique())
#MIS[MIS['Status'] == 'INVALID'] = np.nan
# MIS.loc[MIS['Status'] == 'INVALID', 'Dose rate'] = np.nan
MIS.drop(['Status', 'Detailed status'], axis=1, inplace=True)
print(MIS.index)
MIS.index = pd.to_datetime(MIS.index, utc= True, format= '%Y-%m-%dT%H:%M:%S.%f%z')
print(MIS.index)
MIS.describe()
MIS = MIS.sort_index()  # Dataframe is sorted in ascending order by date
# counting nan values
MIS.isnull().sum()

### Calculating hourly, daily and weekly average 
# defining function to calculate hourly mean when 50% data points are available 
def mean_when_3non_nan(x):
    non_nulls = x.notnull()
    if non_nulls.sum() > 2: # Among 6 datapoints, calculate mean when 3 datapoints are available
        return x[non_nulls].mean()
    return np.nan

MIS_hourly = MIS.resample('h').apply(mean_when_3non_nan)
MIS_daily = MIS_hourly.resample('D').mean()
MIS_weekly= MIS_daily.resample('W').mean()
MIS.describe()
MIS_hourly.describe()
MIS_daily.describe()
MIS_weekly.describe()   

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
plt.show()



# Plotting 10 min, hourly, daily and weekly average ambient gamma dose rate (EGR) with precipitation
# Create figure and plot space
fig, ax = plt.subplots(figsize=(25.5, 19.7), sharex=False, sharey=False, constrained_layout = True, dpi = 50) # No axis sharing
plt.axis('off')   # Turning the general axis off in order to create individual axis for each subplot
gs = gridspec.GridSpec(2, 1, height_ratios=[0.5, 1.2], wspace=0, hspace=0) # no of row 2, column 1 and no space bet. subplots
rain = plt.subplot(gs[0])
GR = plt.subplot(gs[1]) # add_subplot command adds each plot in fig 
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
rain.set_xlim('2024-02-02 00:00', '2024-12-30 00:20')
#rain.set_xlim([pd.to_datetime('2023-02-04 08:20', format = '%Y-%m-%d %H:%M:%S%z'),
             #pd.to_datetime('2024-07-02 07:20', format = '%Y-%m-%d %H:%M:%S%z')])
rain.set_xticks([])
rain.invert_yaxis()
# fig.add_subplot(111) works for arranging subgraphs within this graph.
GR.scatter(MIS.index, MIS['Dose rate'], label = "10 min data", marker='.', s = 70)
GR.scatter(MIS_hourly.index, MIS_hourly['Dose rate'], marker='.', color= 'green', s = 70, label = "Hourly average")
GR.plot(MIS_daily.index, MIS_daily['Dose rate'], color= 'red', label = "Daily average")
GR.plot(MIS_weekly.index, MIS_weekly['Dose rate'],color= 'black', label = "Weekly average", linewidth = 3)
# Setting axes's limit
#GR.set_xlim([pd.to_datetime('2023-02-04 07:00:00+00:00', format = '%Y-%m-%d %H:%M:%S%z'),
             #pd.to_datetime('2024-09-18 07:00:00+00:00', format = '%Y-%m-%d %H:%M:%S%z')])
GR.set_xlim('2024-02-02 00:00', '2024-12-30 00:00')
GR.set_ylim(65, 169)
# Set title and labels for axes
GR.set_xlabel('Date', fontsize=44)
GR.set_ylabel('$EGR_{G–M}$ intensity (nSv $\mathregular{h^{-1})}$', fontsize=44)
#plt.title('Gamma dose rate of GR3', fontsize=37)
GR.legend(loc='upper left', fontsize=38, frameon=False)
plt.tight_layout()
plt.savefig("D:\Data\Data_3rd_chapter\Figures\MIRA_EGR_raw.png")
plt.show()

# Joining MIS and precipitation dataframe
type(prc)
type(MIS)
print(prc.head())
print(MIS.head())
prc.info()
MIS.info()
MIS = MIS.groupby(MIS.index).first()
prc = prc.groupby(prc.index).first()  # filtering duplicate timestamp
#MIS = MIS.resample('30min').mean()
MIS_prc = pd.merge(MIS, prc, how = 'left', left_index = True, right_index = True )
print(MIS_prc)
MIS_prc.info()
MIS_prc.describe()
MIS_prc[MIS_prc['Precipitation'].isna()]   # calling the rows with nan


#Importing atmospheric pressure time series data
pr = pd.read_excel(r"D:\Data\Data_3rd_chapter\Input_data\Selhausen_2024\SE_EC_air_pressure.xlsx", header = 0, parse_dates= [0], index_col=0, na_values=['noData', '99999'])
pr.columns = ['Feature', 'Air pressure','Data quality']
print(pr.head())
pr.info()
print(pr.index)
pr.index = pd.to_datetime(pr.index, utc= True, format= '%Y-%m-%dT%H:%M:%S.%f%z')
print(pr.index)
print(pr['Data quality'].unique())  # Checking the quality of the data: Bad data when Quality = 4013
#pr['Air pressure'] = np.where(pr['Quality'] == "4_4013", np.nan, pr['Air pressure'])
#pr['Air pressure'] = np.where(pr['Air pressure'] > 1500, np.nan, pr['Air pressure'])
#pr['Air pressure'] = np.where(pr['Air pressure'] < 960, np.nan, pr['Air pressure'])
pr.drop(['Feature', 'Data quality'], axis = 1, inplace = True)
pr.describe()
# counting nan values
pr.isnull().sum()
##plotting
fig, ax = plt.subplots(figsize=(10, 7))
# Add x-axis and y-axis, to plot scatter plot use ax.scatter() command 
ax.plot (pr.index, pr['Air pressure'])
# Set title and labels for axes
ax.set_xlabel("Date", fontsize = 30)
ax.set_ylabel("Air pressure (kpa)", fontsize = 30)
#ax.set_title("GR1", fontsize = 35)
plt.xticks(fontsize = 22)
plt.yticks(fontsize = 22)
plt.tight_layout()
plt.savefig("D:\Data\Data_3rd_chapter\Figures\atmpressure_selhausen.png")
plt.show()

# Joining atmospheric pressure with Dose rate + precipitation data
pr = pr.groupby(pr.index).first()  # filtering duplicate timestamp
MIS_prc.info()
pr.info()
MIS_prc_pr = pd.merge(MIS_prc, pr, how = 'left', left_index = True, right_index = True )
print(MIS_prc_pr)
MIS_prc_pr.info()
MIS_prc_pr.describe()
MIS_metero = MIS_prc_pr

### Filtering rain effects
MIS_metero = MIS_metero.dropna(how='any')
# calculate a new column that contains the previous 3 hour precipitation sum
MIS_metero['Last 3h sum'] = MIS_metero['Precipitation'].rolling('3h', center=False, closed='both').sum()
# we need to round this number to some decimal points, otherwise we get error because of floating point precision problem
# details of this issues (https://randomascii.wordpress.com/2012/02/25/comparing-floating-point-numbers-2012-edition/)
# https://stackoverflow.com/questions/5595425/what-is-the-best-way-to-compare-floats-for-almost-equality-in-python
MIS_metero['Last 3h sum'] = MIS_metero['Last 3h sum'].round(decimals=5)
# now we add a corrected column based on the Last 3h sum column
MIS_metero['Corrected dose rate'] = np.where(MIS_metero['Last 3h sum'] > 0.0, np.nan, MIS_metero['Dose rate'])
MIS_metero.drop(['Last 3h sum'], axis=1, inplace=True)
print(MIS_metero.describe()) 

# save the result to a file
MIS_metero.to_csv("D:\Data\Data_3rd_chapter\Outputs\MIRA_EGR_after_rain_filter.csv", sep=";", header=True, index = True)


## Importing MIS data (after using rainfilter)
MIS_metero = pd.read_csv(r"D:\Data\Data_3rd_chapter\Outputs\MIRA_EGR_after_rain_filter.csv", sep=";", header = 0, parse_dates= [0], index_col=0)
print(MIS_metero.index)

MIS_metero_hourly = MIS_metero.resample('h').apply(mean_when_3non_nan)
MIS_metero_daily = MIS_metero_hourly.resample('D').mean()
MIS_metero_weekly= MIS_metero_daily.resample('W').mean()
MIS_metero['Corrected dose rate'].describe()
MIS_metero_hourly['Corrected dose rate'].describe()
MIS_metero_daily['Corrected dose rate'].describe()
MIS_metero_weekly['Corrected dose rate'].describe()  

# Plotting 10 min, hourly, daily and weekly average ambient gamma dose rate (EGR) after applying rain filter
# Create figure and plot space
fig, ax = plt.subplots(figsize=(25.5, 19.7), sharex=False, sharey=False, constrained_layout = True, dpi = 50) # No axis sharing
plt.axis('off')   # Turning the general axis off in order to create individual axis for each subplot
gs = gridspec.GridSpec(2, 1, height_ratios=[0.5, 1.2], wspace=0, hspace=0) # no of row 2, column 1 and no space bet. subplots
rain = plt.subplot(gs[0])
GR = plt.subplot(gs[1]) # add_subplot command adds each plot in fig 
# add_subplot(total no of row, total no of column, position of this subplot)
#plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)
matplotlib.rc('xtick', labelsize=23) # defining the xtick fontsize for all subplots
matplotlib.rc('ytick', labelsize=23)
#plt.tick_params(axis='both', which='major', labelsize=14) for one specific subplot
matplotlib.rcParams['xtick.major.pad']='13'
matplotlib.rcParams['ytick.major.pad']='13'

rain.bar (MIS_metero.index, MIS_metero['Precipitation'])
#rain.set_xlabel("Date", fontsize = 30)
rain.set_ylabel("Precipitation (mm)", fontsize = 44)
rain.set_ylim(0, 13)
#rain.set_xlim([pd.to_datetime('2023-02-04 08:24', format = '%Y-%m-%d %H:%M:%S.%f%z'),
             #pd.to_datetime('2024-01-02 07:20', format = '%Y-%m-%d %H:%M:%S.%f%z')])
rain.set_xlim('2024-02-02 00:00', '2024-12-30 00:00')
rain.set_xticks([])
rain.invert_yaxis()
# fig.add_subplot(111) works for arranging subgraphs within this graph.
GR.scatter(MIS_metero.index, MIS_metero['Corrected dose rate'], label = "10 min data", marker='.', s = 70)
GR.scatter(MIS_metero_hourly.index, MIS_metero_hourly['Corrected dose rate'], marker='.', color= 'green', s = 70, label = "Hourly average")
GR.plot(MIS_metero_daily.index, MIS_metero_daily['Corrected dose rate'], color= 'red', label = "Daily average", linewidth = 3)
GR.plot(MIS_metero_weekly.index, MIS_metero_weekly['Corrected dose rate'],color= 'black', label = "Weekly average", linewidth = 3)
# Setting axes's limit
#GR.set_xlim([pd.to_datetime('2023-02-04 08:24', format = '%Y-%m-%d %H:%M:%S.%f%z'),
             #pd.to_datetime('2024-01-02 07:20', format = '%Y-%m-%d %H:%M:%S.%f%z')])
GR.set_xlim('2024-02-02 00:00', '2024-12-30 00:00')
GR.set_ylim(65, 169)
# Set title and labels for axes
GR.set_xlabel('Date', fontsize=44)
GR.set_ylabel('$EGR_{G–M}$ intensity (nSv $\mathregular{h^{-1})}$', fontsize=44)
#plt.title('Gamma dose rate of GR3', fontsize=37)
GR.legend(loc='upper right', fontsize=38, frameon=False)

plt.tight_layout()
plt.savefig("D:\Data\Data_3rd_chapter\Figures\MIRA_EGR_after_rainfilter.png")
plt.show()


## Importing neutron count rate data from JUNG station
N = pd.read_csv(r"D:\Data\Data_3rd_chapter\Input_data\Selhausen_2024\Neutron_Jung.txt", sep=";", header=None, names=['Datetime', 'N count'])
print(N.head())
N.info()
N = N.set_index('Datetime')
print(N.index)
# converting index: from object to datetime format
N.index = pd.to_datetime(N.index, utc=True, format= '%Y-%m-%d %H:%M:%S')  
print(N.index)
N.describe()
#N['Incoming neutron'] = np.where(N['Incoming neutron'] < 130, np.nan, N['Incoming neutron'])
N = N.groupby(N.index).first()  # filtering duplicate timestamp
N_hourly = N.resample('h').apply(mean_when_3non_nan)
## Merging with the MIS_metero_hourly data
N_hourly.info()
MIS_metero_hourly.info()
MIS = pd.merge(MIS_metero_hourly, N_hourly, how = 'left', left_index = True, right_index = True )
print(MIS)
MIS.info()
MIS.describe()
#MIS.isnull().sum()
MIS = MIS.dropna(how='any')

### Calculating terrestrial dose rate
#MIS.loc[MIS.isna().any(1)] = np.nan
mu=32.7      # average muon equivalent dose
ne=8         # average neutron equivalent dose
Pref=1013.25 # referece atmosphere pressure in kpa. 1013.25 hpa
Navg=147.45  # average incoming neutron count: MIS['N count'].mean()

MIS['Terrestrial dose rate'] = MIS['Corrected dose rate'] - ((mu - 0.051 * (MIS['Air pressure'] - Pref)) * (
    1 + 0.52 * ((MIS['N count'] - Navg)/Navg))) - ((ne - 0.076 *(MIS['Air pressure'] - Pref)) * (
        1 + ((MIS['N count'] - Navg)/Navg)))
        
MIS['Corrected EGR for short-term SCR variability'] = MIS['Terrestrial dose rate'] + 40.7       
#The long-term SCR contribution, mu+ne = 32.7 + 8 = 40.7, is not considered here.
#Only short-term variability due to pressure and incoming neutron is considered.        
#MIS['Alternate SCR cor'] = 40.7 + (- (MIS['Air pressure'] - Pref) * (0.051 * (1 + 0.52 * ((MIS['N count'] - Navg)/Navg)) + 0.076 * (1 + ((MIS['N count'] - Navg)/Navg))))
#MIS['Alternate TGR'] = MIS['Corrected dose rate'] - MIS['Alternate SCR cor']   
#Why the small difference? The original equation applies:
#Different correction magnitudes to different baselines (the coefficients 0.051 and 0.076 are distinct).
#The compact version applies:
#A single combined correction to the summed baseline.
MIS['Corrected EGR for short-term SCR variability'] = np.where(MIS['Corrected dose rate'].isna(), np.nan, MIS['Corrected EGR for short-term SCR variability'])

# save the file
MIS.to_csv("D:\Data\Data_3rd_chapter\Outputs\MIS_EGR_processed.csv", header=True, index = True)



# Importing processed EGR data
MIS = pd.read_csv(r"D:\Data\Data_3rd_chapter\Outputs\MIS_EGR_processed.csv", header = 0, parse_dates= [0], index_col=0)
print(MIS.index)
# Daily TDR
MIS['Corrected dose rate'].describe()
MIS_daily = MIS.resample('D').mean()
MIS_weekly = MIS_daily.resample('W').mean()
MIS_daily['Corrected dose rate'].describe()
MIS_weekly['Corrected dose rate'].describe()
#MIS = MIS.dropna(how='any')  # For plotting, do not run this command. Run only to check the correlation
#MIS_daily = MIS_daily.dropna(how='any')
#MIS_weekly = MIS_weekly.dropna(how='any')
print(MIS_daily[['Corrected dose rate', 'Air pressure']].corr(method='pearson')) 
print(MIS_daily[['Corrected EGR for short-term SCR variability', 'Air pressure']].corr(method='pearson'))



## Plotting environmental dose rate and environmental dose rate corrected for short-term SCR
plt.rcParams["font.family"] = "Times New Roman"
fig = plt.figure(figsize=(18, 12), dpi = 300)
ax1 = fig.add_subplot(111)
# fig.add_subplot(111) works for arranging subgraphs within this graph.
ax1.plot(MIS_daily.index, MIS_daily['Corrected dose rate'], color= 'black', label = "EGR", linewidth = 2.5)
ax1.plot(MIS_daily.index, MIS_daily['Corrected EGR for short-term SCR variability'], color= 'red', label = "EGR'", linewidth = 2.5)
ax1.set_xlabel('Date', fontsize=43)
ax1.set_ylabel('GR intensity (nSv $\mathregular{h^{-1})}$', fontsize=43)
# Setting axes's limit
ax1.set_xlim('2024-02-02 00:00', '2024-12-30 00:00')
ax1.set_ylim(85, 106)
# Set title and labels for axes
ax1.legend(loc='upper left', fontsize=38, frameon=False)
#plt.title('Gamma dose rate of GR1', fontsize=37)
plt.xticks(fontsize=29)
plt.yticks(fontsize=29)
plt.tight_layout()
plt.savefig("D:\Data\Data_3rd_chapter\Figures\MIRA_EGR_EGR'.png")
plt.show()



