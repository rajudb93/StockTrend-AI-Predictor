def macd_strategy(df):
    df = df.copy()
    df['Signal'] = 0
    df.loc[df['MACD'] > df['Signal_Line'], 'Signal'] = 1   # Buy
    df.loc[df['MACD'] < df['Signal_Line'], 'Signal'] = -1  # Sell
    return df
