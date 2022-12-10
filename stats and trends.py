# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 19:14:09 2022

@author: omolulu adelana
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def data_extractor(url, columns_to_delete, rows_to_skip, indicator):
    
    '''
    
    '''
  
    df = pd.read_csv(url, skiprows=rows_to_skip)
    df = df.loc[df['Indicator Name'] == indicator]
  
    #dropping columns that are not needed. Also, rows with NA were dropped
    df = df.drop(columns_to_delete, axis=1)

    #this extracts a dataframe with countries as column
    df1 = df
    
    #this section extract a dataframe with year as columns
    df2 = df.transpose()

    #removed the original headers after a transpose and dropped the row
    #used as a header
    df2 = df2.rename(columns=df2.iloc[0])
    df2 = df2.drop(index=df2.index[0], axis=0)
    df2 = df2.reset_index()
    df2 = df2.rename(columns={"index":"Year"})
    
    return df1, df2


def create_df_by_country(country, url, indicator):
  
    #generate the original data from file/url
    df1, df2 = data_extractor(url, columns_to_delete, rows_to_skip, indicator)
    
    #create a dataframe
    df = pd.DataFrame()
    
    #extract a dataframe of a specific country
    for c in country:
        #df = df1[(df1['Country Name'] == c)]
        df = pd.concat([df, df1.loc[df1['Country Name'] == c]])
    
    df = df[['Country Name'] + year]
    return df

def create_df_by_year(year, url, indicator):
  
    #generate the original data from file/url
    df1, df2 = data_extractor(url, columns_to_delete, rows_to_skip, indicator)
    
    df = pd.DataFrame()
    #extract a dataframe of a specific country
    for y in year:
        df = pd.concat([df, df2.loc[df2['Year'] == y]])
    
    df = df[['Year'] + country]
    return df


country = ['New Zealand', 'China', 'Nigeria', 'Angola']
year = ['2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']
url = 'API_19_DS2_en_csv_v2_4700503.csv'
columns_to_delete = ['Country Code', 'Indicator Name', 'Indicator Code']
rows_to_skip = 4


df_pop_country = create_df_by_country(country, url, 'Population growth (annual %)')
df_pop_year = create_df_by_year(year, url, 'Population growth (annual %)')
df_urban_country = create_df_by_country(country, url, 'Urban population')
df_urban_year = create_df_by_year(year, url, 'Urban population')
df_arable_country = create_df_by_country(country, url, 'Arable land (% of land area)')
df_arable_year = create_df_by_year(year, url, 'Population growth (annual %)')


x_data = df_pop_year['Year']


y_data = [df_pop_year['New Zealand'], df_urban_year['New Zealand'], df_arable_year['New Zealand'],
          df_pop_year['China'], df_urban_year['China'], df_arable_year['China'],
          df_pop_year['Nigeria'], df_urban_year['Nigeria'], df_arable_year['Nigeria'],
          df_pop_year['Angola'], df_urban_year['Angola'], df_arable_year['Angola']
         ]

legend = ['New Zealand Population', 'New Zealand Urban Migration', 'New Zealand Arable Land',
        'China Population', 'China Urban Migration', 'China Arable Land',
        'Nigeria Population', 'Nigeria Urban Migration', 'Nigeria Arable Land',
        'Angola Population', 'Angola Urban Migration', 'Angola Arable Land']

colors = ['blue', 'red', 'green',
          'blue', 'red', 'green',
          'blue', 'red', 'green',
          'blue', 'red', 'green']

title = ['population', 'Urban Migration', 'Arable Land',
          'population', 'Urban Migration', 'Arable Land',
          'population', 'Urban Migration', 'Arable Land',
          'population', 'Urban Migration', 'Arable Land']

plt.figure(figsize=(20, 30))

for i in range(len(y_data)):
    plt.subplot(4, 3, i+1)
    plt.plot(x_data, y_data[i], label=title[i], color=colors[i])
    plt.xticks(rotation='vertical')
    plt.xlabel('Year')
    plt.xlabel('Count')
    plt.title(legend[i])
    plt.legend()

plt.title('Date Rate comparison across 4 countries in 2020')
plt.show()

def sum_country_data(dataframe):
    dataframe['sum'] = dataframe.iloc[:, 1:].sum(axis=1)
    return dataframe


data = sum_country_data(df_pop_country)

def plot_pie(sum_population):
    plt.pie(sum_population['sum'], labels=sum_population['Country Name'], autopct='%1.3f%%', shadow=True, startangle=90)
    plt.title('Population fo select countries compared')
    plt.show()


plot_pie(data)

plt.figure()
df_pop_country.plot('Country Name', ['2019', '2020', '2021'], kind='bar')
plt.show()

plt.figure()
df_urban_year.plot('Year', ['New Zealand', 'China', 'Nigeria', 'Angola'], kind='bar')
plt.show()