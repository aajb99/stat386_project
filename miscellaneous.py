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

###### Previous attempt to parse through home page table ######

url = 'https://wcc.sc.egov.usda.gov/nwcc/snow-course-sites.jsp?state=UT'
#response = requests.get(url)

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(url)

home_data = []

# Find the table containing the data (you may need to inspect the webpage to locate the specific table)
container = driver.find_element(By.CLASS_NAME, 'wcis')
# products = container.find_elements(By.XPATH, './/li[contains(@class, "productListItem")]')

site_name = []
elevation = []
lat = []
long = []
yr_installed = []
state = []
county = []

row_data = []
col_index = 0

# Iterate through rows of the table
for row in container.find_elements(By.TAG_NAME, 'tr'):
    # Extract data from each row (you may need to modify this based on the table's structure)
    if row.find_elements(By.TAG_NAME, 'td'):
    
        columns = row.find_elements(By.TAG_NAME, 'td')
    
        for col in columns:
            row_data.append(col.text)  # Extract the text content for each column
    
        site_name = row_data[1 + col_index] if row_data[1 + col_index] else "N/A"
        #elevation = columns[2 + col_index].text if columns[2 + col_index].text else "N/A"
        #lat = columns[3 + col_index].text if columns[3 + col_index].text else "N/A"
        # long = columns[4 + col_index].text if columns[4 + col_index].text else "N/A"
        # yr_installed = columns[5 + col_index].text if columns[5 + col_index].text else "N/A"
        # state = columns[6 + col_index].text if columns[6 + col_index].text else "N/A"
        # county = columns[7 + col_index].text if columns[7 + col_index].text else "N/A"


        # site_name = row_data[1 + col_index]
        # print(row_data[2 + col_index])
        #elevation = columns[8 + col_index]
        # lat = columns[col_index + 3]
        # long = columns[col_index + 4]
        # yr_installed = columns[col_index + 5]
        # state = columns[col_index + 6]
        # county = columns[col_index + 7]

        # col_num = col_num + 12
    
        home_data.append((site_name))
        #home_data.append((site_name, elevation, lat, long, yr_installed, state, county))
        #print(str(len(row_data)))
        col_index = col_index + 12



#soup = BeautifulSoup(response.content, 'html.parser')

####################################################################

#table = soup.find_all('div',{'class':'article_movie_title'})
table = soup.find_all('div',{'class': 'wcis'})
home_site_df = pd.DataFrame()

# Create necessary columns
column_names = ['site_name', 'elevation', 'lat', 'long', 'yr_installed', 'state', 'county']
for col in column_names:
    home_site_df[col] = None

# Fill columns
for div in table:
    div_info = div.find('tr').text



###################################### .click function code ############################################

# link[1].click
        # driver.switch_to.window(driver.window_handles[-1])
        # driver.implicitly_wait(10)
        # page_text = driver.page_source
        # snow_data_text.append(page_text)
        # driver.close()  # Close the current tab/window
        # driver.switch_to.window(driver.window_handles[0]) 



###################################### Cleaning txt file from first historic link: Agua Canyon ############################################

### work on this link first, and create a df for it before iterating through other links

r = requests.get(links[0])
r_txt = r.text
r_txt = re.split(r'(Water Year)', r_txt)
r_txt = r_txt[1] + r_txt[2]

#r_txt = r.text.split('Water Year', 1)[1]

string_remove = "\n,Snow Water Equivalent Collection Date Start of Month Values,Snow Depth (in) " \
    "Start of Month Values,Snow Water Equivalent (in) Start of Month Values,Snow Water Equivalent " \
        "Collection Date Start of Month Values,Snow Depth (in) Start of Month Values,Snow Water " \
            "Equivalent (in) Start of Month Values,Snow Water Equivalent Collection Date Start of " \
                "Month Values,Snow Depth (in) Start of Month Values,Snow Water Equivalent (in) Start " \
                    "of Month Values,Snow Water Equivalent Collection Date Start of Month Values,Snow " \
                        "Depth (in) Start of Month Values,Snow Water Equivalent (in) Start of Month " \
                            "Values,Snow Water Equivalent Collection Date Start of Month Values,Snow " \
                                "Depth (in) Start of Month Values,Snow Water Equivalent (in) Start of " \
                                    "Month Values,Snow Water Equivalent Collection Date Start of Month " \
                                        "Values,Snow Depth (in) Start of Month Values,Snow Water Equivalent " \
                                            "(in) Start of Month Values"

