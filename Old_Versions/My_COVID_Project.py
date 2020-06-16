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
from matplotlib.dates import DateFormatter
from sklearn.linear_model import LinearRegression

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
df['PosPerTest']= df['positiveIncrease']/df['totalTestResultsIncrease']*100
df['TotMinusHosptializedIncresase'] = np.abs(df['positiveIncrease'] - df['hospitalizedIncrease'])


df['date'] = pd.to_datetime(df['date'], format = '%Y%m%d')

df.set_index('date')



plt.close('all')
df.to_excel('df.xlsx')


# In[3]:
                 ### Subset the data for specific states ### 
sns.set()
# First we look at Utah

def watermark(loc_x = 0.92, loc_y =0.15):
    """ Puts Property Of David McKenna on LRH corner of plots"""
    
    fig.text(loc_x,loc_y, 'Property of David McKenna \n data from: covidtracking.com',
         fontsize=10, color='gray', rotation=270,
         ha='right', va='bottom', alpha=0.75)
    

UT = df[df['state']=='UT']
UT= UT[UT['date'] >= '2020-03-15' ]

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


#%%
# Create date ordinal for simplicity of plot labels
UT['date_ordinal'] = pd.to_datetime(UT['date']).apply(lambda date: date.toordinal())

OrangeDate = UT[UT['date']=='2020-04-28']['date_ordinal']
OrangeDate = int(OrangeDate)

YellowDate = UT[UT['date']=='2020-05-14']['date_ordinal']
YellowDate = int(YellowDate)

MemorialDay = UT[UT['date']=='2020-05-25']['date_ordinal']
MemorialDay = int(MemorialDay)

ProtestDate = UT[UT['date']=='2020-05-29']['date_ordinal']
ProtestDate = int(ProtestDate)

text_loc = max(UT['positiveIncrease'])-250

fig, ax = plt.subplots(figsize = (12,6))
watermark()

ax.bar(UT['date_ordinal'], UT['positiveIncrease'], label='Case Increase',color='blue')
ax.bar(UT['date_ordinal'], UT['hospitalizedIncrease'], 
       label='Hospitalized Increase',color='red')

ax.legend(loc='upper left')


new_labels = [date.fromordinal(int(item)) for item in ax.get_xticks()]
ax.set_xticklabels(labels=new_labels, rotation=30, ha='right',fontdict={'fontsize':12})

ax.axvline(x=OrangeDate, color='orange', linewidth=2)
ax.annotate('Code Orange Date', (OrangeDate - 2,text_loc),color='black',rotation=90,fontsize=13)
ax.axvline( x=YellowDate, color='yellow', linewidth=2)
ax.annotate('Code Yellow Date', (YellowDate - 2,text_loc),color='black',rotation=90,fontsize=13)
ax.axvline( x=MemorialDay, color='red', linewidth=1.5)
ax.annotate('Memorial Day', (MemorialDay - 2 ,text_loc),color='black',rotation=90,fontsize=13)
ax.axvline( x=ProtestDate, color='purple', linewidth=1.5)
ax.annotate('Protest Start Date', (ProtestDate - 2 ,text_loc),color='black',rotation=90,fontsize=13)



ax.axvline(x=OrangeDate + 7, color='orange', linewidth=2, linestyle = '--')
ax.annotate('Code Orange + 7-Days', (OrangeDate +5,text_loc),color='black',rotation=90,fontsize=13)
ax.axvline( x=YellowDate + 7, color='yellow', linewidth=2, linestyle = '--')
ax.axvline( x=ProtestDate + 7, color='purple', linewidth=2, linestyle = '--')


plt.title('Utah Case Increase (non)Hospitalized', fontdict={'fontsize':20})
plt.xlabel('Date', fontdict={'fontsize':12})
plt.ylabel('Case Increase', fontdict={'fontsize':12})
plt.axis('tight')
plt.savefig('Utah_Increase_Hospitalized.png')

