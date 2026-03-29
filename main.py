# work.py  –– Full Streamlit dashboard
import streamlit as st
import datetime
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from indicator.technical_indicator import add_technical_indicators
from strategy.rsi_strategy         import rsi_strategy
from strategy.macd_strategy        import macd_strategy
from strategy.bollinger_strategy   import bollinger_strategy
from strategy.backtest             import backtest_strategy
from lstm_model                    import forecast_next_7_days   # your LSTM helper

# ░░░ 1. Page‑wide settings ░░░
st.set_page_config(page_title="📊 Stock Strategy Dashboard", layout="wide", page_icon="💹")
st.title("💹 Advanced Stock Market Dashboard")

# ░░░ 2. Sidebar controls ░░░
st.sidebar.header("⚙️ Settings")
# user_input    = st.sidebar.text_input("Enter ticker (e.g., META, INFY)", value="META")
ticker_company_name = st.sidebar.text_input("Enter the company name")
if ticker_company_name:
    tick = yf.Lookup(query = ticker_company_name).all.index[0:3]
    user_input = st.sidebar.selectbox("Enter Stock Ticker", options=tick)
start_date    = st.sidebar.date_input("Start Date", pd.to_datetime("2025-01-01"))
end_date      = st.sidebar.date_input("End Date",   pd.to_datetime("today"))
strategy_name = st.sidebar.selectbox("📈 Select Strategy", ["RSI", "MACD", "Bollinger"])
model_option  = st.sidebar.selectbox("🤖 Select Forecast Model", ["None", "LSTM"])
amount = st.sidebar.number_input("💲Amount to invest")
run_button    = st.sidebar.button("🚀 Run")

# ░░░ 3. Run workflow ░░░
if run_button and user_input:
    try:
        stock = yf.Ticker(user_input)
        df    = stock.history(start=start_date, end=end_date)
        info  = stock.info
        currency = info["currency"]

        if df.empty:
            st.error("No data for this ticker / date-range."); st.stop()

        # ── Indicators & chosen strategy ─────────────────────────────────────
        df_ind = add_technical_indicators(df.copy())
        if strategy_name == "RSI":
            df_strat = rsi_strategy(df_ind.copy())
        elif strategy_name == "MACD":
            df_strat = macd_strategy(df_ind.copy())
        else:
            df_strat = bollinger_strategy(df_ind.copy())

        total_profit, trades_raw = backtest_strategy(df_strat, amount)

        # Turn tuple list → DataFrame  (handles BUY & SELL rows)
        trades = []
        for t in trades_raw:
            if t[0] == "BUY":
                trades.append({"Type": "Buy",  "Date": t[1], "Price": t[2], "Profit": 0.0})
            else:  # SELL tuple = ('SELL', date, price, profit)
                trades.append({"Type": "Sell", "Date": t[1], "Price": t[2], "Profit": t[3]})
        trades = pd.DataFrame(trades)
        if not trades.empty:
            trades["Cumulative Profit"] = trades["Profit"].cumsum()

        # ── Build tabs ───────────────────────────────────────────────────────
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["📊 Summary", "📈 Chart", "📉 Indicators",
             "🔮 Forecast", "📋 Strategy"])

