def backtest_strategy(df, initial_investment=1000):
    position = 0  # 0 = No position, 1 = Holding
    buy_price = 0
    total_profit = 0
    trades = []

    for i in range(len(df)):
        signal = df['Signal'].iloc[i]
        price = df['Close'].iloc[i]

        # Buy
        if signal == 1 and position == 0:
            position = 1
            buy_price = price
            trades.append(('BUY', df.index[i], price))

        # Sell
        elif signal == -1 and position == 1:
            position = 0
            sell_price = price
            profit = ((sell_price - buy_price) / buy_price) * initial_investment
            total_profit += profit
            trades.append(('SELL', df.index[i], price, profit))

    return total_profit, trades
