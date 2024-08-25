"""
This script creates a Flask application instance and runs it on a specified host and port.
It also initializes the Flask-Migrate extension for database migrations.

Example usage:
    python app.py

This will start the Flask development server on host '0.0.0.0' and port 8000.
"""

from flask_migrate import Migrate
from app import create_app
from app.extensions import db


if __name__ == "__main__":

    CONFIG_NAME = 'development'  # Configuration name for the Flask app
    app = create_app(CONFIG_NAME)  # Create the Flask app instance
    migrate = Migrate(app, db)  # Initialize Flask-Migrate extension
    app.run(host='0.0.0.0', port=8000)  # Run the Flask development server
    