from fastapi import FastAPI, HTTPException
import random
from datetime import datetime
import uvicorn

app = FastAPI()

INSTRUMENTS = [
    "AAPL",
    "GOOGL",
    "MSFT",
    "BTC-USD",
    "ETH-USD"
]

@app.get("/v1/market-data")
def get_market_data():

    # Fault Injection (5%)
    fault = random.randint(1, 100)

    # Simulate API failure
    if fault <= 3:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

    records = []

    for _ in range(10):

        instrument = random.choice(INSTRUMENTS)

        price = round(
            random.uniform(100, 50000),
            2
        )

        volume = round(
            random.uniform(1, 1000),
            2
        )

        # malformed data
        if fault in [4, 5]:
            price = "INVALID_PRICE"

        records.append({
            "instrument_id": instrument,
            "price": price,
            "volume": volume,
            "timestamp": datetime.utcnow().isoformat()
        })

    return records


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )