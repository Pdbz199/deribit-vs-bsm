#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from bsm import calculate_d1, calculate_d2, get_bsm_price
from greeks import calculate_greeks

TIME_SCALE_MINUTES = 60 # number of seconds in a minute

instrument_data = pd.read_csv('options_data.csv')
btc_historical_dataframe = pd.read_csv('btc_historical_prices.csv')
btc_historical_dataframe = btc_historical_dataframe.rename(columns={"time": "timestamp"})

# grouped_instrument_data = instrument_data.groupby('contract_name')

#%% Calculate volatility
# 2-3 hours/~180 data points
window_size = 180
log_prices = btc_historical_dataframe['close'].apply(lambda close: np.log(close))
log_returns = log_prices.pct_change(periods=window_size)
btc_historical_dataframe['std_dev'] = log_returns.rolling(window_size).std()

combined_dataframes = pd.merge(instrument_data, btc_historical_dataframe, on='timestamp')

#%% Contracts expire at 8 UTC exactly
contract_types = instrument_data['option_type'].to_numpy()
strikes = instrument_data['strike'].to_numpy()
expirations = instrument_data['expiration'].to_numpy()
times_to_expiration = instrument_data['time_to_expiration'].to_numpy()

#%% Calculate Black-Scholes
# start_time = 1619402183684
current_time = 1621821383684

r = 0
for i, row in combined_dataframes.iterrows():
    option_type = row['option_type']
    print("Option type:", option_type)
    S = row['close_y']
    print("S:", S)
    K = row['strike']
    print("K:", K)
    T = row['time_to_expiration']
    T /= TIME_SCALE_MINUTES # T is in minutes
    print("T:", T)
    sigma = row['std_dev']
    print("sigma:", sigma)
    d1 = calculate_d1(S, K, r, sigma, T)
    print("d1:", d1)
    d2 = calculate_d2(d1, sigma, T)
    print("d2:", d2)
    greeks = calculate_greeks(S, K, r, sigma, T, d1, d2, option_type)
    print("greeks:", greeks)
    bsm_price = get_bsm_price(S, K, option_type, r, sigma, T, d1, d2)
    print("BSM price:", bsm_price)
    deribit_price = row['close_x']
    print("Deribit price:", deribit_price)

    if i == 5: break

# %%
