import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint
import os

def calculate_cointegration(csv_path='data/historical_prices.csv'):
    print("Loading price matrix for cointegration testing...")
    df = pd.read_csv(csv_path, index_col='Date', parse_dates=True)
    
    # Extract asset vectors
    asset1 = df['GLD']
    asset2 = df['GDX']
    
    # 1. Engle-Granger Cointegration Test
    score, p_value, _ = coint(asset1, asset2)
    print(f"Cointegration Test P-Value: {p_value:.4f}")
    
    if p_value < 0.05:
        print("Result: The asset pair is statistically cointegrated (p < 0.05). Mean-reversion is mathematically viable.")
    else:
        print("Result: The asset pair is NOT cointegrated. Spread may drift.")
        
    # 2. Ordinary Least Squares (OLS) Regression to find the dynamic hedge ratio
    asset1_const = sm.add_constant(asset1)
    model = sm.OLS(asset2, asset1_const).fit()
    hedge_ratio = model.params.iloc[1] # Using iloc to dynamically grab the coefficient
    
    # 3. Calculate the Spread
    spread = asset2 - (hedge_ratio * asset1)
    
    # 4. Normalize into a Z-Score for trading signals
    z_score = (spread - spread.mean()) / spread.std()
    
    # Save the expanded matrix
    df['Spread'] = spread
    df['Z_Score'] = z_score
    df.to_csv('data/cointegrated_spread.csv')
    
    print(f"Calculated Hedge Ratio: {hedge_ratio:.4f}")
    print("Spread and Z-Score matrix successfully saved to data/cointegrated_spread.csv")
    
    return z_score

if __name__ == "__main__":
    calculate_cointegration()