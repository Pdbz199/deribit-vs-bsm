import numpy as np
from scipy.stats import norm

def calculate_d1(S, K, r, sigma, T):
    # d1 = (log(S/K) + (r + (sigma^2/2))) / (sigma sqrt(T))
    return (np.log(S/K) + (r + ((np.power(sigma,2))/(2))) * T) / (sigma * np.sqrt(T))

def calculate_d2(d1, sigma, T):
    # d2 = d_1 - sigma sqrt(T)
    return d1 - sigma * np.sqrt(T)

def get_bsm_price(
    S, K, contract_type, r, sigma, T, d1, d2
) -> float:
    if contract_type == "call":
        # c = S N(d_1) - K e^(-r T) N(d_2)
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif contract_type == "put":
        # p = K e^(-r T) N(-d_2) - S N(-d_1)
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)