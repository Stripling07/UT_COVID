#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 11:08:59 2020

@author: davidr.mckenna
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import datetime as dt

    

    
def Merge_Pop(df_to_merge):
    #Define names of columns to be used and dropped
    names = ['State','Census','Estimates Base','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019']
    drop = ['Census','Estimates Base','2010','2011','2012','2013','2014','2015','2016','2017','2018']
    # Import the data and clean
    pop = pd.read_excel('pop_data.xlsx',header=4,names=names)
    pop.drop(columns=drop,inplace=True) #drop the unused columns
    
    states = {
        'AK': '.Alaska',
        'AL': '.Alabama',
        'AR': '.Arkansas',
        'AS': '.American Samoa',
        'AZ': '.Arizona',
        'CA': '.California',
        'CO': '.Colorado',
        'CT': '.Connecticut',
        'DC': '.District of Columbia',
        'DE': '.Delaware',
        'FL': '.Florida',
        'GA': '.Georgia',
        'GU': '.Guam',
        'HI': '.Hawaii',
        'IA': '.Iowa',
        'ID': '.Idaho',
        'IL': '.Illinois',
        'IN': '.Indiana',
        'KS': '.Kansas',
        'KY': '.Kentucky',
        'LA': '.Louisiana',
        'MA': '.Massachusetts',
        'MD': '.Maryland',
        'ME': '.Maine',
        'MI': '.Michigan',
        'MN': '.Minnesota',
        'MO': '.Missouri',
        'MP': '.Northern Mariana Islands',
        'MS': '.Mississippi',
        'MT': '.Montana',
        'NA': '.National',
        'NC': '.North Carolina',
        'ND': '.North Dakota',
        'NE': '.Nebraska',
        'NH': '.New Hampshire',
        'NJ': '.New Jersey',
        'NM': '.New Mexico',
        'NV': '.Nevada',
        'NY': '.New York',
        'OH': '.Ohio',
        'OK': '.Oklahoma',
        'OR': '.Oregon',
        'PA': '.Pennsylvania',
        'PR': '.Puerto Rico',
        'RI': '.Rhode Island',
        'SC': '.South Carolina',
        'SD': '.South Dakota',
        'TN': '.Tennessee',
        'TX': '.Texas',
        'UT': '.Utah',
        'VA': '.Virginia',
        'VI': '.Virgin Islands',
        'VT': '.Vermont',
        'WA': '.Washington',
        'WI': '.Wisconsin',
        'WV': '.West Virginia',
        'WY': '.Wyoming'
        }

    #Subset the dataset with only the columns of interest, this speeds up the merge:

    # Subset the dataset with only the columns of interest, this speeds up the merge:
    #df_to_merge = df_to_merge[['state','date','positiveIncrease','deathIncrease','totalTestResultsIncrease']].reset_index()
    df_to_merge['full'] = df_to_merge['state'].map(states)

    # Merge datasets
    df_pop = pd.merge(df_to_merge,pop, left_on='full',right_on='State')
    df_pop.drop(columns=['full','State'],inplace=True)

    today = str(df_pop.date.max())
    # sort index by formated date
    df_pop['Date'] = pd.to_datetime(df_pop['date'], format= '%Y%m%d')
    df_pop.rename(columns={'2019': 'Population'},inplace=True)
    
    df_pop.sort_index(inplace=True)
    
    return df_pop

