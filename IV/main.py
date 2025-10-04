# main file

import argparse
from earnings import getEarningsDates, realizedMoves
from implied import currentImpliedMove
from plots import histogramRealized, timelineMoves

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--events", type, default=12)
    args = ap.parse_args()
    
    edates = getEarningsDates(args.ticker, args.events)
    rdf = realizedMoves(args.ticker, edates)
    idct = currentImpliedMove(args.ticker, edates[-1]) if edates else None
    
    print(rdf.tail())
    print("\n Summary")
    print("Avg 1 Day Move: ", rdf["oneDayMovePct"].mean())
    
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
    