plt.show()

# In[4]:



UT['rolling_mean'] = UT.loc[:,'positiveIncrease'].rolling(3).mean().shift(periods=-3)
UT['rolling_mean2'] = UT.loc[:,'positiveIncrease'].rolling(7).mean().shift(periods=-7)
UT['rolling_mean3'] = UT.loc[:,'positiveIncrease'].rolling(20).mean().shift(periods=-20)
#x_dates = UT['date'].dt.strftime('%m-%d').sort_values().unique()




fig, ax = plt.subplots(figsize = (12,6))
watermark()


plt.bar(UT['date_ordinal'], UT['positiveIncrease'], label='Positive Increase',color='grey')
plt.plot(UT['date_ordinal'], UT.rolling_mean, label='3 Day Average', color='red')
plt.plot(UT['date_ordinal'], UT.rolling_mean2, label='7 Day Average', color='green')
plt.plot(UT['date_ordinal'], UT.rolling_mean3, label='20 Day Average', color='blue')


plt.legend(loc='upper left')
new_labels = [date.fromordinal(int(item)) for item in ax.get_xticks()]
ax.set_xticklabels(labels=new_labels, rotation=30, ha='right',fontdict={'fontsize':12})

ax.axvline(x=OrangeDate, color='orange', linewidth=2)
ax.annotate('Code Orange Date', (OrangeDate - 2,text_loc),color='black',rotation=90,fontsize=13)
ax.axvline( x=YellowDate, color='yellow', linewidth=2)
ax.annotate('Code Yellow Date', (YellowDate - 2,text_loc),color='black',rotation=90,fontsize=13)
ax.axvline( x=MemorialDay, color='red', linewidth=1.5)
ax.annotate('Memorial Day', (MemorialDay - 2 ,text_loc),color='black',rotation=90,fontsize=13)
ax.axvline( x=ProtestDate, color='purple', linewidth=1.5)
ax.annotate('Protest Start Date', (ProtestDate - 2 ,text_loc),color='black',rotation=90,fontsize=13)
ax.axvline(x=OrangeDate + 7, color='orange', linewidth=2, linestyle = '--')
ax.annotate('Code Orange + 7-Days', (OrangeDate +5,text_loc),color='black',rotation=90,fontsize=13)

ax.axvline( x=YellowDate + 7, color='yellow', linewidth=2, linestyle = '--')
ax.axvline( x=ProtestDate + 7, color='purple', linewidth=2, linestyle = '--')


plt.title('Utah Case Increase Rolling Average', fontdict={'fontsize':20})
plt.xlabel('Date', fontdict={'fontsize':12})
plt.ylabel('Case Increase', fontdict={'fontsize':12})
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
watermark()

plt.bar(UT['date_ordinal'], UT['deathIncrease'], label='Death Increase',color='grey')
plt.plot(UT['date_ordinal'], UT.rolling_mean_d, label='3 Day Average', color='red')
plt.plot(UT['date_ordinal'], UT.rolling_mean_d2, label='7 Day Average', color='green')
plt.plot(UT['date_ordinal'], UT.rolling_mean_d3, label='20 Day Average', color='blue')
plt.legend(loc='upper left')
new_labels = [date.fromordinal(int(item)) for item in ax.get_xticks()]
ax.set_xticklabels(labels=new_labels, rotation=30, ha='right',fontdict={'fontsize':12})
plt.title('Utah Deaths Increase Rolling Average', fontdict={'fontsize':20})
plt.xlabel('Date', fontdict={'fontsize':12})
plt.ylabel('Deaths Increase', fontdict={'fontsize':12})
plt.axis('tight')
plt.savefig('Utah_Death_Rolling_Avg.png')
plt.show()

#%%

# ## Investigating the percentage of tests that return positive results:
# ### If this number remains high it shows that we are not testing enough. 

