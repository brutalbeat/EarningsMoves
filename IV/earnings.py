# this file fetches earnings dates, prices, and computes realized moves around past earnings events.
# checking emil
import pandas as pd
import yfinance as yf

# this function takes a ticker then spits out the last limit earnings dates
def getEarningsDates(symbol, limit):
    t = yf.Ticker(symbol)
    df = t.get_earnings_dates(limit)
    if df is None or df.empty:
        return []
    dates = sorted(df.index.tz_localize(None).to_list())
    if limit:
        # keep only the most recent `limit` earnings dates
        return dates[-limit:]
    return dates

# this function calculates realized % moves of prices around the earnings dates
def realizedMoves(symbol, earningsDates, preDays=1, postDays=1):
    t = yf.Ticker(symbol)
    history = t.history(period="10y", auto_adjust=True)
    if history.empty:
        return pd.DataFrame(columns=["event_date", "gapMovePct", "oneDayMovePct"])
    history.index = history.index.tz_localize(None)
    
    def nearestIDX(ts): return history.index.get_indexer([ts], method="backfill")[0]
    
    rows = []
    
    for ed in earningsDates:
        iT = nearestIDX(pd.Timestamp(ed))
        if iT - preDays < 0 or iT + postDays >= len(history):
            continue

        Tm1 = history.index[iT - preDays]
        T = history.index[iT]
        Tp1 = history.index[iT + postDays]

        ctm1 = history.loc[Tm1, "Close"]
        ot = history.loc[T, "Open"]
        ctp1 = history.loc[Tp1, "Close"]

        rows.append({
            "event_date": T.date(),
            "gapMovePct": abs((ot - ctm1) / ctm1),
            "oneDayMovePct": abs((ctp1 - ctm1) / ctm1),
        })
    
    return pd.DataFrame(rows, columns=["event_date", "gapMovePct", "oneDayMovePct"])
