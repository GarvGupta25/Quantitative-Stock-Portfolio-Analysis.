import yfinance as yf
import pandas as pd
import time

nifty_50_tickers = [
    'BHARTIARTL.NS', 'LTIM.NS', 'HDFCLIFE.NS', 'NTPC.NS', 'MARUTI.NS',
    'NESTLEIND.NS', 'BAJFINANCE.NS', 'KOTAKBANK.NS', 'TATASTEEL.NS',
    'ONGC.NS', 'BAJAJ-AUTO.NS', 'LT.NS', 'ITC.NS', 'TCS.NS', 'BRITANNIA.NS',
    'SHRIRAMFIN.NS', 'ADANIENT.NS', 'CIPLA.NS', 'WIPRO.NS', 'INDUSINDBK.NS',
    'ULTRACEMCO.NS', 'TATACONSUM.NS', 'BAJAJFINSV.NS', 'RELIANCE.NS',
    'HEROMOTOCO.NS', 'COALINDIA.NS', 'TITAN.NS', 'HINDALCO.NS',
    'APOLLOHOSP.NS'
]

all_stocks_data = []

print("Starting data download...\n")

for ticker in nifty_50_tickers:
    print(f"Downloading data for {ticker}...")
    try:
        data = yf.download(ticker, period="5y")

        if data.empty:
            print(f"No data for {ticker}")
            continue

        
        data.columns = [str(col).lower().replace(' ', '_') for col in data.columns]
        data.reset_index(inplace=True)
        data.rename(columns={'Date': 'price_date'}, inplace=True)

        
        data['ticker'] = ticker

        all_stocks_data.append(data)

        time.sleep(1) 

    except Exception as e:
        print(f"Could not download data for {ticker}: {e}")


if all_stocks_data:
    final_dataframe = pd.concat(all_stocks_data, ignore_index=True)
    final_dataframe.to_csv('nifty50_stocks.csv', index=False)
    print("\nDownload complete! Clean data has been saved.")
    print(final_dataframe.tail())
else:
    print("No data was downloaded.")
