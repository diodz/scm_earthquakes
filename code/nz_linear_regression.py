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
from sklearn import linear_model
import matplotlib.pyplot as plt
import os
os.chdir("G:\Mi unidad\Research\Araucania\code")

DISASTERS_DATA = r"G:\Mi unidad\Research\Araucania\dataverse_files\maceda_2.0.dta"
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
    weather = read_and_clean_weather_data()
    pop = pd.read_csv(POPULATION_PATH)
    region_names = pop[['id', 'region']].drop_duplicates()
    pop = pop.drop('region', axis=1)
    merged = weather.merge(pop, on=['year', 'id'], how='left')\
        .merge(region_names, on='id', how='left')
    merged['population'] = merged['population'].bfill()
    df_regions_1974 = merged.groupby(['year', 'region', 'id']).sum()
    rv = df_regions_1974.reset_index()
    return rv
    


def read_and_clean_weather_data():
    SELECTED = ['year', 'id', 'GDP', 'region_1974']
    weather = pd.read_stata(WEATHER_DATA)[SELECTED].dropna()
    for c in weather.columns[:-1]:
        weather[c] = weather[c].astype(int)
    regions = weather[['id', 'region_1974']].drop_duplicates().dropna()
    regions['region_1974'] = regions['region_1974'].astype(int)
    weather = weather.drop('region_1974', axis=1)
    rv = weather.merge(regions, on='id', how='left').drop('id', axis=1)
    rv.columns = ['year', 'GDP', 'id']
    return rv


#%%

def make_synthetic_control():
    #%%
    df = combine_weather_and_population_data()
    df['gdppc'] = df['GDP'] / df['population']
    df = df[['year', 'region', 'gdppc']]  
    
    df_wide = df.pivot(index='year', columns='region', values='gdppc')
    training = df_wide.reset_index()
    treatment_start = 1997
    training = training[training['year'] < treatment_start].set_index('year')



#%%
    reg = linear_model.LinearRegression(positive=True)
    #reg = linear_model.LinearRegression(positive=False)
    lst = list(training.columns)
    lst.remove('Araucania')
    reg.fit(training[lst], training['Araucania'])    
    y_pred = reg.predict(df_wide[lst])
    araucania = df_wide[['Araucania']]
    araucania['Synthetic Araucania'] = y_pred
    araucania.plot()
    plt.rcParams['figure.figsize'] = [10, 6]

    # create a new figure and axes
    fig, ax = plt.subplots()
    # plot the two lines with circles as markers
    ax.plot(araucania[['Araucania']], '-o', label='Araucania')
    ax.plot(araucania[['Synthetic Araucania']], '-o',
            label='Synthetic Araucania')
    
    ax.axvline(x=treatment_start, linestyle='--', color='red')
    ax.annotate('   Lumaco Attack', xy=(treatment_start, 3), xytext=(treatment_start, 3.5),
            arrowprops=dict(facecolor='black', arrowstyle='->'))

    #date = datetime.strptime('2020-06-25', '%Y-%m-%d')
    
    # add axis titles and labels
    ax.set_title('Synthetic Control Method: Araucania Region (GDPPC)')
    ax.set_ylabel('GDPPC')
    
    # add a legend and show the plot
    ax.legend()
    plt.grid()
    plt.show()

    weights = pd.DataFrame({'region': lst, 'weights': reg.coef_})
