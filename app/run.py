"""
This script creates a Flask application instance and runs it.

The application configuration is determined by the `FLASK_CONFIG` environment
variable, which can be set to one of the following values:

* `development`: Development configuration (default)
* `testing`: Testing configuration
* `production`: Production configuration

Example:
    To run the application in development mode, set the `FLASK_CONFIG` environment
    variable to `development` and run the script:
    ```
    $ FLASK_CONFIG=development python app.py
    ```

    To run the application in production mode, set the `FLASK_CONFIG` environment
    variable to `production` and run the script:
    ```
    $ FLASK_CONFIG=production python app.py
    ```
"""
from app import create_app

app = create_app('development')

if __name__ == '__main__':
    app.run()
