def bollinger_strategy(df):
    df = df.copy()
    df['Signal'] = 0
    df.loc[df['Close'] < df['BB_Lower'], 'Signal'] = 1   # Buy
    df.loc[df['Close'] > df['BB_Upper'], 'Signal'] = -1  # Sell
    return df
