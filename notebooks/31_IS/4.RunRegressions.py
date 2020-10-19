# RunRegressions.py
# create linear regrssion models for all 21 economies

# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import sys
import datetime as dt
from matplotlib.ticker import MultipleLocator, FixedLocator, FixedFormatter

print("Script started. -- Current date/time:", dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# import regression functions from RegressionFunctions.py
sys.path.insert(0, 'Common')
from CommonFunctions import run_regression, run_prediction, plot2

# Perform regressions
# read in data from csv
SteelHistoricalPrepared = pd.read_csv(r'modified\SteelHistoricalPrepared.csv')
GDPPop8thFuturePrepared = pd.read_csv(r'modified\GDPPop8thFuturePrepared.csv')

# get list of economies and create economy-model pairs
economies = SteelHistoricalPrepared.Economy.unique()
models = {economy: LinearRegression() for economy in economies}

# set Economy as index 
df1 = SteelHistoricalPrepared.set_index('Economy')
# set explanatory variable x and dependent variable y
x = ['Year','lnGDPpercap'] # data that has relationship with y
y = ['lnPROpercap'] # what you want to know

# run regression
SteelRegressionModel = run_regression(models, economies, df1, x, y)

print('\nGenerated regression. Please wait for plotting.\n')

# make predictions using historical values of GDP per capita
HistoricalX = df1[['Year','lnGDPpercap']]
ResultsColumn = ['Predicted Steel Production per capita']
HistoricalPredictionResults = run_prediction(SteelRegressionModel, economies, HistoricalX, ResultsColumn)

# make predictions using FUTURE values of GDP per capita
FutureX = GDPPop8thFuturePrepared.set_index('Economy')[['Year','lnGDPpercap']]
FuturePredictionResults = run_prediction(SteelRegressionModel, economies, FutureX, ResultsColumn)

# -- Compute steel production (instead of per capita)
# read historical and future population data from csv
Pop8thHistorical = pd.read_csv(r'..\Macro\results\Pop8thHistorical.csv')
Pop8thFuture = pd.read_csv(r'..\Macro\results\Pop8thFuture.csv')

# add population column to historical and future prediction results
HistoricalPredictionResults = pd.merge(HistoricalPredictionResults, Pop8thHistorical, how='left', on=['Economy','Year'])
FuturePredictionResults = pd.merge(FuturePredictionResults,Pop8thFuture, how='left',on=['Economy','Year'])

# compute steel production
# Jan 16 2020: delete 'div(1000)' because I want thousand tons for my list
# HistoricalPredictionResults['Predicted Steel Production'] = HistoricalPredictionResults['Predicted Steel Production per capita'].mul(HistoricalPredictionResults['Population']).div(1000)
# FuturePredictionResults['Predicted Steel Production'] = FuturePredictionResults['Predicted Steel Production per capita'].mul(FuturePredictionResults['Population']).div(1000)
HistoricalPredictionResults['Predicted Steel Production'] = HistoricalPredictionResults['Predicted Steel Production per capita'].mul(HistoricalPredictionResults['Population'])
FuturePredictionResults['Predicted Steel Production'] = FuturePredictionResults['Predicted Steel Production per capita'].mul(FuturePredictionResults['Population'])

# combine results
SteelResultsCombined = pd.concat([HistoricalPredictionResults,FuturePredictionResults])

# write results to csv
HistoricalPredictionResults.to_csv(r'results\HistoricalPredictionResults.csv', index=False)
FuturePredictionResults.to_csv(r'results\FuturePredictionResults.csv', index=False)
SteelResultsCombined.to_csv(r'results\SteelResultsCombined.csv', index=False)

print("Results are saved. -- Current date/time:", dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# STEP 6 - plot results
# set file name
# Use sharex and sharey = True or False to share those axes
figurename = 'Industry\steel\steel production.png'
Plotylabel = 'million tonnes'
sharex = True
sharey = True

# create dataframe with Historical results in one column and Future in another
df1 = HistoricalPredictionResults.drop(['Predicted Steel Production per capita','Population'], axis=1)
df2 = FuturePredictionResults.drop(['Predicted Steel Production per capita','Population'], axis=1)
df1.rename(columns={'Predicted Steel Production':'Historical'},inplace=True)
df2.rename(columns={'Predicted Steel Production':'Future'},inplace=True)
dfPlot = pd.merge(df1,df2,how='outer')

# Create the figure
# plot2 is a function from CommonFunctions.py
print('Preparing to show the figure...')
plot2(economies, dfPlot, figurename, Plotylabel, sharex, sharey)
print('Figure saved as %s' % figurename)

# Finished
print("\nFINISHED. -- Current date/time:", dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print('\nSteel production demand saved in the folder Industry\steel\results')