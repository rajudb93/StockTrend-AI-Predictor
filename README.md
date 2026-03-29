💹 StockTrend AI-Predictor
Hybrid Quant & Deep Learning Engine
A professional-grade algorithmic trading dashboard that bridges the gap between Traditional Technical Analysis and Modern Deep Learning. This engine uncovers market patterns using three core strategies (RSI, MACD, Bollinger Bands) and forecasts future movements using a Custom Attention-based LSTM Neural Network.

🚀 Key Features

Multi-Model Forecasting — Leverages LSTM (Deep Learning) with a custom Attention Layer to focus on the most important historical price "events."
Strategy Backtesting — A built-in "Time Machine" to test strategies against historical data with real-time profit/loss calculation.
Technical Indicator Suite — Custom-built engine for EMA, SMA, RSI, MACD, and Bollinger Bands.
Interactive Dashboard — A sleek Streamlit UI for real-time stock lookups, company profiles, and visual trade signals.
Recency-Weighted Training — AI training logic that prioritizes recent market data to adapt to current volatility.


📁 Project Structure
├── indicator/
│   └── technical_indicator.py  # Core math for RSI, MACD, BB, EMA
├── strategy/
│   ├── rsi_strategy.py         # Mean-reversion logic (30/70 levels)
│   ├── macd_strategy.py        # Momentum crossover logic
│   ├── bollinger_strategy.py   # Volatility boundary logic
│   └── backtest.py             # Profit/Loss accounting engine
├── lstm_model.py               # Attention-based Deep Learning model
├── app.py                      # Main Streamlit Dashboard entry point
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation

🛠️ Installation & Setup
1. Clone the Repository
bashgit clone https://github.com/YOUR_USERNAME/StockTrend-AI-Predictor.git
cd StockTrend-AI-Predictor
2. Create a Virtual Environment (Recommended)
bashpython -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
3. Install Dependencies
bashpip install -r requirements.txt

Note: Ensure your requirements.txt includes: streamlit, yfinance, pandas, numpy, matplotlib, scikit-learn, and tensorflow.


🚦 How to Run the Project
Launch the interactive dashboard with:
bashstreamlit run app.py

Enter a Company Name — The system will search for the correct ticker (e.g., "Apple" → "AAPL").
Select a Strategy — Choose between RSI, MACD, or Bollinger Bands.
Toggle AI Forecast — Select LSTM to trigger the deep learning 7-day price prediction.
Click "Run Strategy" — View buy/sell signals, profit curves, and AI forecasts.


🧠 The Science Behind the Patterns
1. Technical Indicators — The Sensors
IndicatorWhat It UncoversRSIPsychological Exhaustion — when the market is overbought or oversoldMACDMomentum Shifts — acts as a speedometer for trend acceleration or decelerationBollinger BandsVolatility Extremes — statistical boundaries to detect abnormal price movement
2. Attention-Based LSTM — The Crystal Ball
Unlike standard models, this LSTM uses an Attention Layer that mimics human intelligence — paying closer attention to specific historical days (sudden crashes, massive breakouts) rather than treating all past data equally.
3. The Backtester — The Truth
The backtester calculates profit using the formula:
Profit=SellPrice−BuyPriceBuyPrice×InvestmentProfit = \frac{SellPrice - BuyPrice}{BuyPrice} \times InvestmentProfit=BuyPriceSellPrice−BuyPrice​×Investment
This provides a realistic view of how a strategy would have performed in the real world.
