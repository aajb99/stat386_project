# %%
import pandas as pd
import numpy as np
import requests
import re
import urllib.parse
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from sklearn.preprocessing import MinMaxScaler
import plotly.figure_factory as ff
import plotly.graph_objects as go
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


# Normalized Jan and Jan (WE) for scatterplot EDA below:
scaler = MinMaxScaler()
# Normalize Jan
site_snow_main['Jan norm.'] = scaler.fit_transform(site_snow_main[['Jan']])
# Normalize the Jan (WE) column
site_snow_main['Jan (WE) norm.'] = scaler.fit_transform(site_snow_main[['Jan (WE)']])

# Normalized May and May (WE) for scatterplot EDA below:
scaler = MinMaxScaler()
# Normalize Jan
site_snow_main['May norm.'] = scaler.fit_transform(site_snow_main[['May']])
# Normalize the Jan (WE) column
site_snow_main['May (WE) norm.'] = scaler.fit_transform(site_snow_main[['May (WE)']])


# %%

site_snow_main



# %%

# EDA: Monthly Correlation Heatmaps #
#####################################
plt.figure(figsize=(10, 8)) 
# January:
site_snow_main_jan = site_snow_main.iloc[:, list(range(1, 9)) + [19]].dropna()
site_snow_main_jan['Decade'] = pd.to_numeric(site_snow_main_jan['Decade'], errors='coerce')
corr_matrix = site_snow_main_jan.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm_r', center=0.00)
plt.title('January (early season) Correlation Heatmap')
plt.xticks(rotation=1, fontsize=8)

plt.savefig("./images/jan_heatmap.png")
plt.clf()

# February:
site_snow_main_feb = site_snow_main.iloc[:, list(range(1, 7)) + [9] + [10] + [19]].dropna()
site_snow_main_feb['Decade'] = pd.to_numeric(site_snow_main_feb['Decade'], errors='coerce')
corr_matrix = site_snow_main_feb.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm_r', center=0.00)
plt.title('February (early season) Correlation Heatmap')
plt.xticks(rotation=1, fontsize=8)

plt.savefig("./images/feb_heatmap.png")
plt.clf()

# April:
site_snow_main_apr = site_snow_main.iloc[:, list(range(1, 7)) + [13] + [14] + [19]].dropna()
site_snow_main_apr['Decade'] = pd.to_numeric(site_snow_main_apr['Decade'], errors='coerce')
corr_matrix = site_snow_main_apr.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm_r', center=0.00)
plt.title('April (late season) Correlation Heatmap')
plt.xticks(rotation=1, fontsize=8)

plt.savefig("./images/apr_heatmap.png")
plt.clf()

# May:
site_snow_main_may = site_snow_main.iloc[:, list(range(1, 7)) + [15] + [16] + [19]].dropna()
site_snow_main_may['Decade'] = pd.to_numeric(site_snow_main_may['Decade'], errors='coerce')
corr_matrix = site_snow_main_may.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm_r', center=0.00)
plt.title('May (late season) Correlation Heatmap')
plt.xticks(rotation=1, fontsize=8)

plt.savefig("./images/may_heatmap.png")
plt.clf()


# %%

site_snow_main


# %%

# EDA: Scatterplots of snow levels by elevation: 1980s #
########################################################

fig, axes = plt.subplots(4, 2, figsize=(12, 10))

scatter1a = sns.scatterplot(site_snow_main[site_snow_main['Decade'] == '1980'], x = "Elev", y = "Jan norm.", size=0.5, ax=axes[0,0])
reg_line1a = sns.regplot(x="Elev", y="Jan norm.", data=site_snow_main, scatter=False, color='red', ax=axes[0,0])
axes[0,0].set_ylim(-.05,1.05)
scatter1a.legend_.remove()
# plt.savefig("snow_elev_scatter.png")


scatter1b = sns.scatterplot(site_snow_main[site_snow_main['Decade'] == '1980'], x = "Elev", y = "Jan (WE) norm.", size=0.5, ax=axes[1,0])
reg_line1b = sns.regplot(x="Elev", y="Jan (WE) norm.", data=site_snow_main, scatter=False, color='red', ax=axes[1,0])
axes[1,0].set_ylim(-.05,1.05)
scatter1b.legend_.remove()
# plt.savefig("we_elev_scatter.png")

scatter2a = sns.scatterplot(site_snow_main[site_snow_main['Decade'] == '1980'], x = "Elev", y = "May norm.", size=0.5, ax=axes[2,0])
reg_line2a = sns.regplot(x="Elev", y="May norm.", data=site_snow_main, scatter=False, color='red', ax=axes[2,0])
axes[2,0].set_ylim(-.05,1.05)
scatter2a.legend_.remove()
# plt.savefig("snow_elev_scatter.png")


scatter2b = sns.scatterplot(site_snow_main[site_snow_main['Decade'] == '1980'], x = "Elev", y = "May (WE) norm.", size=0.5, ax=axes[3,0])
reg_line2b = sns.regplot(x="Elev", y="May (WE) norm.", data=site_snow_main, scatter=False, color='red', ax=axes[3,0])
axes[3,0].set_ylim(-.05,1.05)
scatter2b.legend_.remove()

