import numpy as np
from scipy.stats import norm
from typing import List

TIME_SCALE_WEEKS = 604800 # number of seconds in a week
TIME_SCALE_DAYS = 86400 # number of seconds in a day

UNIX_TIMESTAMP_TYPE = float # float representation of current time

def d1(S, K, r, sigma, T):
    # d1 = (log(S/K) + (r + (sigma^2/2))) / (sigma sqrt(T))
    return (np.log(S/K) + (r + ((np.power(sigma,2))/(2))) * T) / (sigma * np.sqrt(T))

def d2(d1, sigma, T):
    # d2 = d_1 - sigma sqrt(T)
    return d1 - sigma * np.sqrt(T)

def getBSMPrice(
    strike: float,
    contractType: str,
    expTime: float,
    currentTime: UNIX_TIMESTAMP_TYPE,
    priceData: List[float]
) -> float:
    # time
    tau = (expTime - currentTime) / TIME_SCALE_DAYS
    
    r = 0
    returns = priceData[1:] / priceData[:-1]
    log_returns = np.log(returns)
    sd = np.std(log_returns)

    currentPrice = priceData[-1]

    # d1 = (1/(sd*np.sqrt(tau))) * (np.log(currentPrice/strike) + (r + 0.5*sd**2)*tau)
    d1 = d1(currentPrice, strike, r, sd, tau)
    # d2 = d1 - sd*np.sqrt(tau)
    d2 = d2(d1, sd, tau)

    if contractType == "call":
        # c = S N(d_1) - K e^(-r T) N(d_2)
        BSMPrice = norm.cdf(d1) * currentPrice - norm.cdf(d2) * strike * np.exp(-r*tau)
        
    if contractType == "put":
        # p = K e^(-r T) N(-d_2) - S N(-d_1)
        BSMPrice = -norm.cdf(-d1) * currentPrice + norm.cdf(-d2) * strike * np.exp(-r*tau)
    
    return(BSMPrice)