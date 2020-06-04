#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 11:54:49 2020

@author: dmckenna
"""

import numpy as np
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns
import requests, json
import matplotlib.dates as mdates
import matplotlib.dates as mdates
import warnings
warnings.filterwarnings('ignore')

#%%

    ### Import the latest data ###
 
# The data is imported from the covidtracking.com website. 

url = 'https://covidtracking.com/api/v1/states/daily.json'

r = requests.get(url)

json_data = r.json()

df = pd.json_normalize(json_data)

# Add columns Deaths per Positive case (DperP), Positive per Test (PosPerTest),
# and Total Increase Minus Hosptialized Increase (TotMinusHosptializedIncresase)

df['DperP'] = df['death']/df['positive']
df['PosPerTest']= df['positiveIncrease']/df['totalTestResultsIncrease']
df['TotMinusHosptializedIncresase'] = np.abs(df['positiveIncrease'] - df['hospitalizedIncrease'])


df['date'] = pd.to_datetime(df['date'], format = '%Y%m%d')




#%%


df_1 = df[['state','date','positiveIncrease','deathIncrease']].reset_index()

today = str(df.date.max())

df_1['date_mod'] = pd.to_datetime(df_1['date'], format= '%Y%m%d')
df_1.set_index(['state','date_mod'],inplace=True)

df_1.sort_index(inplace=True)

df_1['date_ordinal'] = pd.to_datetime(df_1['date']).apply(lambda date: date.toordinal())



df_1['posDiff'] = df_1.groupby(level='state')['positiveIncrease'].apply(lambda x: (x.rolling(7).sum() / 7))





largest = df_1[df_1['date']==today]['posDiff'].nlargest(10).astype(int)



df_2 = pd.DataFrame(largest).reset_index()
plt.bar(df_2.state,df_2.posDiff)
plt.title('States with Largest 7 day Avg Increase', fontsize=16)
plt.ylabel('7 Day Avg Case Increase')




#%%

