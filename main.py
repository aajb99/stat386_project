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

# %%

url = 'https://wcc.sc.egov.usda.gov/nwcc/snow-course-sites.jsp?state=UT'
#response = requests.get(url)


# %%

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

# %%

len(columns)


#### ISSUE TO HERE AND ABOVE ####



# %%

#table = soup.find_all('div',{'class':'article_movie_title'})
table = soup.find_all('div',{'class': 'wcis'})
home_site_df = pd.DataFrame()


# %%

# Create necessary columns
column_names = ['site_name', 'elevation', 'lat', 'long', 'yr_installed', 'state', 'county']
for col in column_names:
    home_site_df[col] = None

# Fill columns
for div in table:
    div_info = div.find('tr').text
    

# %%

div_info



