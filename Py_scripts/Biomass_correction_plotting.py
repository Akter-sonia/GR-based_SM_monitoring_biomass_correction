# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 14:55:47 2026

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
from matplotlib.ticker import MultipleLocator



### Biomass correction plotting for K-40
### Importing K-40 data for 2023
K_23 = pd.read_csv(r"D:\Data\Data_3rd_chapter\Outputs\K_SM_Biomass_2023.csv", header = 0, parse_dates= [0], index_col=0)
K_23 = K_23.drop(K_23.columns[np.r_[1:6,7,8, 10]], axis=1) 
K_23['FB (mm)'] = K_23['FB (mm)'].fillna(0)

## Correcting K for beta = 0.01
K_23['Corrected K']= K_23['K']/(1-0.01* K_23['FB (mm)'])

# curve fitting
#K_23 = K_23.dropna(how='any')
x23 =K_23['SM_av_dw'].values
y23 =K_23['K'].values
y232 =K_23['Corrected K'].values

##  K-40 GR Prediction based on theoritically derived physics based equation
K_23['K_predicted1'] = (13.33 / (1 + 1.49 * ((K_23['SM_av_dw']/100)/1.39)))      ## Beta = 0
K_23['K_predicted2'] = (14.25 / (1 + 1.83 * ((K_23['SM_av_dw']/100)/1.39)))      ## Beta = 0.01


z23 =K_23['K_predicted1'].values
z232 =K_23['K_predicted2'].values


# Import curve fitting package from scipy
from scipy.optimize import curve_fit
# Function to calculate the linear fit with constants a and b
def lin(x, a, b):
    return a+b*x
pars23, cov = curve_fit(f=lin, xdata=x23, ydata=z23, p0=[0, 0], bounds=(-np.inf, np.inf))
pars232, cov = curve_fit(f=lin, xdata=x23, ydata=z232, p0=[0, 0], bounds=(-np.inf, np.inf))

## Ref vs pred
K_23['SM_predicted1'] = ((1.39*(13.33-K_23['K']))/(1.49*K_23['K']))*100   ## Beta = 0
K_23['SM_predicted2'] = ((1.39*(14.25-K_23['Corrected K']))/(1.83*K_23['Corrected K']))*100   ## Beta = 0.01


### Importing K-40 data for 2024
K_24 = pd.read_csv(r"D:\Data\Data_3rd_chapter\Outputs\K_ref_SM_Biomass.csv", header = 0, parse_dates= [0], index_col=0)
K_24 = K_24.drop(K_24.columns[np.r_[1:5,7,8,10:13]], axis=1) 
K_24['FB_AG (mm)'] = K_24['FB_AG (mm)'].fillna(0)

## Correcting K for beta = 0.01
K_24['Corrected K']= K_24['K']/(1-0.01* K_24['FB_AG (mm)'])

# curve fitting
K_24 = K_24.dropna(how='any')
x24 =K_24['SM_av_dw'].values
y24 =K_24['K'].values
y242 =K_24['Corrected K'].values

##  K-40 GR Prediction based on theoritically derived physics based equation
K_24['K_predicted1'] = (12.75 / (1 + 1.04 * ((K_24['SM_av_dw']/100)/1.36)))      ## Beta = 0
K_24['K_predicted2'] = (15.44 / (1 + 2.08 * ((K_24['SM_av_dw']/100)/1.36)))      ## Beta = 0.01


z24 =K_24['K_predicted1'].values
z242 =K_24['K_predicted2'].values


# Import curve fitting package from scipy
from scipy.optimize import curve_fit
# Function to calculate the linear fit with constants a and b
def lin(x, a, b):
    return a+b*x
pars24, cov = curve_fit(f=lin, xdata=x24, ydata=z24, p0=[0, 0], bounds=(-np.inf, np.inf))
pars242, cov = curve_fit(f=lin, xdata=x24, ydata=z242, p0=[0, 0], bounds=(-np.inf, np.inf))

