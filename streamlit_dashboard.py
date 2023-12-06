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
from PIL import Image
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

selected_decs2 = st.multiselect('Select a decade (cumulative)', ['1980', '2000', '2020'],
                                 ['1980', '2000', '2020'])
df_dec_selected = eda.site_snow_main[eda.site_snow_main['Decade'].isin(selected_decs2)]

elev_hist = px.histogram(df_dec_selected, 
                       x='Elev', nbins=30, title='Elevation Distributions: 1980s, 2000s (cumul.), 2020s (cumul.)', 
                       opacity=0.5, histnorm='probability density', color = 'Decade', color_discrete_sequence=['forestgreen', 'cornflowerblue', 'coral'],
                       category_orders={'Decade': ['2020', '2000', '1980']}
                       )
elev_hist.update_layout(barmode='overlay')

st.plotly_chart(elev_hist, use_container_width=True)


###########################################################
# Snow levels by elevation: comparing 1980 and 2010 decades
# Create 2x2 scatter subplot matrix
st.subheader('Does Elevation ')

fig_scatter = Image.open('./images/snow_we_elev_scatter.png')

st.image(fig_scatter, 
         caption='Interpretation: these plots are designed to determine whether or not ' \
            'the nature of the snowpack and respective WE by elevation levels varies ' \
                'on a seasonal basis or over decades of time. As it is seen by the chart ' \
                'and (slope computation), the average snowpack and respective WE levels ' \
                    'change by elevation at a nearly-equivalent rate across decades. ' \
                        '.....',
         use_column_width=True)

# st.pyplot(img_scatter, use_container_width=True)


##############################################
### Snowpack by Month hists: comparing decades
st.subheader('Snowpack by Month: Comparing Grouped Decades')

selected_month = st.selectbox('Select a Month:', ['Jan', 'Feb', 'Apr', 'May'])

# snowpack_hist_early = sns.distplot(eda.site_snow_main[(eda.site_snow_main['Decade'] == '1980') | (eda.site_snow_main['Decade'] == '1990')][selected_month], kde=True, label='1979 - 1999')
# snowpack_hist_late = sns.distplot(eda.site_snow_main[(eda.site_snow_main['Decade'] == '2010') | (eda.site_snow_main['Decade'] == '2020')][selected_month], kde=True, label='2010 - 2023')
# plt.legend()
plt.savefig("snowpack_month_decade.png")

fig_snow_month_decade = Image.open('./images/snowpack_month_decade.png')

st.image(fig_snow_month_decade)


# Side by side (doesn't work with map)
# col1, col2 = st.columns(2)

# with col1:
#     st.plotly_chart(eda.plot2)

# with col2:
#     st.plotly_chart(eda.plot1)