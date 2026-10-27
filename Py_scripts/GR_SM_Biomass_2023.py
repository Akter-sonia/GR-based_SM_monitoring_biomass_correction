# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 11:01:31 2026

@author: s.akter
"""

import pandas as pd # library for data management
import numpy as np
import matplotlib
import matplotlib.pyplot as plt #Library for plotting
import matplotlib.cm
import matplotlib.dates as mdates
from matplotlib import gridspec
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import glob
import scipy.signal as ss


## Importing biomass data
B = pd.read_excel(r"D:\Data\Data_3rd_chapter\Input_data\Biomass_CRNS_2023.xlsx", header = 0, parse_dates= [0], index_col=0)
B['FB (mm)'] = ss.medfilt(B['FB (mm)'], kernel_size=15)  ## removing the spikes using median filter
B['BWC (mm)'] = ss.medfilt(B['BWC (mm)'], kernel_size=15)
B.drop(B.columns[1:2], axis = 1, inplace = True)
##plotting
fig, ax = plt.subplots(figsize=(10, 7))
# Add x-axis and y-axis, to plot scatter plot use ax.scatter() command 
ax.plot (B.index, B['FB (mm)'])
ax.scatter (B.index, B['Biomass_measured'])
# Set title and labels for axes
ax.set_xlabel("Date", fontsize = 30)
ax.set_ylabel("FB (mm)", fontsize = 30)
plt.xticks(fontsize = 22)
plt.yticks(fontsize = 22)
plt.tight_layout()
plt.savefig("D:\Data\Data_3rd_chapter\Figures\Biomass_selhausen2023.png")
plt.show()


### Importing K-40 data for 2023
K_SM = pd.read_csv(r"D:\Data\Data_3rd_chapter\Input_data\K_ref_SM_2023.csv", header = 0, parse_dates= [0], index_col=0)
print(K_SM.index)
### Importing MIRA EGR data for 2023
MIS_SM = pd.read_csv(r"D:\Data\Data_3rd_chapter\Input_data\MIRA_EGR_ref_SM_2023.csv", header = 0, parse_dates= [0], index_col=0)


### Joining data
Data1 = pd.merge(K_SM, B, how = 'left', left_index = True, right_index = True )
Data2 = pd.merge(MIS_SM, B, how = 'left', left_index = True, right_index = True )



# save the file
Data1.to_csv("D:\Data\Data_3rd_chapter\Outputs\K_SM_Biomass_2023.csv", header=True, index = True)
Data2.to_csv("D:\Data\Data_3rd_chapter\Outputs\MIS_SM_Biomass_2023.csv", header=True, index = True)