## Ref vs pred
K_24['SM_predicted1'] = ((1.36*(12.75-K_24['K']))/(1.04*K_24['K']))*100   ## Beta = 0
K_24['SM_predicted2'] = ((1.36*(15.44-K_24['Corrected K']))/(2.08*K_24['Corrected K']))*100   ## Beta = 0.01


### Coloring based on the period when fresh biomass was high
w1 = K_23['2023-04-10':'2023-07-26']  ## period with high fresh biomass, FB > 1.7 kg/m2
w2 = K_23['2023-07-27':'2023-08-20']  ## period with low biomass, FB < 1.7 kg/m2
w3 = K_24['2024-05-24':'2024-07-01']  ## period with low biomass, FB < 1.7 kg/m2
w4 = K_24['2024-07-02':'2024-09-15']  ## period with high biomass, FB > 1.7 kg/m2
w5 = K_23['2023-03-13':'2023-04-09']  ## period with low biomass, FB < 1.7 kg/m2


## Plotting
p1 = (70,70)
p2 = (0,0)
from matplotlib.gridspec import GridSpec
plt.rcParams["font.family"] = "Calibri"
fig = plt.figure(figsize=(25, 13.4), dpi=300)
gs = GridSpec(2, 5, figure=fig, width_ratios=[1, 1, 0, 1, 1], wspace=0.19, hspace=0.22)  # middle column 0 controls crop gap

# Adjust outer margins
gs.update(left=0.055, right=0.99, top=0.88, bottom=0.1)

# Subplots
a = fig.add_subplot(gs[0,0])
b = fig.add_subplot(gs[0,1])
c = fig.add_subplot(gs[0,3])
d = fig.add_subplot(gs[0,4])
e = fig.add_subplot(gs[1,0])
f = fig.add_subplot(gs[1,1])
g = fig.add_subplot(gs[1,3])
h = fig.add_subplot(gs[1,4])

# Column titles
fig.text(0.27, 0.97, 'Winter wheat', ha='center', va='center',fontsize=50)
fig.text(0.76, 0.97, 'Sugar beet', ha='center', va='center',fontsize=50)

# Tick sizes
plt.rc('xtick', labelsize=25)
plt.rc('ytick', labelsize=25)

## Calibration models, first row
##Biomass uncorrected 2023
a.scatter(K_23['SM_av_dw'], K_23['K'], s=100, color='black')
a.scatter(w2['SM_av_dw'], w2['K'], s=100, label = "low biomass", color='limegreen')
a.scatter(w1['SM_av_dw'], w1['K'], s=100, label = "high biomass", color='darkgreen')
a.scatter(w5['SM_av_dw'], w5['K'], s=100, color='limegreen')
a.plot(x23, lin(x23, *pars23), linewidth = 5, linestyle = 'solid', color='black')
a.text(40, 12.2, r'$\alpha_{^{40}K}$= 1.49', fontsize = 30, color = 'black') 
a.text(40, 11.82, '$R^2$ = 0.85', fontsize = 30, color = 'black')
a.text(40, 11.47, 'RMSE = 0.30', fontsize = 30, color = 'black')
a.text(7.5, 9.0, 'Calibration', fontsize = 38, color = 'black')
a.set_xlim(5, 67)
a.set_title("Uncorrected", fontsize = 43)
a.set_ylim(8.85, 12.6)
#a.set_xlabel("Reference SM [vol. %]", fontsize = 30)
a.set_ylabel("$^{40}$K GR [nSv $\mathregular{h^{-1}]}$", fontsize = 40)

