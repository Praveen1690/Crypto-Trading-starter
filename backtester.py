import pandas as pd
from backtesting import Backtest, Strategy


class TrendStrategy(Strategy):
    # 200-period EMA
    ema_period = 200

    def init(self):
        self.ema = self.I(
            lambda x: pd.Series(x).ewm(span=self.ema_period, adjust=False).mean(),
            self.data.Close
        )

    def next(self):
        close = self.data.Close[-1]
        ema = self.ema[-1]

        # Buy when price is above EMA
        if close > ema:
            if not self.position:
                self.buy()

        # Exit when price falls below EMA
        elif close < ema:
            if self.position:
                self.position.close()


def prepare_data(symbol):
    # Load CSV
    df = pd.read_csv(
        f"data/{symbol}.csv",
        index_col="time",
        parse_dates=True
    )

    # Ensure datetime index
    df.index = pd.to_datetime(df.index)

    # Resample to 4-hour candles
    df = df.resample("4h").agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum"
    }).dropna()

    # Rename columns for backtesting.py
    df.columns = [c.capitalize() for c in df.columns]

    # Optional date filter
    df = df.loc["2026-05-01":"2026-05-30"]

    return df


def run_backtest(symbol):
    data = prepare_data(symbol)

    bt = Backtest(
        data,
        TrendStrategy,
        cash=500,
        commission=0.001,
        exclusive_orders=True
    )

    stats = bt.run()

    print(f"\n{'=' * 50}")
    print(f"{symbol} RESULTS")
    print(f"{'=' * 50}")
    print(stats)

    report_file = f"{symbol.lower()}_report.html"
    bt.plot(filename=report_file)

    print(f"\nReport saved: {report_file}")

    return stats


if __name__ == "__main__":
    eth_stats = run_backtest("ETHUSDT")
    bnb_stats = run_backtest("BNBUSDT")

    print("\nBacktests completed successfully.")
