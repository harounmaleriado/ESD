from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

app = FastAPI()

# Define your Pydantic models to enforce type checking and data validation
class ItemIDs(BaseModel):
    item_ids: list[str]

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

DATASERVICE_URL = 'http://localhost:5001/compare'

@app.post('/compare')
async def compare_items(item_ids: ItemIDs):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(DATASERVICE_URL, json={'item_ids': item_ids.item_ids}, timeout=10.0)
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Data service error")
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=str(exc))

# Note: FastAPI's development server is run differently compared to Flask
# You would typically run a FastAPI app with a command like:
# uvicorn filename:app --reload --port 5000