##Biomass corrected 2023
b.scatter(K_23['SM_av_dw'], K_23['Corrected K'], s=100, color='black')
b.scatter(w2['SM_av_dw'], w2['Corrected K'], s=100, label = "low biomass", color='limegreen')
b.scatter(w1['SM_av_dw'], w1['Corrected K'], s=100, label = "high biomass", color='darkgreen')
b.scatter(w5['SM_av_dw'], w5['Corrected K'], s=100, color='limegreen')
b.plot(x23, lin(x23, *pars232), linewidth = 5, linestyle = 'solid', color='black')
b.text(40, 12.2, r'$\alpha_{^{40}K}$= 1.83', fontsize = 30, color = 'black')
b.text(40, 11.82, '$R^2$ = 0.91', fontsize = 30, color = 'black')
b.text(40, 11.47, 'RMSE = 0.26', fontsize = 30, color = 'black') 
b.set_xlim(5, 67)
b.set_ylim(8.85, 12.6)
b.set_title("Corrected", fontsize = 43)
#b.set_xlabel("Reference SM [vol. %]", fontsize = 30)
#b.set_ylabel("$^{40}$K GR intensity [nSv $\mathregular{h^{-1}]}$", fontsize = 30)

##Biomass uncorrected 2024
c.scatter(K_24['SM_av_dw'], K_24['K'], s=100, color='black')
c.scatter(w3['SM_av_dw'], w3['K'], s=100, label = "low biomass", color='limegreen')
c.scatter(w4['SM_av_dw'], w4['K'], s=100, label = "high biomass", color='darkgreen')
c.plot(x24, lin(x24, *pars24), linewidth = 5, linestyle = 'solid', color='black')
c.text(40, 12.2, r'$\alpha_{^{40}K}$= 1.04', fontsize = 30, color = 'black')
c.text(40, 11.82, '$R^2$ = 0.52', fontsize = 30, color = 'black')
c.text(40, 11.47, 'RMSE = 0.34', fontsize = 30, color = 'black')
c.set_xlim(5, 67)
c.set_ylim(8.85, 12.6)
#c.set_xlabel("Reference SM [vol. %]", fontsize = 30)
#c.set_ylabel("$^{40}$K GR intensity [nSv $\mathregular{h^{-1}]}$", fontsize = 30)
c.set_title("Uncorrected", fontsize = 43)

##Biomass corrected 2024
d.scatter(K_24['SM_av_dw'], K_24['Corrected K'], s=100, color='black')
d.scatter(w3['SM_av_dw'], w3['Corrected K'], s=100, label = "low biomass", color='limegreen')
d.scatter(w4['SM_av_dw'], w4['Corrected K'], s=100, label = "high biomass", color='darkgreen')
d.plot(x24, lin(x24, *pars242), linewidth = 5, linestyle = 'solid', color='black')
d.text(40, 12.2, r'$\alpha_{^{40}K}$= 2.08', fontsize = 30, color = 'black')
d.text(40, 11.82, '$R^2$ = 0.78', fontsize = 30, color = 'black')
d.text(40, 11.47, 'RMSE = 0.33', fontsize = 30, color = 'black')
d.set_xlim(5, 67)
d.set_ylim(8.85, 12.6)
d.set_title("Corrected", fontsize = 43)
#d.set_xlabel("Reference SM [vol. %]", fontsize = 30)
#d.set_ylabel("$^{40}$K GR intensity [nSv $\mathregular{h^{-1}]}$", fontsize = 30)

## Prediction models, second row
##Biomass uncorrected 2023
e.scatter(K_23['SM_av_dw'], K_23['SM_predicted1'], color = 'black', s=100)
e.scatter(w2['SM_av_dw'], w2['SM_predicted1'], s=100, label = "low biomass", color='limegreen')
e.scatter(w1['SM_av_dw'], w1['SM_predicted1'], s=100, label = "high biomass", color='darkgreen')
e.scatter(w5['SM_av_dw'], w5['SM_predicted1'], s=100, color='limegreen')
e.plot([p1, p2], [p1, p2], color = 'black', linestyle='dashed', linewidth =5)
e.set_ylim(0, 67)
e.set_xlim(0, 67)
e.text(38, 8, 'R$^2$ = 0.86', fontsize = 30, color = 'black')
e.text(38, 2, 'RMSE = 3.28', fontsize = 30, color = 'black')
e.text(3, 60, 'Prediction', fontsize = 38, color = 'black')
e.set_xlabel("Reference SM [vol. %]", fontsize = 40)
e.set_ylabel("Predicted SM [vol. %]", fontsize = 40)

