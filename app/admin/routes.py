"""
This module initializes a Flask application with user-related routes.
It supports retrieving all users and deleting a user by their ID.
Swagger is used for API documentation, and Flask-Session is configured
to manage user sessions.
"""

from flask import Flask, jsonify, Blueprint
from flasgger import Swagger
from flask_session import Session
from app import models, schemas, extensions

app = Flask(__name__)
swagger = Swagger(app)

# Initialize Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'supersecretkey'
Session(app)

db = extensions.db
User = models.User
UserSchema = schemas.UserSchema

users_blueprint = Blueprint('users', __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@users_blueprint.route('/users', methods=['GET'])
def get_users():
    """
    Get all users
    ---
    responses:
      200:
        description: A list of users
        schema:
          type: array
          items:
            $ref: '#/definitions/User'
    """
    users = User.query.all()
    users_dict_list = users_schema.dump(users)  # Use Marshmallow schema to serialize
    return jsonify(users_dict_list), 200

@users_blueprint.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete user
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: The user ID
    responses:
      200:
        description: User deleted successfully
      404:
        description: User not found
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
