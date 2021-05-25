#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from bsm import calculate_d1, calculate_d2, get_bsm_price
from greeks import calculate_greeks

MINUTES_PER_YEAR = 60 * 24 * 7 * 52
SECONDS_PER_YEAR = 60 * MINUTES_PER_YEAR

instrument_data = pd.read_csv('options_data.csv')
btc_historical_dataframe = pd.read_csv('btc_historical_prices.csv')
btc_historical_dataframe = btc_historical_dataframe.rename(columns={"time": "timestamp"})

# grouped_instrument_data = instrument_data.groupby('contract_name')

#%% Calculate volatility
# 2-3 hours/~180 data points
window_size = 1000 #180
log_prices = btc_historical_dataframe['close'].apply(lambda close: np.log(close))
log_returns = log_prices.pct_change(periods=window_size)
btc_historical_dataframe['std_dev'] = log_returns.rolling(window_size).std()

#? funky shit?
combined_dataframes = pd.merge(instrument_data, btc_historical_dataframe, on='timestamp')

#%% Separate out important pieces
# contract_types = instrument_data['option_type'].to_numpy()
# strikes = instrument_data['strike'].to_numpy()
# expirations = instrument_data['expiration'].to_numpy()
# times_to_expiration = instrument_data['time_to_expiration'].to_numpy()

#%% Calculate Black-Scholes
# start_time = 1619402183684
current_time = 1621821383684

r = 0.0

bsm_prices = []
deribit_prices = []

# window_size = 1000 #180
# log_prices = btc_historical_dataframe['close'].apply(lambda close: np.log(close))
# log_returns = log_prices.pct_change(periods=window_size)
# btc_historical_dataframe['std_dev'] = log_returns.rolling(window_size).std()

# for_one_contract = combined_dataframes[combined_dataframes['contract_name']==combined_dataframes['contract_name'].iloc[0]]
# timestamps = (for_one_contract['timestamp'].apply(lambda time: pd.Timestamp(time).strftime('%m-%d %H:%M'))).to_numpy()

deltas = []
gammas = []
thetas = []
vegas = []
rhos = []
for i, row in combined_dataframes.iterrows():
    option_type = row['option_type']
    # print("Option type:", option_type)
    S = row['close_y']
    # print("S:", S)
    K = row['strike']
    # print("K:", K)
    T = row['time_to_expiration']
    T /= SECONDS_PER_YEAR # T is in years
    # print("T:", T)
    sigma = row['std_dev']
    sigma *= np.sqrt(MINUTES_PER_YEAR)
    # print("sigma:", sigma)
    d1 = calculate_d1(S, K, r, sigma, T)
    # print("d1:", d1)
    d2 = calculate_d2(d1, sigma, T)
    # print("d2:", d2)
    greeks = calculate_greeks(S, K, r, sigma, T, d1, d2, option_type)
    # deltas.append(greeks['delta'])
    # gammas.append(greeks['gamma'])
    # thetas.append(greeks['theta'])
    # vegas.append(greeks['vega'])
    # rhos.append(greeks['rho'])
    # print("greeks:", greeks)
    # bsm_price = get_bsm_price(S, K, option_type, r, T, d1, d2)
    # print("BSM price:", bsm_price)
    # bsm_prices.append(bsm_price)
    # deribit_price = row['close_x'] * S
    # print("Deribit price:", deribit_price)
    # deribit_prices.append(deribit_price)
    break

# wedges = np.load('wedges.npy')
# combined_dataframes['wedges'] = wedges
# grouped = combined_dataframes.groupby('timestamp')
# mean_wedges_over_time = grouped['wedges'].median().to_numpy()
# grouped_times = np.array(list(map(lambda x: x[5:-3], list(grouped.groups.keys()))))
# plt.plot(grouped_times, mean_wedges_over_time)
# plt.xticks(range(0, len(grouped_times), 2000))
# plt.show()

# greek_cols = ['delta', 'gamma', 'theta', 'vega', 'rho']
# all_greeks = pd.DataFrame(np.array([deltas, gammas, thetas, vegas, rhos]).T, columns=greek_cols)
# all_greeks.describe().T.to_csv('greeks.csv')
all_greeks = pd.read_csv('greeks.csv')

# graph price comparison - done
# mean wedge between bsm_prices and deribit_prices
# time series volatility (same thing as returns but with wedges)
# graph how the (median) wedge varies with the underlier

# summary stats greeks table
# summary stats for wedge over all contracts and all times

#%%
bsm_prices = np.array(bsm_prices)
deribit_prices = np.array(deribit_prices)

#%%