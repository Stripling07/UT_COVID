#!/usr/bin/env python
# coding: utf-8


"""
Created on Thu May 28 12:04:02 2020

@author: David R McKenna
"""
# In[1]:

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
#pd.__version__




# In[2]:
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

df.set_index('date')



plt.close('all')
df.to_excel('df.xlsx')


# In[3]:
                 ### Subset the data for specific states ### 
sns.set()
# First we look at Utah

UT = df[df['state']=='UT']


A = UT['hospitalizedIncrease'].loc[lambda x: x==389].index
B = UT['hospitalizedIncrease'].loc[lambda x: x== -365].index
C =UT['positiveIncrease'].loc[lambda x: x== 0].index

UT.loc[A,'hospitalizedIncrease'] = 12
UT.loc[B,'hospitalizedIncrease'] = 12


UT.drop(C,inplace=True)

# Reove clear outliers, looks like they added too many (389) one day and the 
# corrected that by adding a (-354) a couple days later.


# UT = UT[UT['hospitalizedIncrease']!=389]  
# UT = UT[UT['hospitalizedIncrease']> 0]

UT.to_excel('df.xlsx')
#%%
# Create date ordinal for simplicity of plot labels

UT['date_ordinal'] = pd.to_datetime(UT['date']).apply(lambda date: date.toordinal())

OrangeDate = UT[UT['date']=='2020-04-28']['date_ordinal']
OrangeDate = int(OrangeDate)

YellowDate = UT[UT['date']=='2020-05-14']['date_ordinal']
YellowDate = int(YellowDate)

ProtestDate = UT[UT['date']=='2020-05-30']['date_ordinal']
ProtestDate = int(ProtestDate)

fig, ax = plt.subplots(figsize = (12,6))
ax.bar(UT['date_ordinal'], UT['hospitalizedIncrease'], label='Hospitalized Increase',color='red')
ax.bar(UT['date_ordinal'], UT['TotMinusHosptializedIncresase'], label='Non-Hospitalized Increase',color='blue',bottom=UT['hospitalizedIncrease'])
ax.legend(loc='upper left')


new_labels = [date.fromordinal(int(item)) for item in ax.get_xticks()]
ax.set_xticklabels(labels=new_labels, rotation=90, ha='right',fontdict={'fontsize':12})


ax.axvline(x=OrangeDate, color='orange', linewidth=3, linestyle = '--')
ax.annotate('Code Orange Date', (OrangeDate - 2,340),color='gray',rotation=90,fontsize=13)
ax.axvline( x=YellowDate, color='yellow', linewidth=3, linestyle = '--')
ax.annotate('Code Yellow Date', (YellowDate - 2,340),color='gray',rotation=90,fontsize=13)
ax.axvline( x=ProtestDate, color='black', linewidth=3, linestyle = '--')
ax.annotate('Protest Start Date', (ProtestDate - 2 ,355),color='black',rotation=90,fontsize=13)

plt.title('Utah Positive Increase (non)Hospitalized', fontdict={'fontsize':20})
plt.xlabel('Date', fontdict={'fontsize':12})
plt.ylabel('Positive Increase', fontdict={'fontsize':12})
plt.axis('tight')
plt.savefig('Utah_Increase_Hospitalized.png')

plt.show()

# In[4]:



UT['rolling_mean'] = UT.loc[:,'positiveIncrease'].rolling(3).mean().shift(periods=-3)
UT['rolling_mean2'] = UT.loc[:,'positiveIncrease'].rolling(7).mean().shift(periods=-7)
UT['rolling_mean3'] = UT.loc[:,'positiveIncrease'].rolling(20).mean().shift(periods=-20)
#x_dates = UT['date'].dt.strftime('%m-%d').sort_values().unique()



fig, ax = plt.subplots(figsize = (12,6))
plt.bar(UT['date_ordinal'], UT['positiveIncrease'], label='Positive Increase',color='grey')
plt.plot(UT['date_ordinal'], UT.rolling_mean, label='3 Day Average', color='red')
plt.plot(UT['date_ordinal'], UT.rolling_mean2, label='7 Day Average', color='green')
plt.plot(UT['date_ordinal'], UT.rolling_mean3, label='20 Day Average', color='blue')


plt.legend(loc='upper left')
new_labels = [date.fromordinal(int(item)) for item in ax.get_xticks()]
ax.set_xticklabels(labels=new_labels, rotation=45, ha='right',fontdict={'fontsize':12})