UT_1 = UT[UT['date'] >= '2020-04-15' ]

UT_1['rolling_mean'] = UT_1.loc[:,'PosPerTest'].rolling(3).mean().shift(periods= -3)
UT_1['rolling_mean2'] = UT_1.loc[:,'PosPerTest'].rolling(7).mean().shift(periods= -7)
UT_1['rolling_mean3'] = UT_1.loc[:,'PosPerTest'].rolling(20).mean().shift(periods= -20)


fig, ax = plt.subplots(figsize = (12,6))
watermark()

fig = sns.regplot(x = 'date_ordinal', y = 'PosPerTest', data = UT, fit_reg=False)
plt.plot(UT_1['date_ordinal'], UT_1.rolling_mean, label='3 Day Average', color='red')
plt.plot(UT_1['date_ordinal'], UT_1.rolling_mean2, label='7 Day Average', color='green')
plt.plot(UT_1['date_ordinal'], UT_1.rolling_mean3, label='20 Day Average', color='blue')

plt.legend(loc='upper right')
ax.set_xlim(UT_1['date_ordinal'].min() , UT_1['date_ordinal'].max()+1 )
ax.set_ylim(0,30)
new_labels = [date.fromordinal(int(item)) for item in ax.get_xticks()]
plt.title('UT Positve Per Test', fontdict={'fontsize':20})
plt.xlabel('Date', fontdict={'fontsize':12})
plt.ylabel('Positive/Test', fontdict={'fontsize':12})
ax.set_xticklabels(new_labels, rotation = 30)

plt.savefig('UT_Positive_Per_Test.png')
plt.show()



#%%
UT_1= UT[UT['date'] >= '2020-04-15' ]

UT_1['rolling_mean3'] = UT_1.loc[:,'PosPerTest'].rolling(20).mean().shift(periods= -20)
UT_1['rolling_mean2'] = UT_1.loc[:,'PosPerTest'].rolling(7).mean().shift(periods= -7)

X = UT_1['date_ordinal']
Y = UT_1['totalTestResultsIncrease']
X = np.array(X).reshape(-1,1)


X_i = UT_1['date_ordinal']
X_i = np.array(X).reshape(-1,1)
X_t = X_i
Y_i = UT_1['totalTestResultsIncrease']
Y_t = UT_1['positiveIncrease']
X = np.array(X).reshape(-1,1)
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(X_t, Y_i)  # perform linear regression
Y_i_pred = linear_regressor.predict(X)  # make predictions


linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(X_t, Y_t)  # perform linear regression
Y_t_pred = linear_regressor.predict(X)  # make predictions
 

sns.set_style("dark")                    
fig, ax1 = plt.subplots(figsize = (12,6))

plt.title('UT Tests and Positive per Test', fontdict={'fontsize':20})
watermark()

color = 'gray'

ax1.bar(UT_1['date_ordinal'], UT_1['totalTestResultsIncrease'], 
        label='Total Tests',color='gray',alpha=0.50)
ax1.bar(UT_1['date_ordinal'], UT_1['positiveIncrease'], 
        label='Positive Tests',color='red',alpha=0.55)
ax1.plot(UT_1['date_ordinal'],Y_i_pred, color='black',
         linestyle = '--', linewidth = 3, label = 'Linear Regression Tests')
ax1.plot(UT_1['date_ordinal'],Y_t_pred, color='purple',
         linestyle = '--', linewidth = 3,label = 'Linear Regression Increase')
ax1.tick_params(axis='y', labelcolor=color)
ax1.legend(loc='upper left')
ax2 = plt.ylabel('Tests', fontdict={'fontsize':12},color=color)
new_labels = [date.fromordinal(int(item)) for item in ax1.get_xticks()]
ax1.set_xticklabels(new_labels, rotation = 30)

ax2 = ax1.twinx() 

