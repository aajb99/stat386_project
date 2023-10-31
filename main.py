# %%
import pandas as pd
import numpy as np
import requests
import re
import urllib.parse
import matplotlib.pyplot as plt
import seaborn as sns
import json


# %%

url = "https://jsearch.p.rapidapi.com/search"

query_params = {"query":"Data Scientist in US, USA","page":"1","num_pages":"2"}

# API Key
with open('localbusiness_apikey.txt', 'r') as file:
    localbusiness_key = file.read()

headers = {'X-RapidAPI-Key': localbusiness_key,
    'X-RapidAPI-Host': 'jsearch.p.rapidapi.com'}

response = requests.get(url, headers=headers, params = query_params)

print(response.json())

# %%

localbusiness_raw_df = pd.json_normalize(response.json().get('data'))


# %%

localbusiness_raw_df


# %%