ax.axvline(x=OrangeDate, color='orange', linewidth=3, linestyle = '--')
ax.annotate('Code Orange Date', (OrangeDate - 2,240),color='gray',rotation=90,fontsize=13)
ax.axvline( x=YellowDate, color='yellow', linewidth=3, linestyle = '--')
ax.annotate('Code Yellow Date', (YellowDate - 2,240),color='gray',rotation=90,fontsize=13)
ax.axvline( x=ProtestDate, color='black', linewidth=3, linestyle = '--')
ax.annotate('Protest Start Date', (ProtestDate - 3 ,240),color='black',rotation=90,fontsize=13)

plt.title('Utah Positive Increase Rolling Average', fontdict={'fontsize':20})
plt.xlabel('Date', fontdict={'fontsize':12})
plt.ylabel('Positive Increase', fontdict={'fontsize':12})
plt.axis('auto')

plt.savefig('Utah_Increase_Rolling_Avg.png')
plt.show()


# In[5]:


UT['rolling_mean_d'] = UT.loc[:,'deathIncrease'].rolling(3).mean().shift(periods=-2)
UT['rolling_mean_d2'] = UT.loc[:,'deathIncrease'].rolling(7).mean().shift(periods=-6)
UT['rolling_mean_d3'] = UT.loc[:,'deathIncrease'].rolling(20).mean().shift(periods=-19)
#x_dates = UT['date'].dt.strftime('%m-%d').sort_values().unique()
UT['date_ordinal'] = pd.to_datetime(UT['date']).apply(lambda date: date.toordinal())

fig, ax = plt.subplots(figsize = (12,6))
plt.bar(UT['date_ordinal'], UT['deathIncrease'], label='Death Increase',color='grey')
plt.plot(UT['date_ordinal'], UT.rolling_mean_d, label='3 Day Average', color='red')
plt.plot(UT['date_ordinal'], UT.rolling_mean_d2, label='7 Day Average', color='green')
plt.plot(UT['date_ordinal'], UT.rolling_mean_d3, label='20 Day Average', color='blue')
plt.legend(loc='upper left')
new_labels = [date.fromordinal(int(item)) for item in ax.get_xticks()]
ax.set_xticklabels(labels=new_labels, rotation=90, ha='right',fontdict={'fontsize':12})
plt.title('Utah Death Increase Rolling Average', fontdict={'fontsize':20})
plt.xlabel('Date', fontdict={'fontsize':12})
plt.ylabel('Death Increase', fontdict={'fontsize':12})
plt.axis('tight')
plt.savefig('Utah_Death_Rolling_Avg.png')
plt.show()

#%%

UT_1 = UT[UT['date'] >= '2020-04-05' ]

UT_1['rolling_mean'] = UT_1.loc[:,'PosPerTest'].rolling(3).mean().shift(periods= -3)
UT_1['rolling_mean2'] = UT_1.loc[:,'PosPerTest'].rolling(7).mean().shift(periods= -7)
UT_1['rolling_mean3'] = UT_1.loc[:,'PosPerTest'].rolling(20).mean().shift(periods= -20)

fig, ax = plt.subplots(figsize = (12,6)) 


fig = sns.regplot(x = 'date_ordinal', y = 'PosPerTest', data = UT, fit_reg=False)
plt.plot(UT_1['date_ordinal'], UT_1.rolling_mean, label='3 Day Average', color='red')
plt.plot(UT_1['date_ordinal'], UT_1.rolling_mean2, label='7 Day Average', color='green')
plt.plot(UT_1['date_ordinal'], UT_1.rolling_mean3, label='20 Day Average', color='blue')

plt.legend(loc='upper right')
ax.set_xlim(UT_1['date_ordinal'].min() , UT_1['date_ordinal'].max() )
ax.set_ylim(0,0.3)
new_labels = [date.fromordinal(int(item)) for item in ax.get_xticks()]
plt.title('UT Positve Per Test', fontdict={'fontsize':20})
plt.xlabel('Date', fontdict={'fontsize':12})
plt.ylabel('Positive/Test', fontdict={'fontsize':12})
ax.set_xticklabels(new_labels, rotation = 45)

plt.savefig('UT_Positive_Per_Test.png')
plt.show()



# In[6]:


fig, ax = plt.subplots(figsize = (12,6))    
fig = sns.pointplot(x = 'date', y = 'positive',
                    data = UT, markers = '.')

x_dates = UT['date'].dt.strftime('%m-%d').sort_values().unique()
ax.set_xticklabels(labels=x_dates, rotation=90, ha='right',
                   fontdict={'fontsize':12})