color = 'green'
ax2 = plt.scatter(UT_1['date_ordinal'], UT_1['PosPerTest'],
                  marker='+',s=100,color=color ,label='Percent Positive Tests')
ax2=plt.plot(UT_1['date_ordinal'], UT_1.rolling_mean2, label='7 Day Average', color='green')
#ax2 =plt.plot(UT_1['date_ordinal'], UT_1.rolling_mean3, label='20 Day Average', color='blue')
ax2 = plt.ylabel('Positive/Test', fontdict={'fontsize':12},color=color)
ax2=plt.tick_params(axis='y', labelcolor=color)
ax2 = plt.ylim(0,25)
ax2 = plt.legend(loc='upper right')



fig=plt.tight_layout()

plt.savefig('UT_Test_+_Positive_Per_Test.png')




plt.show()


#%%
sns.set()
# UT = df[df['state']=='UT']

# UT.to_excel('UT.xlsx')

# UT['date_ordinal'] = pd.to_datetime(UT['date']).apply(lambda date: date.toordinal())

OrangeDate = UT[UT['date']=='2020-04-28']['date_ordinal']
OrangeDate = int(OrangeDate)

YellowDate = UT[UT['date']=='2020-05-14']['date_ordinal']
YellowDate = int(YellowDate)

ProtestDate = UT[UT['date']=='2020-05-29']['date_ordinal']
ProtestDate = int(ProtestDate)


fig, ax = plt.subplots(figsize = (12,6))
watermark()

ax.bar(UT['date_ordinal'], UT['totalTestResultsIncrease'],
       label='Total Test Increase',color='green',alpha=0.75)
ax.bar(UT['date_ordinal'], UT['positiveIncrease'],
       label='Positive Tests',color='red',alpha=0.75)


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


plt.title('Utah Test Tests Per Day', fontdict={'fontsize':20})
plt.xlabel('Date', fontdict={'fontsize':12})
plt.ylabel('Tests', fontdict={'fontsize':12})
plt.axis('tight')
plt.savefig('Utah_Increase_Test.png')

plt.show()

#%%
    
UT_1.sort_index()

UT_1['PreviousDayICU'] = UT_1['inIcuCumulative'].shift(-1)

for row in UT_1.iterrows() :
    UT_1['icuIncrease'] = UT_1['inIcuCumulative'] - UT_1['PreviousDayICU']

UT_1.drop(columns = 'PreviousDayICU',inplace=True)

UT= UT[UT['date'] >= '2020-04-15' ]
                                   
fig, ax = plt.subplots(figsize = (12,6))
watermark()
ax.bar(UT_1['date_ordinal'], UT_1['hospitalizedIncrease'],
       label='Total Hospital Increase',color='blue',alpha=0.75)
ax.bar(UT_1['date_ordinal'], UT_1['icuIncrease'],
       label='ICU Increase',color='red',alpha=0.75)
ax.legend(loc='upper left')
plt.title('Hospitalizations and ICU Increase', fontdict={'fontsize':20})
plt.ylabel('Hospitalized Cases', fontdict={'fontsize':12})

new_labels = [date.fromordinal(int(item)) for item in ax.get_xticks()]
ax.set_xticklabels(labels=new_labels, rotation=30, ha='right',fontdict={'fontsize':12})
ax.axvline(x=OrangeDate, color='orange', linewidth=2)
ax.annotate('Code Orange Date', (OrangeDate - 2,19.5),color='black',rotation=90,fontsize=13)
ax.axvline( x=YellowDate, color='yellow', linewidth=2)
ax.annotate('Code Yellow Date', (YellowDate - 2,19.5),color='black',rotation=90,fontsize=13)
ax.axvline( x=ProtestDate, color='purple', linewidth=1.5)
ax.annotate('Protest Start Date', (ProtestDate - 1 ,20),color='black',rotation=90,fontsize=13)