# EDA: Scatterplots of snow levels by elevation: 2010s #
########################################################

scatter3a = sns.scatterplot(site_snow_main[site_snow_main['Decade'] == '2010'], x = "Elev", y = "Jan norm.", size=0.5, ax=axes[0,1])
reg_line3a = sns.regplot(x="Elev", y="Jan norm.", data=site_snow_main, scatter=False, color='red', ax=axes[0,1])
axes[0,1].set_ylim(-.05,1.05)
scatter3a.legend_.remove()
# plt.savefig("snow_elev_scatter.png")


scatter3b = sns.scatterplot(site_snow_main[site_snow_main['Decade'] == '2010'], x = "Elev", y = "Jan (WE) norm.", size=0.5, ax=axes[1,1])
reg_line3b = sns.regplot(x="Elev", y="Jan (WE) norm.", data=site_snow_main, scatter=False, color='red', ax=axes[1,1])
axes[1,1].set_ylim(-.05,1.05)
scatter3b.legend_.remove()
# plt.savefig("we_elev_scatter.png")

scatter4a = sns.scatterplot(site_snow_main[site_snow_main['Decade'] == '2010'], x = "Elev", y = "May norm.", size=0.5, ax=axes[2,1])
reg_line4a = sns.regplot(x="Elev", y="May norm.", data=site_snow_main, scatter=False, color='red', ax=axes[2,1])
axes[2,1].set_ylim(-.05,1.05)
scatter4a.legend_.remove()
# plt.savefig("snow_elev_scatter.png")


scatter4b = sns.scatterplot(site_snow_main[site_snow_main['Decade'] == '2010'], x = "Elev", y = "May (WE) norm.", size=0.5, ax=axes[3,1])
reg_line4b = sns.regplot(x="Elev", y="May (WE) norm.", data=site_snow_main, scatter=False, color='red', ax=axes[3,1])
axes[3,1].set_ylim(-.05,1.05)
scatter4b.legend_.remove()

plt.suptitle('Snowpack Patterns by Elevation (ft): Comparing Patterns between 1980s (Left Column) and 2010s (Right Column)', fontsize=15)

plt.savefig("./images/snow_we_elev_scatter.png")
plt.clf()

# %%
site_snow_main[site_snow_main['Decade'] == '2010']


# %%

# Snow and WE Levels by Elevation: Regression Slopes

# # 1980 Snow Slopes
# x_vals = reg_line1a.get_lines()[0].get_xdata()
# y_vals = reg_line1a.get_lines()[0].get_ydata()
# slope1 = (y_vals[1] - y_vals[0]) / (x_vals[1] - x_vals[0])

# # 1980 WE Slopes
# x_vals = reg_line1b.get_lines()[0].get_xdata()
# y_vals = reg_line1b.get_lines()[0].get_ydata()
# slope2 = (y_vals[1] - y_vals[0]) / (x_vals[1] - x_vals[0])

# # 2010 Snow Slopes
# x_vals = reg_line3a.get_lines()[0].get_xdata()
# y_vals = reg_line3a.get_lines()[0].get_ydata()
# slope3 = (y_vals[1] - y_vals[0]) / (x_vals[1] - x_vals[0])

# # 2010 WE Slopes
# x_vals = reg_line3b.get_lines()[0].get_xdata()
# y_vals = reg_line3b.get_lines()[0].get_ydata()
# slope4 = (y_vals[1] - y_vals[0]) / (x_vals[1] - x_vals[0])

# slope1
# slope2
# slope3
# slope4



# %%




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