def States_Won(df):
    """Adds catagorical column of who won each state in 2016"""
    
    states_won = {
    'AK': 'Trump',
    'AL': 'Trump',
    'AR': 'Trump',
    'AZ': 'Trump',
    'CA': 'Clinton',
    'CO': 'Clinton',
    'CT': 'Clinton',
    'DC': 'Clinton',
    'DE': 'Clinton',
    'FL': 'Trump',
    'GA': 'Trump',
    'HI': 'Clinton',
    'IA': 'Trump',
    'ID': 'Trump',
    'IL': 'Clinton',
    'IN': 'Trump',
    'KS': 'Trump',
    'KY': 'Trump',
    'LA': 'Trump',
    'MA': 'Clinton',
    'MD': 'Clinton',
    'ME': 'Clinton',
    'MI': 'Trump',
    'MN': 'Clinton',
    'MO': 'Trump',
    'MS': 'Trump',
    'MT': 'Trump',
    'NC': 'Trump',
    'ND': 'Trump',
    'NE': 'Trump',
    'NH': 'Clinton',
    'NJ': 'Clinton',
    'NM': 'Clinton',
    'NV': 'Clinton',
    'NY': 'Clinton',
    'OH': 'Trump',
    'OK': 'Trump',
    'OR': 'Clinton',
    'PA': 'Trump',
    'RI': 'Clinton',
    'SC': 'Trump',
    'SD': 'Trump',
    'TN': 'Trump',
    'TX': 'Trump',
    'UT': 'Trump',
    'VA': 'Clinton',
    'VT': 'Clinton',
    'WA': 'Clinton',
    'WI': 'Trump',
    'WV': 'Trump',
    'WY': 'Trump'
    }
    # Add catagorical column that identifies if state was won by Trump or Clinton
    df['2016 Won By'] = df['state'].map(states_won)
    df_election = df[df['2016 Won By'].notna()] # Define df with states with no vote info (US Territories) removed
    df_election['2016 Won By'] = df_election['2016 Won By'].apply(lambda x: 'States Won By '+str(x))

    return df_election

def watermark(fig, loc_x = 0.92, loc_y =0.15):
    """ Puts Property Of David McKenna on LRH corner of plots"""
    
    fig.text(loc_x,loc_y, 'Property of David McKenna \n data from: covidtracking.com',
         fontsize=10, color='gray', rotation=270,
         ha='right', va='bottom', alpha=0.75)

    # Format the datetime x-axis tick marks    
def date_ticks(ax,df,interval = 7) :
    # Define the date format
    
    months = mdates.MonthLocator()  # every month
    mon_fmt = mdates.DateFormatter('%b')
    days = mdates.DayLocator(interval = interval)  # every 7 days
    day_fmt = mdates.DateFormatter('%d')

    # format the ticks
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(mon_fmt)
    ax.xaxis.set_minor_locator(days)
    ax.xaxis.set_minor_formatter(day_fmt)
    

    # # round to nearest day.
    # start = df['date'].min()
    # end = df['date'].max() + pd.DateOffset(1)
    # ax.set_xlim([start,end])
    ax.xaxis.set_tick_params(pad=15)
    # format the coords message box
    #ax.format_xdata = mdates.DateFormatter('%m-%d')
    ax.grid(True)


# Calculate the rolling averages of selected columns     
def Roll_Avg(df, col, interval) :
    """Calculate the rolling averages of interval duration of columns in df"""
    length = len(interval)
    
    for n in range(length) :
        # make new col called roll_col_interval
        new_col = 'roll_' + str(col) + '_'+ str(interval[n])
        
        df[new_col] = df.loc[:,col].rolling(interval[n]).mean().shift(periods= - interval[n])
        
def place_value(number): 
    return ("{:,}".format(number))


def State_Subset(state_abbrev,df, start_date = '2020-03-15') :
    #new_df = state_abbrev
    new_df = df[df['state']== state_abbrev]
    new_df = new_df[new_df['date']>= start_date]

    return new_df

