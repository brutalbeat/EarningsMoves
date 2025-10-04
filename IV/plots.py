# file for plotting data
import matplotlib.pyplot as plt
import pandas as pd

def histogramRealized(df, implied, out="hist.png"):
    plt.figure()
    df["oneDayMovePct"].plot(kind="hist",bins=15)
    if implied is not None:
        plt.axvline(implied, ls="--", c="red")
    plt.title("Post Earnings 1-Day Moves")
    plt.xlabel("Absolute Move %")
    plt.savefig(out)
    plt.close()
    
    
def timelineMoves(df, implied, out="timeline.png"):
    plt.figure()
    s = df.set_index("event_date")["oneDayMovePct"]
    s.plot(marker="o")
    if implied is not None:
        plt.axhline(implied, ls="--", c="red")
    plt.title("Post Earnings Moves Over Time")
    plt.ylabel("Absolute Move %")
    plt.savefig(out)
    plt.close()
