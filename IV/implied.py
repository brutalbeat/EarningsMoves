# this file will calculate implied moves 

import pandas as pd
import yfinance as yf
import math

def currentImpliedMove(symbol, earningsDate):
    t = yf.Ticker(symbol)
    expiries = [pd.Timestamp(x) for x in t.options]
    if not expiries:
        return None
    expiries.sort()
    ed = pd.Timestamp(earningsDate).tz_localize(None)
    expiry = next((e for e in expiries if e>=ed), expiries[-1])
    
    period = "1d"
    
    spotPrice = float(t.history(period)["Close"].iloc[-1])
    oc = t.option_chain(expiry.strftime("%Y-%m-%d"))
    
    # find nearest ATM IV
    calls = oc.calls.copy()
    puts = oc.puts.copy()

    # drop expired strikes so we don't average in zero or implied vol figures
    calls = calls[calls["impliedVolatility"].notna() & (calls["impliedVolatility"] > 0)].copy()
    puts = puts[puts["impliedVolatility"].notna() & (puts["impliedVolatility"] > 0)].copy()
    if calls.empty or puts.empty:
        return None

    calls["dist"] = (calls["strike"]-spotPrice).abs()
    puts["dist"] = (puts["strike"]-spotPrice).abs()
    ivCall = float(calls.loc[calls["dist"].idxmin(),"impliedVolatility"])
    ivPut  = float(puts.loc[puts["dist"].idxmin(),"impliedVolatility"])
    atmIV = (ivCall+ivPut)/2
    
    daysTilExpiry = max((expiry - pd.Timestamp.today().tz_localize(None)).days, 1)
    
    T = daysTilExpiry/365.0
    
    impliedMovePct = atmIV*math.sqrt(T) # from Black-Scholes
    
    return {
        "expiry": expiry.date(),
        "spot": spotPrice,
        "atmIV": atmIV,
        "impliedMovePct": impliedMovePct,
    }
    
