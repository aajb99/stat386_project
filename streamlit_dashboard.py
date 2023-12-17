import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import requests
import re
import urllib.parse
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
#from selenium import webdriver
#from selenium.webdriver.chrome.service import Service as ChromeService
#from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.common.by import By
#import time
#from sklearn.preprocessing import MinMaxScaler
from PIL import Image
import plotly.graph_objects as go
pd.set_option('display.max_columns', 200) # Shows all columns rather than "..."

st.title('Utah Snow Accumulation Study: Patterns Between 1979-2023')

st.write('This is a study to determine whether or not snow accumulation patterns have changed over time in the ' \
         'state of Utah (US). Has there been a decrease in snowpack? Or maybe an increase? If so, where do we see ' \
            'these changes occurring, and what should they be attributed to? Let\'s take a look:')

st.write('Here is the primary dataset for the study. Month columns, such as as "Jan" or "May", denote the levels of ' \
         'snow data (in inches) collected at the beginning of that particular month. "Jan (WE)" contains the calculated ' \
            'water equivalent for such snow. The remaining categorical factors describe each SNOTEL Site (instrument for ' \
                'measuring snowpack—https://opensnow.com/news/post/snotel-explained).')


# Read in Data and Customize Features#################################################################################################
site_snow_main = pd.read_csv('site_snow.csv')

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

# site_snow_main


# # Normalized Jan and Jan (WE) for scatterplot EDA below:
# scaler = MinMaxScaler()
# # Normalize Jan
# site_snow_main['Jan norm.'] = scaler.fit_transform(site_snow_main[['Jan']])
# # Normalize the Jan (WE) column
# site_snow_main['Jan (WE) norm.'] = scaler.fit_transform(site_snow_main[['Jan (WE)']])

# # Normalized May and May (WE) for scatterplot EDA below:
# scaler = MinMaxScaler()
# # Normalize Jan
# site_snow_main['May norm.'] = scaler.fit_transform(site_snow_main[['May']])
# # Normalize the Jan (WE) column
# site_snow_main['May (WE) norm.'] = scaler.fit_transform(site_snow_main[['May (WE)']])

#################################################################################################################################


