# MakeTidy.py
# Take Steel subsector consumption data from the 7th and reshape in Tidy format
# https://stackoverflow.com/questions/45066873/pandas-melt-with-multiple-value-vars

# import math and data table functions
import numpy as np
import pandas as pd
import os
import datetime as dt

print("Script started. -- Current date/time:", dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# create directories for modified and results data
paths = {'path1': 'modified',
         'path2': 'results'}

for key, value in paths.items(): 
        try:
            os.makedirs(value)
        except OSError:
            print (" ")
        else:
            print ("Successfully created the directory %s " % value)

# read in raw steel data
RawSteelData = pd.read_csv(r'data/IS_production.csv')
RawSteelData.head()

# Replace missing numbers with NaN
# BD, HKC, PNG do not have steel production, set 2018 production value 1 as dummy and backfill the historical numbers for later regression
RawSteelData.replace (0,np.NaN,inplace=True)

# Backfill the NaN with numbers
RawSteelData = RawSteelData.bfill(axis = 'columns')

# using melt to make a tidy set with multiple measured variables - see Table 12 in Tidy Data paper
TidySteel = pd.melt(RawSteelData, id_vars=['Economy'], var_name='Year')
TidySteel.rename(columns={'value':'SteelProduction'}, inplace=True)

# replace economies using APEC approved abbreviations
EconomyNames = {
    '01_AUS':'AUS',
    '02_BD':'BD',
    '03_CDA':'CDA',
    '04_CHL':'CHL',
    '05_PRC':'PRC',
    '06_HKC':'HKC',
    '07_INA':'INA',
    '08_JPN':'JPN',
    '09_ROK':'KOR',
    '10_MAS':'MAS',
    '11_MEX':'MEX',
    '12_NZ':'NZ',
    '13_PNG':'PNG',
    '14_PE':'PE',
    '15_RP':'RP',
    '16_RUS':'RUS',
    '17_SIN':'SIN',
    '18_CT':'CT',
    '19_THA':'THA',
    '20_USA':'USA',
    '21_VN':'VN'}

TidySteel.replace(EconomyNames, inplace=True)

# write to csv
TidySteel.to_csv(r'modified/TidySteel.csv', index=False)

print("Results are saved. -- Current date/time:", dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
