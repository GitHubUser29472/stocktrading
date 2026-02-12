import os
from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest

# =====================
# CONFIG
# =====================
STOCK = "TSLA"
PRICE_ALERT = 550  # example alert price

#Alerts you when TESLA stock in over $500
#tells you not to buy

# Load API keys from environment variables
# Load API keys from environment variables (make sure they match your Alpaca keys)
from dotenv import load_dotenv

load_dotenv()  # loads keys from a .env file in your project folder

API_KEY = os.getenv("ALPACA_API_KEY")
API_SECRET = os.getenv("ALPACA_API_SECRET")  # ✅ NOTE: change to API_SECRET

if not API_KEY or not API_SECRET:
    raise ValueError("API keys not found. Set ALPACA_API_KEY and ALPACA_API_SECRET in your environment or .env file.")

# =====================
# CLIENTS (PAPER TRADING)
# =====================
trading_client = TradingClient(
    API_KEY,
    API_KEY_SECRET,
    paper=True          # ✅ REQUIRED FOR PAPER TRADING
)

data_client = StockHistoricalDataClient(
    API_KEY,
    API_KEY_SECRET
)

# =====================
# FETCH LATEST PRICE
# =====================
print("===== Running TSLA & Portfolio Check =====")

try:
    request = StockLatestQuoteRequest(symbol_or_symbols=STOCK)
    quote = data_client.get_stock_latest_quote(request)

    price = quote[STOCK].ask_price
    print(f"TSLA price: ${price}")

    if price >= PRICE_ALERT:
        print("🚨 PRICE ALERT TRIGGERED")

except Exception as e:
    print("ERROR fetching TSLA price:", e)

# =====================
# FETCH PORTFOLIO
# =====================
try:
    account = trading_client.get_account()
    print(f"Equity: ${account.equity}")
    print(f"Buying Power: ${account.buying_power}")

except Exception as e:
    print("ERROR fetching portfolio:", e)

print("===== Check Complete =====")
