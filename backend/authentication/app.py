from flask import Flask, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer
import os
from datetime import datetime, timedelta
import base64

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'zMq@aTjz@Za!RrT#4!YL63rP'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/authentication'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'd4vidg0ggins2023@gmail.com'
app.config['MAIL_PASSWORD'] = 'chsr bmhk urzj ayzd'
app.config['MAIL_DEFAULT_SENDER'] = 'd4vidg0ggins2023@gmail.com'

# Initialize SQLAlchemy
db = SQLAlchemy(app)
mail = Mail(app)

serializer = Serializer(app.config['SECRET_KEY'], salt='password-reset-salt')

# Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_token = db.Column(db.Text, unique=True, nullable=False)  # Use Text type to accommodate longer tokens
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Use DateTime for compatibility
    expires_at = db.Column(db.DateTime, nullable=False)  # Ensure this column is defined to store expiration
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Use DateTime

    user = db.relationship('User', backref=db.backref('sessions', lazy=True))

class PasswordResetToken(db.Model):
    __tablename__ = 'password_reset_tokens'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    expires_at = db.Column(db.TIMESTAMP, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)

# Routes
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_data = []
    for user in users:
        users_data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            # Do not return password hashes
            'created_at': user.created_at,
            'updated_at': user.updated_at
        })
    return jsonify(users_data), 200

@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            # Do not return password hashes
            'created_at': user.created_at,
            'updated_at': user.updated_at
        }
        return jsonify(user_data), 200
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User.query.filter((User.username == data['username']) | (User.email == data['email'])).first()
    if user:
        return jsonify({"message": "User already exists"}), 400
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password'])
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        serializer = Serializer(app.config['SECRET_KEY'], salt='session-token')
        session_token = serializer.dumps(str(user.id))

        new_session = Session(user_id=user.id, session_token=session_token, expires_at=datetime.utcnow() + timedelta(days=1))
        db.session.add(new_session)
        db.session.commit()

        return jsonify({"message": "Login successful", "session_token": session_token}), 200
    return jsonify({"message": "Invalid username or password"}), 401

@app.route('/request-password-reset', methods=['POST'])
def request_password_reset():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user:
        reset_token = serializer.dumps(user.email, salt='password-reset-salt')
        # Send reset email
        send_reset_email(user.email, reset_token)
    return jsonify({"message": "If your email is registered, you will receive a password reset link"}), 200

def send_reset_email(email, token):
    msg = Message("Password Reset Request", recipients=[email])
    msg.body = f"""To reset your password, visit the following link:
{url_for('reset_password', token=token, _external=True)}
If you did not make this request, simply ignore this email and no changes will be made.
"""
    mail.send(msg)

@app.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        return jsonify({"message": "Invalid or expired token"}), 400
    data = request.get_json()
    user = User.query.filter_by(email=email).first()
    user.password_hash = generate_password_hash(data['password'])
    db.session.commit()
    return jsonify({"message": "Your password has been updated"}), 200

@app.route('/logout', methods=['POST'])
def logout():
    session_token = request.headers.get('Authorization')
    session = Session.query.filter_by(session_token=session_token).first()
    if session:
        db.session.delete(session)
        db.session.commit()
    return jsonify({"message": "Logged out successfully"}), 200


@app.route('/validate-user/<int:user_id>', methods=['GET'])
def validate_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({"message": "User exists", "valid": True}), 200
    else:
        return jsonify({"message": "User does not exist", "valid": False}), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