##Biomass corrected 2023
f.scatter(K_23['SM_av_dw'], K_23['SM_predicted2'], color = 'black', s=100)
f.scatter(w2['SM_av_dw'], w2['SM_predicted2'], s=100, label = "low biomass", color='limegreen')
f.scatter(w1['SM_av_dw'], w1['SM_predicted2'], s=100, label = "high biomass", color='darkgreen')
f.scatter(w5['SM_av_dw'], w5['SM_predicted2'], s=100, color='limegreen')
f.plot([p1, p2], [p1, p2], color = 'black', linestyle='dashed', linewidth =5)
f.set_ylim(0, 67)
f.set_xlim(0, 67)
f.text(38, 8, 'R$^2$ = 0.92', fontsize = 30, color = 'black')
f.text(38, 2, 'RMSE = 2.44', fontsize = 30, color = 'black')
f.set_xlabel("Reference SM [vol. %]", fontsize = 40)

##Biomass uncorrected 2024
g.scatter(K_24['SM_av_dw'], K_24['SM_predicted1'], color = 'black', s=100)
g.scatter(w3['SM_av_dw'], w3['SM_predicted1'], s=100, label = "low biomass", color='limegreen')
g.scatter(w4['SM_av_dw'], w4['SM_predicted1'], s=100, label = "high biomass", color='darkgreen')
g.plot([p1, p2], [p1, p2], color = 'black', linestyle='dashed', linewidth =5)
g.set_ylim(0, 67)
g.set_xlim(0, 67)
g.text(38, 8, 'R$^2$ = 0.54', fontsize = 30, color = 'black')
g.text(38, 2, 'RMSE = 5.19', fontsize = 30, color = 'black')
g.set_xlabel("Reference SM [vol. %]", fontsize = 40)
#g.set_ylabel("Predicted SM [vol. %]", fontsize = 30)

##Biomass corrected 2024
h.scatter(K_24['SM_av_dw'], K_24['SM_predicted2'], color = 'black', s=100)
h.scatter(w3['SM_av_dw'], w3['SM_predicted2'], s=100, label = "low biomass", color='limegreen')
h.scatter(w4['SM_av_dw'], w4['SM_predicted2'], s=100, label = "high biomass", color='darkgreen')
h.plot([p1, p2], [p1, p2], color = 'black', linestyle='dashed', linewidth =5)
h.set_ylim(0, 67)
h.set_xlim(0, 67)
h.text(38, 8, 'R$^2$ = 0.78', fontsize = 30, color = 'black')
h.text(38, 2, 'RMSE = 2.92', fontsize = 30, color = 'black')
h.set_xlabel("Reference SM [vol. %]", fontsize = 40)
h.legend(loc='upper left', fontsize = 33, frameon=False, handletextpad=0.06, borderpad=0.06, labelspacing=0.2)
#h.set_ylabel("Predicted SM [vol. %]", fontsize = 30)

# -------------------------
# Tick interval
# -------------------------
for ax in [a, b, c, d, e, f, g, h]:
    ax.xaxis.set_major_locator(MultipleLocator(10))

for ax in [e, f, g, h]:
    ax.yaxis.set_major_locator(MultipleLocator(10))
    
# Grid
for ax in [a, b, c, d, e, f, g, h]:
    ax.set_axisbelow(True)
    ax.grid(True, linestyle='--', linewidth=0.8, alpha=0.9)

plt.savefig("D:\Data\Data_3rd_chapter\Figures\Biomass_correction_K40.png")
plt.show()






