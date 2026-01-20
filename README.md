# 📈 Indian Mutual Fund Analyzer & Comparator

A Python-based financial tool that fetches **Real-Time Data** directly from the Association of Mutual Funds in India (AMFI). It allows users to search for funds, analyze their historical performance, and perform quantitative risk assessments.

## 🚀 Key Features
* **Live Data Fetching:** Uses the `mftool` library to scrape the latest NAV and fund details.
* **Smart Search:** Fuzzy search capability to find funds by name (e.g., "Quant Small" -> finds "Quant Small Cap Fund").
* **Quantitative Analysis:**
    * **Returns (CAGR):** Automatically calculates 1-Year, 3-Year, and 5-Year Compound Annual Growth Rates based on historical NAVs.
    * **Risk (Volatility):** Calculates the Annualized Standard Deviation of daily returns to quantify risk.
* **Head-to-Head Comparison:** Compares two funds side-by-side on metrics like NAV, Returns, and Risk profiles.
* **Data Export:** Capability to save analyzed data into CSV format for further analysis in Excel.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Data Processing:** Pandas, NumPy
* **Data Source:** `mftool` (AMFI API wrapper)
* **Visualization:** Matplotlib / Seaborn (Planned)


## 🧮 The Mathematics Behind The Model

Unlike basic scrapers that just read static numbers, this model **computes** its own metrics from raw historical data to ensure accuracy.

### 1. Risk (Annualized Volatility)
The model calculates the standard deviation of daily logarithmic returns to quantify how risky a fund is.

$$
\text{Risk} = \sigma_{\text{daily}} \times \sqrt{252}
$$

*(Where 252 represents the number of trading days in a year)*

### 2. Return (CAGR)
Compound Annual Growth Rate is calculated to smooth out volatility and show true annual growth.

$$
\text{CAGR} = \left( \frac{\text{Current NAV}}{\text{Initial NAV}} \right)^{\frac{1}{n}} - 1
$$

# version 1.0.0


## 🔮 Future Scope
* **Sharpe Ratio:** Adding risk-adjusted return metrics.
* **Portfolio Simulator:** Allowing users to "backtest" a lump-sum investment.
* **GUI:** Converting the CLI into a Streamlit Web Dashboard.

---
*Created by Rudra Chauhan - Computer Science Student & Quant Finance Enthusiast*
