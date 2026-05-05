"""
End-to-end test: replicates every cell in Crypto_Analysis.ipynb
and saves the plots to disk for visual verification.
"""
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for headless execution

import matplotlib.pyplot as plt
from crypto_data import get_crypto_data

print("=" * 60)
print("  Cryptocurrency Data Analysis - End-to-End Test")
print("=" * 60)

# --- Cell 1: Fetch full OHLCV data ---
print("\n[1/5] Fetching 1000 days of daily BTC-USDT data...")
df_full = get_crypto_data('BTCUSDT', interval='1d', limit=1000)
print(f"      [OK] Received {len(df_full)} rows, columns: {list(df_full.columns)}")

# --- Cell 2: Extract close series ---
df = df_full['close']

# --- Cell 3: df.head() ---
print("\n[2/5] df.head():")
print(df.head())

# --- Cell 4: Historical price plot ---
print("\n[3/5] Plotting historical price -> output/price_history.png")
fig, ax = plt.subplots(figsize=(12, 6))
df.plot(ax=ax, title="BTC/USDT Historical Daily Close Price", color='orange')
ax.set_ylabel("Price (USDT)")
ax.grid(True, alpha=0.3)
fig.savefig("output/price_history.png", dpi=150, bbox_inches='tight')
plt.close(fig)
print("      [OK] Saved.")

# --- Cell 5: Descriptive stats of returns ---
returns = df.pct_change().dropna()
print("\n[4/5] df.pct_change().describe():")
print(returns.describe())

# --- Cell 6: Returns histogram ---
print("\n[5/5] Plotting returns histogram -> output/returns_histogram.png")
fig, ax = plt.subplots(figsize=(10, 6))
returns.hist(bins=100, ax=ax, color='skyblue', edgecolor='black', alpha=0.7)
ax.set_title("BTC/USDT Daily Close Returns Distribution")
ax.set_xlabel("Daily Return")
ax.set_ylabel("Frequency")
ax.grid(True, alpha=0.3)
fig.savefig("output/returns_histogram.png", dpi=150, bbox_inches='tight')
plt.close(fig)
print("      [OK] Saved.")

print("\n" + "=" * 60)
print("  ALL TESTS PASSED")
print("=" * 60)