def Basic_Analysis_Roll(df, state_abbrev, start_date = '2020-03-15', test_date='2020-04-15',ICU_date='2020-05-01'):
    """Plot Case Increase and Death Increase with 7 & 20 day rolling averages
        for the state_abbrev"""


    #subset the state of interest
    new_df = State_Subset(state_abbrev, df, start_date)
    interval = [7,20]#sets the intervals for the rolling averages
    
    #Calculate the rolling averages of positive Increase and deathIncrease
    Roll_Avg(new_df,'positiveIncrease',interval)
    Roll_Avg(new_df,'deathIncrease',interval)
    Roll_Avg(new_df,'PosPerTest',interval)
    Roll_Avg(new_df,'totalTestResultsIncrease',interval)


    sns.set()#set plot style to have grid
    
    # plot the positive increase figure 
    fig, ax = plt.subplots(figsize = (12,6))
    #watermark(fig)
    date_ticks(ax,new_df)
    plt.bar(new_df['date'], new_df['positiveIncrease'], label='Positive Increase',color='grey')
    plt.plot(new_df['date'], new_df.roll_positiveIncrease_7,
         label='7 Day Average', color='green')
    plt.plot(new_df['date'], new_df.roll_positiveIncrease_20,
         label='20 Day Average', color='blue')
    #annot_tot(new_df,'positiveIncrease','Cases')
    plt.legend(loc='upper left')
    plt.title( state_abbrev +' Case Increase Rolling Average', fontdict={'fontsize':20})
    plt.xlabel('Date', fontdict={'fontsize':12})
    plt.ylabel('Case Increase', fontdict={'fontsize':12})
    
    plt.show()
    
    #Plot the death increase figure
    fig, ax = plt.subplots(figsize = (12,6))
    #watermark(fig)
    date_ticks(ax, new_df)
    plt.bar(new_df['date'], new_df['deathIncrease'], label='Positive Increase',color='indianred')
    plt.plot(new_df['date'], new_df.roll_deathIncrease_7,
         label='7 Day Average', color='green')
    plt.plot(new_df['date'], new_df.roll_deathIncrease_20,
         label='20 Day Average', color='blue')
    plt.legend(loc='upper left')
    #annot_tot(new_df,'deathIncrease','Deaths')
    plt.title( state_abbrev +' Deaths Increase Rolling Average', fontdict={'fontsize':20})
    plt.xlabel('Date', fontdict={'fontsize':12})
    plt.ylabel('Case Increase', fontdict={'fontsize':12})

    plt.show()
    
    #create the test df so we can limit the dates to be considered for regression
    test_df = new_df[(new_df['PosPerTest']<50) & (new_df['PosPerTest']>0)]
    test_df = test_df[test_df['date']>= test_date]
    start = test_df[test_df['date'] == test_date]['date']
    end = test_df.date.max() + pd.DateOffset(1)
    


    #plot the overlaying plots:
    sns.set_style("dark")  # to remove grid lines because of the 2 y axis they overlap and are confusing                  
    fig, ax1 = plt.subplots(figsize = (12,6))

    plt.title(state_abbrev +' Tests and Positive per Test', fontdict={'fontsize':20})
    #watermark(fig,loc_x=0.94)
    date_ticks(ax,test_df,interval=5)
    color = 'gray'

    ax1.bar(test_df['date'], test_df['totalTestResultsIncrease'], 
        label='Total Tests',color='gray',alpha=0.5)
    ax1.bar(test_df['date'], test_df['positiveIncrease'], 
        label='Positive Tests',color='tab:red',alpha=0.6)
    ax1.plot(test_df['date'],test_df.roll_totalTestResultsIncrease_7, color='black',
        linestyle = '--', linewidth = 3, 
        label = 'Total Tests Rolling 7-day Avg')
    ax1.plot(test_df['date'],test_df.roll_positiveIncrease_7, color='firebrick',
        linestyle = '--', linewidth = 3,
        label = 'Case Increase Rolling 7-day Avg')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.legend(loc='upper left')
    fig = plt.ylabel('Tests', fontdict={'fontsize':12},color=color)
    ax2 = ax1.twinx() 
    color = 'green'
    fig = plt.scatter(test_df['date'], test_df['PosPerTest'],
                  marker='+',s=100,color='tab:green' ,label='Percent Positive Tests')
    ax2 = plt.plot(test_df['date'], test_df.roll_PosPerTest_7, label='7 Day Average (Rate of Infection)', color='tab:green')
    ax2 = plt.ylabel('Positive/Test', fontdict={'fontsize':12},color=color)
    ax2 = plt.tick_params(axis='y', labelcolor=color)
    ax2 = plt.ylim(0,25)
    ax2 = plt.legend(loc='upper right')
    fig = plt.tight_layout()
    plt.show()


