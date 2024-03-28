from os import environ
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Example hardware data
# In a real application, this data could come from a database or an external API
hardware_data = {
    'hardware1Option1': {'name': 'Hardware 1 Option 1', 'cpu': 'Intel i7', 'ram': '16GB', 'storage': '512GB SSD'},
    'hardware1Option2': {'name': 'Hardware 1 Option 2', 'cpu': 'AMD Ryzen 7', 'ram': '32GB', 'storage': '1TB SSD'},
    'hardware2Option1': {'name': 'Hardware 2 Option 1', 'cpu': 'Intel i5', 'ram': '8GB', 'storage': '256GB SSD'},
    'hardware2Option2': {'name': 'Hardware 2 Option 2', 'cpu': 'AMD Ryzen 5', 'ram': '16GB', 'storage': '512GB SSD'},
}

@app.route('/compare', methods=['POST'])
def compare_hardware():
    data = request.json
    hardware1_id = data.get('hardware1')
    hardware2_id = data.get('hardware2')
    
    # Fetch hardware details based on the IDs
    hardware1_details = hardware_data.get(hardware1_id, {})
    hardware2_details = hardware_data.get(hardware2_id, {})
    
    # Here you could implement more sophisticated comparison logic
    comparison_result = {
        'hardware1': hardware1_details,
        'hardware2': hardware2_details,
    }
    
    return jsonify(comparison_result)

if __name__ == '__main__':
    app.run(debug=True)