plt.title('Utah Total Cases', fontdict={'fontsize':20})
plt.xlabel('Date', fontdict={'fontsize':12})
plt.ylabel('Tot. Cases', fontdict={'fontsize':12})

#plt.savefig('Utah Total Cases.png')
plt.show()


# In[7]:


fig, ax = plt.subplots(figsize = (12,6))    
fig = sns.pointplot(x = 'date', y = 'positive',
                    data = UT, markers='.')

x_dates = UT['date'].dt.strftime('%m-%d').sort_values().unique()
ax.set_xticklabels(labels=x_dates, rotation=90, ha='right',fontdict={'fontsize':12})
plt.title('Utah Total Cases (log)', fontdict={'fontsize':20})
plt.xlabel('Date', fontdict={'fontsize':12})
plt.ylabel('Tot. Cases', fontdict={'fontsize':12})
ax.set( yscale='log')

#plt.savefig('Utah Total Cases (log).png')
plt.show()


# ## Investigating the percentage of tests that return positive results:
# ### If this number remains high it shows that we are not testing enough. 


# In[9]:


FourC = UT.append(df[df['state']=='ID']).append(df[df['state']=='CO']).append(df[df['state']=='AZ']).append(df[df['state']=='NM']).append(df[df['state']=='NV']).append(df[df['state']=='WY'])


# In[10]:


fig, ax = plt.subplots(figsize = (12,6))    
fig = sns.pointplot(x = 'date', y = 'positive',hue='state',
                    data = FourC, palette = 'Set1', markers ='.')

x_dates = FourC['date'].dt.strftime('%m-%d').sort_values().unique()
ax.set_xticklabels(labels=x_dates, rotation=90, ha='right',fontdict={'fontsize':12})
plt.title('Nearest States: Total', fontdict={'fontsize':20})
plt.xlabel('Date', fontdict={'fontsize':12})
plt.ylabel('Tot. Cases', fontdict={'fontsize':12})

#plt.savefig('Four Corners Total Cases.png')
plt.show()


# In[11]:


fig, ax = plt.subplots(figsize = (12,6))    
fig = sns.pointplot(x = 'date', y = 'death',hue='state', 
                    data = FourC, palette = 'Set1', markers ='.')

x_dates = FourC['date'].dt.strftime('%m-%d').sort_values().unique()
ax.set_xticklabels(labels=x_dates, rotation=90, ha='right',fontdict={'fontsize':12})
plt.title('Nearest States: Death Total', fontdict={'fontsize':20})
plt.xlabel('Date', fontdict={'fontsize':12})
plt.ylabel('Tot. Deaths', fontdict={'fontsize':12})


plt.show()




fig, ax = plt.subplots(figsize = (12,6))    
fig = sns.pointplot(x = 'date', y = 'DperP',hue='state',
                    data = FourC, palette = 'Set1', markers ='.')

x_dates = FourC['date'].dt.strftime('%m-%d').sort_values().unique()
ax.set_xticklabels(labels=x_dates, rotation=90, ha='right',fontdict={'fontsize':12})
plt.title('Nearest States: Deaths per Case', fontdict={'fontsize':20})
plt.xlabel('Date', fontdict={'fontsize':12})
plt.ylabel('Death per Case', fontdict={'fontsize':12})


plt.show()




CA = df[df['state']=='CA']
CA.to_excel('CA.xlsx')



CA['rolling_mean'] = CA.loc[:,'positiveIncrease'].rolling(3).mean().shift(periods=-2)
CA['rolling_mean2'] = CA.loc[:,'positiveIncrease'].rolling(7).mean().shift(periods=-6)
CA['rolling_mean3'] = CA.loc[:,'positiveIncrease'].rolling(20).mean().shift(periods=-19)
#x_dates = UT['date'].dt.strftime('%m-%d').sort_values().unique()
CA['date_ordinal'] = pd.to_datetime(CA['date']).apply(lambda date: date.toordinal())

fig, ax = plt.subplots(figsize = (12,6))
plt.bar(CA['date_ordinal'], CA['positiveIncrease'], label='Positive Increase',color='grey')
plt.plot(CA['date_ordinal'], CA.rolling_mean, label='3 Day Average', color='red')
plt.plot(CA['date_ordinal'], CA.rolling_mean2, label='7 Day Average', color='green')
plt.plot(CA['date_ordinal'], CA.rolling_mean3, label='20 Day Average', color='blue')
plt.legend(loc='upper left')

