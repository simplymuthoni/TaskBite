"""
This module defines routes for managing user notes and to-do tasks in the Flask application.

It includes endpoints for 
creating and deleting notes and to-dos, 
with JWT authentication required for all actions.

Routes:
    - POST /api/tasks/notes: Create a new note.
    - DELETE /api/tasks/notes/<string:note_id>: Delete a note by its ID.
    - POST /api/tasks/todos: Create a new to-do task.
    - DELETE /api/tasks/todos/<string:todo_id>: Delete a to-do task by its ID.

Authentication:
    All routes require JWT authentication.

Dependencies:
    - Flask
    - Flask-JWT-Extended
    - SQLAlchemy
    - app.models.Note
    - app.models.ToDo
    - app (for database session management)
"""
from datetime import datetime
from flask import Blueprint, request, jsonify, Flask
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Note, ToDo
from app import db

app = Flask(__name__)
# Create a Blueprint for notes and to-dos
tasks = Blueprint('tasks', __name__, url_prefix='/api/tasks')

@tasks.route('/notes', methods=['POST'])
@jwt_required()
def create_note():
    """
    Create a new note
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Note
          required:
            - content
          properties:
            content:
              type: string
    responses:
      201:
        description: Note created successfully
      400:
        description: Invalid input
    """
    data = request.get_json()
    content = data.get('content')

    if not content:
        return jsonify({"error": "Content is required"}), 400

    user_id = get_jwt_identity()
    note = Note(content=content, user_id=user_id)
    db.session.add(note)
    db.session.commit()

    return jsonify({"message": "Note created successfully", "note": content}), 201

@tasks.route('/notes/<string:note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    """
    Delete a note by its ID
    ---
    parameters:
      - name: note_id
        in: path
        type: string
        required: true
        description: The ID of the note to delete
    responses:
      200:
        description: Note deleted successfully
      404:
        description: Note not found
    """
    note = Note.query.get(note_id)
    if not note or note.user_id != get_jwt_identity():
        return jsonify({"error": "Note not found or unauthorized"}), 404

    db.session.delete(note)
    db.session.commit()

    return jsonify({"message": "Note deleted successfully"}), 200

@tasks.route('/todos', methods=['POST'])
@jwt_required()
def create_todo():
    """
    Create a new to-do task
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: ToDo
          required:
            - task
            - priority
            - due_date
          properties:
            task:
              type: string
            priority:
              type: string
              enum: [high, medium, low]
            due_date:
              type: string
              format: date-time
    responses:
      201:
        description: To-do created successfully
      400:
        description: Invalid input
    """
    data = request.get_json()
    task = data.get('task')
    priority = data.get('priority')
    due_date = data.get('due_date')

    if not all([task, priority, due_date]):
        return jsonify({"error": "Missing required fields"}), 400

    if priority not in ['high', 'medium', 'low']:
        return jsonify({"error": "Invalid priority value"}), 400

    user_id = get_jwt_identity()
    todo = ToDo(
        task=task,
        priority=priority,
        due_date=datetime.fromisoformat(due_date),
        user_id=user_id
    )
    db.session.add(todo)
    db.session.commit()

    return jsonify({"message": "To-do created successfully", "todo": task}), 201

@tasks.route('/todos/<string:todo_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(todo_id):
    """
    Delete a to-do task by its ID
    ---
    parameters:
      - name: todo_id
        in: path
        type: string
        required: true
        description: The ID of the to-do task to delete
    responses:
      200:
        description: To-do deleted successfully
      404:
        description: To-do not found
    """
    todo = ToDo.query.get(todo_id)
    if not todo or todo.user_id != get_jwt_identity():
        return jsonify({"error": "To-do not found or unauthorized"}), 404

    db.session.delete(todo)
    db.session.commit()

    return jsonify({"message": "To-do deleted successfully"}), 200

# Register Blueprint
app.register_blueprint(tasks)
