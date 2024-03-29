# dataservice.py
from flask import Flask, request, jsonify
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Simulated database
fake_database = {
    'item1': {'name': 'Item 1', 'description': 'This is item 1'},
    'item2': {'name': 'Item 2', 'description': 'This is item 2'},
    # Add more items as needed
}

@app.route('/get-items', methods=['POST'])  # Note the change to 'get-items' to reflect multiple items
def get_items():
    item_ids = request.json.get('item_ids', [])
    items_data = {item_id: fake_database.get(item_id, 'Not Found') for item_id in item_ids}
    return jsonify(items_data)

# dataservice.py - Add a new route to list items
@app.route('/list-items', methods=['GET'])
def list_items():
    items_list = [{"id": item_id, "name": item["name"]} for item_id, item in fake_database.items()]
    return jsonify(items_list)


if __name__ == '__main__':
    app.run(port=5001, debug=True)