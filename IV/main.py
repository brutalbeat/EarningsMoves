# main file

import argparse
import pandas as pd

from earnings import getEarningsDates, realizedMoves
from implied import currentImpliedMove
from plots import histogramRealized, timelineMoves

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--events", type=int, default=12)
    args = ap.parse_args()
    
    edates = getEarningsDates(args.ticker, args.events)
    rdf = realizedMoves(args.ticker, edates)

    next_event = None
    if edates:
        today = pd.Timestamp.today().normalize()
        next_event = next((d for d in edates if d >= today), edates[-1]) # d must be later than today for future earnings call

    idct = currentImpliedMove(args.ticker, next_event) if next_event else None
    
    print(rdf.tail())
    print("\nSummary")
    avg_move = (rdf["oneDayMovePct"].mean())/100 if not rdf.empty else None
    if avg_move is not None and pd.notna(avg_move):
        print("Avg 1 Day Move:", f"{avg_move:.2%}")
    else:
        print("Avg 1 Day Move: n/a")

    
    if idct:
        print("Next expiry:", idct["expiry"])
        print("ATM IV:", f"{idct['atmIV']:.2%}")
        print("Implied move %:", f"{idct['impliedMovePct']:.2%}")
        histogramRealized(rdf, implied=idct["impliedMovePct"] if idct else None,
                       out=f"{args.ticker}_hist.png")
        timelineMoves(rdf, implied=idct["impliedMovePct"] if idct else None,
                   out=f"{args.ticker}_timeline.png")
        

if __name__ == "__main__":
    main()
    
