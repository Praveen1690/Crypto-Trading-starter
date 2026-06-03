import os
import time
import pandas as pd
from decimal import Decimal, ROUND_DOWN
from binance.client import Client
from dotenv import load_dotenv

# ================= CONFIGURATION =================
INTERVAL = "4h"
EMA_PERIOD = 200
SYMBOLS = ["ETHUSDT", "BNBUSDT"]
MIN_TRADE_USD = 15.0 
# =================================================

load_dotenv()
client = Client(os.getenv("DEMO_API_KEY"), os.getenv("DEMO_API_SECRET"), demo=True)

# Cache for precision settings to avoid API overload
_symbol_info = {}

def get_step_size(sym):
    """Fetches Binance step size to ensure order quantity is valid."""
    if sym not in _symbol_info:
        info = client.get_symbol_info(sym)
        for f in info['filters']:
            if f['filterType'] == 'LOT_SIZE':
                _symbol_info[sym] = float(f['stepSize'])
    return _symbol_info[sym]

def _round_down(qty, step):
    """Rounds quantity down to the nearest step size allowed by Binance."""
    return float((Decimal(str(qty)) // Decimal(str(step))) * Decimal(str(step)))

def get_trend_state():
    """Returns True if Price > EMA, False otherwise."""
    states = {}
    for sym in SYMBOLS:
        kl = client.get_klines(symbol=sym, interval=INTERVAL, limit=250)
        closes = pd.Series([float(k[4]) for k in kl])
        ema = closes.ewm(span=EMA_PERIOD).mean().iloc[-1]
        current_price = closes.iloc[-1]
        states[sym] = current_price > ema
    return states

def rebalance():
    # 1. Get Trend
    states = get_trend_state()
    
    # 2. Determine target allocation
    if states["ETHUSDT"] and states["BNBUSDT"]:
        targets = {"ETHUSDT": 0.5, "BNBUSDT": 0.5}
    elif states["ETHUSDT"]:
        targets = {"ETHUSDT": 1.0, "BNBUSDT": 0.0}
    elif states["BNBUSDT"]:
        targets = {"ETHUSDT": 0.0, "BNBUSDT": 1.0}
    else:
        targets = {"ETHUSDT": 0.0, "BNBUSDT": 0.0}

    print(f"Trend: ETH={states['ETHUSDT']} | BNB={states['BNBUSDT']} | Targets: {targets}")

    # 3. Execution
    # Get current total portfolio equity to calculate positions
    usdt_free = float(client.get_asset_balance(asset="USDT")["free"])
    
    # Calculate current values
    current_values = {}
    total_equity = usdt_free
    for sym in SYMBOLS:
        base = sym.replace("USDT", "")
        bal = float(client.get_asset_balance(asset=base)["free"])
        price = float(client.get_symbol_ticker(symbol=sym)["price"])
        current_values[sym] = bal * price
        total_equity += current_values[sym]

    print(f"Total Equity: ${total_equity:.2f}")

    # Process orders
    for sym in SYMBOLS:
        target_val = total_equity * targets[sym]
        curr_val = current_values[sym]
        diff = target_val - curr_val
        
        if abs(diff) > MIN_TRADE_USD:
            price = float(client.get_symbol_ticker(symbol=sym)["price"])
            qty = abs(diff) / price
            step = get_step_size(sym)
            qty = _round_down(qty, step)
            
            if diff > 0: # BUY
                client.order_market_buy(symbol=sym, quantity=qty)
                print(f"[BUY] {sym} | ${diff:.2f}")
            else: # SELL
                client.order_market_sell(symbol=sym, quantity=qty)
                print(f"[SELL] {sym} | ${abs(diff):.2f}")

if __name__ == "__main__":
    print("Trend-Following Strategy Live (4H)...")
    while True:
        try:
            rebalance()
        except Exception as e:
            print(f"Error: {e}")
        # Sleep for 1 hour between checks to avoid rate limits
        # Since we use 4H candles, 1 hour checks ensure we don't miss the close
        time.sleep(3600)
