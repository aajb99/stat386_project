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
    
