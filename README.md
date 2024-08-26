TaskBite

TaskBite is a task management application with a React Native frontend and a Flask backend. This app allows users to register, log in, manage notes, and track to-do tasks. It includes features like user authentication, email verification, and a dashboard to view notes and tasks.
Table of Contents

    Features
    Technologies
    Backend Setup
    Frontend Setup
    API Documentation
    Contributing
    License

Features

    User Registration & Authentication: Secure registration, login, and logout functionalities with JWT.
    Email Verification: Email verification for new users.
    Dashboard: View and manage notes and to-do tasks.
    CRUD Operations: Create, read, update, and delete notes and to-do tasks.
    Rate Limiting: Prevent abuse with request rate limiting.
    Password Hashing: Secure storage of user passwords.

Technologies

    Frontend: React Native
    Backend: Flask
    Database: SQLite (or your preferred SQL database)
    Authentication: Flask-JWT-Extended
    Email Sending: Flask-Mail
    Rate Limiting: Flask-Limiter
    Password Hashing: Flask-Bcrypt
    Session Management: Flask-Session

Backend Setup

    Clone the Repository

    bash

git clone https://github.com/simplymuthoni/taskbite.git

cd taskbite

Set Up a Virtual Environment

bash

python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install Dependencies

bash

pip install -r requirements.txt

Create a .env File

Create a .env file in the root directory and add the following environment variables:

env

SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
MAIL_SENDER=your_email@example.com

Run Database Migrations

bash

flask db upgrade

Start the Flask Server

bash

    flask run

    The backend server will be running at http://localhost:8000.

Frontend Setup

    Clone the Repository

    bash

git clone https://github.com/simplymuthoni/taskbite.git

cd taskbite

Install Dependencies

bash

npm install

Start the React Native App

Ensure you have Expo CLI installed. Then, start the app with:

bash

    expo start

    The app will open in your default browser. You can scan the QR code with the Expo Go app on your mobile device to view the app.

API Documentation

API documentation for the Flask backend can be accessed at http://localhost:5000/apidocs. It provides details on available endpoints, request parameters, and response formats.
Example Endpoints

    Register: POST /api/auth/register
    Login: POST /api/auth/login
    View Dashboard: GET /api/dashboard
    View Note: GET /api/notes/<note_id>
    View To-Do: GET /api/todos/<todo_id>

Contributing

Contributions are welcome! Please follow these steps to contribute:

    Fork the repository.
    Create a feature branch: git checkout -b feature/your-feature.
    Commit your changes: git commit -am 'Add new feature'.
    Push to the branch: git push origin feature/your-feature.
    Open a Pull Request.

License

This project is licensed under the MIT License - see the LICENSE file for details.
