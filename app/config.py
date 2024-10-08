"""
config.py

This module contains the configuration settings for the Flask application. 

It includes:
- Configuration variables for Flask extensions such as 
Flask-Session, Flask-JWT-Extended, and Flask-Mail.
- Any other application-specific settings such as 
secret keys, session management settings, and JWT expiration times.

Configuration variables:
- SECRET_KEY: The secret key used by Flask for session management and security.
- JWT_SECRET_KEY: The secret key used for signing JWT tokens.
- JWT_ACCESS_TOKEN_EXPIRES: The expiration time for JWT access tokens.
- SESSION_TYPE: The type of session management used by Flask-Session.
- MAIL_SENDER: The email address used as the sender for outgoing emails.

Ensure that all sensitive information, such as secret keys, 
is set through environment variables and not hardcoded in this file.

Usage:
Import the configuration settings into your 
Flask application using `app.config.from_object('config')`.

Example:
    from flask import Flask
    app = Flask(__name__)
    app.config.from_object('config')
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Base configuration class
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')

    """
    Secret key for Flask application. Should be set as an environment variable.
    Example: `SECRET_KEY=my_secret_key`
    """

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    """
    URI for SQLAlchemy database connection. Should be set as an environment variable.
    Example: `SQLALCHEMY_DATABASE_URI=postgresql://user:password@host:port/dbname`
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')

    """
    Username for email server. Should be set as an environment variable.
    Example: `MAIL_USERNAME=my_email_username`
    """

    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    """
    Password for email server. Should be set as an environment variable.
    Example: `MAIL_PASSWORD=my_email_password`
    """

    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'flask_session:'
    # JWT Config
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

    """
    Secret key for JWT token generation. Should be set as an environment variable.
    Example: `JWT_SECRET_KEY=my_jwt_secret_key`
    """

    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_ACCESS_TOKEN_EXPIRES=3600  # 1 hour in seconds
    JWT_REFRESH_TOKEN_EXPIRES=2592000  # 30 days in seconds

    # Logging Config
    LOG_LEVEL = 'DEBUG'
    LOG_FILE = 'taskbite.log'


class ProductionConfig(Config):

    """
    Production configuration class
    """

    DEBUG = False

    """
    Disable debug mode in production environment.
    """


class DevelopmentConfig(Config):

    """
    Development configuration class
    """

    DEBUG = True

    """
    Enable debug mode in development environment.
    """

    USE_RELOADER = False

    """
    Disable automatic reloading of application in development environment.
    """


class TestingConfig(Config):

    """
    Testing configuration class
    """

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')
    """
    URI for test database connection. Should be set as an environment variable.
    Example: `TEST_DATABASE_URL=postgresql://user:password@host:port/test_dbname`
    """


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
"""
Dictionary of configuration classes for different environments.
"""
