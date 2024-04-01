from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

# Define the Pydantic model for the request body
class ItemIds(BaseModel):
    item_ids: list[str]

app = FastAPI()

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Assuming dataservice.py has been updated to accept multiple item IDs at the '/get-items' endpoint
DATASERVICE_URL = 'http://localhost:8000/compare'

@app.post("/compare")
async def compare_items(item_ids: ItemIds):
    # Use an async http client from httpx
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(DATASERVICE_URL, json={'item_ids': item_ids.item_ids})
            if response.status_code == 200:
                # Return the fetched data directly to the client
                return response.json()
            else:
                # Handle possible errors from the dataservice with its response status
                raise HTTPException(status_code=response.status_code, detail="Data service error")
        except httpx.RequestError as e:
            # Handle exceptions related to the request made to dataservice, such as connection errors
            raise HTTPException(status_code=500, detail=str(e))
