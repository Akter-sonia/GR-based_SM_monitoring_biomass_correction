# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 11:40:05 2026

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


#### Importing SARA K40 2024 data
# Importing SARA K-40 data for the Selhausen
K_SM_24 = pd.read_csv(r"D:\Data\Data_3rd_chapter\Outputs\K_ref_SM_Biomass.csv", header = 0, parse_dates= [0], index_col=0)

### Importing K_SM 2023 data
K_SM_23 = pd.read_csv(r"D:\Data\Data_3rd_chapter\Outputs\K_SM_Biomass_2023.csv", header = 0, parse_dates= [0], index_col=0)
K_SM_23.drop(['Precipitation', 'Biomass_measured'], axis = 1, inplace = True)
K_SM_23 = K_SM_23['2023/02/05 00:00:00':'2024/01/31 00:00:00']
K_SM_23.rename(columns={"SM_0cm": "SM_2cm", "FB (mm)": "FB_AG (mm)", "BWC (mm)": "BWC_AG (mm)"}, inplace=True)

## Stacking the 2023 data with the 2024 data
df = pd.concat([K_SM_23, K_SM_24], axis=0)
print(df)

## replacing NaN values in the biomass column with 0
df["FB_AG (mm)"] = df["FB_AG (mm)"].fillna(0)

## eleminating the high biomass period
df_without_high_biomass = df[df["FB_AG (mm)"] <= 1.4]

## saving the output
df.to_csv("D:\Data\Data_3rd_chapter\Outputs\K_SM_2023_2024.csv")
df_without_high_biomass.to_csv("D:\Data\Data_3rd_chapter\Outputs\K_SM_2023_2024_without_high_biomass.csv")





## Importing MIRA EGR data
# MIRA 2024 data
MIS_SM_24 = pd.read_csv(r"D:\Data\Data_3rd_chapter\Outputs\MIRA_EGR_ref_SM_Biomass.csv", header = 0, parse_dates= [0], index_col=0)
MIS_SM_24 = MIS_SM_24.drop(MIS_SM_24.columns[0:6], axis=1)
## Creating a new column SM_0to7.5cm and insert it in the dataframe after "SM_av_dw" column to make it identical to the 2023 dataframe  
SM_0to75 = ((MIS_SM_24['SM_2cm']*3.5)+ (MIS_SM_24['SM_5cm']*4))/7.5
MIS_SM_24.insert(
    MIS_SM_24.columns.get_loc("SM_av_dw") + 1,
    "SM_0to7.5cm",
    SM_0to75
)
SM_0to15 = ((MIS_SM_24['SM_2cm']*3.5)+ (MIS_SM_24['SM_5cm']*4)+ (MIS_SM_24['SM_10cm']*7.5))/15
MIS_SM_24.insert(
    MIS_SM_24.columns.get_loc("SM_0to7.5cm") + 1,
    "SM_0to15cm",
    SM_0to15
)

### Importing MIS_SM 2023 data
MIS_SM_23 = pd.read_csv(r"D:\Data\Data_3rd_chapter\Outputs\MIS_SM_Biomass_2023.csv", header = 0, parse_dates= [0], index_col=0)
MIS_SM_23 = MIS_SM_23['2023/02/05 00:00:00':'2024/01/31 00:00:00']
MIS_SM_23.drop(['Biomass_measured'], axis = 1, inplace = True)
MIS_SM_23.rename(columns={"SM_0cm": "SM_2cm", "FB (mm)": "FB_AG (mm)", "BWC (mm)": "BWC_AG (mm)"}, inplace=True)

## Stacking the 2023 data with the 2024 data
df1 = pd.concat([MIS_SM_23, MIS_SM_24], axis=0)
print(df1)

## replacing NaN values in the biomass column with 0
df1["FB_AG (mm)"] = df1["FB_AG (mm)"].fillna(0)

## eleminating the high biomass period
df1_without_high_biomass = df1[df1["FB_AG (mm)"] <= 1.4]

## saving the output
df1.to_csv("D:\Data\Data_3rd_chapter\Outputs\MIS_SM_2023_2024.csv")
df1_without_high_biomass.to_csv("D:\Data\Data_3rd_chapter\Outputs\MIS_SM_2023_2024_without_high_biomass.csv")


