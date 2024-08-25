"""
This module provides the authentication and user management functionality for the application.

It includes routes for user registration, login, email verification, and account updates.
The module also handles: 
-session management
-JWT authentication 
-rate limiting
-token blacklisting.

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
from flask import Flask, request, jsonify, Blueprint, session, url_for
from flasgger import Swagger
from werkzeug.security import check_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask_jwt_extended import create_access_token, get_jwt
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.models import User, Note, ToDo
from app.extensions import db
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
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])


def is_valid_username(username):
    """
    Validate the username based on allowed characters.

    Args:
        username (str): The username to validate.

    Returns:
        bool: True if the username is valid, False otherwise.
    """
    return re.match(r'^[a-zA-Z0-9_.-]+$', username) is not None

def validate_email(email):
    """
    Validates an email address using a regular expression.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email address is valid, False otherwise.
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

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
      500:
        description: Server error, could not send verification email
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

    # Validate email address
    if not validate_email(email):
        return jsonify({"error": "Invalid email address"}), 400

    # Check if username or email already exists
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"error": "Username or email already taken"}), 400

    # Hash password using Argon2
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    user = User(
        username=username,
        name=name,
        email=email,
        password=hashed_password
    )

    db.session.add(user)
    db.session.commit()

     # Generate a token for email verification
    token = serializer.dumps(user.email, salt='email-confirm')
    # Create the verification link
    confirm_url = url_for('confirm_email', token=token, _external=True)
    # Send the email
    send_email(user.email, 'Confirm Your Email', confirm_url=confirm_url)
    return jsonify({'message': 'User created. Please check your email to verify your account.'}), 201

def send_email(to, subject, **kwargs):
    """
    Sends an email to the specified recipient with the provided subject and content.

    Args:
        to (str): The recipient's email address.
        subject (str): The subject of the email.
        template (str): The template to use for the email body (not used in this example).
        **kwargs: Additional keyword arguments, such as 'confirm_url' for the email content.

    Example:
        >>> send_email('user@example.com', 
        'Confirm Your Email',confirm_url='http://example.com/confirm/abc123')

    Returns:
        None
    """
    msg = Message(subject, recipients=[to])
    msg.body = f'Click the link to verify your email: {kwargs["confirm_url"]}'
    mail.send(msg)


@auth.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    """
    Confirms the user's email address using a token sent via email.

    Args:
        token (str): The token used to verify the user's email.

    Example:
        >>> confirm_email('abc123')

    Returns:
        Response: A JSON response with a message indicating the result of the confirmation process.

        - 200: If the account is successfully verified or has already been verified.
        - 400: If the token is invalid or has expired.
    """
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=3600)
    except:
        return jsonify({'message': 'The confirmation link is invalid or has expired.'}), 400
    user = User.query.filter_by(email=email).first_or_404()
    if user.email_verified:
        return jsonify({'message': 'Account already verified. Please log in.'}), 200
    user.email_verified = True
    db.session.commit()
    return jsonify({'message': 'You have confirmed your account. Thanks!'}), 200


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

@auth.route('/users', methods=['GET'])
@jwt_required
def get_users():
    """
    Get all users
    ---
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        default: 1
      - name: per_page
        in: query
        type: integer
        required: false
        default: 10
    responses:
      200:
        description: List of users
        schema:
          type: array
          items:
            $ref: '#/definitions/User'
      401:
        description: Unauthorized
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    users = User.query.paginate(page, per_page, error_out=False)
    output = []

    for user in users.items:
        user_data = {}
        user_data['id'] = user.id
        user_data['username'] = user.username
        user_data['email'] = user.email
        output.append(user_data)

    return jsonify({'users': output, 'has_next': users.has_next, 'has_prev': users.has_prev, 'page': page, 'per_page': per_page}), 200


if __name__ == '__main__':
    app.run(debug=True)
