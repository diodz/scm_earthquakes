# -*- coding: utf-8 -*-
"""
Spyder Editoraan

This is a temporary script file.
"""

#Import packages
import pandas as pd
import sys
PATH_SYNTH = "G:\Mi unidad\Research\Araucania\code\SyntheticControlMethods-"\
    + "master"
sys.path.insert(0, PATH_SYNTH)
from SyntheticControlMethods import Synth
import os
os.chdir("G:\Mi unidad\Research\Araucania\code")

WEATHER_DATA = r"G:\Mi unidad\Research\Araucania\data\chile_eco_wea_1950_2017.dta"
POPULATION_PATH = '../data/population.csv'

#%%
#Import data
def combine_weather_and_population_data():
    '''
    Reads and combines both datasets

    Returns
    -------
    A Dataframe

    '''
    weather = pd.read_csv(WEATHER_DATA)
    pop = pd.read_csv(POPULATION_PATH)


#%%

SELECTED = ['id', 'year', 'GDP_r', 'UF', 'GDP']
#SELECTED = ['year', 'GDP_r', 'UF', 'GDP', 'precip1', 'region_1974']
weather = pd.read_stata(WEATHER_DATA)#[SELECTED]
#maceda = pd.read_stata(DISASTERS_DATA, convert_categoricals=False)
#maceda.columns

#%%

aux = weather.dropna().copy(deep=True)
aux['year'] = aux['year'].astype(int)
aux['id'] = aux['id'].astype(int)
#aux['region_1974'] = aux['region_1974'].astype(int)

#Fit classic Synthetic Control
sc = Synth(aux, "GDP_r", "id", "year", 1997, 9, pen=0)

#Visualize synthetic control
sc.plot(["original", "pointwise", "cumulative"], treated_label="Araucania Region", 
            synth_label="Synthetic Araucania", treatment_label="Lumaco Attack")

