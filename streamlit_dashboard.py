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
import plotly.graph_objects as go
pd.set_option('display.max_columns', 200) # Shows all columns rather than "..."

st.title('Utah Snow Accumulation Study: Patterns 1979-2023')

st.write('This is a study to determine whether or not Snow Accumulation has changed its pattern over time in the ' \
         'state of Utah (US). Has there been a decrease in snowpack? Or maybe an increase? If so, where do we see ' \
            'these changes occurring, and what should they be attributed to? Let\'s take a look:')

st.write('Here is the primary dataset for the study. Month columns, such as as "Jan" or "May", denote the levels of ' \
         'snow data (in inches) collected at the beginning of that particular month. "Jan (WE)" contains the calculated ' \
            'water equivalent for such snow. The remaining categorical factors describe each SNOTEL Site (instrument for ' \
                'measuring snowpack—https://opensnow.com/news/post/snotel-explained).')
    

df_display = eda.site_snow_main.copy()
df_display['installed'] = df_display['installed'].astype('string')
df_display['Water Year'] = df_display['Water Year'].astype('string')
st.dataframe(df_display.head(5))

st.write('(Additional information on data collection/compilation and EDA/findings can be found here: ' \
         'https://aajb99.github.io/. Here\'s access to my Github with my code and figures: ' \
         'https://github.com/aajb99/stat386_project)')

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


st.write('The SNOTEL Site Maps above depict location and year/decade when they were installed/in use. This is to provide ' \
         'evidence that since the initial installments, SNOTEL Sites have been well distributed across Utah by decade, ' \
            'and thus each decade is well-represented across levels of location. There are a few obvious exceptions, but ' \
                'the general trend shows an even distribution across decades.')


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

st.write('The histograms above depict the distribution elevation level across the three decades listed. Similarly to ' \
         'the SNOTEL Site Maps, these provide evidence that the elevation of sites across decades is (fairly) evenly ' \
            'distributed, and thus decades are well-represented across levels of elevation.')


###########################################################
# Snow levels by elevation: comparing 1980 and 2010 decades
# Create 2x2 scatter subplot matrix
st.subheader('Is Elevation a Major Factor in Snowpack Variation Over Time?')

fig_scatter = Image.open('./images/snow_we_elev_scatter.png')

st.image(fig_scatter, 
         caption='These plots are designed to determine whether or not ' \
            'the nature of the snowpack (and respective WE) by elevation levels varies ' \
                'on a seasonal basis and over decades of time. As seen by the chart, ' \
                'the average snowpack and respective WE levels change at a consistent rate ' \
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
st.subheader('Snowpack by Month: Comparing Grouped Decades')

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
         'of the year progress, the observed snowpack distributions shift in opposite directions—specifically, the ' \
            'distribution from 1979-1999 sees relatively-higher levels of snowpack in the late season. It is interesting ' \
                'because at the same time, the distribution from 2010-2023 sees relatively-higher levels of snowpack ' \
                    'in the early season. Therefore, these trends provide evidence that if there is a general decline in snowfall ' \
                        'over years, it is more likely attributed to fluctuating weather patterns and temperature increases (causing shorter winter seasons) due ' \
                            'to global trends, and not a long-term drought issue.')


#####################################################
### Snowpack comparing months by decade: violin plots
st.subheader('Comparing Snowpack Progression over Months, by Decade')

selected_months = st.multiselect('Select Month(s)', ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
                                 ['Jan', 'Feb', 'Mar', 'Apr', 'May'])

snow_month_decade_vioplots = go.Figure()
color_list = ['darkblue', 'blue', 'turquoise', 'limegreen', 'darkgreen']

selected_columns = ['Decade'] + selected_months
df_selected = eda.site_snow_main[eda.site_snow_main['Decade'] != '2020']
df_selected = eda.site_snow_main[selected_columns]

# Iterate over selected months to create violin plots
for month, color in zip(['Jan', 'Feb', 'Mar', 'Apr', 'May'], color_list):
    if month in selected_months:
        trace = go.Violin(
            x=eda.melted_site_snow_main['Decade'][eda.melted_site_snow_main['variable'] == month],
            y=eda.melted_site_snow_main['value'][eda.melted_site_snow_main['variable'] == month],
            legendgroup=month, scalegroup=month, name=month,
            line_color=color
        )
        snow_month_decade_vioplots.add_trace(trace)

