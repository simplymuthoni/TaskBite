"""
This script creates a Flask application instance and runs it on a specified host and port.
It also initializes the Flask-Migrate extension for database migrations.

Example usage:
    python app.py

This will start the Flask development server on host '0.0.0.0' and port 8000.
"""
from app import create_app


if __name__ == "__main__":

    CONFIG_NAME = 'development'  # Configuration name for the Flask app
    app = create_app(CONFIG_NAME)  # Create the Flask app instance
    app.run(host='0.0.0.0', port=8000)  # Run the Flask development server
    