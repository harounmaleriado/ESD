from fastapi import FastAPI
from typing import List
from pydantic import BaseModel

app = FastAPI()

class Product(BaseModel):
    name: str
    price: float
    description: str
    # Add more fields as necessary

# Mock data - replace this with your actual data fetching logic
products = [
    Product(name="Guitar", price=100.0, description="An acoustic guitar"),
    Product(name="Piano", price=1000.0, description="A grand piano"),
    # Add more products
]

@app.get("/search/", response_model=List[Product])
async def search(query: str):
    result = [product for product in products if query.lower() in product.name.lower()]
    return result
