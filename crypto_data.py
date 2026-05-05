import pandas as pd
import requests
import datetime
import os
import numpy as np

def get_crypto_data(symbol: str, interval: str = '1d', limit: int = 1000) -> pd.DataFrame:
    """
    Fetches historical OHLCV data from Binance Public API or generates mock data.
    
    Args:
        symbol (str): Trading pair symbol (e.g., 'BTCUSDT', 'ETHUSDT').
        interval (str): Timeframe for the bars (e.g., '1d' for daily, '1h' for hourly).
        limit (int): Number of bars to return (max 1000).
        
    Returns:
        pd.DataFrame: A pandas DataFrame containing the historical OHLCV data.
    """
    if os.environ.get("MOCK_DATA") == "true":
        return _generate_mock_data(symbol, interval, limit)

    url = "https://api.binance.com/api/v3/klines"
    
    params = {
        'symbol': symbol.upper(),
        'interval': interval,
        'limit': limit
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"⚠️  API Error: {e}. Falling back to MOCK_DATA.")
        return _generate_mock_data(symbol, interval, limit)
    
    # Binance kline format:
    # [Open time, Open, High, Low, Close, Volume, Close time, Quote asset volume, Number of trades, Taker buy base asset volume, Taker buy quote asset volume, Ignore]
    
    # We only care about the first 6 columns
    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume', 
        'close_time', 'quote_asset_volume', 'num_trades', 
        'taker_buy_base', 'taker_buy_quote', 'ignore'
    ])
    
    # Keep OHLCV + date
    df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    
    # Convert types
    numeric_cols = ['open', 'high', 'low', 'close', 'volume']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, axis=1)
    
    # Convert timestamp to datetime and set as index
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('date', inplace=True)
    df.drop('timestamp', axis=1, inplace=True)
    
    return df

def _generate_mock_data(symbol: str, interval: str, limit: int) -> pd.DataFrame:
    """Generates synthetic price data for testing/demo purposes."""
    print(f"🛠️  MOCK_DATA mode enabled for {symbol}")
    
    np.random.seed(42)
    end_date = datetime.datetime.now()
    dates = pd.date_range(end=end_date, periods=limit, freq='D')
    
    # Simple random walk for price starting at 50k
    prices = 50000 * (1 + np.random.normal(0.001, 0.02, limit).cumsum())
    
    df = pd.DataFrame({
        'open': prices * (1 + np.random.normal(0, 0.005, limit)),
        'high': prices * (1 + np.abs(np.random.normal(0, 0.01, limit))),
        'low': prices * (1 - np.abs(np.random.normal(0, 0.01, limit))),
        'close': prices,
        'volume': np.random.uniform(1000, 5000, limit)
    }, index=dates)
    
    df.index.name = 'date'
    return df

if __name__ == "__main__":
    # Test the function
    print("Fetching daily BTC-USDT data...")
    df = get_crypto_data('BTCUSDT', interval='1d', limit=5)
    print(df.head())
