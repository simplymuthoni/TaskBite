from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_migrate import Migrate
from flask_cors import CORS
from flask_session import Session
from flasgger import Swagger
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import os
from .extensions import db
from flask_swagger_ui import get_swaggerui_blueprint
import config

load_dotenv()

def create_app(config_name):

    """
    Creates a Flask application instance with the specified configuration.

    Args:
        config_name (str): The name of the configuration to use. Can be 'development', 'testing', or 'production'.

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

    # Load environment variables from .env file
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Initialize extensions
    bcrypt = Bcrypt()
    jwt = JWTManager()
    mail = Mail()
    sess = Session()
    migrate = Migrate()
    swagger = Swagger()

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    sess.init_app(app)
    migrate.init_app(app, db)
    swagger.init_app(app)

    # Enable CORS
    CORS(app)

    with app.app_context():
        #import routes
        from app.routes import auth
        app.register_blueprint(auth, url_prefix='/api/auth')

    # Swagger setup
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "TaskBite"})
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Index route
    @app.route('/')
    def index():
        """
        Returns a welcome message.

        Returns:
            dict: A dictionary containing a welcome message.

        Example:
            >>> response = app.test_client().get('/')
            >>> response.json
            {'message': 'Welcome to TaskBite API'}
        """
        return jsonify({"message": "Welcome to TaskBite API"}), 200

    # Error handling
    @app.errorhandler(422)
    @app.errorhandler(400)
    def handle_error(err):
        """
        Handles 422 and 400 errors.

        Args:
            err (Exception): The error to handle.

        Returns:
            dict: A dictionary containing error messages.

        Example:
            >>> response = app.test_client().post('/invalid', data={'invalid': 'data'})
            >>> response.json
            {'errors': ['Invalid request.']}
        """
        headers = err.data.get("headers", None)
        messages = err.data.get("messages", ["Invalid request."])
        if headers:
            return jsonify({"errors": messages})
        else:
            return jsonify({"errors": messages})

    return app