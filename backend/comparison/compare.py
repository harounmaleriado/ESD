# compare.py
from flask import Flask, request, jsonify
from flask import Flask
from flask_cors import CORS
import requests
app = Flask(__name__)
CORS(app)

# Assuming dataservice.py has been updated to accept multiple item IDs at the '/get-items' endpoint
DATASERVICE_URL = 'http://localhost:5001/get-items'

@app.route('/compare-items', methods=['POST'])
def compare_items():
    # Example payload: {"item_ids": ["item1", "item2"]}
    item_ids = request.json.get('item_ids', [])
    
    # Forward the request to dataservice.py to fetch data for the specified item IDs
    try:
        response = requests.post(DATASERVICE_URL, json={'item_ids': item_ids}, timeout=10)
        if response.status_code == 200:
            # Return the fetched data directly to the client
            return jsonify(response.json())
        else:
            # Handle possible errors from the dataservice with its response status
            return jsonify({'error': 'Data service error', 'status': response.status_code}), response.status_code
    except requests.exceptions.RequestException as e:
        # Handle exceptions related to the request made to dataservice, such as connection errors
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)