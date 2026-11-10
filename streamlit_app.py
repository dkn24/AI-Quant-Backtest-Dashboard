import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
from google import genai

# --- Page Configuration ---
st.set_page_config(page_title="AI Quant Backtest Dashboard", layout="wide")

st.title("📈 AI-Powered Moving Average Crossover Backtest")
st.markdown("Test a **50/200 Day Moving Average Crossover Strategy** against a Buy & Hold benchmark, with automated **Gemini AI quantitative analysis**.")

# --- Sidebar Controls ---
st.sidebar.header("Strategy Parameters")
ticker = st.sidebar.text_input("Stock Ticker", value="NVDA")
short_window = st.sidebar.number_input("Short-term MA Window", value=50, min_value=5, max_value=100)
long_window = st.sidebar.number_input("Long-term MA Window", value=200, min_value=50, max_value=365)
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2024-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2026-01-01"))

# --- Run Backtest Button ---
if st.sidebar.button("Run Backtest & AI Analysis"):
    with st.spinner(f"Running backtest and querying Gemini AI for {ticker}..."):
        
        # 1. Download Data
        data = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=False)
        
        if data.empty:
            st.error("No data found for this ticker/date range. Try a different symbol.")
        else:
            # Safely extract prices
            if 'Adj Close' in data.columns:
                prices = data['Adj Close']
            elif isinstance(data.columns, pd.MultiIndex):
                prices = data['Adj Close'][ticker]
            else:
                prices = data['Close']
            
            prices = prices.dropna()

            # 2. Calculate Moving Averages
            df = pd.DataFrame(index=prices.index)
            df['Price'] = prices
            df['SMA_Short'] = df['Price'].rolling(window=short_window).mean()
            df['SMA_Long'] = df['Price'].rolling(window=long_window).mean()
            df = df.dropna()

            # 3. Strategy Logic & Returns
            df['Signal'] = np.where(df['SMA_Short'] > df['SMA_Long'], 1, 0)
            df['Market_Returns'] = df['Price'].pct_change()
            df['Strategy_Returns'] = df['Signal'].shift(1) * df['Market_Returns']
            df = df.dropna()

            df['Buy_Hold_Equity'] = (1 + df['Market_Returns']).cumprod()
            df['Strategy_Equity'] = (1 + df['Strategy_Returns']).cumprod()

            # 4. Calculate Performance Metrics
            trading_days = 252
            bh_ret = df['Buy_Hold_Equity'].iloc[-1] - 1
            strat_ret = df['Strategy_Equity'].iloc[-1] - 1
            
            bh_vol = df['Market_Returns'].std() * np.sqrt(trading_days)
            strat_vol = df['Strategy_Returns'].std() * np.sqrt(trading_days)
            
            rf = 0.03
            bh_sharpe = ((df['Market_Returns'].mean() * trading_days) - rf) / bh_vol
            strat_sharpe = ((df['Strategy_Returns'].mean() * trading_days) - rf) / strat_vol

            # Display Metrics in Columns
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Buy & Hold Return", f"{bh_ret*100:.2f}%")
            col2.metric("Strategy Return", f"{strat_ret*100:.2f}%")
            col3.metric("Buy & Hold Sharpe", f"{bh_sharpe:.2f}")
            col4.metric("Strategy Sharpe", f"{strat_sharpe:.2f}")

            # 5. Plot Interactive Chart with Plotly
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df.index, y=df['Buy_Hold_Equity'], 
                mode='lines', name='Buy & Hold (Benchmark)',
                line=dict(color='gray', width=1.5)
            ))
            fig.add_trace(go.Scatter(
                x=df.index, y=df['Strategy_Equity'], 
                mode='lines', name=f'MA Crossover ({short_window}/{long_window})',
                line=dict(color='blue', width=2),
                hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br><b>Strategy Value</b>: $%{y:.2f}<extra></extra>'
            ))
            
            fig.update_layout(
                title=f'Backtest Performance: {ticker}',
                xaxis_title='Date',
                yaxis_title='Growth of $1',
                hovermode='x unified',
                template='plotly_white',
                height=500
            )

            st.plotly_chart(fig, use_container_width=True)

            # 6. Call Google Gemini AI for Automated Analysis Report
            try:
                client = genai.Client()
                prompt = f"""
                You are an expert quantitative financial analyst. 
                I just ran a {short_window}/{long_window} Moving Average Crossover backtest on {ticker}.
                Here are the final performance results:
                - Buy & Hold Final Value: ${df['Buy_Hold_Equity'].iloc[-1]:.2f} (Sharpe: {bh_sharpe:.2f})
                - MA Strategy Final Value: ${df['Strategy_Equity'].iloc[-1]:.2f} (Sharpe: {strat_sharpe:.2f})

                Provide a short, 3-bullet point executive summary evaluating whether the trend-following strategy outperformed or lagged behind Buy & Hold in this timeframe, and explain the key risk/reward trade-off observed.
                """
                
                response = client.models.generate_content(
                    model='gemini-3.1-flash-lite',
                    contents=prompt,
                )
                
                st.subheader("Gemini AI Quantitative Analysis")
                st.write(response.text)
                
            except Exception as e:
                st.warning(f"Could not generate AI report. Check if GEMINI_API_KEY is set in your environment variables. Error: {e}")
else:
    st.info("👈 Adjust your parameters in the sidebar and click **Run Backtest & AI Analysis** to launch the web app!")