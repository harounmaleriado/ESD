import os
from firebase_admin import credentials, initialize_app

# This is just a test script to diagnose Firebase initialization issues
print("FIREBASE_ADMIN_KEY path from environment:", os.environ.get('FIREBASE_ADMIN_KEY'))

try:
    cred = credentials.Certificate(os.environ.get('FIREBASE_ADMIN_KEY'))
    initialize_app(cred)
    print("Firebase Admin initialized successfully.")
except Exception as e:
    print("Error initializing Firebase Admin SDK:", e)
