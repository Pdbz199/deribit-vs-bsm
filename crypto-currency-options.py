from deribit_options_data import DeribitOptionsData
from bsm import get_bsm_price, calculate_d1, calculate_d2

optObj = DeribitOptionsData('BTC')
exp = optObj.expiries()

calls = optObj.get_side_exp('Call', exp[-2])
calls = calls[calls.dollar_mid > 0]
vols_a = []
print(calls.columns)
for row in calls.itertuples():
    sigma = float(optObj.option_info(row.instrument_name)['result']['ask_iv'] / 100)
    print("sigma:", sigma)
    S = row.underlying_price
    print("S:", S)
    K = row.strike
    print("K:", K)
    r = row.interest_rate
    print("r:", r)
    T = row.time
    print("T:", T)
    d1 = calculate_d1(S, K, r, sigma, T)
    d2 = calculate_d2(d1, sigma, T)
    V = get_bsm_price(S, K, 'call', row.interest_rate, calls.time, d1, d2)
    vols_a.append(sigma)
    print('#'*50)
    print(f'Calculated BS {V}')
    print(f'From api call {row.dollar_ask}')

calls['implied_vol_ask'] = vols_a