new_labels = [date.fromordinal(int(item)) for item in ax.get_xticks()]
ax.set_xlim(CA['date_ordinal'].min() , CA['date_ordinal'].max() )
ax.set_xticklabels(labels=new_labels, rotation=90, ha='right',fontdict={'fontsize':12})
plt.title('California Positive Increase Rolling Average', fontdict={'fontsize':20})
plt.xlabel('Date', fontdict={'fontsize':12})
plt.ylabel('Positive Increase', fontdict={'fontsize':12})
plt.axis('tight')
plt.savefig('CA_Increase_Rolling_Avg.png')


ax.axvline(x=OrangeDate, color='orange', linewidth=3, linestyle = '--')
ax.annotate('Code Orange Date', (OrangeDate - 2,2500),color='gray',rotation=90,fontsize=13)
ax.axvline( x=YellowDate, color='yellow', linewidth=3, linestyle = '--')
ax.annotate('Code Yellow Date', (YellowDate - 2,2500),color='gray',rotation=90,fontsize=13)
ax.axvline( x=ProtestDate, color='black', linewidth=3, linestyle = '--')
ax.annotate('Protest Start Date', (ProtestDate - 2 ,2700),color='black',rotation=90,fontsize=13)


plt.show()
 


CA['rolling_mean_d'] = CA.loc[:,'deathIncrease'].rolling(3).mean().shift(periods=-2)
CA['rolling_mean_d2'] = CA.loc[:,'deathIncrease'].rolling(7).mean().shift(periods=-6)
CA['rolling_mean_d3'] = CA.loc[:,'deathIncrease'].rolling(20).mean().shift(periods=-19)
#x_dates = UT['date'].dt.strftime('%m-%d').sort_values().unique()
CA['date_ordinal'] = pd.to_datetime(CA['date']).apply(lambda date: date.toordinal())

fig, ax = plt.subplots(figsize = (12,6))

plt.bar(CA['date_ordinal'], CA['deathIncrease'], label='Death Increase',color='grey')
plt.plot(CA['date_ordinal'], CA.rolling_mean_d, label='3 Day Average', color='red')
plt.plot(CA['date_ordinal'], CA.rolling_mean_d2, label='7 Day Average', color='green')
plt.plot(CA['date_ordinal'], CA.rolling_mean_d3, label='20 Day Average', color='blue')
plt.legend(loc='upper left')
new_labels = [date.fromordinal(int(item)) for item in ax.get_xticks()]
ax.set_xlim(CA['date_ordinal'].min() , CA['date_ordinal'].max() )
ax.set_xticklabels(labels=new_labels, rotation=45, ha='right',fontdict={'fontsize':12})
plt.title('California Death Increase Rolling Average', fontdict={'fontsize':20})
plt.xlabel('Date', fontdict={'fontsize':12})
plt.ylabel('Death Increase', fontdict={'fontsize':12})
plt.axis('tight')

plt.savefig('CA_Death_Rolling_Avg.png')
plt.show()


#%%

CA_1 = CA[CA['date'] >= '2020-04-15' ]
#CA_1 = CA


CA_1['rolling_mean'] = CA_1.loc[:,'PosPerTest'].rolling(3).mean().shift(periods=-3)
CA_1['rolling_mean2'] = CA_1.loc[:,'PosPerTest'].rolling(7).mean().shift(periods=-7)
CA_1['rolling_mean3'] = CA_1.loc[:,'PosPerTest'].rolling(20).mean().shift(periods=-20)

fig, ax = plt.subplots(figsize = (12,6)) 


fig = sns.regplot(x = 'date_ordinal', y = 'PosPerTest', data = CA, fit_reg=False)

plt.plot(CA_1['date_ordinal'], CA_1.rolling_mean, label='3 Day Average', color='red')
plt.plot(CA_1['date_ordinal'], CA_1.rolling_mean2, label='7 Day Average', color='green')
plt.plot(CA_1['date_ordinal'], CA_1.rolling_mean3, label='20 Day Average', color='blue')

plt.legend(loc='upper right')
ax.set_xlim(CA_1['date_ordinal'].min() , CA_1['date_ordinal'].max() )
ax.set_ylim(0,0.5)
new_labels = [date.fromordinal(int(item)) for item in ax.get_xticks()]
plt.title('CA Positve Per Test', fontdict={'fontsize':20})
plt.xlabel('Date', fontdict={'fontsize':12})
plt.ylabel('Positive/Test', fontdict={'fontsize':12})
ax.set_xticklabels(new_labels, rotation = 45)




plt.savefig('CA_Positive_Per_Test.png')
plt.show()



