from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from main.models.auth_models import db, User
from main.jwt_utils import generate_jwt_token
import pika
from main.amqp_connection import create_connection, check_exchange
import os, sys
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

    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    #retrieve geenrate user id from the database
    try:
        user_id = new_user.id

        profile_data = {
            "user_id": user_id,
            "email": email
        }

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

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        token = generate_jwt_token(user_id=user.id)
        return jsonify({
            "message": "Login successful",
            "jwt_token": token
        }), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

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