### Biomass correction plotting for MIRA
### Importing MIRA data for 2023
MI_23 = pd.read_csv(r"D:\Data\Data_3rd_chapter\Outputs\MIS_SM_BWE_2023.csv", header = 0, parse_dates= [0], index_col=0)
MI_23.rename(columns={"Corrected EGR for short-term SCR variability": "EGR"}, inplace=True)
MI_23 = MI_23.drop(MI_23.columns[np.r_[1:5, 6:10]], axis=1) 
MI_23['FB (mm)'] = MI_23['FB (mm)'].fillna(0)

## Correcting EGR for beta = 0.01
MI_23['Corrected EGR']= MI_23['EGR']/(1-0.01* MI_23['FB (mm)'])

# curve fitting
#MI_23 = MI_23.dropna(how='any')
x23 =MI_23['SM_av_dw'].values
y23 =MI_23['EGR'].values
y232 =MI_23['Corrected EGR'].values

##  EGR Prediction based on theoritically derived physics based equation
MI_23['EGR_predicted1'] = (100.50 / (1 + 0.46 * ((MI_23['SM_av_dw']/100)/1.39)))      ## Beta = 0
MI_23['EGR_predicted2'] = (106.84 / (1 + 0.71 * ((MI_23['SM_av_dw']/100)/1.39)))      ## Beta = 0.01


z23 =MI_23['EGR_predicted1'].values
z232 =MI_23['EGR_predicted2'].values


# Import curve fitting package from scipy
from scipy.optimize import curve_fit
# Function to calculate the linear fit with constants a and b
def lin(x, a, b):
    return a+b*x
pars23, cov = curve_fit(f=lin, xdata=x23, ydata=z23, p0=[0, 0], bounds=(-np.inf, np.inf))
pars232, cov = curve_fit(f=lin, xdata=x23, ydata=z232, p0=[0, 0], bounds=(-np.inf, np.inf))

## Ref vs pred
MI_23['SM_predicted1'] = ((1.39*(100.50-MI_23['EGR']))/(0.46*MI_23['EGR']))*100   ## Beta = 0
MI_23['SM_predicted2'] = ((1.39*(106.84-MI_23['Corrected EGR']))/(0.71*MI_23['Corrected EGR']))*100   ## Beta = 0.01


### Importing MIRA data for 2024
MI_24 = pd.read_csv(r"D:\Data\Data_3rd_chapter\Outputs\MIRA_EGR_ref_SM_BWE.csv", header = 0, parse_dates= [0], index_col=0)
MI_24 = MI_24.drop(MI_24.columns[np.r_[0:6,7:11,12,14:17]], axis=1) 
MI_24.rename(columns={"Corrected EGR for short-term SCR variability": "EGR"}, inplace=True)
MI_24['FB_AG (mm)'] = MI_24['FB_AG (mm)'].fillna(0)

## Correcting EGR for beta = 0.01
MI_24['Corrected EGR']= MI_24['EGR']/(1-0.01* MI_24['FB_AG (mm)'])

# curve fitting
MI_24 = MI_24.dropna(how='any')
x24 =MI_24['SM_av_dw'].values
y24 =MI_24['EGR'].values
y242 =MI_24['Corrected EGR'].values

##  EGR Prediction based on theoritically derived physics based equation
MI_24['EGR_predicted1'] = (93.42 / (1 + 0.13 * ((MI_24['SM_av_dw']/100)/1.36)))      ## Beta = 0
MI_24['EGR_predicted2'] = (109.95 / (1 + 0.84 * ((MI_24['SM_av_dw']/100)/1.36)))      ## Beta = 0.01


z24 =MI_24['EGR_predicted1'].values
z242 =MI_24['EGR_predicted2'].values


# Import curve fitting package from scipy
from scipy.optimize import curve_fit
# Function to calculate the linear fit with constants a and b
def lin(x, a, b):
    return a+b*x
pars24, cov = curve_fit(f=lin, xdata=x24, ydata=z24, p0=[0, 0], bounds=(-np.inf, np.inf))
pars242, cov = curve_fit(f=lin, xdata=x24, ydata=z242, p0=[0, 0], bounds=(-np.inf, np.inf))

