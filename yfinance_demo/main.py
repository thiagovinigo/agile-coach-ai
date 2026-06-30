from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/stock/{ticker}")
def get_stock_price(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        todays_data = stock.history(period='1d')
        if todays_data.empty:
            return {"error": "Ticker not found or no data available"}
        
        current_price = todays_data['Close'].iloc[0]
        
        info = stock.info
        short_name = info.get("shortName", ticker)
        currency = info.get("currency", "BRL")
        
        # Calculate daily change if not available in info
        open_price = todays_data['Open'].iloc[0]
        change = current_price - open_price
        change_percent = (change / open_price) * 100 if open_price else 0

        regular_market_change = info.get("regularMarketChange", change)
        regular_market_change_percent = info.get("regularMarketChangePercent", change_percent)
        
        # Sometime yfinance returns None for these fields if market is closed
        if regular_market_change is None:
            regular_market_change = change
        if regular_market_change_percent is None:
            regular_market_change_percent = change_percent

        return {
            "ticker": ticker,
            "price": round(current_price, 2),
            "currency": currency,
            "name": short_name,
            "change": round(regular_market_change, 2),
            "change_percent": round(regular_market_change_percent, 2)
        }
    except Exception as e:
        return {"error": str(e)}

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
