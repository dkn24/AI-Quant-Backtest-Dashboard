# 📈 AI-Powered Quantitative Backtest Dashboard

An interactive quantitative finance web application built with Python, Streamlit, Plotly, and Google Gemini. This platform backtests trend-following strategies (such as Moving Average Crossovers) against a standard Buy & Hold benchmark using real-time market data from Yahoo Finance, complete with automated AI-driven performance summaries.

---

## 🌟 Key Features

* **Interactive Strategy Backtesting:** Custom short/long moving average windows (e.g., 50/200-day crossover) for any stock ticker.
* **Look-Ahead Bias Protection:** Domain-accurate trading execution logic using `shift(1)` on historical price series.
* **Interactive Hover Visualizations:** Built with Plotly to allow granular inspection of normalized equity curves ($1.00 base) over time.
* **Risk & Performance Metrics:** Automated calculation of Total Return, Volatility, and Risk-Adjusted Returns (Sharpe Ratio).
* **Gemini LLM Integration:** Uses the `google-genai` SDK (`gemini-2.5-flash`) to generate executive-level quantitative insights and risk/reward evaluations directly within the dashboard.

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Frontend / Dashboard:** Streamlit
* **Data Retrieval & Manipulation:** `yfinance`, `pandas`, `numpy`
* **Data Visualization:** Plotly Graph Objects
* **Artificial Intelligence:** Google Gemini API (`google-genai` SDK)

---

## 🚀 Quickstart Guide

### 1. Clone the Repository
```bash
git clone https://github.com/dkn24/AI-Quant-Backtest-Dashboard
cd AI-Quant-Backtest-Dashboard
```

### 2. Set Up a Virtual Environment & Install Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Set Up Your API Key
Obtain a free Gemini API key from [Google AI Studio](https://aistudio.google.com/). Set it as an environment variable in your terminal session:

* **Windows PowerShell:**
  ```powershell
  $env:GEMINI_API_KEY="your_api_key_here"
  ```
* **Mac / Linux / Bash:**
  ```bash
  export GEMINI_API_KEY="your_api_key_here"
  ```

### 4. Launch the Streamlit Web App
```bash
streamlit run streamlit_app.py
```

---

## 📂 Project Structure

```text
├── streamlit_app.py      # Main Streamlit application and quantitative logic
├── requirements.txt      # Required Python packages
└── README.md             # Project documentation
```

---

## 🤖 How the Quant Logic Works

1. **Signal Generation:** When the short-term moving average (SMA) crosses above the long-term SMA, a signal of `1` (Long) is generated. When it drops below, a signal of `0` (Cash) is assigned.
2. **Returns Calculation:** Daily market returns are shifted by 1 trading day (`df['Signal'].shift(1)`) to ensure buy/sell execution occurs at the next period's close, preventing look-ahead bias.
3. **Compounded Growth:** Cumulative equity curves are constructed starting at $1.00 to compare capital growth directly against a Buy & Hold benchmark.
