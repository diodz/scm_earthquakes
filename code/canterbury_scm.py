# -*- coding: utf-8 -*-
"""
Spyder Editoraan

This is a temporary script file.
"""

#Import packages
import pandas as pd
import sys
import matplotlib.pyplot as plt
PATH_SYNTH = "G:\Mi unidad\Research\Araucania\code\SyntheticControlMethods-"\
    + "master"
sys.path.insert(0, PATH_SYNTH)
from SyntheticControlMethods import Synth
import os
os.chdir("G:\Mi unidad\Research\Chile and NZ\code")

INDUSTRY_DATA = r"G:\Mi unidad\Research\Chile and NZ\data\Regional GDP data.xlsx"
SYNTH_VAR_LIST = ['year', 'region', 'id', 'IND_1', 'IND_2',
       'IND_3', 'IND_4', 'IND_5', 'IND_6', 'IND_7', 'IND_8', 'IND_9', 'IND_10',
       'IND_11', 'IND_12', 'GDP', 'population']


#%%
#Import data
def combine_weather_and_population_data():
    '''
    Reads and combines both datasets

    Returns
    -------
    A Dataframe

    '''
    weather = None
    
    return weather
    


def prepare_data():
    df = read_excel_files('G:/Mi unidad/Research/Chile and NZ/data')

    df2 = df[df['Proportion of region\'s total GDP (%)'].isnull()]
    gdppc = df[df['Series name'] == 'Gdp per capita']
    return df

def read_excel_files(directory):
    dfs = []
    for filename in os.listdir(directory):
        if filename.endswith('.xlsx'):
            filepath = os.path.join(directory, filename)
            df = pd.read_excel(filepath, thousands=',')
            dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

#%%

def make_synthetic_control():
    #%%
    df = prepare_data()
    df = df[SYNTH_VAR_LIST]
    df['gdppc'] = df['GDP'] / df['population']
    #Fit classic Synthetic Control
    synth_df = df.drop(['GDP', 'population', 'id'], axis=1)
    sc = Synth(synth_df, "gdppc", "region", "year", 1997, 'Araucania', pen=0)
    
    #Visualize synthetic control
    plt.rcParams.update({'font.size': 20})

    sc.plot(["original", "pointwise", "cumulative"], treated_label="Araucania Region", 
                synth_label="Synthetic Araucania", treatment_label="Lumaco Attack (1997)")
    sc.plot(["original", "pointwise"], treated_label="Araucania Region", 
                synth_label="Synthetic Araucania", treatment_label="Lumaco Attack (1997)")

    sc.plot(["original"], treated_label="Araucania Region", 
                synth_label="Synthetic Araucania", treatment_label="Lumaco Attack (1997)")

    weights = sc.original_data.weight_df
    #Visualize Placebo
    sc.in_space_placebo()
    sc.plot(['rmspe ratio'])
    sc.plot(['in-space placebo'])
    
