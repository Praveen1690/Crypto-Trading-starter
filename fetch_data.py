import os
import pandas as pd
from binance.client import Client

# ===== CONFIG =====
SYMBOLS  = ["ETHUSDT", "BNBUSDT"]
INTERVAL = Client.KLINE_INTERVAL_5MINUTE      # "5m" — matches your strategy
START    = "2026-02-25"   # a few days before TRAIN_START, so indicators warm up
END      = "2026-05-31"   # through end of May 30 (your TEST_END)
# ==================

client = Client()  # mainnet, public data — no keys needed
os.makedirs("data", exist_ok=True)

for sym in SYMBOLS:
    print(f"Downloading {sym} {INTERVAL}  {START} -> {END} ...")
    kl = client.get_historical_klines(sym, INTERVAL, START, END)
    df = pd.DataFrame(kl, columns=["open_time", "open", "high", "low", "close", "volume",
                                   "close_time", "qv", "trades", "tb", "tq", "ig"])
    df["time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    for c in ["open", "high", "low", "close", "volume"]:
        df[c] = df[c].astype(float)
    df = df[["time", "open", "high", "low", "close", "volume"]].set_index("time")
    path = f"data/{sym}.csv"
    df.to_csv(path)
    print(f"  saved {len(df)} rows -> {path}   ({df.index[0]} .. {df.index[-1]})")