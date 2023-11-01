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

url = "https://ai-weather-by-meteosource.p.rapidapi.com/time_machine"

query_params = {"date":"2022","lat":"40.0966","lon":"111.5707","units":"auto"}

# API Key
with open('localbusiness_apikey.txt', 'r') as file:
    localbusiness_key = file.read()

headers = {'X-RapidAPI-Key': localbusiness_key,
    'X-RapidAPI-Host': 'ai-weather-by-meteosource.p.rapidapi.com'}

response = requests.get(url, headers=headers, params = query_params)

print(response.json())



# %%

weather_raw_df = pd.json_normalize(response.json().get('data'))


# %%

weather_raw_df


# %%
len(weather_raw_df)
# %%
