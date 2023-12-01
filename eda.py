# %%
import pandas as pd
import numpy as np
import requests
import re
import urllib.parse
import matplotlib.pyplot as plt
import seaborn as sns
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
pd.set_option('display.max_columns', 200) # Shows all columns rather than "..."


# %%

site_snow_main = pd.read_csv('site_snow.csv')


# %%

# Custom Features #
###################

# Snow Level Measurements by Decade Column:
site_snow_main['Decade'] = ''
site_snow_main.loc[site_snow_main['Water Year'].isin(range(1979, 1990)), 'Decade'] = '1980'
site_snow_main.loc[site_snow_main['Water Year'].isin(range(1990, 2000)), 'Decade'] = '1990'
site_snow_main.loc[site_snow_main['Water Year'].isin(range(2000, 2010)), 'Decade'] = '2000'
site_snow_main.loc[site_snow_main['Water Year'].isin(range(2010, 2020)), 'Decade'] = '2010'
site_snow_main.loc[site_snow_main['Water Year'].isin(range(2020, 2024)), 'Decade'] = '2020'


# Installments by Decade Column:
site_snow_main['Decade Inst'] = ''
site_snow_main.loc[site_snow_main['installed'].isin(range(1970, 1980)), 'Decade Inst'] = '1978/79'
site_snow_main.loc[site_snow_main['installed'].isin(range(1980, 1990)), 'Decade Inst'] = '1980'
site_snow_main.loc[site_snow_main['installed'].isin(range(1990, 2000)), 'Decade Inst'] = '1990'
site_snow_main.loc[site_snow_main['installed'].isin(range(2000, 2010)), 'Decade Inst'] = '2000'
site_snow_main.loc[site_snow_main['installed'].isin(range(2010, 2020)), 'Decade Inst'] = '2010'
site_snow_main.loc[site_snow_main['installed'].isin(range(2020, 2024)), 'Decade Inst'] = '2020'

# Jan sum by County Column:
site_snow_main['County Jan Avg'] = ''
for county in site_snow_main['County'].unique():
    county_avg = site_snow_main[site_snow_main['County'] == county]['Jan'].mean()
    
    site_snow_main.loc[site_snow_main['County'] == county, 'County Jan Avg'] = county_avg

site_snow_main




# %%

# EDA: Monthly Correlation Heatmaps #
#####################################

# January:
# site_snow_main_jan = site_snow_main.iloc[:, list(range(1, 9)) + [19]].dropna()
# site_snow_main_jan['Decade'] = pd.to_numeric(site_snow_main_jan['Decade'], errors='coerce')
# corr_matrix = site_snow_main_jan.corr()
# sns.heatmap(corr_matrix, annot=True, cmap='coolwarm_r', center=0.00)
# plt.title('Jan Correlation Heatmap')
# plt.xticks(rotation=1, fontsize=8)

# February:
# site_snow_main_feb = site_snow_main.iloc[:, list(range(1, 7)) + [9] + [10] + [19]].dropna()
# site_snow_main_feb['Decade'] = pd.to_numeric(site_snow_main_feb['Decade'], errors='coerce')
# corr_matrix = site_snow_main_feb.corr()
# sns.heatmap(corr_matrix, annot=True, cmap='coolwarm_r', center=0.00)
# plt.title('Feb Correlation Heatmap')
# plt.xticks(rotation=1, fontsize=8)

# April:
# site_snow_main_apr = site_snow_main.iloc[:, list(range(1, 7)) + [13] + [14] + [19]].dropna()
# site_snow_main_apr['Decade'] = pd.to_numeric(site_snow_main_apr['Decade'], errors='coerce')
# corr_matrix = site_snow_main_apr.corr()
# sns.heatmap(corr_matrix, annot=True, cmap='coolwarm_r', center=0.00)
# plt.title('Apr Correlation Heatmap')
# plt.xticks(rotation=1, fontsize=8)

# May:
site_snow_main_may = site_snow_main.iloc[:, list(range(1, 7)) + [15] + [16] + [19]].dropna()
site_snow_main_may['Decade'] = pd.to_numeric(site_snow_main_may['Decade'], errors='coerce')
corr_matrix = site_snow_main_may.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm_r', center=0.00)
plt.title('May Correlation Heatmap')
plt.xticks(rotation=1, fontsize=8)


# %%

site_snow_main


# %%

# EDA: Scatterplots of snow levels by elevation #
#################################################

