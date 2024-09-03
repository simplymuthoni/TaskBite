"""
This module provides a Flask API for user authentication and management.

It includes endpoints for registering new users, logging in and out, resetting passwords,
and updating and deleting user accounts.

The API uses JSON Web Tokens (JWT) for authentication and authorization.

Usage:
    To run the API, execute this module as a script.
    To use the API, send HTTP requests to the various endpoints.

Endpoints:
    /register: Register a new user
    /login: Log in a user
    /logout: Log out a user
    /forgot-password: Send a password reset email to a user
    /reset-password: Reset a user's password
    /update/<int:user_id>: Update a user's account information
    /delete: Delete a user account
"""
import os
import re
from flask import Flask, request, jsonify, Blueprint
from flasgger import Swagger
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_session import Session

#Import from package 'app'
from app import models, extensions, schemas

#Intialize Flask app
app = Flask(__name__)
swagger = Swagger(app)
bcrypt = Bcrypt(app)
limiter = Limiter(app=app, key_func=get_remote_address)

# Initialize Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
Session(app)

#Intialize database and schema
db = extensions.db
User = models.User
UserSchema = schemas.UserSchema

#Initialize blueprint
auth = Blueprint('auth', __name__, url_prefix='/api/auth')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

def generate_password_reset_token(user_id):
    """
    Generates a password reset token for the given user ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        str: The password reset token.
    """
    return serializer.dumps(user_id, salt='password-reset-salt')

def send_password_reset_email(user, token):
    """
    Sends a password reset email to the given user.

    Args:
        user (User): The user to send the email to.
        token (str): The password reset token.

    Returns:
        None
    """
    # Implement your email sending logic here
    # For example, using Flask-Mail:
    mail = Mail(app)
    msg = Message("Password Reset", sender="your-email@example.com", recipients=[user.email])
    msg.body = f"Your password reset token is: {token}"
    mail.send(msg)

def validate_email(email):
    """
    Validates an email address.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_username(username):
    """
    Validates a username.

    Args:
        username (str): The username to validate.

    Returns:
        bool: True if the username is valid, False otherwise.
    """
    pattern = r'^[a-zA-Z0-9_.-]+$'
    return bool(re.match(pattern, username))

def validate_password(password):
    """
    Validates a password.

    Args:
        password (str): The password to validate.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    return len(password) >= 8

@auth.route('/register', methods=['POST'])
@limiter.limit("10/minute")
def register():
    """
    Register a new user
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: User
          required:
            - username
            - name
            - password
            - email
          properties:
            username:
              type: string
            name:
              type: string
            password:
              type: string
            email:
              type: string
    responses:
      201:
        description: User registered successfully
      400:
        description: Invalid input or missing required fields
    """
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    username = data.get('username')
    name = data.get('name')
    password = data.get('password')
    email = data.get('email')

    if not all([username, name, password, email]):
        return jsonify({'message': 'Missing required fields'}), 400

    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return jsonify({'message': 'Invalid email address'}), 400

    if not re.match(r'^[a-zA-Z0-9_.-]+$', username):
        return jsonify({'message': 'Invalid username'}), 400

    if len(password) < 8:
        return jsonify({'message': 'Password must be at least 8 characters'}), 400

    try:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    except Exception as e:
        return jsonify({'message': 'Failed to hash password'}), 400

    user = User(username=username, name=name, password=hashed_password, email=email)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        return jsonify({'message': 'Failed to create user'}), 400

    return jsonify({'message': 'User registered successfully'}), 201

@auth.route('/login', methods=['POST'])
@limiter.limit("10/minute")
@jwt_required()
def login():

    """
    Login a user
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Login
          required:
            - email
            - password
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login successful
      400:
        description: Invalid input or missing required fields
      401:
        description: Unauthorized
    """
    data = request.get_json()

    if data is None:
        return jsonify({'message': 'No input data provided'}), 400

    email = data.get('email')
    password = data.get('password')

    if email is None or password is None:
        return jsonify({'message': 'Missing required fields'}), 400

    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return jsonify({'message': 'Invalid email address'}), 400

    user = User.query.filter_by(email=email).first()

    if user is None or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"message": "Login successful","access_token": access_token}), 200

@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout user
    ---
    responses:
      200:
        description: Logout successful
    """

    return jsonify({"message": "Logout successful"}), 200

@auth.route('/forgot-password', methods=['POST'])
def forgot_password():
    """
    Forgot password
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: ForgotPassword
          required:
            - email
          properties:
            email:
              type: string
    responses:
      200:
        description: Password reset email sent successfully
      400:
        description: Invalid input or email not found
    """
    data = request.get_json()

    if data is None:
        return jsonify({'message': 'No input data provided'}), 400

    email = data.get('email')
    if email is None:
        return jsonify({'message': 'Missing required fields'}), 400

    if not isinstance(email, str) or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return jsonify({'message': 'Invalid email address'}), 400

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({'message': 'Email not found'}), 400

    try:
        token = generate_password_reset_token(user.id)
        send_password_reset_email(user, token)
    except Exception as e:
        return jsonify({'message': 'Error sending password reset email: {}'.format(str(e))}), 400

    return jsonify({'message': 'Password reset email sent successfully'}), 200

@auth.route('/reset-password', methods=['POST'])
def reset_password():
    """
    Resets a user's password

    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: ResetPassword
          required:
            - token
            - password
          properties:
            token:
              type: string
            password:
              type: string
    responses:
      200:
        description: Password reset successfully
      400:
        description: Invalid input or token
      500:
        description: Server error, could not reset password
    """
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    token = data.get('token')
    password = data.get('password')

    if not all([token, password]):
        return jsonify({'message': 'Missing required fields'}), 400

    if len(password) < 8:
        return jsonify({'message': 'Password must be at least 8 characters'}), 400

    try:
        user_id = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except (BadSignature, SignatureExpired):
        return jsonify({'message': 'Invalid or expired token'}), 400

    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    user.password = bcrypt.generate_password_hash(password).decode('utf-8')
    db.session.commit()

    return jsonify({'message': 'Password reset successfully'}), 200

@auth.route('/update/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """
    Update user
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: The user ID
      - name: body
        in: body
        required: true
        schema:
          id: User
          required:
            - username
            - name
            - email
          properties:
            username:
              type: string
            name:
              type: string
            email:
              type: string
    responses:
      200:
        description: User updated successfully
      400:
        description: Invalid input or missing required fields
      401:
        description: Unauthorized
      404:
        description: User not found
    """
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()

    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    username = data.get('username')
    name = data.get('name')
    email = data.get('email')

    if not username or not name or not email:
        return jsonify({'message': 'Missing required fields'}), 400

    user.username = username
    user.name = name
    user.email = email

    db.session.commit()

    return jsonify({'message': 'User updated successfully'}), 200
@auth.route('/delete', methods=['POST'])
@jwt_required
def delete_user():
    """
    Delete a user
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: User
          required:
            - id
          properties:
            id:
              type: integer
    responses:
      200:
        description: User deleted successfully
      401:
        description: Unauthorized
      404:
        description: User not found
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    user_id = data.get('id')

    if not user_id:
        return jsonify({"error": "Missing required fields"}), 400
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.id != get_jwt_identity():
        return jsonify({"error": "Unauthorized"}), 401

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200

# Register Blueprint
app.register_blueprint(auth)

if __name__ == '__main__':
    app.run(debug=True)