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

plt.show()







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

UT = df[df['state']=='UT']
#UT= UT[UT['date'] >= '2020-03-15' ]

A = UT['hospitalizedIncrease'].loc[lambda x: x==389].index
B = UT['hospitalizedIncrease'].loc[lambda x: x== -365].index
C =UT['positiveIncrease'].loc[lambda x: x== 0].index

UT.loc[A,'hospitalizedIncrease'] = 12
UT.loc[B,'hospitalizedIncrease'] = 12

UT.to_excel('UT.xlsx')

UT['date_ordinal'] = pd.to_datetime(UT['date']).apply(lambda date: date.toordinal())

OrangeDate = UT[UT['date']=='2020-04-28']['date_ordinal']
OrangeDate = int(OrangeDate)

YellowDate = UT[UT['date']=='2020-05-14']['date_ordinal']
YellowDate = int(YellowDate)

ProtestDate = UT[UT['date']=='2020-05-29']['date_ordinal']
ProtestDate = int(ProtestDate)

fig, ax = plt.subplots(figsize = (12,6))

ax.bar(UT['date_ordinal'], UT['totalTestResultsIncrease'], label='Total Test Increase',color='blue')
ax.bar(UT['date_ordinal'], UT['positiveIncrease'], label='Positive Tests',color='red')
ax.legend(loc='upper left')


new_labels = [date.fromordinal(int(item)) for item in ax.get_xticks()]
ax.set_xticklabels(labels=new_labels, rotation=90, ha='right',fontdict={'fontsize':12})

ax.axvline(x=OrangeDate, color='orange', linewidth=2)
# ax.annotate('Code Orange Date', (OrangeDate - 2,240),color='black',rotation=90,fontsize=13)
ax.axvline( x=YellowDate, color='yellow', linewidth=2)
# ax.annotate'Code Yellow Date', (YellowDate - 2,240),color='black',rotation=90,fontsize=13)
ax.axvline( x=ProtestDate, color='purple', linewidth=1.5)
# ax.annotate('Protest Start Date', (ProtestDate - 2 ,240),color='black',rotation=90,fontsize=13)

ax.axvline(x=OrangeDate + 7, color='orange', linewidth=2, linestyle = '--')
# ax.annotate('Code Orange + 7-Days', (OrangeDate +5,210),color='black',rotation=90,fontsize=13)
ax.axvline( x=YellowDate + 7, color='yellow', linewidth=2, linestyle = '--')
ax.axvline( x=ProtestDate + 7, color='purple', linewidth=2, linestyle = '--')


plt.title('Utah Test Increase', fontdict={'fontsize':20})
plt.xlabel('Date', fontdict={'fontsize':12})
plt.ylabel('Test Increase', fontdict={'fontsize':12})
plt.axis('tight')
plt.savefig('Utah_Increase_Test.png')

plt.show()

#%%
    ###  Populate UT['icuIncrease] ###
    
UT.sort_index()

UT['PreviousDayICU'] = UT['inIcuCumulative'].shift(-1)

for row in UT.iterrows() :
    UT['icuIncrease'] = UT['inIcuCumulative'] - UT['PreviousDayICU']

UT.drop(columns = 'PreviousDayICU',inplace=True)
UT.to_excel('UT.xlsx')



#%%
UT= UT[UT['date'] >= '2020-04-15' ]

left= UT[UT['date']=='2020-04-05']['date_ordinal']
right = UT[UT['date']==max(UT['date'])]['date_ordinal']
                                   
fig, ax = plt.subplots(figsize = (12,6))

ax.bar(UT['date_ordinal'], UT['hospitalizedIncrease'], label='Total Hospital Increase',color='blue')
ax.bar(UT['date_ordinal'], UT['icuIncrease'], label='ICU Increase',color='red')
ax.legend(loc='upper left')


new_labels = [date.fromordinal(int(item)) for item in ax.get_xticks()]
ax.set_xticklabels(labels=new_labels, rotation=30, ha='right',fontdict={'fontsize':12})
ax.axvline(x=OrangeDate, color='orange', linewidth=2)
# ax.annotate('Code Orange Date', (OrangeDate - 2,240),color='black',rotation=90,fontsize=13)
ax.axvline( x=YellowDate, color='yellow', linewidth=2)
# ax.annotate'Code Yellow Date', (YellowDate - 2,240),color='black',rotation=90,fontsize=13)
ax.axvline( x=ProtestDate, color='purple', linewidth=1.5)
# ax.annotate('Protest Start Date', (ProtestDate - 2 ,240),color='black',rotation=90,fontsize=13)

ax.axvline(x=OrangeDate + 7, color='orange', linewidth=2, linestyle = '--')
# ax.annotate('Code Orange + 7-Days', (OrangeDate +5,210),color='black',rotation=90,fontsize=13)
ax.axvline( x=YellowDate + 7, color='yellow', linewidth=2, linestyle = '--')
ax.axvline( x=ProtestDate + 7, color='purple', linewidth=2, linestyle = '--')
ax.set_xlim(left=left,right=right)

plt.show()

