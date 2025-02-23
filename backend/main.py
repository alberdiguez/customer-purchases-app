from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import date
from typing import Optional, List
import io
import csv
from collections import defaultdict

app = FastAPI(title="Customer Purchases API")

# In-memory storage
purchases = []

class Purchase(BaseModel):
    customer_name: str
    country: str
    purchase_date: date
    amount: float

@app.post("/purchase/", response_model=Purchase)
async def add_purchase(purchase: Purchase):
    if not purchase.customer_name:
        raise HTTPException(status_code=422, detail="Customer name cannot be empty")
    if not purchase.country:
        raise HTTPException(status_code=422, detail="Country cannot be empty")
    if not purchase.purchase_date:
        raise HTTPException(status_code=422, detail="Purchase date cannot be empty")
    if purchase.amount is None or purchase.amount < 0:
        raise HTTPException(status_code=422, detail="Amount cannot be empty or negative")
    purchases.append(purchase)
    return purchase

@app.post("/purchase/bulk/")
async def add_bulk_purchases(file: UploadFile = File(...)):
    if file.content_type not in ["text/csv"]:
        raise HTTPException(status_code=400, detail="Invalid file format")
    contents = await file.read()
    decoded = contents.decode("utf-8")
    reader = csv.DictReader(io.StringIO(decoded))
    new_purchases = []
    for row in reader:
        try:
            purchase = Purchase(
                customer_name=row["customer_name"],
                country=row["country"],
                purchase_date=date.fromisoformat(row["purchase_date"]),
                amount=float(row["amount"])
            )
            purchases.append(purchase)
            new_purchases.append(purchase)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing row: {row} - {e}")
    return JSONResponse(content={"added": len(new_purchases)})

@app.get("/purchases/", response_model=dict)
def get_purchases(country: Optional[str] = None, start_date: Optional[date] = None, end_date: Optional[date] = None):
    filtered = purchases
    if country:
        filtered = [p for p in filtered if p.country.lower() == country.lower()]
    if start_date:
        filtered = [p for p in filtered if p.purchase_date >= start_date]
    if end_date:
        filtered = [p for p in filtered if p.purchase_date <= end_date]

    # If no filters are matched, returns empty list and None for KPIs
    if not filtered:
        return {"purchases": [], "kpis": None}

    # Mean purchases per client
    custSpending = defaultdict(float)
    for p in filtered:
        custSpending[p.customer_name] += p.amount
    mean = sum(custSpending.values()) / len(custSpending)

    # Number of clients per country
    custPerCountry = defaultdict(set)
    for p in filtered:
        custPerCountry[p.country].add(p.customer_name)
    custPerCountry = {country: len(clients) for country, clients in custPerCountry.items()}

    return {
        "purchases": filtered,
        "kpis": {
            "avg_purchases_per_client": mean,
            "clients_per_country": custPerCountry
        }
    }
