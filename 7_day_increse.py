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


# ten_states = df_2.state



# df_1.reset_index(inplace=True)
# df_3 = pd.DataFrame()

# for state in ten_states :

    
#     data = df_1[df_1['state']==str(state)]
   

#     df_3 = pd.concat([df_3,data])
    
    
  
# # df_3.to_excel('df_3.xlsx')    

# fig, ax = plt.subplots(figsize = (12,6))
# new_labels = [date.fromordinal(int(item)) for item in ax.get_xticks()]


# ax.sns.pointplot(data=df_3, x='date_ordinal',y='posDiff',hue='state', marker = '.')

# ax.set_xlim(df_3['date_ordinal'].min()  , df_3['date_ordinal'].max() )
# ax.set_xticklabels(labels=new_labels, rotation=45, ha='right',fontdict={'fontsize':12})


# plt.show()

#%%

names = ['State','Census','Estimates Base','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019']

pop = pd.read_excel('pop_data.xlsx',header=4,names=names)
pop.drop(columns=['Census','Estimates Base','2010','2011','2012','2013','2014','2015','2016','2017','2018'],inplace=True)


print(pop[pop['State']== '.Alabama'])    
