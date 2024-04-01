from flask import Blueprint, request, jsonify
import firebase_admin
from firebase_admin import credentials, auth, firestore
from main.models.auth_models import db, User
from main.jwt_utils import generate_jwt_token
import pika
from main.amqp_connection import create_connection, check_exchange
import sys
import json

auth_bp = Blueprint('auth_bp', __name__)

exchangename = "auth_direct"
exchangetype = "direct"

connection = create_connection()
channel = connection.channel()

if not check_exchange(channel, exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  # Exit with a success status

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({"message": "Missing information"}), 400

    existing_user = User.get_by_email(email)
    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    # Create the user in Firebase Authentication
    uid = User.create(email, password, username)

    # Assuming you also send the profile data to the Profile service
    profile_data = {
        "user_id": uid,
        "email": email
    }

    #retrieve geenrate user id from the database
    try:
        channel.basic_publish(
            exchange=exchangename, 
            routing_key="profile", 
            body=json.dumps(profile_data), 
            properties=pika.BasicProperties(delivery_mode = 2))
    except pika.exceptions.AMQPError as e:
        print(f"Error: {e}")
        return jsonify({"message": "User registered successfully but failed to publish to the profile microservice"}), 201

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400

    user_data = User.get_by_username(username)
    if not user_data:
        return jsonify({"message": "Invalid username"}), 404

    try:
        user = auth.get_user_by_email(user_data['email'])
        # Since Firebase does not support password checks via the server SDK,
        # you would need to check the password on the client side using Firebase methods.
        # Once verified on the client side, you can create a custom token:
        token = generate_jwt_token(user.uid)
        return jsonify({
            "message": "Login successful",
            "jwt_token": token
        }), 200
    except auth.AuthError:
        return jsonify({"message": "Invalid login credentials"}), 401

@auth_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.isoformat(),  # Formatting datetime for JSON response
            'updated_at': user.updated_at.isoformat()
        }
        return jsonify(user_data), 200
    else:
        return jsonify({'message': 'User not found'}), 404

@auth_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_data = [
        {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.isoformat(),
            'updated_at': user.updated_at.isoformat()
        } for user in users
    ]
    return jsonify(users_data), 200