## Ref vs pred
MI_24['SM_predicted1'] = ((1.36*(93.42-MI_24['EGR']))/(0.13*MI_24['EGR']))*100   ## Beta = 0
MI_24['SM_predicted2'] = ((1.36*(109.95-MI_24['Corrected EGR']))/(0.84*MI_24['Corrected EGR']))*100   ## Beta = 0.01

### Coloring based on the period when fresh biomass was high
w1 = MI_23['2023-04-10':'2023-07-26']  ## period with high fresh biomass, FB > 1.7 kg/m2
w2 = MI_23['2023-07-27':'2023-08-20']  ## period with low biomass, FB < 1.7 kg/m2
w3 = MI_24['2024-05-24':'2024-07-01']  ## period with low biomass, FB < 1.7 kg/m2
w4 = MI_24['2024-07-02':'2024-09-15']  ## period with high biomass, FB > 1.7 kg/m2
w5 = MI_23['2023-03-13':'2023-04-09']  ## period with low biomass, FB < 1.7 kg/m2



## Plotting
p1 = (70,70)
p2 = (0,0)
from matplotlib.gridspec import GridSpec
plt.rcParams["font.family"] = "Calibri"
fig = plt.figure(figsize=(25.5, 13.4), dpi=300)
gs = GridSpec(2, 5, figure=fig, width_ratios=[1, 1, 0, 1, 1], wspace=0.22, hspace=0.22)  # middle column 0 controls crop gap

# Adjust outer margins
gs.update(left=0.057, right=0.99, top=0.88, bottom=0.1)

# Subplots
a = fig.add_subplot(gs[0,0])
b = fig.add_subplot(gs[0,1])
c = fig.add_subplot(gs[0,3])
d = fig.add_subplot(gs[0,4])
e = fig.add_subplot(gs[1,0])
f = fig.add_subplot(gs[1,1])
g = fig.add_subplot(gs[1,3])
h = fig.add_subplot(gs[1,4])

# Column titles
fig.text(0.27, 0.97, 'Winter wheat', ha='center', va='center',fontsize=50)
fig.text(0.76, 0.97, 'Sugar beet', ha='center', va='center',fontsize=50)

# Tick sizes
plt.rc('xtick', labelsize=25)
plt.rc('ytick', labelsize=25)

## Calibration models, first row
##Biomass uncorrected 2023
a.scatter(MI_23['SM_av_dw'], MI_23['EGR'], s=100, color='black')
a.scatter(w2['SM_av_dw'], w2['EGR'], s=100, label = "low biomass", color='limegreen')
a.scatter(w1['SM_av_dw'], w1['EGR'], s=100, label = "high biomass", color='darkgreen')
a.scatter(w5['SM_av_dw'], w5['EGR'], s=100, color='limegreen')
a.plot(x23, lin(x23, *pars23), linewidth = 5, linestyle = 'solid', color='black')
a.text(40, 103, r'$\alpha_{EGR}$ = 0.46', fontsize = 30, color = 'black')
a.text(40, 100.7, '$R^2$ = 0.58', fontsize = 30, color = 'black')
a.text(40, 98.8, 'RMSE = 1.90', fontsize = 30, color = 'black')
a.text(7.5, 85, 'Calibration', fontsize = 38, color = 'black')
a.set_xlim(5, 67)
a.set_title("Uncorrected", fontsize = 43)
a.set_ylim(84, 105)
#a.set_xlabel("Reference SM [vol. %]", fontsize = 30)
a.set_ylabel("EGR [nSv $\mathregular{h^{-1}]}$", fontsize = 40)

##Biomass corrected 2023
b.scatter(MI_23['SM_av_dw'], MI_23['Corrected EGR'], s=100, color='black')
b.scatter(w2['SM_av_dw'], w2['Corrected EGR'], s=100, label = "low biomass", color='limegreen')
b.scatter(w1['SM_av_dw'], w1['Corrected EGR'], s=100, label = "high biomass", color='darkgreen')
b.scatter(w5['SM_av_dw'], w5['Corrected EGR'], s=100, color='limegreen')
b.plot(x23, lin(x23, *pars232), linewidth = 5, linestyle = 'solid', color='black')
b.text(40, 103, r'$\alpha_{EGR}$ = 0.71', fontsize = 30, color = 'black')
b.text(40, 100.7, '$R^2$ = 0.85', fontsize = 30, color = 'black')
b.text(40, 98.8, 'RMSE = 1.42', fontsize = 30, color = 'black')
b.set_xlim(5, 67)
b.set_ylim(84, 105)
b.set_title("Corrected", fontsize = 43)
#b.set_xlabel("Reference SM [vol. %]", fontsize = 30)
#b.set_ylabel("$^{40}$K GR intensity [nSv $\mathregular{h^{-1}]}$", fontsize = 30)

##Biomass uncorrected 2024
c.scatter(MI_24['SM_av_dw'], MI_24['EGR'], s=100, color='black')
c.scatter(w3['SM_av_dw'], w3['EGR'], s=100, label = "low biomass", color='limegreen')
c.scatter(w4['SM_av_dw'], w4['EGR'], s=100, label = "high biomass", color='darkgreen')
c.plot(x24, lin(x24, *pars24), linewidth = 5, linestyle = 'solid', color='black')
c.text(40, 103, r'$\alpha_{EGR}$ = 0.13', fontsize = 30, color = 'black')
c.text(40, 100.7, '$R^2$ = 0.05', fontsize = 30, color = 'black')
c.text(40, 98.8, 'RMSE = 2.02', fontsize = 30, color = 'black')
c.set_xlim(5, 67)
c.set_ylim(84, 105)
#c.set_xlabel("Reference SM [vol. %]", fontsize = 30)
#c.set_ylabel("$^{40}$K GR intensity [nSv $\mathregular{h^{-1}]}$", fontsize = 30)
c.set_title("Uncorrected", fontsize = 43)

##Biomass corrected 2024
d.scatter(MI_24['SM_av_dw'], MI_24['Corrected EGR'], s=100, color='black')
d.scatter(w3['SM_av_dw'], w3['Corrected EGR'], s=100, label = "low biomass", color='limegreen')
d.scatter(w4['SM_av_dw'], w4['Corrected EGR'], s=100, label = "high biomass", color='darkgreen')
d.plot(x24, lin(x24, *pars242), linewidth = 5, linestyle = 'solid', color='black')
d.text(40, 103, r'$\alpha_{EGR}$ = 0.84', fontsize = 30, color = 'black')
d.text(40, 100.7, '$R^2$ = 0.67', fontsize = 30, color = 'black')
d.text(40, 98.8, 'RMSE = 1.85', fontsize = 30, color = 'black')
d.set_xlim(5, 67)
d.set_ylim(84, 105)
d.set_title("Corrected", fontsize = 43)
#d.set_xlabel("Reference SM [vol. %]", fontsize = 30)
#d.set_ylabel("$^{40}$K GR intensity [nSv $\mathregular{h^{-1}]}$", fontsize = 30)

## Prediction models, second row
##Biomass uncorrected 2023
e.scatter(MI_23['SM_av_dw'], MI_23['SM_predicted1'], color = 'black', s=100)
e.scatter(w2['SM_av_dw'], w2['SM_predicted1'], s=100, label = "low biomass", color='limegreen')
e.scatter(w1['SM_av_dw'], w1['SM_predicted1'], s=100, label = "high biomass", color='darkgreen')
e.scatter(w5['SM_av_dw'], w5['SM_predicted1'], s=100, color='limegreen')
e.plot([p1, p2], [p1, p2], color = 'black', linestyle='dashed', linewidth =5)
e.set_ylim(0, 67)
e.set_xlim(0, 67)
e.text(38, 8, 'R$^2$ = 0.58', fontsize = 30, color = 'black')
e.text(38, 2, 'RMSE = 6.73', fontsize = 30, color = 'black')
e.text(3, 59, 'Prediction', fontsize = 38, color = 'black')
e.set_xlabel("Reference SM [vol. %]", fontsize = 40)
e.set_ylabel("Predicted SM [vol. %]", fontsize = 40)

