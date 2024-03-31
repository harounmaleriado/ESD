from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from algoliasearch.search_client import SearchClient
from typing import List, Dict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Algolia
client = SearchClient.create('60IC04XR8A', '8766f78f6c717baf768884e6ca4d36a5')
index = client.init_index('search_posts')

@app.get("/search")
def search(query: str = '') -> List[Dict]:
    if not query:
        return []
    
    # Perform the search on Algolia
    results = index.search(query)
    return results['hits']

# if __name__ == '__main__':
#     app.run(debug=True, host='127.0.0.1', port=5000)



