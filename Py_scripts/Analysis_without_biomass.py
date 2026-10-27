# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 13:52:34 2026

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




### SM prediction for diff depths without biomass period for K-40
### Importing corrected K_SM data without biomass period for 2023 and 2024
K_SM = pd.read_csv(r"D:\Data\Data_3rd_paper_cleaned\Outputs\K_SM_2023_2024_without_high_biomass.csv", header = 0, parse_dates= [0], index_col=0)
# Dropping unnecessary columns
K_SM = K_SM.drop(K_SM.columns[9:14], axis=1)
# curve fitting
K_SM = K_SM.dropna(how='any')
x =K_SM['SM_av_dw'].values
y =K_SM['K'].values

##  K-40 GR Prediction based on theoritically derived physics based equation
K_SM['K_predicted'] = (14.66 / (1 + 1.92 * ((K_SM['SM_av_dw']/100)/1.38)))         ## for 0-25 cm depth
#x =MIS_SM['SM_av_dw'].values
z =K_SM['K_predicted'].values

# Import curve fitting package from scipy
from scipy.optimize import curve_fit
# Function to calculate the linear fit with constants a and b
def lin(x, a, b):
    return a+b*x
pars, cov = curve_fit(f=lin, xdata=x, ydata=z, p0=[0, 0], bounds=(-np.inf, np.inf))

## Ref vs pred
K_SM['SM_predicted'] = ((1.38*(14.66-K_SM['K']))/(1.92*K_SM['K']))*100   ## for 0-25 cm depth



## Plotting
fig, (a, b) = plt.subplots(1, 2, figsize=(15.5, 6.2), dpi=250)
# Set font
plt.rcParams['font.family'] = 'Calibri'

# Calibration
a.scatter(K_SM['SM_av_dw'], K_SM['K'], s=90, color='black')
a.plot(x, lin(x, *pars), linewidth=5, linestyle='solid')
a.text(34, 11.7, r'$\alpha_{40K}$ = 1.92', fontsize=24)
a.text(34, 11.4, r'$R^2$ = 0.68', fontsize=24)
a.text(34, 11.15, r'RMSE = 0.32', fontsize=24)
a.set_title('Calibration', fontsize=34)
a.set_xlabel('Reference SM [vol. %]', fontsize=30)
a.set_ylabel('$^{40}$K GR intensity [nSv $\mathregular{h^{-1}]}$', fontsize=30)
a.set_xlim(5, 55)
a.tick_params(axis='both', labelsize=20)
a.grid(True, linestyle='--', linewidth=0.8, alpha=0.8)

# Prediction
b.scatter(K_SM['SM_av_dw'], K_SM['SM_predicted'], s=90, color='black')
# 1:1 line
b.plot([0, 55], [0, 55], linewidth=5, color = 'black', linestyle='dashed')
b.text(3, 49.5, r'$R^2$ = 0.69', fontsize=24)
b.text(3, 44.8, r'RMSE = 3.19', fontsize=24)
b.text(47, 44, '1:1', fontsize=24)
b.set_title('Prediction', fontsize=34)
b.set_xlabel('Reference SM [vol. %]', fontsize=30)
b.set_ylabel('Predicted SM [vol. %]', fontsize=30)
b.set_xlim(0, 55)
b.set_ylim(0, 55)
b.tick_params(axis='both', labelsize=20)
b.grid(True, linestyle='--', linewidth=0.8, alpha=0.8)

# Adjust layout
plt.subplots_adjust(wspace=0.25)

# Save figure
plt.savefig("D:\Data\Data_3rd_paper_cleaned\Analysis_without_high_biomass\Figures\K_SM_no_biomass.png")
plt.show()





### SM prediction for diff depths without biomass period for MIRA_EGR
### Importing corrected MIS_SM data without biomass period for 2023 and 2024
MIS_SM = pd.read_csv(r"D:\Data\Data_3rd_paper_cleaned\Outputs\MIS_SM_2023_2024_without_high_biomass.csv", header = 0, parse_dates= [0], index_col=0)
MIS_SM.rename(columns={"Corrected EGR for short-term SCR variability": "Corrected EGR"}, inplace=True)
# Dropping unnecessary columns
MIS_SM = MIS_SM.drop(MIS_SM.columns[9:14], axis=1)
# curve fitting
MIS_SM = MIS_SM.dropna(how='any')
x =MIS_SM['SM_av_dw'].values
y =MIS_SM['Corrected EGR'].values

##  EGR Prediction based on theoritically derived physics based equation
MIS_SM['EGR_predicted'] = (106.13 / (1 + 0.68 * ((MIS_SM['SM_av_dw']/100)/1.38)))         ## for 0-25 cm depth

z =MIS_SM['EGR_predicted'].values

# Import curve fitting package from scipy
from scipy.optimize import curve_fit
# Function to calculate the linear fit with constants a and b
def lin(x, a, b):
    return a+b*x
pars, cov = curve_fit(f=lin, xdata=x, ydata=z, p0=[0, 0], bounds=(-np.inf, np.inf))

## Ref vs pred
MIS_SM['SM_predicted'] = ((1.38*(106.13-MIS_SM['Corrected EGR']))/(0.68*MIS_SM['Corrected EGR']))*100   ## for 0-25 cm depth



## Plotting
fig, (a, b) = plt.subplots(1, 2, figsize=(15.5, 6.2), dpi=250)
# Set font
plt.rcParams['font.family'] = 'Calibri'

# Calibration
a.scatter(MIS_SM['SM_av_dw'], MIS_SM['Corrected EGR'], s=90, color='black')
a.plot(x, lin(x, *pars), linewidth=5, linestyle='solid')
a.text(34, 98.8, r'$\alpha_{EGR}$ = 0.68', fontsize=24)
a.text(34, 97.25, '$R^2$ = 0.61', fontsize=24)
a.text(34, 96.05, 'RMSE = 1.46', fontsize=24)
a.set_title('Calibration', fontsize=34)
a.set_xlabel('Reference SM [vol. %]', fontsize=30)
a.set_ylabel('EGR intensity [nSv $\mathregular{h^{-1}]}$', fontsize=30)
a.set_xlim(5, 55)
a.tick_params(axis='both', labelsize=20)
a.grid(True, linestyle='--', linewidth=0.8, alpha=0.8)

# Prediction
b.scatter(MIS_SM['SM_av_dw'], MIS_SM['SM_predicted'], s=90, color='black')
# 1:1 line
b.plot([0, 55], [0, 55], linewidth=5, color = 'black', linestyle='dashed')
b.text(3, 49.5, r'$R^2$ = 0.63', fontsize=24)
b.text(3, 44.8, r'RMSE = 3.75', fontsize=24)
b.text(47, 44, '1:1', fontsize=24)
b.set_title('Prediction', fontsize=34)
b.set_xlabel('Reference SM [vol. %]', fontsize=30)
b.set_ylabel('Predicted SM [vol. %]', fontsize=30)
b.set_xlim(0, 55)
b.set_ylim(0, 55)
b.tick_params(axis='both', labelsize=20)
b.grid(True, linestyle='--', linewidth=0.8, alpha=0.8)

# Adjust layout
plt.subplots_adjust(wspace=0.25)

# Save figure
plt.savefig("D:\Data\Data_3rd_paper_cleaned\Analysis_without_high_biomass\Figures\MIS_SM_no_biomass.png")
plt.show()




