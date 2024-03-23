import firebase_admin
from firebase_admin import credentials, firestore
from os import environ

#cred = credentials.Certificate('E:\Codes\ESD_Tech\profile\main\esd-project-bec59-firebase-adminsdk-3vbkj-566a693eaa.json')
cred = credentials.Certificate(environ.get('FIREBASE_ADMIN_KEY'))
firebase_admin.initialize_app(cred)

db = firestore.client()


class Profile:
    def __init__(self, user_id, name, email, contact_details=None, bio=None, profile_pic=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.contact_details = contact_details
        self.bio = bio
        self.profile_pic = profile_pic

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'contact_details': self.contact_details,
            'bio': self.bio,
            'profile_pic': self.profile_pic
        }
    
    @staticmethod
    def create(profile_data):
        doc_ref = db.collection('profiles').add(profile_data.to_dict())
        print(f"Profile created with ID: {doc_ref[1].id}")

    @staticmethod
    def get_by_user_id(user_id):
        # Assumes user_id is unique
        profiles = db.collection('profiles').where('user_id', '==', user_id).get()
        if profiles:
        # Return the first profile found
            return Profile(**profiles[0].to_dict())
        else:
            return None
    
    @staticmethod
    def update(profile_data):
        user_id = profile_data['user_id']
        doc_ref = db.collection('profiles').where('user_id', '==', user_id).get()
        if doc_ref:
            document_id = doc_ref[0].id  # Get the Firestore document ID
            db.collection('profiles').document(document_id).set(profile_data, merge=True)



