import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, jsonify

app = Flask(__name__)

# Initialize Firebase Admin
cred = credentials.Certificate('path/to/your/firebase_credentials.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route('/get-hardware-options', methods=['GET'])
def get_hardware_options():
    collection_ref = db.collection('post')
    docs = collection_ref.stream()

    hardware_options = [{"id": doc.id, "name": doc.to_dict().get('name')} for doc in docs]
    return jsonify(hardware_options)

if __name__ == '__main__':
    app.run(debug=True)
