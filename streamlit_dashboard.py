import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import eda

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






# Side by side (doesn't work with map)
# col1, col2 = st.columns(2)

# with col1:
#     st.plotly_chart(eda.plot2)

# with col2:
#     st.plotly_chart(eda.plot1)