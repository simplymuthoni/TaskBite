"""
config.py

This module provides configuration settings for the Flask application. 

It sets up the application configurations based on the environment 
(development, testing, or production) 
and initializes necessary extensions such as 
SQLAlchemy, Bcrypt, JWTManager, Mail, and more.

Configuration:
- SQLALCHEMY_DATABASE_URI: URI for SQLAlchemy database connection.
- JWT_SECRET_KEY: Secret key for signing JWT tokens.
- MAIL_SERVER: Server for sending emails.
- MAIL_PORT: Port for the mail server.
- MAIL_USE_TLS: Boolean to enable TLS for the mail server.
- MAIL_USERNAME: Username for the mail server.
- MAIL_PASSWORD: Password for the mail server.
- SESSION_TYPE: Type of session management.
- SECRET_KEY: Secret key used for Flask session management.

Usage:
Call `create_app(config_name)` 
to create a Flask application instance with the desired configuration.

Example:
    >>> app = create_app('development')
"""

import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_migrate import Migrate
from flask_cors import CORS
from flasgger import Swagger
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from flask_session import Session
from app import config
from .extensions import db

# Load environment variables from .env file
load_dotenv()

# Initialize extensions
bcrypt = Bcrypt()
jwt = JWTManager()
mail = Mail()
sess = Session()
migrate = Migrate()
swagger = Swagger()
migrate = Migrate()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def create_app(config_name):
    """
    Creates a Flask application instance with the specified configuration.

    Args:
        config_name (str): The name of the configuration to use. 
        Can be 'development', 'testing', or 'production'.

    Returns:
        Flask: The created Flask application instance.

    Raises:
        KeyError: If the specified configuration name is not valid.

    Example:
        >>> app = create_app('development')
    """

    app = Flask(__name__)

    # Load additional config
    app_config = {
        'development': config.DevelopmentConfig,
        'testing': config.TestingConfig,
        'production': config.ProductionConfig,
    }

    if config_name not in app_config:
        raise KeyError(f"Configuration '{config_name}' is not a valid configuration name.")

    app.config.from_object(app_config[config_name])

    # Load environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    if __name__ == "__main__":
        config_name = 'development'
    CORS(app)  

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    sess.init_app(app)
    migrate.init_app(app, db)
    swagger.init_app(app)

    #Register blueprints only once
    if not hasattr(app, 'blueprints'):
        from app.routes import auth
        app.register_blueprint(auth, url_prefix='/api/auth')

        # Swagger setup
        swagger_url = '/api/docs'
        api_url = '/static/swagger.json'
        swaggerui_blueprint = get_swaggerui_blueprint(swagger_url,
                                                      api_url,config={'app_name': "TaskBite"})
        app.register_blueprint(swaggerui_blueprint, url_prefix=swagger_url)

    # Index route
    @app.route('/')
    def root():
        """Returns a welcome message."""
        return {'message': 'Welcome to TaskBite API'}, 200

    # Error handling
    @app.errorhandler(422)
    @app.errorhandler(400)
    def handle_validation_error(exc):
        """Handles 422 and 400 errors."""
        if exc is None:
            return jsonify({"errors": ["Invalid request."]})
        if exc.data is None:
            return jsonify({"errors": ["Invalid request."]})
        messages = exc.data.get("messages", ["Invalid request."])
        return jsonify({"errors": messages})

    return app
