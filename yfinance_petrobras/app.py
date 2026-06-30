import os
import ssl
import warnings

# Suprimir warnings de SSL
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"

# Fix SSL para curl_cffi (usado pelo yfinance >= 0.2.x)
try:
    import curl_cffi.requests as curl_req
    _orig_session_init = curl_req.Session.__init__

    def _patched_init(self, *args, **kwargs):
        kwargs["verify"] = False
        _orig_session_init(self, *args, **kwargs)

    curl_req.Session.__init__ = _patched_init
except Exception as e:
    print(f"[WARN] curl_cffi patch falhou: {e}")

import yfinance as yf
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Petrobras Stock API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/price/{ticker}")
async def get_price(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")

        if hist.empty:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado para o ticker informado.")

        latest = hist.iloc[-1]

        try:
            info = stock.fast_info
            previous_close = float(info.previous_close) if info.previous_close else float(latest["Open"])
            currency = info.currency or "BRL"
        except Exception:
            previous_close = float(latest["Open"])
            currency = "BRL"

        current_price = float(latest["Close"])
        change = current_price - previous_close
        change_percent = (change / previous_close) * 100 if previous_close else 0

        return {
            "ticker": ticker.upper(),
            "price": current_price,
            "open": float(latest["Open"]),
            "high": float(latest["High"]),
            "low": float(latest["Low"]),
            "volume": int(latest["Volume"]),
            "change": change,
            "change_percent": change_percent,
            "currency": currency,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
