import yfinance as yf
import pandas as pd
import os

def fetch_pair_data(ticker1='GLD', ticker2='GDX', start_date='2023-01-01', end_date='2024-01-01'):
    print(f"Fetching daily close prices for {ticker1} and {ticker2}...")
    
    # Download pricing matrix using the updated yfinance column mapping
    data = yf.download([ticker1, ticker2], start=start_date, end=end_date)['Close']
    
    # Drop missing values to ensure exact matrix alignment for statistical tests
    data = data.dropna()
    
    # Ensure data directory exists and save the output
    os.makedirs('data', exist_ok=True)
    file_path = 'data/historical_prices.csv'
    data.to_csv(file_path)
    
    print(f"Successfully saved {len(data)} trading days to {file_path}")
    return data

if __name__ == "__main__":
    fetch_pair_data()