melted_site_snow_main = pd.melt(site_snow_main, id_vars=['Decade'], value_vars=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'])
melted_site_snow_main = melted_site_snow_main[melted_site_snow_main['Decade'] != '2020']

df_display = site_snow_main.copy()
df_display['installed'] = df_display['installed'].astype('string')
df_display['Water Year'] = df_display['Water Year'].astype('string')
st.dataframe(df_display.head(5))

#############################################################################################################################

########################
### Correlation Heatmaps
st.subheader('Correlation Heatmaps: By Month, Observing Key Factors')

selected_month = st.selectbox('Select a Month:', ['Jan', 'Feb', 'Apr', 'May'])

fig_h1 = Image.open('./images/jan_heatmap.png')
fig_h2 = Image.open('./images/feb_heatmap.png')
fig_h3 = Image.open('./images/apr_heatmap.png')
fig_h4 = Image.open('./images/may_heatmap.png')

if selected_month == 'Jan':
    st.image(fig_h1, caption='January',
             use_column_width=True)
    st.empty()
elif selected_month == 'Feb':
    st.image(fig_h2, caption='February',
             use_column_width=True)
    st.empty()
elif selected_month == 'Apr':
    st.image(fig_h3, caption='April',
             use_column_width=True)
    st.empty()
elif selected_month == 'May':
    st.image(fig_h4, caption='May',
             use_column_width=True)
    st.empty()

st.write('The correlation heatmaps depict each monthly snowpack factor and its correlation ' \
         'with other variables. As it is depicted here, there is a general trend of decreasing correlation ' \
            'between the monthly snowpack/water equivalent factors with factors of time, including decade, water year, ' \
                'and year installed. This will be explored further, but other relationships must be analyzed, such as ' \
                    'elevation and location (Lat/Lon) with snowpack—strong correlations here would prove difficult to ' \
                        'isolate and analyze the relationship between snowpack and time variables.')


########################
### Site Installment Map
st.subheader('SNOTEL Site Installment Maps')

selected_unit = st.selectbox('Select a unit of time', ['By Year', 'By Decade'])

if selected_unit == 'By Year':
    st.write('SNOTEL Sites: Location and Year Installed')
    year = st.slider('Select year',site_snow_main['installed'].min(),site_snow_main['installed'].max())
    plot1 = px.scatter_geo(site_snow_main[site_snow_main['installed'] <= year], 
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
    selected_decs = st.multiselect('Select Decade(s)', site_snow_main['Decade Inst'].unique(), 
                   site_snow_main['Decade Inst'].unique())
    df_selected = site_snow_main[site_snow_main['Decade Inst'].isin(selected_decs)]
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
    year = st.slider('Select year',site_snow_main['Water Year'].min(),site_snow_main['Water Year'].max())
    plot1 = px.scatter_geo(site_snow_main[site_snow_main['Water Year'] == year], 
                           lat='Lat', lon='Lon', scope='usa', hover_name='Site_Name')
    
    plot1.update_layout(width = 1000, height = 500)
    plot1.update_traces(marker=dict(size=4))
    
    lat_foc = 39.61
    lon_foc = -111.0937
    
    plot1.update_layout(geo = dict(projection_scale=4.75, center=dict(lat=lat_foc, lon=lon_foc)))
    st.plotly_chart(plot1, use_container_width=True)
elif selected_unit == 'Decade':
    st.write('SNOTEL Sites: Location and Decade In Use')
    selected_decs = st.multiselect('Select Decade(s)', site_snow_main['Decade'].unique(), 
                   site_snow_main['Decade'].unique())
    df_selected = site_snow_main[site_snow_main['Decade'].isin(selected_decs)]
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


st.write('The SNOTEL Site Maps above depict location and year/decade when they were installed/in use. This is to provide ' \
         'evidence that since their initial installments, SNOTEL Sites have been well distributed across Utah by decade, ' \
            'and thus each decade is well-representative of location. There are a few obvious exceptions, but ' \
                'the general trend shows an even distribution across decades.')


########################
### Elevation by Decade
st.subheader('Elevation (ft) by Decade')

selected_decs2 = st.multiselect('Select a decade (cumulative)', ['1980', '2000', '2020'],
                                 ['1980', '2000', '2020'])
df_dec_selected = site_snow_main[site_snow_main['Decade'].isin(selected_decs2)]

elev_hist = px.histogram(df_dec_selected, 
                       x='Elev', nbins=30, title='Elevation Distributions: 1980s, 2000s (cumul.), 2020s (cumul.)', 
                       opacity=0.5, histnorm='probability density', color = 'Decade', color_discrete_sequence=['forestgreen', 'cornflowerblue', 'coral'],
                       category_orders={'Decade': ['2020', '2000', '1980']}
                       )
elev_hist.update_layout(barmode='overlay')

st.plotly_chart(elev_hist, use_container_width=True)

st.write('The histograms above depict the distribution elevation level (feet) across the three decades listed. Similarly to ' \
         'the SNOTEL Site Maps, these provide evidence that the elevation of sites across decades is (fairly) evenly ' \
            'distributed, and thus decades are well-representative of elevation.')


###########################################################
# Snow levels by elevation: comparing 1980 and 2010 decades
# Create 2x2 scatter subplot matrix
st.subheader('Is Elevation a Major Factor in Snowpack Variation Over Time?')

fig_scatter = Image.open('./images/snow_we_elev_scatter.png')

st.image(fig_scatter, 
         caption='These plots are designed to determine whether or not ' \
            'the nature of the snowpack (and respective WE) by elevation levels varies ' \
                'on a seasonal basis and over decades of time. As seen by the chart, ' \
                'the average snowpack and respective WE levels (in) change at a consistent rate ' \
                    'at each level of month (slope calculations also reflect this consistency) across decades. '\
                        'While the regression pattern does change between months (Jan to May), ' \
                            'which is expected as lower elevations experience a faster transition to ' \
                                'above-freezing temperatures, the trends stay consistent across decades. Thus,' \
                                'we can assume that the nature of snow is constant and comparable across decades.',
         use_column_width=True)

st.empty()

# st.pyplot(img_scatter, use_container_width=True)


##############################################
### Snowpack by Month hists: comparing decades
st.subheader('Snowpack (in) by Month: Comparing Grouped Decades')

selected_month2 = st.selectbox('Select a Month:', ['January', 'February', 'April', 'May'])

fig_smd1 = Image.open('./images/snowpack_jan_decade.png')
fig_smd2 = Image.open('./images/snowpack_feb_decade.png')
fig_smd3 = Image.open('./images/snowpack_apr_decade.png')
fig_smd4 = Image.open('./images/snowpack_may_decade.png')

if selected_month2 == 'January':
    st.image(fig_smd1, caption='January',
             use_column_width=True)
    st.empty()
elif selected_month2 == 'February':
    st.image(fig_smd2, caption='February',
             use_column_width=True)
    st.empty()
elif selected_month2 == 'April':
    st.image(fig_smd3, caption='April',
             use_column_width=True)
    st.empty()
elif selected_month2 == 'May':
    st.image(fig_smd4, caption='May',
             use_column_width=True)
    st.empty()


st.write('Going back to the previous trends depicted in the correlation heatmaps, it is noted that as the months ' \
         'of the year progress, the observed snowpack (in) distributions shift in opposite directions—specifically, the ' \
            'distribution from 1979-1999 sees relatively-higher levels of snowpack in the late season. It is interesting ' \
                'because at the same time, the distribution from 2010-2023 sees relatively-higher levels of snowpack ' \
                    'in the early season. Therefore, these trends provide evidence that if there is a general decline in snowfall ' \
                        'over years, it is more likely attributed to fluctuating weather patterns and temperature increases (causing shorter winter seasons) due ' \
                            'to global trends, rather than a long-term drought issue.')


#####################################################
### Snowpack comparing months by decade: violin plots
st.subheader('Comparing Snowpack (in) Progression over Months, by Decade')

selected_months = st.multiselect('Select Month(s)', ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
                                 ['Jan', 'Feb', 'Mar', 'Apr', 'May'])

snow_month_decade_vioplots = go.Figure()
color_list = ['darkblue', 'blue', 'turquoise', 'limegreen', 'darkgreen']

selected_columns = ['Decade'] + selected_months
df_selected = site_snow_main[site_snow_main['Decade'] != '2020']
df_selected = site_snow_main[selected_columns]

# Iterate over selected months to create violin plots
for month, color in zip(['Jan', 'Feb', 'Mar', 'Apr', 'May'], color_list):
    if month in selected_months:
        trace = go.Violin(
            x=melted_site_snow_main['Decade'][melted_site_snow_main['variable'] == month],
            y=melted_site_snow_main['value'][melted_site_snow_main['variable'] == month],
            legendgroup=month, scalegroup=month, name=month,
            line_color=color
        )
        snow_month_decade_vioplots.add_trace(trace)

snow_month_decade_vioplots.update_traces(box_visible=True, meanline_visible=True)
snow_month_decade_vioplots.update_layout(xaxis=dict(categoryorder='array', 
                                                    categoryarray=['1980', '1990', '2000', '2010']), 
                                                    violinmode='group')
snow_month_decade_vioplots.update_yaxes(title_text = 'Snow Level (in)')
snow_month_decade_vioplots.update_xaxes(title_text = 'Decade')
st.plotly_chart(snow_month_decade_vioplots, use_container_width=True)

st.write('Lastly, to further support my claim that there is a gradual decline in snowfall in Utah (due to weather fluctuations and ' \
         'temperature increases), this chart provides evidence of a general decrease as the distributions of observed snowpack ' \
            'gravitate to zero as decades increase. It is seen that extreme levels of snowpack are more frequent in earlier decades, ' \
                'and while months like Jan see higher median values in later decades, later months see a significant drop in median values' \
                    'over time. Thus, later decades experience shorter seasons of snowfall, and it is less evident that this . \
                        would be due to a decrease in precipitation, rather than in changes in global weather patterns and temperature.')


st.subheader('Links')
st.write('Data collection/compilation and EDA/findings: https://aajb99.github.io/')
st.write('My Github with code and figures: https://github.com/aajb99/stat386_project')
st.write('For more on SNOTEL Sites: https://opensnow.com/news/post/snotel-explained')
st.write('USDA—Air & Water Database: https://wcc.sc.egov.usda.gov/nwcc/snow-course-sites.jsp?state=UT')