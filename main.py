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

# Scrape home table #
#####################

home_table = pd.read_html('https://wcc.sc.egov.usda.gov/nwcc/snow-course-sites.jsp?state=UT')
home_table = home_table[0]
home_df = pd.DataFrame(home_table, columns=['Site_Name', 'Station', 'Ntwk', 'Elev', 'Lat', 'Lon', 'installed', 'state', 'County'])
home_df

# %%

# Scrape links (Selenium) #
###########################

url = 'https://wcc.sc.egov.usda.gov/nwcc/snow-course-sites.jsp?state=UT'
#response = requests.get(url)

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(url)

# Find the table containing the links
container = driver.find_element(By.CLASS_NAME, 'wcis')

rows = container.find_elements(By.TAG_NAME, 'tr')

row_links = container.find_elements(By.XPATH, './/td[contains(@class, "a")]')

links = []
snow_data_text = []
for row in rows:
    cells = row.find_elements(By.TAG_NAME, 'td')
    if len(cells) > 0:
        link = cells[0].find_elements(By.TAG_NAME, 'a')
        href = link[1].get_attribute('href')
        links.append(href)  



# %%

# MAIN SCRAPER LOOP #
# Loop through links and scrape txt data #
##########################################

snow_main = pd.DataFrame()

aerial_count = 0
no_data_count = 0

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

for site in range(0, len(links)):

    r = requests.get(links[site])
    r_txt = r.text

    if 'Water Year' in r.text:
        if 'AERIAL' in r.text:
            print('Failed Scrape: not SNOTEL measurement at link ' + str(site + 1))
            aerial_count += 1
        else:
            r_txt = re.split(r'(Water Year)', r_txt)
            r_txt = r_txt[1] + r_txt[2]

            # Use the replace method to remove the above string
            r_txt_clean = r_txt.replace(string_remove, '')
            # Split up string into rows using \n string
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
            r_clean_df['Site_Name'] = home_df['Site_Name'][site]

            snow_main = pd.concat([snow_main, r_clean_df], ignore_index=True)
    else:
        print('Failed Scrape: no txt data at link ' + str(site + 1))
        no_data_count += 1

    # print('Successful Scrape')

print('Total Sites with Aerial Measurements: ' + str(aerial_count))
print('Total Sites without txt data: ' + str(no_data_count))



# %%

# Save copy of snow_main
# For testing
snow_main_copy = snow_main


# %%

# Drop rows with more than half the columns as na

threshold = snow_main.shape[1] / 2
# snow_main[snow_main.isna().sum(axis=1) >= threshold]

snow_main = snow_main.replace('', pd.NA).dropna(thresh = threshold).reset_index(drop=True)
snow_main = snow_main.replace(pd.NA, np.nan)

# %%

# Convert snow levels columns to floats

snow_main.iloc[:, 1:13] = snow_main.iloc[:, 1:13].astype(float)


# %%

# Fill in missing Snow level data #
###################################

######### Snow / WE Coefficient #####################################
# Drop all rows with NAs
snowfall_vals = snow_main.dropna().reset_index(drop=True)

# Drop all rows with 0 to avoid nan vals and averages weighted to 0
snowfall_vals = snowfall_vals[~(snowfall_vals == 0).any(axis=1)]
snowfall_vals= snowfall_vals.reset_index(drop=True)

# Snow to WE coefficient (average of ~400 vals of snowfall/WE)
snow_we_coeff = np.mean([(snowfall_vals['Jan'] / snowfall_vals['Jan (WE)']), (snowfall_vals['Feb'] / snowfall_vals['Feb (WE)']), (snowfall_vals['Mar'] / snowfall_vals['Mar (WE)']),
                         (snowfall_vals['Apr'] / snowfall_vals['Apr (WE)']), (snowfall_vals['May'] / snowfall_vals['May (WE)']), (snowfall_vals['Jun'] / snowfall_vals['Jun (WE)'])])
# snow_we_coeff
######################################################################


######### Fill NaN values with coefficient ###########################
######### By column: coeff * ['Month' (WE)]
snow_main['Jan'] = snow_main['Jan'].fillna(snow_we_coeff * snow_main['Jan (WE)'])
snow_main['Feb'] = snow_main['Feb'].fillna(snow_we_coeff * snow_main['Feb (WE)'])
snow_main['Mar'] = snow_main['Mar'].fillna(snow_we_coeff * snow_main['Mar (WE)'])
snow_main['Apr'] = snow_main['Apr'].fillna(snow_we_coeff * snow_main['Apr (WE)'])
snow_main['May'] = snow_main['May'].fillna(snow_we_coeff * snow_main['May (WE)'])
snow_main['Jun'] = snow_main['Jun'].fillna(snow_we_coeff * snow_main['Jun (WE)'])
######################################################################



# %%

# Merge snow_main and home_df by Site_Name:

# Drop SNOW Ntwk
home_df = home_df[home_df['Ntwk'] == 'SNTL'].reset_index(drop=True)
# Merger:
site_snow_main = pd.merge(home_df, snow_main, on='Site_Name', how='inner')


# %%

site_snow_main = site_snow_main[['Site_Name', 
                                 # 'Station', 
                                 'Elev', 'Lat', 'Lon', 'installed', 
                                 # 'state',
       'County', 'Water Year', 'Jan', 'Jan (WE)', 'Feb', 'Feb (WE)', 'Mar',
       'Mar (WE)', 'Apr', 'Apr (WE)', 'May', 'May (WE)', 'Jun', 'Jun (WE)']]

site_snow_main


# %%

# site_snow_main.to_csv('site_snow.csv', index=None)


# %%

###################
# Custom Features #
###################

# 



# %%

# EDA #
#######

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

plt.savefig("snow_elev_scatter.png")



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

plt.savefig("we_elev_scatter.png")


# %%



# %%

site_snow_main['installed'].value_counts()

# %%

site_snow_main.columns

# %%

site_snow_main
# %%