### sns scatter subplots Jan, Feb, Apr, May Snow Levels by Elev ###
# Create the 3x2 subplot matrix
fig, axes = plt.subplots(3, 2, figsize=(12, 10))

scatter1 = sns.scatterplot(site_snow_main, x = "Elev", y = "Jan", size=0.5, ax=axes[0,0])
sns.regplot(x="Elev", y="Jan", data=site_snow_main, scatter=False, color='red', ax=axes[0,0])
axes[0,0].set_title('Utah January Snow Levels (in) by Elevation (ft)')
axes[0,0].set_ylabel('SNOTEL Level (in)')
axes[0,0].set_xlabel('Elevation (ft)')

scatter2 = sns.scatterplot(site_snow_main, x = "Elev", y = "Feb", size=0.5, ax=axes[0,1])
sns.regplot(x="Elev", y="Feb", data=site_snow_main, scatter=False, color='red', ax=axes[0,1])
axes[0,1].set_title('February Snow Levels (in) by Elevation (ft)')
axes[0,1].set_ylabel('SNOTEL Level (in)')
axes[0,1].set_xlabel('Elevation (ft)')

scatter3 = sns.scatterplot(site_snow_main, x = "Elev", y = "Mar", size=0.5, ax=axes[1,0])
sns.regplot(x="Elev", y="Mar", data=site_snow_main, scatter=False, color='red', ax=axes[1,0])
axes[1,0].set_title('March Snow Levels (in) by Elevation (ft)')
axes[1,0].set_ylabel('SNOTEL Level (in)')
axes[1,0].set_xlabel('Elevation (ft)')

scatter4 = sns.scatterplot(site_snow_main, x = "Elev", y = "Apr", size=0.5, ax=axes[1,1])
sns.regplot(x="Elev", y="Apr", data=site_snow_main, scatter=False, color='red', ax=axes[1,1])
axes[1,1].set_title('April Snow Levels (in) by Elevation (ft)')
axes[1,1].set_ylabel('SNOTEL Level (in)')
axes[1,1].set_xlabel('Elevation (ft)')

scatter5 = sns.scatterplot(site_snow_main, x = "Elev", y = "May", size=0.5, ax=axes[2,0])
sns.regplot(x="Elev", y="May", data=site_snow_main, scatter=False, color='red', ax=axes[2,0])
axes[2,0].set_title('May Snow Levels (in) by Elevation (ft)')
axes[2,0].set_ylabel('SNOTEL Level (in)')
axes[2,0].set_xlabel('Elevation (ft)')

# Delete 6th plot
fig.delaxes(axes[2, 1])

plt.tight_layout()

# plt.show()

# plt.savefig("snow_elev_scatter.png")



### sns scatter subplots Jan, Feb, Apr, May Snow Levels by Elev ###
# Create the 3x2 subplot matrix
fig, axes = plt.subplots(3, 2, figsize=(12, 10))

scatter1 = sns.scatterplot(site_snow_main, x = "Elev", y = "Jan (WE)", size=0.5, ax=axes[0,0])
sns.regplot(x="Elev", y="Jan (WE)", data=site_snow_main, scatter=False, color='red', ax=axes[0,0])
axes[0,0].set_title('Utah January Water Equiv Levels (in) by Elevation (ft)')
axes[0,0].set_ylabel('Level (in)')
axes[0,0].set_xlabel('Elevation (ft)')

scatter2 = sns.scatterplot(site_snow_main, x = "Elev", y = "Feb (WE)", size=0.5, ax=axes[0,1])
sns.regplot(x="Elev", y="Feb (WE)", data=site_snow_main, scatter=False, color='red', ax=axes[0,1])
axes[0,1].set_title('February Water Equiv Levels (in) by Elevation (ft)')
axes[0,1].set_ylabel('Level (in)')
axes[0,1].set_xlabel('Elevation (ft)')

scatter3 = sns.scatterplot(site_snow_main, x = "Elev", y = "Mar (WE)", size=0.5, ax=axes[1,0])
sns.regplot(x="Elev", y="Mar (WE)", data=site_snow_main, scatter=False, color='red', ax=axes[1,0])
axes[1,0].set_title('March Water Equiv Levels (in) by Elevation (ft)')
axes[1,0].set_ylabel('Level (in)')
axes[1,0].set_xlabel('Elevation (ft)')

