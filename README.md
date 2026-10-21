# Albion Online Market Analyzer & Scanner Replicated Architecture

We have successfully brought in reference architectures and repositories:
1. **`AlbionOnline-StatisticsAnalysis`** (C# Windows desktop application structure featuring packet analysis, market auction house reading, crafting calculators, and loggers).
2. **`albion-online-analyzer`** (Next.js web frontend & full-stack market platform with profit calculators, build databases, and community features).

## Replicated Architecture Plan (`/root/albion-analyzer-clone/`)

We are combining the backend market data syncing logic with a clean, modern web interface.

### Project Layout
```
/root/albion-analyzer-clone/
├── backend/                  # FastAPI service for querying pricing data & calculating flips
│   ├── main.py               # REST API endpoints for prices, crafting, and arbitrage
│   ├── calculations.py       # Refining/Crafting/Tax formulas
│   └── requirements.txt
├── scanner/                  # Packet-sniffing / client log parser utility (Python)
│   └── sniffer.py            # Local UDP / Photon packet sniffer concepts
└── frontend/                 # Next.js web application (Dashboard & Calculators)
    └── src/app/              # UI pages adapted from Aditya-Bichave's codebase
```

---

### Core Implementation: `backend/main.py`

```python
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Albion Market Analyzer Clone API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "https://www.albion-online-data.com/api/v2/stats/prices"

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "albion-analyzer-clone"}

@app.get("/api/prices/{item_id}")
async def get_item_prices(item_id: str, locations: str = "Bridgewatch,Martlock,Lymhurst,Fort Sterling,Thetford,Caerleon,Brecilien"):
    async with httpx.AsyncClient() as client:
        url = f"{BASE_URL}/{item_id}.json?locations={locations}"
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Error fetching from Albion Data Project API")
        return response.json()

@app.post("/api/calculate/crafting")
async def calculate_crafting(
    item_value: int,
    material_cost: int,
    return_rate: float = 0.15, # 15% standard return rate
    station_tax: int = 1000,
    market_tax: float = 0.065 # 6.5% with premium
):
    # Effective material cost after return rate
    effective_material_cost = material_cost * (1.0 - return_rate)
    total_cost = effective_material_cost + station_tax
    revenue_after_tax = item_value * (1.0 - market_tax)
    net_profit = revenue_after_tax - total_cost
    
    return {
        "item_value": item_value,
        "effective_material_cost": round(effective_material_cost, 2),
        "total_cost": round(total_cost, 2),
        "revenue_after_tax": round(revenue_after_tax, 2),
        "net_profit": round(net_profit, 2),
        "margin_percentage": round((net_profit / revenue_after_tax) * 100, 2) if revenue_after_tax > 0 else 0
    }
```