##Biomass corrected 2023
f.scatter(MI_23['SM_av_dw'], MI_23['SM_predicted2'], color = 'black', s=100)
f.scatter(w2['SM_av_dw'], w2['SM_predicted2'], s=100, label = "low biomass", color='limegreen')
f.scatter(w1['SM_av_dw'], w1['SM_predicted2'], s=100, label = "high biomass", color='darkgreen')
f.scatter(w5['SM_av_dw'], w5['SM_predicted2'], s=100, color='limegreen')
f.plot([p1, p2], [p1, p2], color = 'black', linestyle='dashed', linewidth =5)
f.set_ylim(0, 67)
f.set_xlim(0, 67)
f.text(38, 8, 'R$^2$ = 0.85', fontsize = 30, color = 'black')
f.text(38, 2, 'RMSE = 3.32', fontsize = 30, color = 'black')
f.set_xlabel("Reference SM [vol. %]", fontsize = 40)

##Biomass uncorrected 2024
g.scatter(MI_24['SM_av_dw'], MI_24['SM_predicted1'], color = 'black', s=100)
g.scatter(w3['SM_av_dw'], w3['SM_predicted1'], s=100, label = "low biomass", color='limegreen')
g.scatter(w4['SM_av_dw'], w4['SM_predicted1'], s=100, label = "high biomass", color='darkgreen')
g.plot([p1, p2], [p1, p2], color = 'black', linestyle='dashed', linewidth =5)
g.set_ylim(0, 67)
g.set_xlim(0, 67)
g.text(38, 8, 'R$^2$ = 0.05', fontsize = 30, color = 'black')
g.text(38, 2, 'RMSE = 23.6', fontsize = 30, color = 'black')
g.set_xlabel("Reference SM [vol. %]", fontsize = 40)
#g.set_ylabel("Predicted SM [vol. %]", fontsize = 30)

##Biomass corrected 2024
h.scatter(MI_24['SM_av_dw'], MI_24['SM_predicted2'], color = 'black', s=100)
h.scatter(w3['SM_av_dw'], w3['SM_predicted2'], s=100, label = "low biomass", color='limegreen')
h.scatter(w4['SM_av_dw'], w4['SM_predicted2'], s=100, label = "high biomass", color='darkgreen')
h.plot([p1, p2], [p1, p2], color = 'black', linestyle='dashed', linewidth =5)
h.set_ylim(0, 67)
h.set_xlim(0, 67)
h.text(38, 8, 'R$^2$ = 0.66', fontsize = 30, color = 'black')
h.text(38, 2, 'RMSE = 3.81', fontsize = 30, color = 'black')
h.set_xlabel("Reference SM [vol. %]", fontsize = 40)
h.legend(loc='upper left', fontsize = 33, frameon=False, handletextpad=0.06, borderpad=0.06, labelspacing=0.2)

# -------------------------
# Tick interval
# -------------------------
for ax in [a, b, c, d, e, f, g, h]:
    ax.xaxis.set_major_locator(MultipleLocator(10))

for ax in [e, f, g, h]:
    ax.yaxis.set_major_locator(MultipleLocator(10))

# Grid
for ax in [a, b, c, d, e, f, g, h]:
    ax.set_axisbelow(True)
    ax.grid(True, linestyle='--', linewidth=0.8, alpha=0.9)

plt.savefig("D:\Data\Data_3rd_chapter\Figures\Biomass_correction_MIRA.png")
plt.show()