ax.axvline(x=OrangeDate + 7, color='orange', linewidth=2, linestyle = '--')
ax.annotate('Code Orange + 7-Days', (OrangeDate +8,16.5),color='black',rotation=90,fontsize=13)
ax.axvline( x=YellowDate + 7, color='yellow', linewidth=2, linestyle = '--')
ax.axvline( x=ProtestDate + 7, color='purple', linewidth=2, linestyle = '--')

plt.savefig('ICU.png')
plt.show()





#%%
df['Date'] = pd.to_datetime(df['date'].astype(str), infer_datetime_format=True)
fc = df[df['state'].isin(['UT','AZ','CO','NM'])]
fc = fc[fc['Date']>= '03-15-2020']

fig, ax = plt.subplots(figsize = (12,6)) 
watermark()
fig = fc.groupby(['Date','state']).sum()['DperP'].unstack().plot(ax=ax)

       

# Define the date format
date_form = DateFormatter("%m-%d")
ax.xaxis.set_major_formatter(date_form)

# Ensure a major tick for each week using (interval=1) 
ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
plt.xticks(rotation=30)

plt.title('Nearest States: Deaths per Case', fontdict={'fontsize':20})
plt.xlabel('Date', fontdict={'fontsize':12})
plt.ylabel('Death per Case', fontdict={'fontsize':12})


plt.show()

#%%

fig, ax = plt.subplots(figsize = (12,6)) 
watermark()
fig = fc.groupby(['Date','state']).sum()['death'].unstack().plot(ax=ax)

       

# Define the date format
date_form = DateFormatter("%m-%d")
ax.xaxis.set_major_formatter(date_form)

# Ensure a major tick for each week using (interval=1) 
ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
plt.xticks(rotation=30)

plt.title('Nearest States: Total Deaths' , fontdict={'fontsize':20})
plt.xlabel('Date', fontdict={'fontsize':12})
plt.ylabel('Deaths', fontdict={'fontsize':12})


plt.show()



#%%

CA = df[df['state']=='CA']
#CA.to_excel('CA.xlsx')
text_loc = max(CA['positiveIncrease'])-1000


CA['rolling_mean'] = CA.loc[:,'positiveIncrease'].rolling(3).mean().shift(periods=-2)
CA['rolling_mean2'] = CA.loc[:,'positiveIncrease'].rolling(7).mean().shift(periods=-6)
CA['rolling_mean3'] = CA.loc[:,'positiveIncrease'].rolling(20).mean().shift(periods=-19)
#x_dates = UT['date'].dt.strftime('%m-%d').sort_values().unique()
CA['date_ordinal'] = pd.to_datetime(CA['date']).apply(lambda date: date.toordinal())


fig, ax = plt.subplots(figsize = (12,6))
watermark()

plt.bar(CA['date_ordinal'], CA['positiveIncrease'], label='Positive Increase',color='grey')
plt.plot(CA['date_ordinal'], CA.rolling_mean, label='3 Day Average', color='red')
plt.plot(CA['date_ordinal'], CA.rolling_mean2, label='7 Day Average', color='green')
plt.plot(CA['date_ordinal'], CA.rolling_mean3, label='20 Day Average', color='blue')
plt.legend(loc='upper left')

new_labels = [date.fromordinal(int(item)) for item in ax.get_xticks()]
ax.set_xlim(CA['date_ordinal'].min() , CA['date_ordinal'].max() )
ax.set_xticklabels(labels=new_labels, rotation=30, ha='right',fontdict={'fontsize':12})
plt.title('California Positive Increase Rolling Average', fontdict={'fontsize':20})
plt.xlabel('Date', fontdict={'fontsize':12})
plt.ylabel('Positive Increase', fontdict={'fontsize':12})
plt.axis('tight')
plt.savefig('CA_Increase_Rolling_Avg.png')

