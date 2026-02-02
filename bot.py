import os
from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest

# =====================
# CONFIG
# =====================
STOCK = "TSLA"
PRICE_ALERT = 550
EQUITY_FILE = "last_equity.txt"

# Fetch API keys from environment variables
API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

if not API_KEY or not SECRET_KEY:
    raise Exception("ALPACA_API_KEY and ALPACA_SECRET_KEY must be set as environment variables!")

# =====================
# ALPACA CLIENTS (PAPER)
# =====================
trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)
data_client = StockHistoricalDataClient(API_KEY, SECRET_KEY)

# =====================
# ALERT FUNCTION
# =====================
def send_alert(message):
    print("ALERT:", message)

# =====================
# TSLA PRICE CHECK
# =====================
def check_tsla_price():
    try:
        request = StockLatestQuoteRequest(symbol_or_symbols=STOCK)
        quote = data_client.get_stock_latest_quote(request)[STOCK]
        price = quote.ask_price
        print(f"DEBUG: Current {STOCK} price: ${price}")  # always print

        if price > PRICE_ALERT:
            send_alert(f"{STOCK} price above ${PRICE_ALERT}: ${price}")

    except Exception as e:
        print("ERROR fetching TSLA price:", e)

# =====================
# PORTFOLIO CHECK
# =====================
def check_portfolio_change():
    try:
        account = trading_client.get_account()
        current_equity = float(account.equity)
        print(f"DEBUG: Current portfolio equity: ${current_equity}")  # always print

        last_equity = None
        if os.path.exists(EQUITY_FILE):
            with open(EQUITY_FILE, "r") as f:
                last_equity = float(f.read())

        if last_equity is not None:
            if current_equity > last_equity:
                send_alert(f"Portfolio increased: {last_equity} → {current_equity}")
            elif current_equity < last_equity:
                send_alert(f"Portfolio decreased: {last_equity} → {current_equity}")

        # Save current equity for next run
        with open(EQUITY_FILE, "w") as f:
            f.write(str(current_equity))

    except Exception as e:
        print("ERROR fetching portfolio:", e)

# =====================
# MAIN
# =====================
def main():
    print("===== Running TSLA & Portfolio Check =====")
    check_tsla_price()
    check_portfolio_change()
    print("===== Check Complete =====\n")

if __name__ == "__main__":
    main()
