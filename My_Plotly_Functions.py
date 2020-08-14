#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 09:20:28 2020

@author: davidr.mckenna
"""

#%%

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import requests
from plotly.graph_objs.scatter.marker import Line


from plotly.subplots import make_subplots



#%%

def Roll_Avg(df, col, interval,shift = True) :
    """Calculate the rolling averages of interval duration of columns in df"""
    length = len(interval)
    
    for n in range(length) :
        # make new col called roll_col_interval
        new_col = 'roll_' + str(col) + '_'+ str(interval[n])
        if shift == False :
            df[new_col] = df.loc[:,col].rolling(interval[n]).mean()
        
        else :
            df[new_col] = df.loc[:,col].rolling(interval[n]).mean().shift(periods= - interval[n])
            
#%%            

# Define function to do the subsetting of the data of selected state
def State_Subset(df,state_abbrev, start_date = '2020-03-01') :
    new_df = state_abbrev
    new_df = df[df['state']== state_abbrev]
    new_df = new_df[new_df['date']>= start_date]
    
    return new_df

#%%

def Make_National_Cases(df):
    national_cases = df.groupby('date')['positiveIncrease'].sum().reset_index()
    
    national_cases['date'] = national_cases.date.dt.strftime('%Y-%m-%d')
    Roll_Avg(national_cases, 'positiveIncrease', [7,20],shift=False)
    
    # print(national_cases['date'], national_cases['positiveIncrease'])
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(x=national_cases['date'],
                y=national_cases['positiveIncrease'],
                marker=dict(color='slategray'),
                name='National Daily Case Increase'
                )
    )
    
    
    fig.add_trace(
        go.Line(x=national_cases['date'],
                y=national_cases['roll_positiveIncrease_7'],
                marker=dict(color='DodgerBlue'),
                line=dict(width=4),
                name='7-Day Average'
                )
        
    )

    fig.add_trace(
        go.Line(x=national_cases['date'],
                y=national_cases['roll_positiveIncrease_20'],
                marker=dict(color='Red'),
                line=dict(width=2),
                name='20-Day Average'
                )
        
    )
    
    
    fig.update_layout(title='National New Cases per Day',
                      title_x=0.5,
                      xaxis_title='Date',
                      yaxis_title='New Cases',
                      legend=dict(
                              yanchor="top",
                              y=0.99,
                              xanchor="left",
                              x=0.01)
    )     
    return fig

#%%

def Make_National_Deaths(df) :
    
    national_deaths = df.groupby('date')['deathIncrease'].sum().reset_index()
    
    national_deaths['date'] = national_deaths.date.dt.strftime('%Y-%m-%d')
    Roll_Avg(national_deaths, 'deathIncrease', [7,20],shift=False)
    
    # print(national_cases['date'], national_cases['positiveIncrease'])
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(x=national_deaths['date'],
                y=national_deaths['deathIncrease'],
                marker=dict(color='slategray'),
                name='National Daily Case Increase'
                )
    )
    
    
    fig.add_trace(
        go.Line(x=national_deaths['date'],
                y=national_deaths['roll_deathIncrease_7'],
                marker=dict(color='DodgerBlue'),
                line=dict(width=4),
                name='7-Day Average'
                )
        
    )

    fig.add_trace(
        go.Line(x=national_deaths['date'],
                y=national_deaths['roll_deathIncrease_20'],
                marker=dict(color='Red'),
                line=dict(width=2),
                name='20-Day Average'
                )
        
    )
    
    
    fig.update_layout(title='National Deaths per Day',
                      title_x=0.5,
                      xaxis_title='Date',
                      yaxis_title='New Deaths',
                      legend=dict(
                              yanchor="top",
                              y=0.99,
                              xanchor="left",
                              x=0.01)
    )
    return fig

#%%


def Make_State_Cases(df,state_of_choice):
    
    new_df = State_Subset(df,state_of_choice)
    interval = [7,20]#sets the intervals for the rolling averages
    state_cases = new_df.groupby('date')['positiveIncrease'].sum().reset_index()
    
    state_cases['date'] = state_cases.date.dt.strftime('%Y-%m-%d')
    Roll_Avg(state_cases, 'positiveIncrease', interval,shift=False)
    
    # print(national_cases['date'], national_cases['positiveIncrease'])
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(x=state_cases['date'],
                y=state_cases['positiveIncrease'],
                marker=dict(color='slategray'),
                name= str(state_of_choice) + ' Daily Case Increase'
                )
    )
    
    
    fig.add_trace(
        go.Line(x=state_cases['date'],
                y=state_cases['roll_positiveIncrease_7'],
                marker=dict(color='DodgerBlue'),
                line=dict(width=4),
                name='7-Day Average'
                )
        
    )
    
    fig.add_trace(
        go.Line(x=state_cases['date'],
                y=state_cases['roll_positiveIncrease_20'],
                marker=dict(color='Red'),
                line=dict(width=2),
                name='20-Day Average'
                )
        
    )
    
    
    fig.update_layout(title=str(state_of_choice)+ ' New Cases per Day',
                      title_x=0.5,
                      xaxis_title='Date',
                      yaxis_title='New Cases',
                      legend=dict(
                              yanchor="top",
                              y=0.99,
                              xanchor="right",
                              x=0.5)
    )     
    return fig

#%%


def Make_State_Deaths(df,state_of_choice) :
    
    new_df = State_Subset(df,state_of_choice)
    interval = [7,20]#sets the intervals for the rolling averages
    state_deaths = new_df.groupby('date')['deathIncrease'].sum().reset_index()
    
    
    state_deaths['date'] = state_deaths.date.dt.strftime('%Y-%m-%d')
    Roll_Avg(state_deaths, 'deathIncrease', interval,shift=False)
    
    # print(national_cases['date'], national_cases['positiveIncrease'])
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(x=state_deaths['date'],
                y=state_deaths['deathIncrease'],
                marker=dict(color='slategray'),
                name= str(state_of_choice)+' Daily Case Increase'
                )
    )
    
    
    fig.add_trace(
        go.Line(x=state_deaths['date'],
                y=state_deaths['roll_deathIncrease_7'],
                marker=dict(color='FireBrick'),
                line=dict(width=4),
                name='7-Day Average'
                )
        
    )
    fig.add_trace(
        go.Line(x=state_deaths['date'],
                y=state_deaths['roll_deathIncrease_20'],
                marker=dict(color='DodgerBlue'),
                line=dict(width=4),
                name='20-Day Average'
                )
        
    )
    
    
    fig.update_layout(title=str(state_of_choice)+' Deaths per Day',
                      title_x=0.5,
                      xaxis_title='Date',
                      yaxis_title='New Deaths',
                      legend=dict(
                              yanchor="top",
                              y=0.99,
                              xanchor="right",
                              x=0.5)
    )
    return fig

#%%

def Make_Test_Plot(df,state_of_choice) :


    
    #subset the state of interest
    new_df = State_Subset(df,state_of_choice)
    interval = [7,20]#sets the intervals for the rolling averages
    
    ## Calculate the ROlling averages of features of interest
    Roll_Avg(new_df,'positiveIncrease',interval)
    Roll_Avg(new_df,'deathIncrease',interval)
    Roll_Avg(new_df,'PosPerTest',interval)
    Roll_Avg(new_df,'totalTestResultsIncrease',interval)
    
    #Create Plotly figure objects
    fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])#secondary y scale for infection rate
    
    # Add barplot of total tests per day
    fig.add_trace(
        go.Bar(x=new_df['date'],
               y=new_df['totalTestResultsIncrease'],
               marker=dict(color='slategray'),
               name='Total Tests',
               legendgroup = 'Tests',
               offsetgroup=0
               ),
        secondary_y=False
               
    )
    
    # Add barplotof positive tests per day
    fig.add_trace(
        go.Bar(x=new_df['date'],
               y=new_df['positiveIncrease'],
               marker=dict(color='Red'),
               name='Positive Tests',
               offsetgroup=0,
               legendgroup = 'Cases'
               ),
        secondary_y=False
               
    )
    
    #Rolling average trace of testing 
    fig.add_trace(
        go.Line(x=new_df['date'],
                y=new_df['roll_totalTestResultsIncrease_7'],
                marker=dict(color='Black'),
                line=dict(width=2),
                name='7-Day Average',
                legendgroup = 'Tests'
                ),
        secondary_y=False
                
        
    )
    
    # Rolling average line of positive tests
    fig.add_trace(
        go.Line(x=new_df['date'],
                y=new_df['roll_positiveIncrease_7'],
                marker=dict(color='FireBrick'),
                line=dict(width=2),
                name='7-Day Average',
                legendgroup = 'Cases'
                ),
        secondary_y=False
                
        
    )
    
    # Scatter of d=Infection Rate
    fig.add_trace(
        go.Scatter(x=new_df['date'],
                y=new_df['PosPerTest'],
                mode='markers',
                marker=dict(color='Green',size=7),
                name='Infection Rate',
                legendgroup = 'Infection'
                ),
        secondary_y=True           
                
        
    )
    
    # Rolling average of Infection Rate
    fig.add_trace(
        go.Line(x=new_df['date'],
                y=new_df['roll_PosPerTest_7'],
                marker=dict(color='forestgreen'),
                line=dict(width=3),
                name='7-Day Average Infection Rate',
                legendgroup = 'Infection'
                ),
        secondary_y=True
    )
    
    # Setup the layout of legend and title 
    fig.update_layout(height=500, width=600,title= str(state_of_choice) + ' Tests and Infection Rate',
                      title_x=0.5, 
                      legend=dict(
                               yanchor="top",
                               y=0.99,
                               xanchor="left",
                               x=0.01,),
                      yaxis2_showgrid=False
                             
    )
    # Update Axis labels and range
    fig.update_yaxes(title_text="Tests", secondary_y=False)
    fig.update_yaxes(title_text="Infection Rate (%)",secondary_y=True, range=[0,50])   
    return fig

#%%


def Make_State (df,state_of_choice):
    
    
    new_df = State_Subset(df,state_of_choice)
    interval = [7,20]#sets the intervals for the rolling averages
    state_cases = new_df.groupby('date')['positiveIncrease'].sum().reset_index()
    state_deaths = new_df.groupby('date')['deathIncrease'].sum().reset_index()

    state_cases['date'] = state_cases.date.dt.strftime('%Y-%m-%d')
    Roll_Avg(state_cases, 'positiveIncrease', interval,shift=False)
    
    state_deaths['date'] = state_deaths.date.dt.strftime('%Y-%m-%d')
    Roll_Avg(state_deaths, 'deathIncrease', interval,shift=False)
    
    # print(national_cases['date'], national_cases['positiveIncrease'])
    
    fig = make_subplots(rows=2, cols=1,
                        subplot_titles = [str(state_of_choice)+ ' Cases per Day'
                                          , str(state_of_choice)+ ' Deaths per Day'],
                        )
    
    fig.add_trace(
        go.Bar(x=state_cases['date'],
                y=state_cases['positiveIncrease'],
                marker=dict(color='slategray'),
                name= str(state_of_choice) + ' Daily Case Increase'
                ),row=1,col=1
    )
    
    
    fig.add_trace(
        go.Line(x=state_cases['date'],
                y=state_cases['roll_positiveIncrease_7'],
                marker=dict(color='DodgerBlue'),
                line=dict(width=4),
                name='7-Day Average'
                ),row=1,col=1
        
    )
    
    fig.add_trace(
        go.Line(x=state_cases['date'],
                y=state_cases['roll_positiveIncrease_20'],
                marker=dict(color='Red'),
                line=dict(width=2),
                name='20-Day Average'
                ),row=1,col=1
        
    )
    
    
    
    fig.add_trace(
        go.Bar(x=state_deaths['date'],
                y=state_deaths['deathIncrease'],
                marker=dict(color='slategray'),
                name= str(state_of_choice)+' Daily Deaths Increase'
                ),row=2,col=1
    )
    
    
    fig.add_trace(
        go.Line(x=state_deaths['date'],
                y=state_deaths['roll_deathIncrease_7'],
                marker=dict(color='FireBrick'),
                line=dict(width=2),
                name='7-Day Average'
                ),row=2,col=1
        
    )
    fig.add_trace(
        go.Line(x=state_deaths['date'],
                y=state_deaths['roll_deathIncrease_20'],
                marker=dict(color='MidnightBlue'),
                line=dict(width=2),
                name='20-Day Average'
                ),row=2,col=1
        
    )
    

    fig.update_layout(height=800, width=650, 
                      title_text="Statewide Outlook"
    )          
    
    return fig
    
#%%

def R_B_National_Scaled(df_election):

    Cases = df_election.groupby(['date','2016 Won By'])['positiveIncrease'].sum().unstack().reset_index()
    Deaths = df_election.groupby(['date','2016 Won By'])['deathIncrease'].sum().unstack().reset_index()
    
    Roll_Avg(Cases, 'States Won By Clinton', [7,20],shift=False)
    Roll_Avg(Deaths, 'States Won By Clinton', [7,20],shift=False)
    Roll_Avg(Cases, 'States Won By Trump', [7,20],shift=False)
    Roll_Avg(Deaths, 'States Won By Trump', [7,20],shift=False)

    
    
    fig = make_subplots(rows=2, cols=1,
                    subplot_titles = ['Cases per Day'
                                          , ' Deaths per Day'],
                        )


    fig.add_trace(
        go.Line(x=Cases['date'],
                y=Cases['States Won By Clinton'],
                marker=dict(color='DodgerBlue'),
                line=dict(width=2),
                name='Won By Clinton'
                ),row=1,col=1
        )
    
    fig.add_trace(
        go.Line(x=Cases['date'],
                y=Cases['roll_States Won By Clinton_7'],
                marker=dict(color='DarkBlue'),
                line=dict(width=2, dash ='dot'),
                name='Clinton 7-Day Avg.'
                ),row=1,col=1
        )

    fig.add_trace(
        go.Line(x=Cases['date'],
                y=Cases['roll_States Won By Trump_7'],
                marker=dict(color='DarkRed'),
                line=dict(width=2, dash ='dot'),
                name='rump 7-Day Avg'
                ),row=1,col=1
        )

    fig.add_trace(
        go.Line(x=Cases['date'],
                y=Cases['States Won By Trump'],
                marker=dict(color='Red'),
                line=dict(width=2),
                name='Won By Trum'
                ),row=1,col=1
        )
    
    fig.add_trace(
        go.Line(x=Deaths['date'],
                y=Deaths['States Won By Clinton'],
                marker=dict(color='DodgerBlue'),
                line=dict(width=2),
                showlegend=False,
                name='Won By Clinton'
                ),row=2,col=1
        )


    fig.add_trace(
        go.Line(x=Deaths['date'],
                y=Deaths['States Won By Trump'],
                marker=dict(color='Red'),
                line=dict(width=2),
                showlegend=False,
                name='Won By Trum'
                ),row=2,col=1
        )

    fig.add_trace(
        go.Line(x=Deaths['date'],
                y=Deaths['roll_States Won By Clinton_7'],
                marker=dict(color='DarkBlue'),
                line=dict(width=2, dash ='dot'),
                name='Clinton 7-Day Avg.'
                ),row=2,col=1
        )

    fig.add_trace(
        go.Line(x=Deaths['date'],
                y=Deaths['roll_States Won By Trump_7'],
                marker=dict(color='DarkRed'),
                line=dict(width=2, dash ='dot'),
                name='rump 7-Day Avg'
                ),row=2,col=1
        )

    fig.update_layout(height=800, width=650,
                title_text="Red v Blue States Per 1M Population"
                )

    return fig


#%%

def R_B_National(df_election):

    
    df_election['positiveIncreasescale'] = df_election['positiveIncrease']/(df_election['Population']/1000000)
    
    df_election['deathIncreasescale'] = df_election['deathIncrease']/(df_election['Population']/1000000)
    Cases = df_election.groupby(['date','2016 Won By'])['positiveIncreasescale'].sum().unstack().reset_index()
    Deaths = df_election.groupby(['date','2016 Won By'])['deathIncreasescale'].sum().unstack().reset_index()
    
    
    fig = make_subplots(rows=2, cols=1,
                    subplot_titles = ['Cases per Day'
                                          , ' Deaths per Day'],
                        )


    fig.add_trace(
        go.Line(x=Cases['date'],
                y=Cases['States Won By Clinton'],
                marker=dict(color='DodgerBlue'),
                line=dict(width=2),
                name='Won By Clinton'
                ),row=1,col=1
        )


    fig.add_trace(
        go.Line(x=Cases['date'],
                y=Cases['States Won By Trump'],
                marker=dict(color='Red'),
                line=dict(width=2),
                name='Won By Trump'
                ),row=1,col=1
        )
    
    fig.add_trace(
        go.Line(x=Deaths['date'],
                y=Deaths['States Won By Clinton'],
                marker=dict(color='DodgerBlue'),
                line=dict(width=2),
                showlegend=False,
                name='Won By Clinton'
                ),row=2,col=1
        )


    fig.add_trace(
        go.Line(x=Deaths['date'],
                y=Deaths['States Won By Trump'],
                marker=dict(color='Red'),
                line=dict(width=2),
                showlegend=False,
                name='Won By Trum'
                ),row=2,col=1
        )


    fig.update_layout(height=800, width=650,
                title_text="Red v Blue States"
                )

    return fig
#%%

def Make_National(df) :

    national_cases = df.groupby('date')['positiveIncrease'].sum().reset_index()
    
    national_cases['date'] = national_cases.date.dt.strftime('%Y-%m-%d')
    Roll_Avg(national_cases, 'positiveIncrease', [7,20],shift=False)
    
    # print(national_cases['date'], national_cases['positiveIncrease'])
    fig = make_subplots(rows=2, cols=1,
                    subplot_titles = ['National Cases per Day'
                                          , 'National Deaths per Day'],
                        )
    
    fig.add_trace(
        go.Bar(x=national_cases['date'],
                y=national_cases['positiveIncrease'],
                marker=dict(color='slategray'),
                name='National Daily Case Increase'
                ),row=1,col=1
    )
    
    
    fig.add_trace(
        go.Line(x=national_cases['date'],
                y=national_cases['roll_positiveIncrease_7'],
                marker=dict(color='DodgerBlue'),
                line=dict(width=4),
                name='7-Day Average'
                ),row=1,col=1
        
    )

    fig.add_trace(
        go.Line(x=national_cases['date'],
                y=national_cases['roll_positiveIncrease_20'],
                marker=dict(color='Red'),
                line=dict(width=2),
                name='20-Day Average'
                ),row=1,col=1
        
    )
    
    national_deaths = df.groupby('date')['deathIncrease'].sum().reset_index()
    
    national_deaths['date'] = national_deaths.date.dt.strftime('%Y-%m-%d')
    Roll_Avg(national_deaths, 'deathIncrease', [7,20],shift=False)
    
    # print(national_cases['date'], national_cases['positiveIncrease'])

    
    fig.add_trace(
        go.Bar(x=national_deaths['date'],
                y=national_deaths['deathIncrease'],
                marker=dict(color='slategray'),
                showlegend=False,
                name='National Daily Case Increase'
                ),row=2, col=1
    )
    
    
    fig.add_trace(
        go.Line(x=national_deaths['date'],
                y=national_deaths['roll_deathIncrease_7'],
                marker=dict(color='DodgerBlue'),
                showlegend=False,
                line=dict(width=4),
                name='7-Day Average'
                ),row=2, col=1
        
    )

    fig.add_trace(
        go.Line(x=national_deaths['date'],
                y=national_deaths['roll_deathIncrease_20'],
                marker=dict(color='Red'),
                showlegend=False,
                line=dict(width=2),
                name='20-Day Average'
                ),row=2, col=1
        
    )
        
    fig.update_layout(height=800, width=650,
                title_text="National Outlook"
                )

    return fig
    