melted_site_snow_main = pd.melt(site_snow_main, id_vars=['Decade'], value_vars=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'])
melted_site_snow_main = melted_site_snow_main[melted_site_snow_main['Decade'] != '2020']
# melted_site_snow_main

snow_month_decade_vioplots = go.Figure()

snow_month_decade_vioplots.add_trace(go.Violin(x=melted_site_snow_main['Decade'][melted_site_snow_main['variable'] == 'Jan'],
                                               y=melted_site_snow_main['value'][melted_site_snow_main['variable'] == 'Jan'],
                                               legendgroup='January', scalegroup='January', name='January',
                                               line_color='darkblue'))
snow_month_decade_vioplots.add_trace(go.Violin(x=melted_site_snow_main['Decade'][melted_site_snow_main['variable'] == 'Feb'],
                                               y=melted_site_snow_main['value'][melted_site_snow_main['variable'] == 'Feb'],
                                               legendgroup='February', scalegroup='February', name='February',
                                               line_color='blue'))
snow_month_decade_vioplots.add_trace(go.Violin(x=melted_site_snow_main['Decade'][melted_site_snow_main['variable'] == 'Mar'],
                                               y=melted_site_snow_main['value'][melted_site_snow_main['variable'] == 'Mar'],
                                               legendgroup='March', scalegroup='March', name='March',
                                               line_color='turquoise'))
snow_month_decade_vioplots.add_trace(go.Violin(x=melted_site_snow_main['Decade'][melted_site_snow_main['variable'] == 'Apr'],
                                               y=melted_site_snow_main['value'][melted_site_snow_main['variable'] == 'Apr'],
                                               legendgroup='April', scalegroup='April', name='April',
                                               line_color='limegreen'))
snow_month_decade_vioplots.add_trace(go.Violin(x=melted_site_snow_main['Decade'][melted_site_snow_main['variable'] == 'May'],
                                               y=melted_site_snow_main['value'][melted_site_snow_main['variable'] == 'May'],
                                               legendgroup='May', scalegroup='May', name='May',
                                               line_color='darkgreen'))

# snow_month_decade_vioplots.update_traces(box_visible=True, meanline_visible=True)
# snow_month_decade_vioplots.update_layout(xaxis=dict(categoryorder='array', categoryarray=['1980', '1990', '2000', '2010', '2020']), violinmode='group')
# snow_month_decade_vioplots.show()


# %%

melted_site_snow_main


# %%

site_snow_main

# %%

len(site_snow_main[site_snow_main['Water Year'] == 1982])

# %%

# Elevation by decade:

elev_hist = px.histogram(site_snow_main[(site_snow_main['Decade'] == '1980') | 
                                      (site_snow_main['Decade'] == '2000') |
                                       (site_snow_main['Decade'] == '2020')], 
                       x='Elev', nbins=30, title='Elevation Distributions: 1980s, 2000s (cumul.), 2020s (cumul.)', 
                       opacity=0.5, histnorm='probability density', color = 'Decade',
                       )
elev_hist.update_layout(barmode='overlay')
# fig2000 = px.histogram(site_snow_main[site_snow_main['Decade'] == '2000'], 
#                        x='Elev', nbins=30, title='Elevation Distribution: 2000', 
#                        opacity=0.5, histnorm='probability density', color_discrete_sequence=['green'])
# fig2020 = px.histogram(site_snow_main[site_snow_main['Decade'] == '2020'], 
#                        x='Elev', nbins=30, title='Elevation Distribution: 2020', 
#                        opacity=0.5, histnorm='probability density', color_discrete_sequence=['blue'])


# %%

site_snow_main['Water Year'].max()


# %%

# January Snow Levels by decade:

sns.distplot(site_snow_main[(site_snow_main['Decade'] == '1980') | (site_snow_main['Decade'] == '1990')]['Jan'], kde=True, label='1979 - 1999')
# sns.distplot(site_snow_main[site_snow_main['Decade'] == '2000']['May'], kde=True)
sns.distplot(site_snow_main[(site_snow_main['Decade'] == '2010') | (site_snow_main['Decade'] == '2020')]['Jan'], kde=True, label='2010 - 2023')

plt.legend()
plt.savefig("./images/snowpack_jan_decade.png")

plt.clf()

# plt.show()


# %%

# February Snow Levels by decade:

sns.distplot(site_snow_main[(site_snow_main['Decade'] == '1980') | (site_snow_main['Decade'] == '1990')]['Feb'], kde=True, label='1979 - 1999')
# sns.distplot(site_snow_main[site_snow_main['Decade'] == '2000']['May'], kde=True)
sns.distplot(site_snow_main[(site_snow_main['Decade'] == '2010') | (site_snow_main['Decade'] == '2020')]['Feb'], kde=True, label='2010 - 2023')

plt.legend()
plt.savefig("./images/snowpack_feb_decade.png")

plt.clf()

# plt.show()


# %%

# Apr Snow Levels by decade:

sns.distplot(site_snow_main[(site_snow_main['Decade'] == '1980') | (site_snow_main['Decade'] == '1990')]['Apr'], kde=True, label='1979 - 1999')
# sns.distplot(site_snow_main[site_snow_main['Decade'] == '2000']['May'], kde=True)
sns.distplot(site_snow_main[(site_snow_main['Decade'] == '2010') | (site_snow_main['Decade'] == '2020')]['Apr'], kde=True, label='2010 - 2023')

plt.legend()
plt.savefig("./images/snowpack_apr_decade.png")

plt.clf()

# plt.legend()
# plt.show()


# %%

# May Snow Levels by decade:

sns.distplot(site_snow_main[(site_snow_main['Decade'] == '1980') | (site_snow_main['Decade'] == '1990')]['May'], kde=True, label='1979 - 1999')
# sns.distplot(site_snow_main[site_snow_main['Decade'] == '2000']['May'], kde=True)
sns.distplot(site_snow_main[(site_snow_main['Decade'] == '2010') | (site_snow_main['Decade'] == '2020')]['May'], kde=True, label='2010 - 2023')

plt.legend()
plt.savefig("./images/snowpack_may_decade.png")

plt.clf()

# plt.legend()
# plt.show()


# %%
site_snow_main
# %%

# site_snow_main[site_snow_main['installed'].astype('string')].head()


# %%
