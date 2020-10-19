# createdatasets.py
# join together GDP, population, and Production

# import math and data table functions
import numpy as np
import pandas as pd
import datetime as dt
import subprocess

print("Script started. -- Current date/time:", dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# read data from csv and store as dataframe
TidySteel = pd.read_csv(r'modified\TidySteel.csv')
GDP8thHistorical = pd.read_csv(r'..\Macro\results\GDP8thHistorical.csv')
Pop8thHistorical = pd.read_csv(r'..\Macro\results\Pop8thHistorical.csv')

# combine datasets
SteelHistorical = pd.merge(GDP8thHistorical, TidySteel, how='left', on=['Economy','Year'])
SteelHistorical = pd.merge(SteelHistorical,Pop8thHistorical,how='left',on=['Economy','Year'])

# Replace negative numbers with NaN
# Instead of dropping NaN, 'impute' the values by using mean, median, min, etc
# this replaces the NaN for BD, PNG, HK and RUS with min values across all economies
# Note that the BD, PNG values are too high - need to impute by economy
# SteelHistorical.loc[SteelHistorical['SteelProduction'] < 0,'SteelProduction'] = np.NaN
# SteelHistorical.fillna(SteelHistorical[['SteelProduction']].min(), inplace=True)

# i = SteelHistorical[['SteelProduction']].min()
# SteelHistorical.loc[SteelHistorical['Economy'].isin(['BD','HKC','PNG'])] = SteelHistorical.loc[SteelHistorical['Economy'].isin(['BD','HKC','PNG'])].fillna(i)
# j = SteelHistorical.loc[SteelHistorical['Economy']=='RUS','SteelProduction'].mean()
# SteelHistorical.loc[SteelHistorical['Economy'].isin(['RUS'])] = SteelHistorical.loc[SteelHistorical['Economy'].isin(['RUS'])].fillna(j)

# combine future GDP and population, drop the world value
GDP8thFuture = pd.read_csv(r'..\Macro\results\GDP8thFuture.csv')
Pop8thFuture = pd.read_csv(r'..\Macro\results\Pop8thFuture.csv')

GDPPop8thFuture = pd.merge(GDP8thFuture,Pop8thFuture,how='left',on=['Economy','Year']).reset_index(drop=True)

# save dataframes to csv
SteelHistorical.to_csv(r'modified\SteelHistorical.csv', index=False)
GDPPop8thFuture.to_csv(r'modified\GDPPop8thFuture.csv', index=False)

print("Results are saved. -- Current date/time:", dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))