# ═════════════ TAB 1 • SUMMARY ═════════════ #
                # ═════════════ TAB 1 • SUMMARY ═════════════ #
        with tab1:
            # ─── Top metrics ──────────────────────
            colA, colB, colC = st.columns(3)
            colA.metric("📈 Current Price", f"{currency} {df['Close'].iloc[-1]:,.2f}")
            colB.metric("💹 Trades Executed", len(trades))
            colC.metric("💰 Total Profit", f"{currency} {total_profit:,.2f}")

            st.divider()

            # ─── Description (Full width top) ─────
            import re
            st.markdown("### 📝 Company Description")
            raw_desc = info.get("longBusinessSummary", "No description available.")

            # Split into sentences
            sentences = re.split(r'(?<=[.!?]) +', raw_desc)

            # Build description of ~600–700 characters (approx. 5-6 lines)
            short_desc = ""
            for sentence in sentences:
                if len(short_desc) + len(sentence) <= 900:
                    short_desc += sentence + " "
                else:
                    break

            # Final formatting
            short_desc = short_desc.strip()
            if len(short_desc) < len(raw_desc):
                short_desc += "..."

            st.write(short_desc)

            st.divider()

            # ─── Row: Profile (left) + OHLCV (right) ─
            left, right = st.columns([1.1, 1.3])

            with left:
                st.subheader("🏢 Company Profile")
                profile = {
                    "Company Name" : info.get("longName", "—"),
                    "Industry"     : info.get("industry", "—"),
                    "Market Cap"   : f"{currency} {info['marketCap']:,}" if info.get("marketCap") else "—",
                    "PE Ratio"     : f"{info['trailingPE']:.2f}" if info.get("trailingPE") else "—",
                    "52-Week High" : f"{currency} {info['fiftyTwoWeekHigh']}" if info.get("fiftyTwoWeekHigh") else "—",
                    "52-Week Low"  : f"{currency} {info['fiftyTwoWeekLow']}" if info.get("fiftyTwoWeekLow") else "—",
                    "Headquarters" : f"{info.get('city','')} {info.get('country','')}".strip() or "—",
                    "Website"      : info.get("website", "—")
                }
                st.table(pd.DataFrame(profile.items(), columns=["Field", "Value"]))

            with right:
                st.subheader("🗓️ Last 5 Trading Days")
                st.dataframe(
                    df.tail(5)[["Open", "High", "Low", "Close", "Volume"]]
                    .style.format(precision=2)
                )

        # TAB‑2  ─ Price history
        with tab2:
            fig, ax = plt.subplots(figsize=(11,4))
            ax.plot(df.index, df["Close"], color="tab:blue", label="Close")
            ax.set_title("Price History"); ax.set_xlabel("Date"); ax.set_ylabel("Price")
            ax.grid(ls="--", alpha=.3); ax.legend()
            st.pyplot(fig)

        # TAB‑3  ─ Indicators table
        with tab3:
            st.subheader("📉 Technical Indicators (tail 10 rows)")
            st.dataframe(df_ind.tail(10))

        # TAB‑4  ─ LSTM forecast (+ zoomed plot)
        if model_option == "LSTM":
            with tab4:
                st.header("🔮 LSTM 7 - Day Forecast")
                with st.spinner("Training LSTM - please wait…"):
                    df_lstm, future_dates, preds = forecast_next_7_days(user_input)

                # Full view
                figF, axF = plt.subplots(figsize=(11, 4))
                axF.plot(df_lstm.index, df_lstm["Close"], label="Historical", color="skyblue")
                axF.plot(future_dates, preds, "--", color="orange", label="Forecast (7 days)")
                axF.grid(ls=":"); axF.legend()
                st.pyplot(figF)

                # Zoom view
                figZ, axZ = plt.subplots(figsize=(10, 3.5))
                axZ.plot(future_dates, preds, marker="o", color="orange")
                for d, p in zip(future_dates, preds.ravel()):
                    axZ.text(d, p, f"{p:.2f}", ha="center", va="bottom", fontsize=8)
                axZ.set_xticks(future_dates)
                axZ.set_xticklabels([d.strftime("%b %d") for d in future_dates],
                                    rotation=45)
                axZ.set_title("Zoomed 7-Day Forecast"); axZ.grid(ls="--", alpha=.5)
                st.pyplot(figZ)

                st.dataframe(pd.DataFrame({"Date": future_dates,
                                           "Predicted": preds.ravel()})
                             .style.format({"Predicted": "{:.2f}"}))
        else:
            with tab4:
                st.info("Select **LSTM** in the sidebar to see a 7-day forecast.")

        # TAB‑5  ─ Strategy, profit curve & download
        with tab5:
            st.header(f"📋 Backtest - {strategy_name}")

            colP, colT = st.columns([1,1])
            colP.metric(f"Total Profit ({currency})", f"{total_profit:,.2f}")
            colT.metric("Trades", len(trades))

            # Buy/Sell chart
            figS, axS = plt.subplots(figsize=(11,4))
            axS.plot(df_strat["Close"], color="gray", alpha=.6)
            axS.plot(df_strat[df_strat["Signal"]==1].index,
                     df_strat[df_strat["Signal"]==1]["Close"],
                     "^", color="green", ms=8, label="Buy")
            axS.plot(df_strat[df_strat["Signal"]==-1].index,
                     df_strat[df_strat["Signal"]==-1]["Close"],
                     "v", color="red",  ms=8, label="Sell")
            axS.set_title(f"{strategy_name} Buy/Sell Signals"); axS.grid(ls=":")
            axS.legend(); st.pyplot(figS)

            # Cumulative‑profit curve
            if not trades.empty:
                figC, axC = plt.subplots(figsize=(10,3))
                axC.plot(trades["Date"], trades["Cumulative Profit"],
                         color="purple", lw=2)
                axC.set_title("💰 Cumulative Profit Curve")
                axC.set_xlabel("Date"); axC.set_ylabel(f"Profit {currency}"); axC.grid(ls="--")
                st.pyplot(figC)

                # Download CSV
                csv = trades.to_csv(index=False).encode("utf-8")
                st.download_button("📥 Download Trade Log",
                                   csv,
                                   file_name=f"{user_input}_{strategy_name}_trades.csv",
                                   mime="text/csv")
            else:
                st.info("No trades produced for this period - nothing to download.")

    except Exception as e:
        st.error(f"⚠️ {e}")

else:
    st.info("Enter a ticker and click **Run** to begin analysis.")