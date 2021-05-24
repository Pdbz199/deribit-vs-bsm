#%%
import os
from dotenv import dotenv_values
config = dotenv_values(".env")
import openapi_client
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from openapi_client.rest import ApiException
from deribit_options_data import DeribitOptionsData
from historical_data import retrieve_historic_data, json_to_dataframe
from bitfinex_test import fetch_data

#%% Setup configuration instance
conf = openapi_client.Configuration()

#%% Setup unauthenticated client
client = openapi_client.ApiClient(conf)
publicAPI = openapi_client.PublicApi(client)

#%% Make requests
instruments = publicAPI.public_get_instruments_get(currency='BTC', kind='option')['result']

res = publicAPI.public_ticker_get(instruments[20]['instrument_name'])
print(res)