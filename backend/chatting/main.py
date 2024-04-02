from flask import Flask, request, jsonify
import redis
import json
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "shit"

# Initialize Redis client
redis_client = redis.Redis(
    host='redis-16378.c1.ap-southeast-1-1.ec2.cloud.redislabs.com',
    port=16378,
    password='muitCdS1YYaNGK1xUoCyouHthRJvjDnY',
    decode_responses=True)

@app.route('/api/messages', methods=['POST'])
def post_message():
    data = request.json
    # Construct a unique chat room ID using buyer and seller IDs
    chat_room_id = f"chat:{data['buyer_id']}_{data['seller_id']}"

    message = {
        'user_id': data['user_id'],
        'text': data['text'],
        'timestamp': datetime.utcnow().isoformat()
    }
    # Use the chat room ID as the key to store messages
    redis_client.rpush(chat_room_id, json.dumps(message))
    store_chat_invitation(data['buyer_id'], data['seller_id'])
    return jsonify({'status': 'success'}), 200

@app.route('/api/messages', methods=['GET'])
def get_messages():
    last_id = request.args.get('last_id', 0, type=int)
    buyer_id = request.args.get('buyerId')
    seller_id = request.args.get('sellerId')
    chat_room_id = f"chat:{buyer_id}_{seller_id}"

    messages = redis_client.lrange(chat_room_id, last_id, -1)
    messages = [json.loads(message) for message in messages]
    return jsonify(messages), 200

@app.route('/api/chat/invitations/<user_id>', methods=['GET'])
def get_chat_invitations(user_id):
    invitations_key = f"chat_invitations:{user_id}"
    invitations = redis_client.lrange(invitations_key, 0, -1)
    invitations = [json.loads(inv) for inv in invitations]
    return jsonify(invitations), 200


def store_chat_invitation(buyer_id, seller_id):
    invitation = {
        'buyer_id': buyer_id,
        'seller_id': seller_id,
        'chat_link': f"/chatroom.html?sellerId={seller_id}&buyerId={buyer_id}",
        'timestamp': datetime.utcnow().isoformat()
    }
    
    # Store the invitation in Redis under a key specific to the seller
    redis_client.rpush(f"chat_invitations:{seller_id}", json.dumps(invitation))

if __name__ == '__main__':
    app.run(debug=True)