#---------------------------------------------------------------------------------   
    #Perform regression on hospitalizations and ICU increase and overlay with positive
    # per test and 7-day avg.
    
    # Because not all states have the ICU data (inIcuCumulative) I use to calculate
    # the ICU increase the program does the analysis if there are at least 40 non-NULL
    # values and if not then it prints "No ICU Data Available"
    
    ICU_df = new_df[new_df['date']>= ICU_date]
    start = ICU_df[ICU_df['date'] == ICU_date]['date']
    end = ICU_df.date.max() + pd.DateOffset(1)
    if ICU_df.inIcuCumulative.notnull().sum() >40 :
       
        ICU_df = ICU_df.dropna(subset=['inIcuCumulative'])

        Roll_Avg(ICU_df,'PosPerTest',interval)
        
        #Hospital and ICU
        #create row for the ICU Increase:


        ICU_df.sort_index() #sort by date

        #create shifted column that I can then calculate the daily increase
        ICU_df = new_df[new_df['date']>= ICU_date]
        start = ICU_df[ICU_df['date'] == ICU_date]['date']
        end = ICU_df.date.max() + pd.DateOffset(1)
        if ICU_df.inIcuCumulative.notnull().sum() >40 :
           
            ICU_df = ICU_df.dropna(subset=['inIcuCumulative'])
    
            Roll_Avg(ICU_df,'PosPerTest',interval)
            
            #Hospital and ICU
            #create row for the ICU Increase:
    
    
            ICU_df.sort_index() #sort by date
    
            #create shifted column that I can then calculate the daily increase
            ICU_df['PreviousDayICU'] = ICU_df['inIcuCumulative'].shift(-1)
            for row in ICU_df.iterrows() :
                ICU_df['icuIncrease'] = ICU_df['inIcuCumulative'] - ICU_df['PreviousDayICU']
            ICU_df = ICU_df[(ICU_df['icuIncrease']<1000) & (ICU_df['icuIncrease']>=0)]
    
            Roll_Avg(ICU_df,'icuIncrease',interval)
            Roll_Avg(ICU_df,'hospitalizedIncrease',interval)
    
            #plot the overlaying plots:
            sns.set_style("dark")  # to remove grid lines because of the 2 y axis they overlap and are confusing                  
            fig, ax1 = plt.subplots(figsize = (12,6))
    
            plt.title(state_abbrev +' Hospitalization/ICU & Positive per Test', fontdict={'fontsize':20})
            watermark(fig,loc_x=0.94)
            date_ticks(ax,ICU_df,interval=5)
            color = 'tab:blue'
    
            ax1.bar(ICU_df['date'], ICU_df['hospitalizedIncrease'], 
                label='New Hospitalizations',color='tab:blue',alpha=0.5)
            ax1.bar(ICU_df['date'], ICU_df['icuIncrease'], 
                label='New ICU Cases',color='tab:red',alpha=0.6)
            ax1.plot(ICU_df['date'],ICU_df.roll_hospitalizedIncrease_7, color='mediumblue',
                linestyle = '--', linewidth = 3,
                label = 'Hospitalizations 7-Day Rolling Avg.')
            ax1.plot(ICU_df['date'],ICU_df.roll_icuIncrease_7, color='firebrick',
                linestyle = '--', linewidth = 3,
                label = 'ICU Increase 7-Day Rolling Avg.')
            ax1.tick_params(axis='y', labelcolor=color)
            ax1.legend(loc='upper left')
            fig = plt.ylabel('Cases', fontdict={'fontsize':12},color=color)
            ax2 = ax1.twinx() 
            color = 'indigo'
            fig = plt.scatter(ICU_df['date'], ICU_df['PosPerTest'],
                          marker='+',s=100,color='indigo' ,label='Percent Positive Tests')
            ax2 = plt.plot(ICU_df['date'], ICU_df.roll_PosPerTest_7, label='7 Day Average (Rate of Infection)', color='indigo')
            ax2 = plt.ylabel('Positive/Test', fontdict={'fontsize':12},color=color)
            ax2 = plt.tick_params(axis='y', labelcolor=color)
            ax2 = plt.ylim(0,25)
            ax2 = plt.legend(loc='upper right')
            fig = plt.tight_layout()
            
            plt.show()
    
    else :
        print("\n\n No ICU data available")
        
        
def annot_tot(df,col,value) :
    today = df.date.max()
    total = df[col].sum()
    x_loc = df.date.min() + pd.DateOffset(5)
    y_loc = df[col].max()/ 1.75
    value_today = df[col].iloc[1]
    plt.annotate('Today: {}'.format(place_value(value_today)),(today + pd.DateOffset(2),value_today/1.75),
                 rotation=270,color='darkslateblue',fontsize=14)
    plt.annotate('Total '+ value +': {}'.format(place_value(total)),(x_loc,y_loc), fontsize = 16,color='navy')