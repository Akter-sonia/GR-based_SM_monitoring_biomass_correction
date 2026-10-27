# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 13:10:43 2026

@author: s.akter
"""

# write "%matplotlib qt" command in console panel to get interactive plot
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
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import MultipleLocator





### Biomass correction sensitivitty analysis for K-40
### Importing K-40 data for 2023
K_23_FB = pd.read_excel(r"D:\Data\Data_3rd_chapter\Biomass_correction_Selhausen\Biomass_correction_2023\Output\K_dwSM_Fresh_AGB.xlsx", header = 0)
K_23_BWC = pd.read_excel(r"D:\Data\Data_3rd_chapter\Biomass_correction_Selhausen\Biomass_correction_2023\Output\K_dwSM_AG_BWC.xlsx", header = 0)

### Importing K-40 data for 2024
K_24_FB = pd.read_excel(r"D:\Data\Data_3rd_chapter\Biomass_correction_Selhausen\Biomass_correction_2024\output\K_dwSM_Fresh_AGB.xlsx", header = 0)
K_24_BWC = pd.read_excel(r"D:\Data\Data_3rd_chapter\Biomass_correction_Selhausen\Biomass_correction_2024\Output\K_dwSM_AG_BWC.xlsx", header = 0)



## Plotting
plt.rcParams["font.family"] = "Calibri"
fig, axes = plt.subplots(3, 2,figsize=(13.5, 16),dpi=300)

a, b = axes[0]
c, d = axes[1]
e, f = axes[2]

# Adjust spacing
plt.subplots_adjust(left=0.12,bottom=0.08,right=0.95,top=0.90,wspace=0.22,hspace=0.22)

# Column titles
fig.text(0.31, 0.94, 'Winter wheat', ha='center', va='center',fontsize=34)
fig.text(0.75, 0.94, 'Sugar beet', ha='center', va='center',fontsize=34)

# Tick sizes
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)

# -------------------------
# Alpha
# -------------------------
a.plot(K_23_FB['Beta'], K_23_FB['Alpha'],marker='o',markersize=9,linewidth=3,color='black', label = r'AGB$_{\mathrm{fresh}}$')
a.plot(K_23_BWC['Beta'], K_23_BWC['Alpha'],marker='o',markersize=9,linewidth=3,color='black', label = r'AGB$_{\mathrm{WC}}$', linestyle = 'dashed')
a.set_ylabel(r'$\alpha_{^{40}K}$', fontsize=32)
a.legend(loc='upper left', fontsize=30, frameon=False)
#a.set_ylim(0.1, 1.2)
a.set_ylim(0, 4)
#a.yaxis.set_major_locator(MultipleLocator(0.5))

b.plot(K_24_FB['Beta'], K_24_FB['Alpha'], marker='o', markersize=9,linewidth=3, color='black', label = r'AGB$_{\mathrm{fresh}}$')
b.plot(K_24_BWC['Beta'], K_24_BWC['Alpha'],marker='o',markersize=9,linewidth=3,color='black', label = r'AGB$_{\mathrm{WC}}$', linestyle = 'dashed')
b.set_ylim(0.1, 1.2)
b.set_ylim(0, 4)

# -------------------------
# R2
# -------------------------
c.plot(K_23_FB['Beta'], K_23_FB['R2'], marker='o', markersize=9,linewidth=3, color='black', label = r'AGB$_{\mathrm{fresh}}$')
c.plot(K_23_BWC['Beta'], K_23_BWC['R2'], marker='o', markersize=9,linewidth=3, color='black', label = r'AGB$_{\mathrm{WC}}$', linestyle = 'dashed')
c.set_ylabel(r'$R^2$', fontsize=32)
c.set_ylim(0, 1)

d.plot(K_24_FB['Beta'], K_24_FB['R2'], marker='o', markersize=9, linewidth=3,color='black', label = r'AGB$_{\mathrm{fresh}}$')
d.plot(K_24_BWC['Beta'], K_24_BWC['R2'], marker='o', markersize=9, linewidth=3,color='black', label = r'AGB$_{\mathrm{WC}}$', linestyle = 'dashed')
d.set_ylim(0, 1)

# -------------------------
# RMSE
# -------------------------
e.plot(K_23_FB['Beta'], K_23_FB['RMSE'], marker='o',markersize=9,linewidth=3,color='black', label = r'AGB$_{\mathrm{fresh}}$')
e.plot(K_23_BWC['Beta'], K_23_BWC['RMSE'], marker='o',markersize=9,linewidth=3,color='black', label = r'AGB$_{\mathrm{WC}}$', linestyle = 'dashed')
e.set_xlabel(r'$\beta$', fontsize=32)
e.set_ylabel('RMSE', fontsize=32)
e.set_ylim(1.5, 5.3)

f.plot(K_24_FB['Beta'], K_24_FB['RMSE'], marker='o', markersize=9,linewidth=3,color='black', label = r'AGB$_{\mathrm{fresh}}$')
f.plot(K_24_BWC['Beta'], K_24_BWC['RMSE'], marker='o', markersize=9,linewidth=3,color='black', label = r'AGB$_{\mathrm{WC}}$', linestyle = 'dashed')
f.set_xlabel(r'$\beta$', fontsize=32)
f.set_ylim(1.5, 5.3)

# -------------------------
# Tick interval
# -------------------------
for ax in [e, f]:
    ax.yaxis.set_major_locator(MultipleLocator(0.5))

# Grid
for ax in axes.flat:
    ax.set_axisbelow(True)
    ax.grid(True, linestyle='--', linewidth=0.8, alpha=0.8)

plt.savefig(r"D:\Data\Data_3rd_chapter\Figures\Biomass_sensitivity_analysis_K40.png",dpi=300,bbox_inches='tight')
plt.show()



### Biomass correction sensitivitty analysis for MIRA
### Importing MIRA data for 2023
MI_23_FB = pd.read_excel(r"D:\Data\Data_3rd_chapter\Biomass_correction_Selhausen\Biomass_correction_2023\Output\MIRA_dwSM_Fresh_AGB.xlsx", header = 0)
MI_23_BWC = pd.read_excel(r"D:\Data\Data_3rd_chapter\Biomass_correction_Selhausen\Biomass_correction_2023\Output\MIRA_dwSM_AG_BWC.xlsx", header = 0)

### Importing MIRA data for 2024
MI_24_FB = pd.read_excel(r"D:\Data\Data_3rd_chapter\Biomass_correction_Selhausen\Biomass_correction_2024\output\MIRA_dwSM_Fresh_AGB.xlsx", header = 0)
MI_24_BWC = pd.read_excel(r"D:\Data\Data_3rd_chapter\Biomass_correction_Selhausen\Biomass_correction_2024\output\MIRA_dwSM_AG_BWC.xlsx", header = 0)


## Plotting
plt.rcParams["font.family"] = "Calibri"
fig, axes = plt.subplots(3, 2,figsize=(13.5, 16),dpi=300)

a, b = axes[0]
c, d = axes[1]
e, f = axes[2]

# Adjust spacing
plt.subplots_adjust(left=0.12,bottom=0.08,right=0.95,top=0.90,wspace=0.22,hspace=0.22)

# Column titles
fig.text(0.31, 0.94, 'Winter wheat', ha='center', va='center',fontsize=34)
fig.text(0.75, 0.94, 'Sugar beet', ha='center', va='center',fontsize=34)

# Tick sizes
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)

# -------------------------
# Alpha
# -------------------------
a.plot(MI_23_FB['Beta'], MI_23_FB['Alpha'],marker='o',markersize=9,linewidth=3,color='black', label = r'AGB$_{\mathrm{fresh}}$')
a.plot(MI_23_BWC['Beta'], MI_23_BWC['Alpha'],marker='o',markersize=9,linewidth=3,color='black', label = r'AGB$_{\mathrm{WC}}$', linestyle = 'dashed')
a.set_ylabel(r'$\alpha_{EGR}$', fontsize=32)
a.legend(loc='upper left', fontsize=30, frameon=False)
a.set_ylim(0, 4)

b.plot(MI_24_FB['Beta'], MI_24_FB['Alpha'], marker='o', markersize=9,linewidth=3, color='black', label = r'AGB$_{\mathrm{fresh}}$')
b.plot(MI_24_BWC['Beta'], MI_24_BWC['Alpha'],marker='o',markersize=9,linewidth=3,color='black', label = r'AGB$_{\mathrm{WC}}$', linestyle = 'dashed')
b.set_ylim(0, 4)

# -------------------------
# R2
# -------------------------
c.plot(MI_23_FB['Beta'], MI_23_FB['R2'], marker='o', markersize=9,linewidth=3, color='black', label = r'AGB$_{\mathrm{fresh}}$')
c.plot(MI_23_BWC['Beta'], MI_23_BWC['R2'], marker='o', markersize=9,linewidth=3, color='black', label = r'AGB$_{\mathrm{WC}}$', linestyle = 'dashed')
c.set_ylabel(r'$R^2$', fontsize=32)
c.set_ylim(0, 1)

d.plot(MI_24_FB['Beta'], MI_24_FB['R2'], marker='o', markersize=9, linewidth=3,color='black', label = r'AGB$_{\mathrm{fresh}}$')
d.plot(MI_24_BWC['Beta'], MI_24_BWC['R2'], marker='o', markersize=9, linewidth=3,color='black', label = r'AGB$_{\mathrm{WC}}$', linestyle = 'dashed')
d.set_ylim(0, 1)

# -------------------------
# RMSE
# -------------------------
e.plot(MI_23_FB['Beta'], MI_23_FB['RMSE'], marker='o',markersize=9,linewidth=3,color='black', label = r'AGB$_{\mathrm{fresh}}$')
e.plot(MI_23_BWC['Beta'], MI_23_BWC['RMSE'], marker='o',markersize=9,linewidth=3,color='black', label = r'AGB$_{\mathrm{WC}}$', linestyle = 'dashed')
e.set_xlabel(r'$\beta$', fontsize=32)
e.set_ylabel('RMSE', fontsize=32)
e.set_ylim(2.5, 24)

f.plot(MI_24_FB['Beta'], MI_24_FB['RMSE'], marker='o', markersize=9,linewidth=3,color='black', label = r'AGB$_{\mathrm{fresh}}$')
f.plot(MI_24_BWC['Beta'], MI_24_BWC['RMSE'], marker='o', markersize=9,linewidth=3,color='black', label = r'AGB$_{\mathrm{WC}}$', linestyle = 'dashed')
f.set_xlabel(r'$\beta$', fontsize=32)
f.set_ylim(2.5, 24)

# -------------------------
# Tick interval
# -------------------------
for ax in [e, f]:
    ax.yaxis.set_major_locator(MultipleLocator(3))
    
# Grid
for ax in axes.flat:
    ax.set_axisbelow(True)
    ax.grid(True,linestyle='--',linewidth=0.8,alpha=0.8)

plt.savefig(r"D:\Data\Data_3rd_chapter\Figures\Biomass_sensitivity_analysis_MIRA.png",dpi=300,bbox_inches='tight')
plt.show()






### Biomass correction sensitivitty analysis for K-40 and EGR, considering total biomass (AGB+BGB)

### Importing K-40 data for 2024
K_24_FB = pd.read_excel(r"D:\Data\Data_3rd_chapter\Biomass_correction_Selhausen\Biomass_correction_2024\output\K_dwSM_Fresh_AGB_BGB.xlsx", header = 0)
K_24_BWC = pd.read_excel(r"D:\Data\Data_3rd_chapter\Biomass_correction_Selhausen\Biomass_correction_2024\Output\K_dwSM_AG_BG_BWC.xlsx", header = 0)

### Importing MIRA data for 2024
MI_24_FB = pd.read_excel(r"D:\Data\Data_3rd_chapter\Biomass_correction_Selhausen\Biomass_correction_2024\output\MIRA_dwSM_Fresh_AGB_BGB.xlsx", header = 0)
MI_24_BWC = pd.read_excel(r"D:\Data\Data_3rd_chapter\Biomass_correction_Selhausen\Biomass_correction_2024\output\MIRA_dwSM_AG_BG_BWC.xlsx", header = 0)


## Plotting
plt.rcParams["font.family"] = "Calibri"
fig, axes = plt.subplots(3, 2,figsize=(13.5, 16.5),dpi=300)

a, b = axes[0]
c, d = axes[1]
e, f = axes[2]

# Adjust spacing
plt.subplots_adjust(left=0.12,bottom=0.08,right=0.95,top=0.90,wspace=0.22,hspace=0.22)

# Column titles
fig.text(0.31, 0.94, '$^{40}$K GR', ha='center', va='center',fontsize=34)
fig.text(0.75, 0.94, 'EGR', ha='center', va='center',fontsize=34)

# Tick sizes
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)

# -------------------------
# Alpha
# -------------------------
a.plot(K_24_FB['Beta'], K_24_FB['Alpha'],marker='o',markersize=9,linewidth=3,color='black', label = r'AGB$_{\mathrm{fresh}}$+BGB$_{\mathrm{fresh}}$')
a.plot(K_24_BWC['Beta'], K_24_BWC['Alpha'],marker='o',markersize=9,linewidth=3,color='black', label = r'AGB$_{\mathrm{WC}}$+BGB$_{\mathrm{WC}}$', linestyle = 'dashed')
a.set_ylabel(r'$\alpha_{^{40}K}$', fontsize=32)
#a.legend(loc='upper left', fontsize=30, frameon=False)
a.set_ylim(0, 8)
a.set_xlim(-0.0013, 0.0263)

b.plot(MI_24_FB['Beta'], MI_24_FB['Alpha'], marker='o', markersize=9,linewidth=3, color='black', label = r'AGB$_{\mathrm{fresh}}$+BGB$_{\mathrm{fresh}}$')
b.plot(MI_24_BWC['Beta'], MI_24_BWC['Alpha'],marker='o',markersize=9,linewidth=3,color='black', label = r'AGB$_{\mathrm{WC}}$+BGB$_{\mathrm{WC}}$', linestyle = 'dashed')
b.set_ylim(0, 8)
b.set_xlim(-0.0013, 0.0263)
b.set_ylabel(r'$\alpha_{EGR}$', fontsize=32)
b.legend(loc='upper left', fontsize=28, frameon=False)

# -------------------------
# R2
# -------------------------
c.plot(K_24_FB['Beta'], K_24_FB['R2'], marker='o', markersize=9,linewidth=3, color='black', label = r'AGB$_{\mathrm{fresh}}$+BGB$_{\mathrm{fresh}}$')
c.plot(K_24_BWC['Beta'], K_24_BWC['R2'], marker='o', markersize=9,linewidth=3, color='black', label = r'AGB$_{\mathrm{WC}}$+BGB$_{\mathrm{WC}}$', linestyle = 'dashed')
c.set_ylabel(r'$R^2$', fontsize=32)
c.set_ylim(0, 1)
c.set_xlim(-0.0013, 0.0263)

d.plot(MI_24_FB['Beta'], MI_24_FB['R2'], marker='o', markersize=9, linewidth=3,color='black', label = r'AGB$_{\mathrm{fresh}}$+BGB$_{\mathrm{fresh}}$')
d.plot(MI_24_BWC['Beta'], MI_24_BWC['R2'], marker='o', markersize=9, linewidth=3,color='black', label = r'AGB$_{\mathrm{WC}}$+BGB$_{\mathrm{WC}}$', linestyle = 'dashed')
d.set_ylim(0, 1)
d.set_xlim(-0.0013, 0.0263)
d.set_ylabel(r'$R^2$', fontsize=32)

# -------------------------
# RMSE
# -------------------------
e.plot(K_24_FB['Beta'], K_24_FB['RMSE'], marker='o',markersize=9,linewidth=3,color='black', label = r'AGB$_{\mathrm{fresh}}$+BGB$_{\mathrm{fresh}}$')
e.plot(K_24_BWC['Beta'], K_24_BWC['RMSE'], marker='o',markersize=9,linewidth=3,color='black', label = r'AGB$_{\mathrm{WC}}$+BGB$_{\mathrm{WC}}$', linestyle = 'dashed')
e.set_xlabel(r'$\beta$', fontsize=32)
e.set_ylabel('RMSE', fontsize=32)
e.set_ylim(1.5, 5.3)
e.set_xlim(-0.0013, 0.0263)

f.plot(MI_24_FB['Beta'], MI_24_FB['RMSE'], marker='o', markersize=9,linewidth=3,color='black', label = r'AGB$_{\mathrm{fresh}}$+BGB$_{\mathrm{fresh}}$')
f.plot(MI_24_BWC['Beta'], MI_24_BWC['RMSE'], marker='o', markersize=9,linewidth=3,color='black', label = r'AGB$_{\mathrm{WC}}$+BGB$_{\mathrm{WC}}$', linestyle = 'dashed')
f.set_xlabel(r'$\beta$', fontsize=32)
f.set_ylim(2.5, 24)
f.set_xlim(-0.0013, 0.0263)
f.set_ylabel('RMSE', fontsize=32)


# -------------------------
# Tick interval
# -------------------------
for ax in [e]:
    ax.yaxis.set_major_locator(MultipleLocator(0.5))

# Grid
for ax in axes.flat:
    ax.set_axisbelow(True)
    ax.grid(True, linestyle='--', linewidth=0.8, alpha=0.8)

plt.savefig(r"D:\Data\Data_3rd_chapter\Figures\Biomass_sensitivity_analysis_K40_EGR_total_biomass.png",dpi=300,bbox_inches='tight')
plt.show()


