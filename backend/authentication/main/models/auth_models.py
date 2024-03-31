import firebase_admin
from firebase_admin import credentials, auth, firestore
from os import environ

cred = credentials.Certificate(environ.get('FIREBASE_ADMIN_KEY'))
firebase_admin.initialize_app(cred)

db = firestore.client()

class User:
    def __init__(self, uid, email, password):
        self.uid = uid
        self.email = email
        self.password = password
    
    @staticmethod
    def create(email, password, username):
        user_record = auth.create_user(email=email, password=password)
        uid = user_record.uid
        # Add the username to Firestore as additional data
        db.collection('users').document(uid).set({'username': username, 'email': email})
        return uid
    
    @staticmethod
    def get_by_email(email):
        try:
            user_record = auth.get_user_by_email(email)
            return user_record
        except firebase_admin.auth.UserNotFoundError:
            return None
    
    @staticmethod
    def get(uid):
        user_data = db.collection('users').document(uid).get()
        if user_data.exists:
            return user_data.to_dict()
        else:
            return None
    
    @staticmethod
    def set_password(uid, new_password):
        auth.update_user(uid, password=new_password)
    
    @staticmethod
    def check_password(uid, password):
        try:
            # Try to sign in with email and password
            user_record = auth.get_user(uid)
            email = user_record.email
            auth.verify_password(password, email)
            return True
        except auth.AuthError:
            return False
        
    @staticmethod
    def get_by_username(username):
        users_ref = db.collection('users').where('username', '==', username).limit(1).stream()
        for user in users_ref:
            return user.to_dict()
        return None