scatter4 = sns.scatterplot(site_snow_main, x = "Elev", y = "Apr (WE)", size=0.5, ax=axes[1,1])
sns.regplot(x="Elev", y="Apr (WE)", data=site_snow_main, scatter=False, color='red', ax=axes[1,1])
axes[1,1].set_title('April Water Equiv Levels (in) by Elevation (ft)')
axes[1,1].set_ylabel('Level (in)')
axes[1,1].set_xlabel('Elevation (ft)')

scatter5 = sns.scatterplot(site_snow_main, x = "Elev", y = "May (WE)", size=0.5, ax=axes[2,0])
sns.regplot(x="Elev", y="May (WE)", data=site_snow_main, scatter=False, color='red', ax=axes[2,0])
axes[2,0].set_title('May Water Equiv Levels (in) by Elevation (ft)')
axes[2,0].set_ylabel('Level (in)')
axes[2,0].set_xlabel('Elevation (ft)')

# Delete 6th plot
fig.delaxes(axes[2, 1])

plt.tight_layout()

# plt.show()

# plt.savefig("we_elev_scatter.png")


# %%

### scatter_geo sites by year installed ###

import plotly.express as px

plot1 = px.scatter_geo(site_snow_main, lat='Lat',
               lon='Lon', scope='usa', 
               color='installed', color_continuous_scale='Sunsetdark',
               hover_name='Site_Name')

plot1.update_layout(width = 1000, height = 500)
plot1.update_traces(marker=dict(size=4))

lat_foc = 39.61
lon_foc = -111.0937
plot1.update_layout(geo = dict(projection_scale=4.75, center=dict(lat=lat_foc, lon=lon_foc)))

plot2 = px.scatter_geo(site_snow_main, lat='Lat',
               lon='Lon', scope='usa', 
               color='Decade Inst', 
               category_orders={'Decade Inst': ['2010', '2000', '1990', '1980', '1978/79']}, 
               color_discrete_sequence=['red', 'gold', 'green', 'blue', 'purple'],
               hover_name='Site_Name')

plot2.update_layout(width = 1000, height = 500)
plot2.update_traces(marker=dict(size=4))

lat_foc = 39.61
lon_foc = -111.0937
plot2.update_layout(geo = dict(projection_scale=4.75, center=dict(lat=lat_foc, lon=lon_foc)))


# %%

# Choropleth map: snow levels

geojson = 'https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json'

choro_map = px.choropleth(site_snow_main, 
                          geojson=geojson,
                          locations='County',
                          color='County Jan Avg',
                          hover_name='Site_Name',
                          color_continuous_scale='rocket',
                          scope='usa',
                          labels={'County Jan Avg': 'Avg Snow Level in January'},
                          hover_data='County Jan Avg'
                          )

choro_map.update_layout(width = 1000, height = 500)

lat_foc = 39.61
lon_foc = -111.0937
choro_map.update_layout(geo = dict(projection_scale=4.75, center=dict(lat=lat_foc, lon=lon_foc)))


# %%

site_snow_main['County Jan Avg'].value_counts()

# site_snow_main[site_snow_main['installed'] == 1979]['Site_Name'].unique()



# %%

### Distributions: Snow levels by decade, each month ###

# sns.violinplot(x='Decade', y='Jan', data=site_snow_main, order=['1980', '1990', '2000', '2010', '2020'])
# plt.title('January Across Decades')
# sns.violinplot(x='Decade', y='Feb', data=site_snow_main, order=['1980', '1990', '2000', '2010', '2020'])
# plt.title('February Across Decades')
# sns.violinplot(x='Decade', y='Mar', data=site_snow_main, order=['1980', '1990', '2000', '2010', '2020'])
# plt.title('March Across Decades')
# sns.violinplot(x='Decade', y='Apr', data=site_snow_main, order=['1980', '1990', '2000', '2010', '2020'])
# plt.title('April Across Decades')
# sns.violinplot(x='Decade', y='May', data=site_snow_main, order=['1980', '1990', '2000', '2010', '2020'])
# plt.title('May Across Decades')
# sns.violinplot(x='Decade', y='Jun', data=site_snow_main, order=['1980', '1990', '2000', '2010', '2020'])
# plt.title('June Across Decades')


# %%

site_snow_main['Water Year'].value_counts()


# %%

site_snow_main.columns

# %%

len(site_snow_main[site_snow_main['Water Year'] == 1982])

# %%

