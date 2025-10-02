# this file fetches earnings dates, prices, and computes realized moves around past earnings events.

import pandas as pd
import yfinance as yf

# this function takes a ticker then spits out the last limit earnings dates
def getEarningsDates(symbol, limit):
    t = yf.Ticker(symbol)
    df = t.get_earnings_dates(limit)
    if df is None or df.empty:
        return []
    return sorted(df.index.tz_localize(None).toList())

# this function calculates realized % moves of prices around the earnings dates
def realizedMoves(symbol, earningsDates, preDays, postDays):
    t = yf.Ticker(symbol)
    history = t.history(period="10y", auto_adjust=True)
    if history.empty: return pd.DataFrame()
    history.index = history.index.tz_localize(None)
    
    def nearestIDX(ts): return history.index.get_indexer([ts], method="backfill")[0]
    
    rows = []
    
    for ed in earningsDates:
        iT = nearestIDX(pd.Timestamp(ed))
        if iT - preDays < 0 or iT + postDays >= len(history): continue
        Tm1, T, Tp1 = history.index[iT-preDays], history.index[iT], history.index[iT+postDays]
        c_tm1, o_t, c_tp1 = history.loc[Tm1,"Close"], history.loc[T,"Open"], history.loc[Tp1,"Close"]
        rows.append({
            "event_date": T.date(),
            "gap_move_pct": abs((o_t - c_tm1) / c_tm1),
            "one_day_move_pct": abs((c_tp1 - c_tm1) / c_tm1),
        })
    
    return pd.DataFrame(rows)

