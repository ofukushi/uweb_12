
# stock_data_loader.py

import yfinance as yf
import logging
import pandas as pd
from datetime import datetime, timedelta

# Global cache (optional)
_stock_cache = {}

def download_stock_data(seccode, years=10):
    logger = logging.getLogger(__name__)
    
    if seccode in _stock_cache:
        logger.info(f"Using cached stock data for {seccode}.")
        return _stock_cache[seccode]

    end_date = datetime.now()
    start_date = end_date - timedelta(days=years * 365)

    logger.info(f"Downloading stock data for {seccode} from {start_date.date()} to {end_date.date()}")
    data = yf.download(
        f"{seccode}.T",
        start=start_date.strftime('%Y-%m-%d'),
        end=end_date.strftime('%Y-%m-%d'),
        auto_adjust=False,
        actions=True
    )

    if data.empty:
        raise ValueError(f"No data returned for stock {seccode}")

    # Optional: flatten MultiIndex columns
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] for col in data.columns]

    # Resample to weekly
    data = data.resample('W-FRI').agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Adj Close': 'last',
        'Volume': 'sum'
    }).dropna()

    _stock_cache[seccode] = data
    return data
