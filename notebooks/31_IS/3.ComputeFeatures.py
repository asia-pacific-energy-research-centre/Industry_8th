# ComputeFeatures.py
# compute per capita and natural logs for regression

# import math and table functions
import pandas as pd
import numpy as np 
import datetime as dt

print("Script started. -- Current date/time:", dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# read datasets from csv
SteelHistorical = pd.read_csv(r'modified/SteelHistorical.csv')
GDPPop8thFuture = pd.read_csv(r'modified/GDPPop8thFuture.csv')

# compute per capita then take natural logs
SteelHistorical['GDPpercap'] = SteelHistorical['GDP'].div(SteelHistorical['Population'])
SteelHistorical['PROpercap'] = SteelHistorical['SteelProduction'].div(SteelHistorical['Population'])

SteelHistorical['lnGDPpercap'] = np.log(SteelHistorical['GDPpercap'])
SteelHistorical['lnPROpercap'] = np.log(SteelHistorical['PROpercap'])

GDPPop8thFuture['GDPpercap'] = GDPPop8thFuture['GDP'].div(GDPPop8thFuture['Population'])
GDPPop8thFuture['lnGDPpercap'] = np.log(GDPPop8thFuture['GDPpercap'])

# write prepared data to csv
SteelHistorical.to_csv(r'modified/SteelHistoricalPrepared.csv', index=False)   
GDPPop8thFuture.to_csv(r'modified/GDPPop8thFuturePrepared.csv', index=False)

print("Results are saved. -- Current date/time:", dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))