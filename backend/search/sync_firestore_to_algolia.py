from algoliasearch.search_client import SearchClient
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate('./firebase-adminsdk.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

# Initialize Algolia
client = SearchClient.create('60IC04XR8A', '8766f78f6c717baf768884e6ca4d36a5')
index = client.init_index('search_posts')

# Fetch documents from Firestore
posts_ref = db.collection('post')
docs = posts_ref.stream()

# Push each document to Algolia
for doc in docs:
    doc_dict = doc.to_dict()
    doc_dict['objectID'] = doc.id  # Algolia requires an objectID

    # Convert any GeoPoint objects to a serializable format
    for key, value in doc_dict.items():
        if isinstance(value, firestore.GeoPoint):
            # Convert GeoPoint to a dictionary
            doc_dict[key] = {'latitude': value.latitude, 'longitude': value.longitude}

    # Now save the object to Algolia
    index.save_object(doc_dict)
