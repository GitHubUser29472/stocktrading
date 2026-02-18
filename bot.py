from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

# =====================================
# 🔑 PUT YOUR NEW PAPER KEYS HERE
# =====================================
API_KEY = PKHFRA3RMF5ESMWW3ETTMKJHKV
SECRET_KEY = PASTE_YOUR_NEW_PAPER_SECRET_HERE

# =====================================
# SETTINGS
# =====================================
STOP_LOSS_PERCENT = -15  # Sell if position drops 15% or more

# =====================================
# CONNECT TO ALPACA (PAPER TRADING)
# =====================================
trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)

def check_positions():
    print("Checking positions...\n")

    try:
        positions = trading_client.get_all_positions()
    except Exception as e:
        print("Connection error:", e)
        return

    if not positions:
        print("No open positions.")
        return

    for position in positions:
        symbol = position.symbol
        qty = position.qty
        percent_change = float(position.unrealized_plpc) * 100

        print(f"{symbol}: {percent_change:.2f}%")

        if percent_change <= STOP_LOSS_PERCENT:
            print(f"Stop loss triggered for {symbol}. Selling...")

            order = MarketOrderRequest(
                symbol=symbol,
                qty=qty,
                side=OrderSide.SELL,
                time_in_force=TimeInForce.DAY
            )

            try:
                trading_client.submit_order(order)
                print(f"{symbol} SOLD.\n")
            except Exception as e:
                print(f"Failed to sell {symbol}:", e)

if __name__ == "__main__":
    check_positions()
