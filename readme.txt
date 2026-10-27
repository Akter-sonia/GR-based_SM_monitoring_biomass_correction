### Introduction
Raw and processed data, codes and figures for gamma radiation biomass correction study for the period of Feb'23 to Dec'25.

### Description 

## Map_Selhausen
All necessary files to regenerate the experimental-site map used in this study.

## Py_script
All python scripts are stored in that folder.

## Data
# Input_data
The raw data are stored in that folder.
# Outputs
The raw data were processed in python and stored in that folder. 
1. MIRA_EGR_after_rain_filter.csv contains MIRA EGR measurements after correcting for radon-washouts for 2024.
2. MIS_EGR_processed.csv contains MIRA EGR measurements for 2024 after further correcting for short-term SCR variability. 
long-term SCR contribution is assumed to be constant, and not subtracted from the EGR measurements.
3.selhausen_ref_SM.csv contains processed ref SM data for 2024 calculated from the data of 5 SoilNet 
stations installed around the GR station (first, horizontal average of each depth for all
locations were calculated, e.g., data for 2cm from all stations were averaged. Later, depth weighted mean SM was calculated). 
4. selhausen_ref_SM_with_add_SoilNet_data.csv contains the ref soil moisture data for 2024 after including the data of 4 additional SoilNet 
stations that were installed in early-summer 2024.
5. MIRA_EGR_ref_SM_Biomass.csv contains combined data of preocessed MIRA EGR measurements, reference soil moisture and 
biomass data for 2024 on daily resolution.K_ref_SM_Biomass.csv contains similiar data for K-40 measurements.
6. MIS_SM_Biomass_2023.csv contains combined data of preocessed MIRA EGR measurements, reference soil moisture and 
biomass data for 2023 on daily resolution. K_SM_Biomass_2023.csv contains similiar data for K-40 measurements.  
7. MIS_SM_2023_2024.csv contains combined data of preocessed MIRA EGR measurements, reference soil moisture and biomass data for 2023 and 2024 on daily resolution.
8. MIS_SM_2023_2024_without_high_biomass.csv contains combined data of preocessed MIRA EGR measurements and reference soil moisture data for 
2023 and 2024 on daily resolution excluding significant biomass period.  
9. mean_bd_23.csv and mean_bd_24.csv files contain averaged bulk density information for the year of 2023 and 2024, respectively. 

## Results
# Biomass_correction_Selhausen
The processed data (i.e., MIS_SM_Biomass_2023.csv, K_SM_Biomass_2023.csv) were used for biomass correction.
Calibration and prediction results for MIRA EGR (corrected) or K-40 measurements are stored in this folder for different biomass correction scenarios
(i.e., calibration and prediction results while changing the β parameter from 0 to 0.025 ).
All the analysis were conducted seperately for the year of 2023 and 2024 considering the winter wheat (2023) and sugar beet (2024) growing period.
# Analysis_without_high_biomass
Calibration and prediction results for MIRA EGR (corrected) or K-40 measurements.
All the analysis were conducted for the year of 2023 and 2024 excluding significant biomass period.

## Figures
Contains all the figures used in the manuscript.

## Abbreviations used in the data
BWC = biomass water content; FB = fresh biomass; AG = above-ground; BG = below-ground; 
SM_av_dw = Calculated mean soil moisture considering the horizontal distribution of the SoilNet sensors through out the soil profile.