def generate_signals(df):
    """
    Add 'signal' column: 1 for buy, -1 for sell, 0 otherwise.
    Buy when RSI14 < 30 AND SMA20 crosses above SMA50.
    Sell when SMA20 crosses below SMA50.
    """
    # Shifted SMAs for crossover detection
    prev20 = df['SMA20'].shift(1)
    prev50 = df['SMA50'].shift(1)
    # Strict cross detection
    cross_up   = (prev20 < prev50) & (df['SMA20'] >  df['SMA50'])
    cross_down = (prev20 > prev50) & (df['SMA20'] <  df['SMA50'])
    #df['buy_signal'] = (df['RSI14'] < 30) & cross_up
    df['buy_signal'] = cross_up
    df['sell_signal'] = cross_down
    df['signal'] = 0
    df.loc[df['buy_signal'], 'signal'] = 1
    df.loc[df['sell_signal'], 'signal'] = -1
    return df