from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator

def compute_indicators(df):
    df['RSI14'] = RSIIndicator(df['Close'], window=14).rsi()
    df['SMA20'] = SMAIndicator(df['Close'], window=20).sma_indicator()
    df['SMA50'] = SMAIndicator(df['Close'], window=50).sma_indicator()
    df = df.dropna(subset=['Open', 'High', 'Low', 'Close', 'RSI14', 'SMA20', 'SMA50'])
    return df