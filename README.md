# Crypto-Trading-Starter

A simple quantitative cryptocurrency portfolio strategy that dynamically allocates capital between **ETH** and **BNB** based on trend signals derived from technical indicators.

The objective of the strategy is to shift portfolio exposure toward assets exhibiting positive momentum while moving capital to cash during unfavorable market conditions.

> **Disclaimer**
>
> This project is intended solely for educational and research purposes. Nothing contained in this repository should be interpreted as financial advice, investment advice, or a recommendation to buy or sell any asset.

---

# Strategy Overview

The strategy operates on **4-hour candles** and uses a **200-period Exponential Moving Average (EMA200)** as a long-term trend filter.

For each asset:

* If Price > EMA200 → Asset is considered bullish.
* If Price < EMA200 → Asset is considered bearish.

Portfolio allocation is determined as follows:

| ETH Trend | BNB Trend | Portfolio Allocation |
| --------- | --------- | -------------------- |
| Bullish   | Bullish   | 50% ETH + 50% BNB    |
| Bullish   | Bearish   | 100% ETH             |
| Bearish   | Bullish   | 100% BNB             |
| Bearish   | Bearish   | 100% USDT            |

This approach allows the portfolio to remain invested during favorable market conditions while preserving capital during broad market weakness.

---

# Methodology

The trend indicator is computed using a 200-period Exponential Moving Average:

[
EMA_t = \alpha P_t + (1-\alpha)EMA_{t-1}
]

where

[
\alpha = \frac{2}{N+1}
]

and

[
N = 200
]

Trading signal:

[
Signal_t=
\begin{cases}
Bullish,& Price_t > EMA_t \
Bearish,& Price_t \le EMA_t
\end{cases}
]

---

# Repository Structure

```text
Crypto-Trading-Starter/
│
├── strategy.py
├── backtester.py
├── fetch_data.py
│
├── ETHUSDT.csv
├── BNBUSDT.csv
│
├── portfolio_performance_report.png
├── swing_strategy_analysis.png
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/Crypto-Trading-Starter.git
cd Crypto-Trading-Starter
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Data Collection

Historical market data can be downloaded using:

```bash
python fetch_data.py
```

The script retrieves historical Binance market data and stores it locally for backtesting.

---

# Running the Backtest

Execute:

```bash
python backtester.py
```

The backtester evaluates the strategy on historical data and generates performance statistics and visualizations.

---

# Performance Visualization

The repository includes portfolio performance comparisons against passive buy-and-hold benchmarks.

### Portfolio Performance

* Strategy Portfolio
* Buy & Hold ETH
* Buy & Hold BNB

### Risk Analysis

* Portfolio Equity Curve
* Drawdown Analysis
* Relative Benchmark Comparison

---

# Bias Analysis

A separate methodology document is included discussing:

* Look-Ahead Bias
* Survivorship Bias
* Data Snooping Bias

The strategy was intentionally designed to maintain a simple rule-based structure and avoid excessive parameter optimization.

---

# Future Improvements

Potential extensions include:

* Additional asset universe
* Risk-adjusted position sizing
* Volatility targeting
* Walk-forward validation
* Machine learning based signal generation
* Multi-factor portfolio construction

---

# Technologies Used

* Python
* Pandas
* NumPy
* Backtesting.py
* Binance API
* Matplotlib

---

# License

This project is distributed under the MIT License.

---

# Authors

Praveen T
Shashank P

Indian Institute of Technology Delhi (IIT Delhi)

Quantitative Finance • Algorithmic Trading • Machine Learning
