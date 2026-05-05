"""
run_all.py — One-click execution for Crypto Data Analysis
==========================================================
Orchestrates the entire process:
1. Fetches data (Binance API or Mock)
2. Performs data inspection
3. Generates historical price plots
4. Calculates returns and volatility
5. Generates returns distribution plots

Outputs are saved in the output/ directory.
"""

import os
import sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from crypto_data import get_crypto_data

# --- Configuration ---
SYMBOL = 'BTCUSDT'
INTERVAL = '1d'
LIMIT = 1000
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

def run_pipeline():
    print("=" * 60)
    print("  🚀 Starting Crypto Data Analysis Pipeline")
    print("=" * 60)

    # 1. Fetch Data
    print(f"\n[1/5] Fetching data for {SYMBOL}...")
    try:
        df_full = get_crypto_data(SYMBOL, interval=INTERVAL, limit=LIMIT)
        print(f"      ✅ Received {len(df_full)} rows of data.")
    except Exception as e:
        print(f"      ❌ Error fetching data: {e}")
        return

    # 2. Inspection
    df = df_full['close']
    print("\n[2/5] Data Sample (Last 5 days):")
    print(df.tail())

    # 3. Price History Plot with Moving Averages
    print(f"\n[3/6] Generating price history (with SMA 50/200) -> {OUTPUT_DIR}/price_history.png")
    fig, ax = plt.subplots(figsize=(12, 6))
    df.plot(ax=ax, label='Close Price', color='orange', alpha=0.6)
    
    # Calculate Moving Averages
    sma50 = df.rolling(window=50).mean()
    sma200 = df.rolling(window=200).mean()
    sma50.plot(ax=ax, label='SMA 50', color='blue', linestyle='--', alpha=0.8)
    sma200.plot(ax=ax, label='SMA 200', color='red', linestyle='-', linewidth=2)
    
    ax.set_title(f"{SYMBOL} Historical Price & Moving Averages")
    ax.set_ylabel("Price (USDT)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.savefig(OUTPUT_DIR / "price_history.png", dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("      ✅ Price history plot saved.")

    # 4. Returns & Volatility Analysis
    print("\n[4/6] Calculating returns and rolling volatility...")
    returns = df.pct_change().dropna()
    cumulative_returns = (1 + returns).cumprod() - 1
    rolling_vol = returns.rolling(window=30).std() * (252**0.5) # Annualized 30-day rolling vol
    
    print("      Statistics for Daily Returns:")
    print(returns.describe())

    # 5. Cumulative Returns Plot
    print(f"\n[5/6] Generating cumulative returns plot -> {OUTPUT_DIR}/cumulative_returns.png")
    fig, ax = plt.subplots(figsize=(12, 6))
    cumulative_returns.plot(ax=ax, color='green', linewidth=2)
    ax.set_title(f"{SYMBOL} Cumulative Investment Returns")
    ax.set_ylabel("Cumulative Return (%)")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x*100:.0f}%'))
    ax.grid(True, alpha=0.3)
    fig.savefig(OUTPUT_DIR / "cumulative_returns.png", dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("      ✅ Cumulative returns plot saved.")

    # 6. Rolling Volatility Plot
    print(f"\n[6/6] Generating rolling volatility plot -> {OUTPUT_DIR}/rolling_volatility.png")
    fig, ax = plt.subplots(figsize=(12, 6))
    rolling_vol.plot(ax=ax, color='purple', linewidth=1.5)
    ax.set_title(f"{SYMBOL} 30-Day Rolling Annualized Volatility")
    ax.set_ylabel("Volatility")
    ax.grid(True, alpha=0.3)
    fig.savefig(OUTPUT_DIR / "rolling_volatility.png", dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("      ✅ Rolling volatility plot saved.")

    print("\n" + "=" * 60)
    print("  ✨ PIPELINE COMPLETED SUCCESSFULLY")
    print(f"     Results available in: {OUTPUT_DIR}/")
    print("=" * 60)

if __name__ == "__main__":
    # Ensure dependencies are available
    try:
        import pandas
        import matplotlib
        import numpy
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("   Please run: pip install -r requirements.txt")
        sys.exit(1)

    run_pipeline()
