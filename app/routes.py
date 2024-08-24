"""
This module provides the authentication and user management functionality for the application.

It includes routes for user registration, login, email verification, and account updates.
The module also handles session management, JWT authentication, rate limiting, and token blacklisting.

Main Features:
- User Registration with email verification
- User Login with JWT-based authentication
- Secure password storage with Flask-Bcrypt
- Rate limiting for routes using Flask-Limiter
- Session management with Flask-Session
- Email notifications via Flask-Mail
- User data updating and management

Dependencies:
- Flask
- Flask-JWT-Extended
- Flask-Mail
- Flask-Bcrypt
- Flask-Limiter
- Flask-Session

Usage:
- Register the blueprint with the Flask app to enable authentication routes.

Example:
    from flask import Flask
    from auth_module import auth

    app = Flask(__name__)
    app.register_blueprint(auth)

    if __name__ == '__main__':
        app.run(debug=True)
"""
import os
import re
from datetime import timedelta
from smtplib import SMTPException
from flask import Flask, request, jsonify, Blueprint, session, url_for
from flasgger import Swagger
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, get_jwt_identity, JWTManager
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.models import User, Note, ToDo
from app import db
from flask_session import Session


app = Flask(__name__)
swagger = Swagger(app)

# Initialize Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
Session(app)

# Initialize Flask-Bcrypt
bcrypt = Bcrypt(app)
limiter = Limiter(app=app, key_func=get_remote_address)
jwt = JWTManager(app)
mail = Mail(app)

auth = Blueprint('auth', __name__, url_prefix='/api/auth')

def is_valid_username(username):
    """
    Validate the username based on allowed characters.

    Args:
        username (str): The username to validate.

    Returns:
        bool: True if the username is valid, False otherwise.
    """
    return re.match(r'^[a-zA-Z0-9_.-]+$', username) is not None

def is_valid_email(email):
    """
    Validate the email address format.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email format is valid, False otherwise.
    """
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is not None

@auth.route('/register', methods=['POST'])
@limiter.limit("10/minute")
def add_user():
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
        return jsonify({"error": "Invalid input"}), 400

    username = data.get('username')
    name = data.get('name')
    password = data.get('password')
    email = data.get('email')


    if not all([username, name, password, email]):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"error": "Username already taken"}), 400
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "Email already registered"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    user = User(
        username=username,
        name=name,
        email=email,
        password=hashed_password
    )

    db.session.add(user)
    db.session.commit()

     # Create a token for email verification with an expiration of 15 minutes
    verification_token = create_access_token(identity=user.id, expires_delta=timedelta(minutes=15))
    verification_url = url_for('auth.verify_email', token=verification_token, _external=True)

    msg = Message("Registration Successful", sender=os.getenv('MAIL_SENDER'), recipients=[email])
    msg_body = (
        f"Dear {name},\n\n"
        f"Thank you for registering with us. Please click on the following link to verify your email address: {verification_url}\n\n"
        "Best regards,\n[TaskBite]"
    )    
    msg.body = msg_body
    try:
        mail.send(msg)
    except SMTPException as e:
      app.logger.error(f"SMTPException occurred: {e}")
      return jsonify({"error": "Could not send verification email"}), 500
    except RuntimeError as e:
      app.logger.error(f"RuntimeError occurred: {e}")
      return jsonify({"error": "Runtime error occurred"}), 500
    except Exception as e:
      app.logger.error(f"Unexpected error occurred: {e}")
      return jsonify({"error": "An unexpected error occurred"}), 500
    
    return jsonify({"message": "User registered successfully"}), 201


# Add a new route to handle email verification
@auth.route('/verify/<token>', methods=['GET'])
@jwt_required()
def verify_email(user_id):
    """
    Verify email address
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: The user ID
    responses:
      200:
        description: Email verified successfully
      404:
        description: User not found
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
    except Exception as e:
        return jsonify({"error": "Invalid or expired token"}), 400

    if not user:
        return jsonify({"error": "User not found"}), 404

    user.email_verified = True
    db.session.commit()

    return jsonify({"message": "Email verified successfully"}), 200


@auth.route('/login', methods=['POST'])
@limiter.limit("10/minute")
def login():
    """
    User login
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

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    user = User.query.filter_by(email=email).first()

    if user is None or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid email or password"}), 401
    
    if not user.email_verified:
        return jsonify({"message": "Email not verified. Please check your inbox."}), 401

    access_token = create_access_token(identity=user.id)
    session['user_id'] = user.id

    return jsonify({"message": "Login successful", "access_token": access_token}), 200  
