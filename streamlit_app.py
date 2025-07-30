import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Parameters
ticker      = "^GSPC"
start_date  = "1950-01-01"
end_date    = "2025-07-29"

# 1⃣  Get the data – force the legacy behaviour you expected
data = yf.download(
    ticker,
    start=start_date,
    end=end_date,
    interval="1mo",
    auto_adjust=False    # keep the separate 'Adj Close' column
)

# 2⃣  Pick the right price series
price_col = "Adj Close" if "Adj Close" in data.columns else "Close"

# 3⃣  Monthly returns
data["Monthly Return"] = data[price_col].pct_change()

# 4⃣  Focus on July
july_returns = data[data.index.month == 7]["Monthly Return"].dropna()

# 5⃣  Stats
percentage_positive = (july_returns > 0).mean() * 100
mean_return         = july_returns.mean()
consecutive_reds    = (
    (july_returns < 0).astype(int).rolling(2).sum()
    .eq(2).sum()
)

print(f"Percentage of Julys with positive returns: {percentage_positive:.2f}%")
print(f"Mean July return: {mean_return:.4f}")
print(f"Back‑to‑back red Julys: {consecutive_reds}")

# 6⃣  Plot
fig, ax = plt.subplots(figsize=(14, 6))
(july_returns * 100).plot(kind="bar", ax=ax)
ax.set_title("S&P 500 — July Returns (1950‑2025)")
ax.set_xlabel("Year")
ax.set_ylabel("Return (%)")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
