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

#%% Authenticate with API credentials
response = publicAPI.public_auth_get('client_credentials', '', '', config['CLIENT_ID'], config['CLIENT_SECRET'], '', '', '')
access_token = response['result']['access_token']

conf_authed = openapi_client.Configuration()
conf_authed.access_token = access_token

#%% Use retrieved authentication token to setup private endpoint client
client_authed = openapi_client.ApiClient(conf_authed)
privateAPI = openapi_client.PrivateApi(client_authed)

#%% Define query params
timeframe = '1'

end = datetime.now()
start = end - timedelta(weeks=4)
# start = end - timedelta(days=1)

start = int(start.timestamp() * 1000)
end = int(end.timestamp() * 1000)

print("Start:", start)
print("End:", end)

bin_size = '1m'
limit = 1000
time_step = 1000 * 60 * limit

#%% Make requests
instruments = publicAPI.public_get_instruments_get(currency='BTC', kind='option')['result']

instrument_names = list(map(lambda instrument: instrument['instrument_name'], instruments))
expiration_times = list(map(lambda instrument: instrument['expiration_timestamp'], instruments))
strikes = list(map(lambda instrument: instrument['strike'], instruments))
option_types = list(map(lambda instrument: instrument['option_type'], instruments))

instrument_data = json_to_dataframe(retrieve_historic_data(start, end, instrument_names[0], timeframe))
instrument_data['contract_name'] = instrument_names[0]
instrument_data['option_type'] = option_types[0]
instrument_data['strike'] = strikes[0]
instrument_data['expiration'] = expiration_times[0]

for i in range(1, len(instrument_names)):
    json_res = retrieve_historic_data(start, end, instrument_names[i], timeframe)

    try:
        df = json_to_dataframe(json_res)
        df['contract_name'] = instrument_names[i]
        df['option_type'] = option_types[i]
        df['strike'] = strikes[i]
        df['expiration'] = expiration_times[i]

        if not df.empty:
            # print(df.head())
            instrument_data = pd.concat([instrument_data,df])
    except:
        print("Exception occurred, continuing...")

instrument_data.drop_duplicates().reset_index(drop=True)
instrument_data['time_to_expiration'] = instrument_data.apply(lambda row: row['expiration'] - (pd.Timestamp(row['timestamp']).timestamp() * 1000), axis=1)
instrument_data.to_csv('options_data.csv')

#%% Underlier historical data
btc_historical_data = fetch_data(start=start, stop=end, symbol='btcusd', interval=bin_size, tick_limit=limit, step=time_step)

# Remove error messages
ind = [np.ndim(x) != 0 for x in btc_historical_data]
btc_historical_data = [i for (i, v) in zip(btc_historical_data, ind) if v]
# Create pandas data frame and clean data
names = ['time', 'open', 'close', 'high', 'low', 'volume']
btc_historical_dataframe = pd.DataFrame(btc_historical_data, columns=names)
btc_historical_dataframe.drop_duplicates(inplace=True)
btc_historical_dataframe['time'] = pd.to_datetime(btc_historical_dataframe['time'], unit='ms')
btc_historical_dataframe.set_index('time', inplace=True)
btc_historical_dataframe.sort_index(inplace=True)
btc_historical_dataframe.to_csv('btc_historical_prices.csv')