@auth.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    """
    Fetches and returns the user's dashboard data including notes and to-do items.

    This endpoint requires a valid JWT token for access. It retrieves the user's notes
    and to-do list items from the database and organizes them into a calendar format.

    Returns:
        jsonify: A JSON response containing the user's dashboard data including
                 notes and to-do items categorized by date.
                 - "message": A welcome message for the user.
                 - "calendar_data": A dictionary with dates as keys and lists of notes
                   and to-do items as values.

    Responses:
        200:
            description: Successful retrieval of dashboard data
        401:
            description: Unauthorized access, invalid or missing JWT token
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    # Fetch user's notes and to-do list items
    notes = Note.query.filter_by(user_id=user.id).all()
    todos = ToDo.query.filter_by(user_id=user.id).all()

    # Prepare data for the calendar
    calendar_data = {}
    for note in notes:
        note_date = note.created_at.strftime('%Y-%m-%d')
        if note_date not in calendar_data:
            calendar_data[note_date] = {"notes": [], "todos": []}
        calendar_data[note_date]["notes"].append(note.content)

    for todo in todos:
        todo_date = todo.due_date.strftime('%Y-%m-%d')
        if todo_date not in calendar_data:
            calendar_data[todo_date] = {"notes": [], "todos": []}
        calendar_data[todo_date]["todos"].append(todo.task)

    return jsonify({
        "message": "Welcome to your dashboard",
        "calendar_data": calendar_data
    }), 200

@auth.route('/notes/<string:note_id>', methods=['GET'])
@jwt_required()
def view_note(note_id):
    """
    View a specific note by its ID
    ---
    parameters:
      - name: note_id
        in: path
        type: string
        required: true
        description: The ID of the note to view
    responses:
      200:
        description: Note details retrieved successfully
      404:
        description: Note not found
      401:
        description: Unauthorized
    """
    user_id = get_jwt_identity()
    note = Note.query.get(note_id)

    if not note or note.user_id != user_id:
        return jsonify({"error": "Note not found or unauthorized"}), 404

    return jsonify({
        "message": "Note retrieved successfully",
        "note": {
            "id": note.id,
            "content": note.content,
            "created_at": note.created_at.isoformat()
        }
    }), 200

@auth.route('/todos/<string:todo_id>', methods=['GET'])
@jwt_required()
def view_todo(todo_id):
    """
    View a specific to-do task by its ID
    ---
    parameters:
      - name: todo_id
        in: path
        type: string
        required: true
        description: The ID of the to-do task to view
    responses:
      200:
        description: To-do details retrieved successfully
      404:
        description: To-do not found
      401:
        description: Unauthorized
    """
    user_id = get_jwt_identity()
    todo = ToDo.query.get(todo_id)

    if not todo or todo.user_id != user_id:
        return jsonify({"error": "To-do not found or unauthorized"}), 404

    return jsonify({
        "message": "To-do retrieved successfully",
        "todo": {
            "id": todo.id,
            "task": todo.task,
            "priority": todo.priority,
            "due_date": todo.due_date.isoformat()
        }
    }), 200


@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    User logout
    ---
    responses:
      200:
        description: Logout successful
    """
    jti = get_jwt()["jti"]  # jti is the unique identifier of the JWT
    # Implement blacklist logic to revoke tokens
    session.clear()
    return jsonify({"message": "Logout successful"}), 200

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
      200:
        description: User updated successfully
      400:
        description: Invalid input or missing required fields
      404:
        description: User not found
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    user = User.query.get(user_id)
    if not user or user.id != get_jwt_identity():
        return jsonify({"error": "User not found or unauthorized"}), 404

    username = data.get('username')
    name = data.get('name')
    password = data.get('password')
    email = data.get('email')

    if username:
        if User.query.filter_by(username=username).first() and User.query.filter_by(username=username).first().id != user_id:
            return jsonify({"error": "Username already taken"}), 400
        user.username = username

    if email:
        if User.query.filter_by(email=email).first() and User.query.filter_by(email=email).first().id != user_id:
            return jsonify({"error": "Email already registered"}), 400
        user.email = email

    if name:
        user.name = name

    if password:
        user.password = bcrypt.generate_password_hash(password).decode('utf-8')
    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200

# Register Blueprint
app.register_blueprint(auth)

if __name__ == '__main__':
    app.run(debug=True)
