import firebase_admin
from firebase_admin import credentials, firestore, storage
from os import environ
from datetime import datetime

cred = credentials.Certificate(environ.get('FIREBASE_ADMIN_KEY'))
#cred = credentials.Certificate('/Users/shauntay/Documents/GitHub/ESD/backend/listings/main/firebase-adminsdk.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

bucket = storage.bucket('techexchange-76048.appspot.com')


class Listing:
    def __init__(self, category, datetime, desc, latitude, longitude, name, price, user_id):
            self.category = category  # This should be a list to reflect an array in Firebase
            self.datetime = datetime  # This can be a string or a datetime object
            self.desc = desc
            self.location = {
                'latitude': latitude,
                'longitude': longitude
            }
            self.name = name
            self.price = price
            self.user_id = user_id  # Link to the user profile

    def save(self):
        # Convert datetime to a Firestore-compatible format if it's a datetime object
        if isinstance(self.datetime, datetime):
            self.datetime = self.datetime.isoformat()

        listing_data = {
            'category': self.category,
            'datetime': self.datetime,
            'desc': self.desc,
            'location': self.location,
            'name': self.name,
            'price': self.price,
            'user_Id': self.user_id
        }
        # Add a new document in collection "listings" with the listing data
        db.collection('post').add(listing_data)
    
    @staticmethod
    def serialize_geo_point(listing):
        # Check if the listing has a 'location' field and if it's an instance of GeoPoint
        if 'location' in listing and isinstance(listing['location'], firestore.GeoPoint):
            # Convert GeoPoint to a dictionary with 'latitude' and 'longitude'
            listing['location'] = {
                'latitude': listing['location'].latitude,
                'longitude': listing['location'].longitude
            }
        return listing

    @staticmethod
    def get_user_listings(user_id):
        # Retrieve all documents in the "listings" collection that belong to the user
        listings_ref = db.collection('post')
        query_ref = listings_ref.where('user_Id', '==', user_id)
        return [doc.to_dict() for doc in query_ref.stream()]
    
    @staticmethod
    def get_listing_by_id(listing_id):
        try:
            listing_ref = db.collection('post').document(listing_id)
            listing = listing_ref.get()
            return listing.to_dict() if listing.exists else None
        except Exception as e:
            raise e
        
    @staticmethod
    def get_all_listings():
        try:
            listings_ref = db.collection('post')
            listings = [Listing.serialize_geo_point({"id": doc.id, **doc.to_dict()}) for doc in listings_ref.stream()]
            return listings
        except Exception as e:
            raise e




