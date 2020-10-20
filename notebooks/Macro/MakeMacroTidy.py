# MakeTidy.py
# take raw population and GDP from the 8th and reshape as Tidy
# save Tidy data in results folder

# import numpy for math and pandas for tables
import numpy as numpy
import pandas as pd
import os
import datetime as dt

print("\nScript started. -- Current date/time:", dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# create directories for modified and results data
paths = {'path1':'data/modified','path2':'results'}
for key, value in paths.items(): 
        try:
            os.makedirs(value)
        except OSError:
            print ("%s already exists. It's OK." % value)
        else:
            print ("Successfully created the directory %s " % value)

# import from Excel
print('\nImporting population and GDP data from the 8th Edition...')
rawGDP8th = pd.read_excel(r'data\raw\Manufacturing_GDP_8th_raw.xlsx')
rawPop8th = pd.read_excel(r'data\raw\Population_8th_raw.xlsx')

# define list of years
year_list = list(range(1990,2051,1))

GDP8th = rawGDP8th.set_index('Economy').stack().reset_index(name='GDP')
GDP8th.rename(columns={'level_1':'Year'}, inplace=True)

Pop8th = rawPop8th.set_index('Economy').stack().reset_index(name='Population')
Pop8th.rename(columns={'level_1':'Year'}, inplace=True)

# use melt to collapse the year columns in to a new column and rename columns
print('\nBegin cleaning...')
Pop8th = pd.melt(rawPop8th, id_vars='Economy', value_vars=year_list)
Pop8th.rename(columns={'variable':'Year','value':'Population'}, inplace=True)

GDP8th = pd.melt(rawGDP8th, id_vars='Economy', value_vars=year_list)
GDP8th.rename(columns={'variable':'Year','value':'GDP'}, inplace=True)

# replace economies using APEC approved abbreviations
# command this out for Excel data manipulation convenience
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

GDP8th.replace(EconomyNames, inplace=True)
Pop8th.replace(EconomyNames, inplace=True)

# remove World Economy data
GDP8th.dropna(inplace=True)
Pop8th.dropna(inplace=True)

GDP8th.drop(GDP8th[GDP8th['Economy']=='27_WOR'].index, inplace=True)
Pop8th.drop(Pop8th[Pop8th['Economy']=='27_WOR'].index, inplace=True)


# separate historical and future
# store all values up up to, and including, 2018 in one dataframe
GDP8thHistorical = GDP8th[GDP8th.Year <= 2018].reset_index(drop=True)
GDP8thFuture = GDP8th[GDP8th.Year > 2018].reset_index(drop=True)
Pop8thHistorical = Pop8th[Pop8th.Year <= 2018].reset_index(drop=True)
Pop8thFuture = Pop8th[Pop8th.Year > 2018].reset_index(drop=True)

# write all dataframes to csv
Pop8thHistorical.to_csv(r'results\Pop8thHistorical.csv', index=False)
Pop8thFuture.to_csv(r'results\Pop8thFuture.csv', index=False)
GDP8thHistorical.to_csv(r'results\GDP8thHistorical.csv', index=False)
GDP8thFuture.to_csv(r'results\GDP8thFuture.csv', index=False)

# Finished
print("\nFINISHED. -- Current date/time:", dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print('\nCleaned data saved in the folder %s' %paths['path2'])