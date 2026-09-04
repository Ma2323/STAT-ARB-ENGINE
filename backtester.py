import pandas as pd
import numpy as np
import os

def run_backtest(csv_path='data/cointegrated_spread.csv', entry_z=2.0, exit_z=0.0):
    print("Loading spread and Z-score matrix for backtesting...")
    df = pd.read_csv(csv_path, index_col='Date', parse_dates=True)
    
    # Array to track market exposure (1 for Long, -1 for Short, 0 for Flat)
    positions = np.zeros(len(df))
    current_pos = 0
    
    # 1. Generate Trading Signals based on Z-Score mean reversion
    for i in range(len(df)):
        z = df['Z_Score'].iloc[i]
        
        if current_pos == 0:
            # Enter Short if spread is statistically overpriced; Long if underpriced
            if z > entry_z:
                current_pos = -1
            elif z < -entry_z:
                current_pos = 1
        else:
            # Exit position when spread reverts to the historical mean
            if (current_pos == -1 and z <= exit_z) or (current_pos == 1 and z >= exit_z):
                current_pos = 0
                
        positions[i] = current_pos
        
    df['Position'] = positions
    
    # Shift positions by 1 day to simulate executing at the market open *after* the signal
    df['Position'] = df['Position'].shift(1).fillna(0)
    
    # 2. Calculate Strategy Returns
    # Spread return is the daily difference in the spread value
    df['Spread_Return'] = df['Spread'].diff()
    df['Strategy_Return'] = df['Position'] * df['Spread_Return']
    df['Cumulative_Return'] = df['Strategy_Return'].cumsum()
    
    # Save the backtested equity curve
    df.to_csv('data/backtest_results.csv')
    
    total_profit = df['Cumulative_Return'].iloc[-1]
    print(f"Backtest complete. Total Strategy Profit (in spread units): {total_profit:.4f}")
    
    return df

if __name__ == "__main__":
    run_backtest()