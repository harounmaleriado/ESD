from flask import Flask, request, jsonify
from flask_cors import CORS
from algoliasearch.search_client import SearchClient

app = Flask(__name__)
CORS(app)

# Initialize Algolia
client = SearchClient.create('60IC04XR8A', '8766f78f6c717baf768884e6ca4d36a5')
index = client.init_index('search_posts')

@app.route('/search')
def search():
    query = request.args.get('query', '')
    if not query:
        return jsonify([])

    # Perform the search on Algolia
    results = index.search(query)
    return jsonify(results['hits'])

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)



