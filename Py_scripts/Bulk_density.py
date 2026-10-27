# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 15:46:03 2026

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





### Importing bulk density measurements for CRNS calibration for the year of 2023
bd_23 = pd.read_csv(r"D:\Data\Data_3rd_chapter\Input_data\Calibration_CRNS_BD_2023.csv", header = 0, parse_dates= [0], index_col=0)
#bd_5 = bd_23.loc[bd_23['Profile_Depth_cm'] == 2.5, 'DryBulkDensity_g_cm3'].mean() ## for individual depth 
#bd_10 = bd_23.loc[bd_23['Profile_Depth_cm'] == 7.5, 'DryBulkDensity_g_cm3'].mean()
#bd_15 = bd_23.loc[bd_23['Profile_Depth_cm'] == 12.5, 'DryBulkDensity_g_cm3'].mean()

mean_bd_23 = (
    bd_23.groupby('Profile_Depth_cm')['DryBulkDensity_g_cm3']
      .mean()
      .reset_index(name='mean_bulk_density')
)

print(mean_bd_23)
## saving the output
mean_bd_23.to_csv("D:\Data\Data_3rd_chapter\Outputs\mean_bd_23.csv")


### Importing bulk density measurements for CRNS calibration for the year of 2024
bd_24 = pd.read_csv(r"D:\Data\Data_3rd_chapter\Input_data\Calibration_CRNS_BD_2024.csv", header = 0, parse_dates= [0], index_col=0)
#bd_5 = bd_24.loc[bd_24['Depth [cm]'] == 2.5, 'Bulk Density [g/cm3]'].mean()  # for individual depth
#bd_10 = bd_24.loc[bd_24['Depth [cm]'] == 7.5, 'Bulk Density [g/cm3]'].mean()

mean_bd_24 = (
    bd_24.groupby('Depth [cm]')['Bulk Density [g/cm3]']
      .mean()
      .reset_index(name='mean_bulk_density')
)

print(mean_bd_24)
## saving the output
mean_bd_24.to_csv("D:\Data\Data_3rd_chapter\Outputs\mean_bd_24.csv")