ax.axvline( x=MemorialDay, color='red', linewidth=1.5)
ax.annotate('Memorial Day', (MemorialDay - 2 ,text_loc),color='black',rotation=90,fontsize=13)
ax.axvline( x=ProtestDate, color='black', linewidth=3)
ax.axvline( x=ProtestDate + 7, color='black', linewidth=3, linestyle = '--')
ax.annotate('Protest Start Date', (ProtestDate - 2 ,text_loc),color='black',rotation=90,fontsize=13)
plt.savefig('CA_Case_Rolling_Avg.png')
plt.show()
 

CA['rolling_mean_d'] = CA.loc[:,'deathIncrease'].rolling(3).mean().shift(periods=-2)
CA['rolling_mean_d2'] = CA.loc[:,'deathIncrease'].rolling(7).mean().shift(periods=-6)
CA['rolling_mean_d3'] = CA.loc[:,'deathIncrease'].rolling(20).mean().shift(periods=-19)
CA['date_ordinal'] = pd.to_datetime(CA['date']).apply(lambda date: date.toordinal())

fig, ax = plt.subplots(figsize = (12,6))
watermark()


plt.bar(CA['date_ordinal'], CA['deathIncrease'], label='Death Increase',color='grey')
plt.plot(CA['date_ordinal'], CA.rolling_mean_d, label='3 Day Average', color='red')
plt.plot(CA['date_ordinal'], CA.rolling_mean_d2, label='7 Day Average', color='green')
plt.plot(CA['date_ordinal'], CA.rolling_mean_d3, label='20 Day Average', color='blue')
plt.legend(loc='upper left')
new_labels = [date.fromordinal(int(item)) for item in ax.get_xticks()]


ax.set_xlim(CA['date_ordinal'].min() , CA['date_ordinal'].max() )
ax.set_xticklabels(labels=new_labels, rotation=30, ha='right',fontdict={'fontsize':12})
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
watermark()

fig = sns.regplot(x = 'date_ordinal', y = 'PosPerTest', data = CA, fit_reg=False)
plt.plot(CA_1['date_ordinal'], CA_1.rolling_mean, label='3 Day Average', color='red')
plt.plot(CA_1['date_ordinal'], CA_1.rolling_mean2, label='7 Day Average', color='green')
plt.plot(CA_1['date_ordinal'], CA_1.rolling_mean3, label='20 Day Average', color='blue')

plt.legend(loc='upper right')
ax.set_xlim(CA_1['date_ordinal'].min() , CA_1['date_ordinal'].max()+ 1 )
ax.set_ylim(0,25)
new_labels = [date.fromordinal(int(item)) for item in ax.get_xticks()]
plt.title('CA Positve Per Test', fontdict={'fontsize':20})
plt.xlabel('Date', fontdict={'fontsize':12})
plt.ylabel('Positive/Test', fontdict={'fontsize':12})
ax.set_xticklabels(new_labels, rotation = 30)


plt.savefig('CA_Positive_Per_Test.png')
plt.show()


#%%

df_1 = df[['state','date','positiveIncrease','deathIncrease']].reset_index()

today = str(df.date.max())

df_1['date_mod'] = pd.to_datetime(df_1['date'], format= '%Y%m%d')
df_1.set_index(['state','date_mod'],inplace=True)
df_1.sort_index(inplace=True)
df_1['date_ordinal'] = pd.to_datetime(df_1['date']).apply(lambda date: date.toordinal())
df_1['posDiff'] = df_1.groupby(level='state')['positiveIncrease'].apply(lambda x: (x.rolling(7).sum() / 7))

largest = df_1[df_1['date']==today]['posDiff'].nlargest(10).astype(int)
fig, ax = plt.subplots(figsize = (12,6))
watermark()

df_2 = pd.DataFrame(largest).reset_index()
plt.bar(df_2.state,df_2.posDiff)
plt.title('States with Largest 7 day Avg Increase', fontsize=16)
plt.ylabel('7 Day Avg Case Increase')

plt.savefig('Top_Ten_Increase.png')



