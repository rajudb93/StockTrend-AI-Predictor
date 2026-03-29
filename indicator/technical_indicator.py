import pandas as pd

# def add_technical_indicators(df):
#     # SMA 20
#     df['SMA_20'] = df['Close'].rolling(window=20).mean()
#     # SMA 50 (strategy ke liye)
#     df['SMA_50'] = df['Close'].rolling(window=50).mean()

#     # EMA 20
#     df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()

#     # RSI 14
#     delta = df['Close'].diff()
#     gain = delta.where(delta > 0, 0)
#     loss = -delta.where(delta < 0, 0)
#     avg_gain = gain.rolling(window=14).mean()
#     avg_loss = loss.rolling(window=14).mean()
#     rs = avg_gain / avg_loss
#     df['RSI_14'] = 100 - (100 / (1 + rs))

#     # MACD & Signal Line
#     exp1 = df['Close'].ewm(span=12, adjust=False).mean()
#     exp2 = df['Close'].ewm(span=26, adjust=False).mean()
#     df['MACD'] = exp1 - exp2
#     df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

#     # Bollinger Bands
#     df['BB_Middle'] = df['Close'].rolling(window=20).mean()
#     df['BB_Std'] = df['Close'].rolling(window=20).std()
#     df['BB_Upper'] = df['BB_Middle'] + (2 * df['BB_Std'])
#     df['BB_Lower'] = df['BB_Middle'] - (2 * df['BB_Std'])

#     return df


# def add_technical_indicators(df):
#     df["SMA_14"] = df["Close"].rolling(window=14).mean()
#     df["EMA_14"] = df["Close"].ewm(span=14, adjust=False).mean()

#     # RSI
#     delta = df["Close"].diff()
#     gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
#     loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
#     rs = gain / loss
#     df["RSI"] = 100 - (100 / (1 + rs))

#     # MACD
#     ema_12 = df["Close"].ewm(span=12, adjust=False).mean()
#     ema_26 = df["Close"].ewm(span=26, adjust=False).mean()
#     df["MACD"] = ema_12 - ema_26
#     df["Signal_Line"] = df["MACD"].ewm(span=9, adjust=False).mean()

#     # Bollinger Bands
#     df["BB_Middle"] = df["Close"].rolling(window=20).mean()
#     df["BB_Std"] = df["Close"].rolling(window=20).std()
#     df["BB_Upper"] = df["BB_Middle"] + 2 * df["BB_Std"]
#     df["BB_Lower"] = df["BB_Middle"] - 2 * df["BB_Std"]

#     return df
def add_technical_indicators(df):
    # Simple Moving Average and EMA
    df["SMA_14"] = df["Close"].rolling(window=14).mean()
    
    '''
    EMA_t = alpha * P_t + (1 - alpha)*EMA_(t-1)
    EMA_t = EMA at time t
    P_t = Price at value time t 
    alpha = smoothing factor 
    EMA_(t-1) = EMA at previous step
    '''
    df["EMA_14"] = df["Close"].ewm(span=14, adjust=False).mean()

    # RSI
    delta = df["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df["RSI_14"] = 100 - (100 / (1 + rs))

    # MACD
    ema_12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema_26 = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema_12 - ema_26
    df["Signal_Line"] = df["MACD"].ewm(span=9, adjust=False).mean()

    # Bollinger Bands
    df["BB_Middle"] = df["Close"].rolling(window=20).mean()
    df["BB_Std"] = df["Close"].rolling(window=20).std()
    df["BB_Upper"] = df["BB_Middle"] + 2 * df["BB_Std"]
    df["BB_Lower"] = df["BB_Middle"] - 2 * df["BB_Std"]

    return df
