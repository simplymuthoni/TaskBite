from flask import Flask, request, jsonify, Blueprint, session
from flasgger import Swagger
from app.models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
import os
from flask_mail import Mail, Message

app = Flask(__name__)
swagger = Swagger(app)

# Initialize Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Session(app)

auth = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth.route('/register', methods=['POST'])
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


    user = User(
        username=username,
        name=name,
        email=email,
        password=password
    )

    db.session.add(user)
    db.session.commit()

    # Send verification email
    msg = Message("Registration Successful", sender="patriciamuthoni414@gmail.com", recipients=[email])
    msg.body = f"Dear {name},\n\nThank you for registering with us. Please click on the following link to verify your email address: {request.url_root}verify/{user.id}\n\nBest regards,\n[TaskBite]"
    Mail.send(msg)

    return jsonify({"message": "Registered successfully"}), 201

# Add a new route to handle email verification
@auth.route('/verify/<int:user_id>', methods=['GET'])
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
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.email_verified = True
    db.session.commit()

    return jsonify({"message": "Email verified successfully"}), 200

@auth.route('/login', methods=['POST'])
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

    # if user is None or not check_password_hash(user.password, password):
    #     return jsonify({"error": "Invalid email or password"}), 400

    session['user_id'] = user.id

    return jsonify({"message": "Login successful", "user": user.to_dict()}), 200

@auth.route('/logout', methods=['POST'])
def logout():
    """
    User logout
    ---
    responses:
      200:
        description: Logout successful
    """
    session.pop('user_id', None)
    session.pop('user_email', None)
    return jsonify({"message": "Logout successful"}), 200

@auth.route('/update/<int:user_id>', methods=['PUT'])
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
    if not user:
        return jsonify({"error": "User not found"}), 404

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
        user.set_password(password)

    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200

# Register Blueprint
app.register_blueprint(auth)

if __name__ == '__main__':
    app.run(debug=True)