snow_month_decade_vioplots.update_traces(box_visible=True, meanline_visible=True)
snow_month_decade_vioplots.update_layout(xaxis=dict(categoryorder='array', categoryarray=['1980', '1990', '2000', '2010']), violinmode='group')
st.plotly_chart(snow_month_decade_vioplots, use_container_width=True)

st.write('Lastly, to further support my claim that there is a gradual decline in snowfall in Utah (due to weather fluctuations and ' \
         'temperature increases), this chart provides evidence of a general decrease as the distributions of observed snowpack ' \
            'gravitate to zero as decades increase. It is seen that extreme levels of snowpack are more frequent in earlier decades, ' \
                'and while months like Jan see higher median values in later decades, later months see a significant drop in median values' \
                    'over time. Thus, later decades experience shorter seasons of snowfall, and it is less evident that this . \
                        would be due to a decrease in precipitation, rather than in changes in global weather patterns and temperature.')







# selected_months = st.multiselect('Select Month(s)', ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
#                                  ['Jan', 'Feb', 'Mar', 'Apr', 'May'])

# snow_month_decade_vioplots = go.Figure()
# color_list = ['darkblue', 'blue', 'turquoise', 'limegreen', 'darkgreen']

# df_selected = eda.site_snow_main[eda.site_snow_main['Decade Inst'].isin(selected_decs)]

# if eda.melted_site_snow_main[eda.melted_site_snow_main['variable'] == 'Jan'].isin(selected_months):
#     snow_month_decade_vioplots.add_trace(go.Violin(x=eda.melted_site_snow_main['Decade'][eda.melted_site_snow_main['variable'] == 'Jan'],
#                                                y=eda.melted_site_snow_main['value'][eda.melted_site_snow_main['variable'] == 'Jan'],
#                                                legendgroup='January', scalegroup='January', name='January',
#                                                line_color='darkblue'))
# elif eda.melted_site_snow_main[eda.melted_site_snow_main['variable'] == 'Feb'].isin(selected_months):
#     snow_month_decade_vioplots.add_trace(go.Violin(x=eda.melted_site_snow_main['Decade'][eda.melted_site_snow_main['variable'] == 'Feb'],
#                                                y=eda.melted_site_snow_main['value'][eda.melted_site_snow_main['variable'] == 'Feb'],
#                                                legendgroup='February', scalegroup='February', name='February',
#                                                line_color='blue'))
# elif eda.melted_site_snow_main[eda.melted_site_snow_main['variable'] == 'Mar'].isin(selected_months):
#     snow_month_decade_vioplots.add_trace(go.Violin(x=eda.melted_site_snow_main['Decade'][eda.melted_site_snow_main['variable'] == 'Mar'],
#                                                y=eda.melted_site_snow_main['value'][eda.melted_site_snow_main['variable'] == 'Mar'],
#                                                legendgroup='March', scalegroup='March', name='March',
#                                                line_color='turquoise'))
# elif eda.melted_site_snow_main[eda.melted_site_snow_main['variable'] == 'Apr'].isin(selected_months):
#     snow_month_decade_vioplots.add_trace(go.Violin(x=eda.melted_site_snow_main['Decade'][eda.melted_site_snow_main['variable'] == 'Apr'],
#                                                y=eda.melted_site_snow_main['value'][eda.melted_site_snow_main['variable'] == 'Apr'],
#                                                legendgroup='April', scalegroup='April', name='April',
#                                                line_color='limegreen'))
# elif eda.melted_site_snow_main[eda.melted_site_snow_main['variable'] == 'May'].isin(selected_months):
#     snow_month_decade_vioplots.add_trace(go.Violin(x=eda.melted_site_snow_main['Decade'][eda.melted_site_snow_main['variable'] == 'May'],
#                                                y=eda.melted_site_snow_main['value'][eda.melted_site_snow_main['variable'] == 'May'],
#                                                legendgroup='May', scalegroup='May', name='May',
#                                                line_color='darkgreen'))

# snow_month_decade_vioplots.update_traces(box_visible=True, meanline_visible=True)
# snow_month_decade_vioplots.update_layout(xaxis=dict(categoryorder='array', categoryarray=['1980', '1990', '2000', '2010', '2020']), violinmode='group')
# st.plotly_chart(snow_month_decade_vioplots, use_container_width=True)



# Side by side (doesn't work with map)
# col1, col2 = st.columns(2)

# with col1:
#     st.plotly_chart(eda.plot2)

# with col2:
#     st.plotly_chart(eda.plot1)