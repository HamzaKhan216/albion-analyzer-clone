from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Albion Market Analyzer with Scanner Endpoint")

class MarketItemUpload(BaseModel):
    item_id: str
    city: str
    price: int
    amount: int

# In-memory storage for uploaded market data (can be replaced with SQLite/Postgres)
local_market_cache = []

@app.get("/")
def read_root():
    return {"message": "Albion Market Analyzer & Private Scanner API is running!"}

@app.post("/api/scanner/upload")
def upload_market_data(item: MarketItemUpload):
    local_market_cache.append(item.dict())
    return {"status": "success", "received": item, "total_cached": len(local_market_cache)}

@app.get("/api/scanner/listings")
def get_scanned_listings():
    return {"listings": local_market_cache}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
