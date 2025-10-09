# EarningsMoves

Python CLI tool for sanity-checking an upcoming earnings move: pull the most recent earnings reactions, compare their realized 1-day moves to what the options market is implying today, and plot the results visually.

## Features
- Fetches the last _N_ earnings dates (default 12) and calculates gap and 1-day absolute move percentages.
- Computes the current ATM implied move based on the option expiry covering the next earnings release.
- Generates a histogram of realized moves and a timeline chart, with the live implied move marked as a reference.

## Requirements
- Python 3.10+
- `pip install -r requirements.txt` (also expects `yfinance`, `pandas`, `matplotlib`)

> `yfinance` pulls live market data; make sure you have network access when running the script.

## Usage
From the repo root:
```bash
python3 IV/main.py <ticker> [--events N]