# Use the replace method to remove the specified substring
r_txt_clean = r_txt.replace(string_remove, '')

r_txt_rows = r_txt_clean.split('\n')

# Convert rows of text into a Dataframe:
r_txt_df = pd.DataFrame([line.split(',') for line in r_txt_rows])
#####Remove empty cols in Dataframe:
r_clean_df = r_txt_df.drop(r_txt_df.columns[[1, 4, 7, 10, 13, 16]], axis=1)
#####Rename First row cells
r_clean_df.at[0, 3] = 'Jan (WE)'
r_clean_df.at[0, 6] = 'Feb (WE)'
r_clean_df.at[0, 9] = 'Mar (WE)'
r_clean_df.at[0, 12] = 'Apr (WE)'
r_clean_df.at[0, 15] = 'May (WE)'
r_clean_df.at[0, 18] = 'Jun (WE)'
##### Set first row to column index
r_clean_df.columns = r_clean_df.iloc[0]
r_clean_df = r_clean_df.iloc[1:].reset_index(drop=True)
##### Add Site_Name to r_clean_df
r_clean_df['Site_Name'] = home_df['Site_Name'][0]
    
# Drop rows with more than half the columns as na
threshold = snow_main.shape[1] / 2
# snow_main[snow_main.isna().sum(axis=1) >= threshold]
snow_main = snow_main.replace('', pd.NA).dropna(thresh = threshold).reset_index(drop=True)







############################################################
# Took from main to eda: ###################################
############################################################

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
site_snow_main.loc[site_snow_main['installed'].isin(range(1979, 1990)), 'Decade Inst'] = '1980'
site_snow_main.loc[site_snow_main['installed'].isin(range(1990, 2000)), 'Decade Inst'] = '1990'
site_snow_main.loc[site_snow_main['installed'].isin(range(2000, 2010)), 'Decade Inst'] = '2000'
site_snow_main.loc[site_snow_main['installed'].isin(range(2010, 2020)), 'Decade Inst'] = '2010'
site_snow_main.loc[site_snow_main['installed'].isin(range(2020, 2024)), 'Decade Inst'] = '2020'



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

# plot1 = px.scatter_geo(site_snow_main, lat='Lat',
#                lon='Lon', scope='usa', 
#                color='installed', color_continuous_scale='Sunsetdark',
#                hover_name='Site_Name')

# plot1.update_layout(width = 1000, height = 500)

# lat_foc = 39.3210
# lon_foc = -111.0937
# plot1.update_layout(geo = dict(projection_scale=4, center=dict(lat=lat_foc, lon=lon_foc)))

plot2 = px.scatter_geo(site_snow_main, lat='Lat',
               lon='Lon', scope='usa', 
               color='Decade Inst', color_continuous_scale='Sunsetdark',
               hover_name='Site_Name')

plot2.update_layout(width = 1000, height = 500)
plot2.update_traces(marker=dict(size=4))

lat_foc = 39.3210
lon_foc = -111.0937
plot2.update_layout(geo = dict(projection_scale=4, center=dict(lat=lat_foc, lon=lon_foc)))


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

#####################################################
### SCATTER PLOT MATRICES CODE ######################

### sns scatter subplots Jan, Feb, Apr, May Snow Levels by Elev ###
# Create the 3x2 subplot matrix

# fig, axes = plt.subplots(3, 2, figsize=(12, 10))

scatter1a = sns.scatterplot(site_snow_main, x = "Elev", y = "Jan", size=0.5)
reg_line1a = sns.regplot(x="Elev", y="Jan", data=site_snow_main, scatter=False, color='red')
# axes[0,0].set_title('Utah January Snow Levels (in) by Elevation (ft)')
# axes[0,0].set_ylabel('SNOTEL Level (in)')
# axes[0,0].set_xlabel('Elevation (ft)')

# scatter2a = sns.scatterplot(site_snow_main, x = "Elev", y = "Feb", size=0.5, ax=axes[0,1])
# reg_line2a = sns.regplot(x="Elev", y="Feb", data=site_snow_main, scatter=False, color='red', ax=axes[0,1])
# axes[0,1].set_title('February Snow Levels (in) by Elevation (ft)')
# axes[0,1].set_ylabel('SNOTEL Level (in)')
# axes[0,1].set_xlabel('Elevation (ft)')

