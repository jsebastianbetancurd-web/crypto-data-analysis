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

    # 3. Price History Plot
    print(f"\n[3/5] Generating price history plot -> {OUTPUT_DIR}/price_history.png")
    fig, ax = plt.subplots(figsize=(12, 6))
    df.plot(ax=ax, title=f"{SYMBOL} Historical Daily Close Price", color='orange')
    ax.set_ylabel("Price (USDT)")
    ax.grid(True, alpha=0.3)
    fig.savefig(OUTPUT_DIR / "price_history.png", dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("      ✅ Plot saved.")

    # 4. Returns Analysis
    print("\n[4/5] Calculating daily returns volatility...")
    returns = df.pct_change().dropna()
    print("      Statistics for Daily Returns:")
    print(returns.describe())

    # 5. Returns Histogram
    print(f"\n[5/5] Generating returns distribution plot -> {OUTPUT_DIR}/returns_histogram.png")
    fig, ax = plt.subplots(figsize=(10, 6))
    returns.hist(bins=100, ax=ax, color='skyblue', edgecolor='black', alpha=0.7)
    ax.set_title(f"{SYMBOL} Daily Close Returns Distribution")
    ax.set_xlabel("Daily Return")
    ax.set_ylabel("Frequency")
    ax.grid(True, alpha=0.3)
    fig.savefig(OUTPUT_DIR / "returns_histogram.png", dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("      ✅ Plot saved.")

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
