import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import eda
import requests
import re
import urllib.parse
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from sklearn.preprocessing import MinMaxScaler
pd.set_option('display.max_columns', 200) # Shows all columns rather than "..."

st.title('Utah Snow Accumulation Study: Patterns 1979-2023')

########################
### Site Installment Map
st.subheader('SNOTEL Site Installment Maps')

selected_unit = st.selectbox('Select a unit of time', ['By Year', 'By Decade'])

if selected_unit == 'By Year':
    st.write('SNOTEL Sites: Location and Year Installed')
    year = st.slider('Select year',eda.site_snow_main['installed'].min(),eda.site_snow_main['installed'].max())
    plot1 = px.scatter_geo(eda.site_snow_main[eda.site_snow_main['installed'] <= year], 
                           lat='Lat', lon='Lon', scope='usa', 
                           color='installed', color_continuous_scale='Sunsetdark', hover_name='Site_Name')
    
    plot1.update_layout(width = 1000, height = 500)
    plot1.update_traces(marker=dict(size=4))
    
    lat_foc = 39.61
    lon_foc = -111.0937
    
    plot1.update_layout(geo = dict(projection_scale=4.75, center=dict(lat=lat_foc, lon=lon_foc)))
    st.plotly_chart(plot1, use_container_width=True)
elif selected_unit == 'By Decade':
    st.write('SNOTEL Sites: Location and Decade Installed')
    selected_decs = st.multiselect('Select Decade(s)', eda.site_snow_main['Decade Inst'].unique(), 
                   eda.site_snow_main['Decade Inst'].unique())
    df_selected = eda.site_snow_main[eda.site_snow_main['Decade Inst'].isin(selected_decs)]
    plot2 = px.scatter_geo(df_selected, lat='Lat',
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
    st.plotly_chart(plot2, use_container_width=True)


########################
### Years in use Map
st.subheader('SNOTEL Sites, Years in Use Maps')

selected_unit = st.selectbox('Select unit of time in use', ['Year', 'Decade'])

if selected_unit == 'Year':
    st.write('SNOTEL Sites: those used in specified year with location')
    year = st.slider('Select year',eda.site_snow_main['Water Year'].min(),eda.site_snow_main['Water Year'].max())
    plot1 = px.scatter_geo(eda.site_snow_main[eda.site_snow_main['Water Year'] == year], 
                           lat='Lat', lon='Lon', scope='usa', hover_name='Site_Name')
    
    plot1.update_layout(width = 1000, height = 500)
    plot1.update_traces(marker=dict(size=4))
    
    lat_foc = 39.61
    lon_foc = -111.0937
    
    plot1.update_layout(geo = dict(projection_scale=4.75, center=dict(lat=lat_foc, lon=lon_foc)))
    st.plotly_chart(plot1, use_container_width=True)
elif selected_unit == 'Decade':
    st.write('SNOTEL Sites: Location and Decade In Use')
    selected_decs = st.multiselect('Select Decade(s)', eda.site_snow_main['Decade'].unique(), 
                   eda.site_snow_main['Decade'].unique())
    df_selected = eda.site_snow_main[eda.site_snow_main['Decade'].isin(selected_decs)]
    plot2 = px.scatter_geo(df_selected, lat='Lat',
               lon='Lon', scope='usa', 
               color='Decade', 
               category_orders={'Decade': ['2020', '2010', '2000', '1990', '1980']}, 
               color_discrete_sequence=['red', 'gold', 'green', 'blue', 'purple'],
               hover_name='Site_Name')

    plot2.update_layout(width = 1000, height = 500)
    plot2.update_traces(marker=dict(size=4))

    lat_foc = 39.61
    lon_foc = -111.0937
    plot2.update_layout(geo = dict(projection_scale=4.75, center=dict(lat=lat_foc, lon=lon_foc)))
    st.plotly_chart(plot2, use_container_width=True)


########################
### Elevation by Decade
st.subheader('Elevation by Decade')

selected_decade = st.selectbox('Select a decade (cumulative)', ['1980', '2000 (cumulative)', '2020 (cumulative)'])

if selected_decade == '1980':
    st.write('SNOTEL Sites Elevation Distribution: 1980')
    dist1 = eda.fig1980
    #st.plotly_chart(dist1, use_container_width=True)
elif selected_decade == '2000 (cumulative)':
    st.write('SNOTEL Sites Elevation Distribution: 2000')
    dist2 = eda.fig2000
    #st.plotly_chart(dist2, use_container_width=True)
elif selected_decade == '2020 (cumulative)':
    st.write('SNOTEL Sites Elevation Distribution: 2020')
    dist3 = eda.fig2020
    #st.plotly_chart(dist3, use_container_width=True)


###########################################################
# Snow levels by elevation: comparing 1980 and 2010 decades
# Create 2x2 scatter subplot matrix
fig, axes = plt.subplots(4, 2, figsize=(12, 10))

scat1a = eda.scatter1a
reg_line1a = eda.reg_line1a
axes[0,0].set_title('1980 Jan Snow Levels (normalized) by Elev (ft)')
axes[0,0].set_ylabel('SNOTEL Level (in)')
axes[0,0].set_xlabel('Elevation (ft)')
#
scat1b = eda.scatter1b
reg_line1b = eda.reg_line1b
axes[1,0].set_title('1980 Jan WE (normalized) by Elev (ft)')
axes[1,0].set_ylabel('SNOTEL Level (in)')
axes[1,0].set_xlabel('Elevation (ft)')
#
scat2a = eda.scatter2a
reg_line2a = eda.reg_line2a
axes[2,0].set_title('1980 May Snow Levels (normalized) by Elev (ft)')
axes[2,0].set_ylabel('SNOTEL Level (in)')
axes[2,0].set_xlabel('Elevation (ft)')
#
scat2b = eda.scatter2b
reg_line2b = eda.reg_line2b
axes[3,0].set_title('1980 May WE (normalized) by Elev (ft)')
axes[3,0].set_ylabel('SNOTEL Level (in)')
axes[3,0].set_xlabel('Elevation (ft)')
#
scat3a = eda.scatter3a
reg_line3a = eda.reg_line3a
axes[0,1].set_title('2010 Jan Snow Levels (normalized) by Elev (ft)')
axes[0,1].set_ylabel('SNOTEL Level (in)')
axes[0,1].set_xlabel('Elevation (ft)')
#
scat3b = eda.scatter3b
reg_line3b = eda.reg_line3b
axes[1,1].set_title('2010 Jan WE (normalized) by Elev (ft)')
axes[1,1].set_ylabel('SNOTEL Level (in)')
axes[1,1].set_xlabel('Elevation (ft)')
#
scat4a = eda.scatter4a
reg_line4a = eda.reg_line4a
axes[2,1].set_title('2010 May Snow Levels (normalized) by Elev (ft)')
axes[2,1].set_ylabel('SNOTEL Level (in)')
axes[2,1].set_xlabel('Elevation (ft)')
#
scat4b = eda.scatter4b
reg_line4b = eda.reg_line4b
axes[3,1].set_title('2010 May WE (normalized) by Elev (ft)')
axes[3,1].set_ylabel('SNOTEL Level (in)')
axes[3,1].set_xlabel('Elevation (ft)')
#
plt.tight_layout()
st.pyplot(fig)






# Side by side (doesn't work with map)
# col1, col2 = st.columns(2)

# with col1:
#     st.plotly_chart(eda.plot2)

# with col2:
#     st.plotly_chart(eda.plot1)