# scatter3a = sns.scatterplot(site_snow_main, x = "Elev", y = "Mar", size=0.5, ax=axes[1,0])
# reg_line3a = sns.regplot(x="Elev", y="Mar", data=site_snow_main, scatter=False, color='red', ax=axes[1,0])
# axes[1,0].set_title('March Snow Levels (in) by Elevation (ft)')
# axes[1,0].set_ylabel('SNOTEL Level (in)')
# axes[1,0].set_xlabel('Elevation (ft)')

# scatter4a = sns.scatterplot(site_snow_main, x = "Elev", y = "Apr", size=0.5, ax=axes[1,1])
# reg_line4a = sns.regplot(x="Elev", y="Apr", data=site_snow_main, scatter=False, color='red', ax=axes[1,1])
# axes[1,1].set_title('April Snow Levels (in) by Elevation (ft)')
# axes[1,1].set_ylabel('SNOTEL Level (in)')
# axes[1,1].set_xlabel('Elevation (ft)')

# scatter5a = sns.scatterplot(site_snow_main, x = "Elev", y = "May", size=0.5, ax=axes[2,0])
# reg_line5a = sns.regplot(x="Elev", y="May", data=site_snow_main, scatter=False, color='red', ax=axes[2,0])
# axes[2,0].set_title('May Snow Levels (in) by Elevation (ft)')
# axes[2,0].set_ylabel('SNOTEL Level (in)')
# axes[2,0].set_xlabel('Elevation (ft)')

# # Delete 6th plot
# fig.delaxes(axes[2, 1])

plt.tight_layout()

plt.show()
# plt.savefig("snow_elev_scatter.png")



### sns scatter subplots Jan, Feb, Apr, May Snow Levels by Elev ###
# Create the 3x2 subplot matrix
# fig, axes = plt.subplots(3, 2, figsize=(12, 10))

scatter1b = sns.scatterplot(site_snow_main, x = "Elev", y = "Jan (WE)", size=0.5)
reg_line1b = sns.regplot(x="Elev", y="Jan (WE)", data=site_snow_main, scatter=False, color='red')
plt.ylim(site_snow_main['Jan'].min(), site_snow_main['Jan'].max())
# axes[0,0].set_title('Utah January Water Equiv Levels (in) by Elevation (ft)')
# axes[0,0].set_ylabel('Level (in)')
# axes[0,0].set_xlabel('Elevation (ft)')

# scatter2b = sns.scatterplot(site_snow_main, x = "Elev", y = "Feb (WE)", size=0.5, ax=axes[0,1])
# reg_line2b = sns.regplot(x="Elev", y="Feb (WE)", data=site_snow_main, scatter=False, color='red', ax=axes[0,1])
# axes[0,1].set_title('February Water Equiv Levels (in) by Elevation (ft)')
# axes[0,1].set_ylabel('Level (in)')
# axes[0,1].set_xlabel('Elevation (ft)')

# scatter3b = sns.scatterplot(site_snow_main, x = "Elev", y = "Mar (WE)", size=0.5, ax=axes[1,0])
# reg_line3b = sns.regplot(x="Elev", y="Mar (WE)", data=site_snow_main, scatter=False, color='red', ax=axes[1,0])
# axes[1,0].set_title('March Water Equiv Levels (in) by Elevation (ft)')
# axes[1,0].set_ylabel('Level (in)')
# axes[1,0].set_xlabel('Elevation (ft)')

# scatter4b = sns.scatterplot(site_snow_main, x = "Elev", y = "Apr (WE)", size=0.5, ax=axes[1,1])
# reg_line4b = sns.regplot(x="Elev", y="Apr (WE)", data=site_snow_main, scatter=False, color='red', ax=axes[1,1])
# axes[1,1].set_title('April Water Equiv Levels (in) by Elevation (ft)')
# axes[1,1].set_ylabel('Level (in)')
# axes[1,1].set_xlabel('Elevation (ft)')

# scatter5b = sns.scatterplot(site_snow_main, x = "Elev", y = "May (WE)", size=0.5, ax=axes[2,0])
# reg_line5b = sns.regplot(x="Elev", y="May (WE)", data=site_snow_main, scatter=False, color='red', ax=axes[2,0])
# axes[2,0].set_title('May Water Equiv Levels (in) by Elevation (ft)')
# axes[2,0].set_ylabel('Level (in)')
# axes[2,0].set_xlabel('Elevation (ft)')

# # Delete 6th plot
# fig.delaxes(axes[2, 1])

plt.tight_layout()

plt.show()
# plt.savefig("we_elev_scatter.png")
