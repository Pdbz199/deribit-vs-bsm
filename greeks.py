import numpy as np
from scipy.stats import norm

def delta(d1, contractType):
    if contractType == "call":
        return norm.cdf(d1)
    elif contractType == "put":
        return -norm.cdf(-d1)

def gamma(S, sigma, T, d1):
    return ((1) / (S * sigma * np.sqrt(T))) * norm.pdf(d1)

def theta(S, K, r, sigma, T, d1, d2, contractType):
    if contractType == "call":
        return -((S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))) - r * K * np.exp(-r * T) * norm.cdf(d2)
    elif contractType == "put":
        return -((S * norm.pdf(-d1) * sigma) / (2 * np.sqrt(T))) + r * K * np.exp(-r * T) * norm.cdf(-d2)

def vega(S, T, d1):
    return S * np.sqrt(T) * norm.pdf(d1)

def rho(K, T, r, d2, contractType):
    if contractType == "call":
        return T * K * np.exp(-r * T) * norm.cdf(d2)
    elif contractType == "put":
        return -T * K * np.exp(-r * T) * norm.cdf(-d2)

def calculate_greeks(S, K, r, sigma, T, d1, d2, contractType):
    D = delta(d1, contractType)
    G = gamma(S, sigma, T, d1)
    Th = theta(S, K, r, sigma, T, d1, d2, contractType)
    V = vega(S, T, d1)
    R = rho(K, T, r, d2, contractType)

    return {
        "delta": D,
        "gamma": G,
        "theta": Th,
        "vega": V,
        "rho": R
    }