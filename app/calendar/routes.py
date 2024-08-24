from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Note, ToDo
from models import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

calendar = Blueprint('calendar', __name__)

@calendar.route('/events', methods=['GET'])
@jwt_required()
def get_events():
    user_id = get_jwt_identity()
    notes = Note.query.filter_by(user_id=user_id).all()
    todos = ToDo.query.filter_by(user_id=user_id).all()

    events = []

    for note in notes:
        events.append({
            'title': note.content,
            'start': note.created_at.strftime('%Y-%m-%d'),
            'end': note.created_at.strftime('%Y-%m-%d'),
            'type': 'note'
        })

    for todo in todos:
        events.append({
            'title': todo.task,
            'start': todo.due_date.strftime('%Y-%m-%d'),
            'end': todo.due_date.strftime('%Y-%m-%d'),
            'type': 'todo'
        })

    return jsonify(events), 200

@calendar.route('/events', methods=['POST'])
@jwt_required()
def add_event():
    data = request.get_json()
    event_type = data.get('type')
    user_id = get_jwt_identity()

    if event_type == 'note':
        new_note = Note(content=data.get('content'), user_id=user_id)
        db.session.add(new_note)
    elif event_type == 'todo':
        new_todo = ToDo(task=data.get('task'), due_date=data.get('due_date'), user_id=user_id)
        db.session.add(new_todo)
    
    db.session.commit()
    return jsonify({"message": "Event added successfully"}), 201

@calendar.route('/events', methods=['POST'])
@jwt_required()
def add_event():
    """
    Adds a new event (note or todo) to the database.

    Expected JSON:
    {
        "type": "note" or "todo",
        "content": "Event content",
        "due_date": "2024-08-23"
    }
    """
    data = request.get_json()
    event_type = data.get('type')
    user_id = get_jwt_identity()

    if event_type == 'note':
        new_note = Note(content=data.get('content'), created_at=datetime.datetime.now(), user_id=user_id)
        db.session.add(new_note)
    elif event_type == 'todo':
        due_date = datetime.datetime.strptime(data.get('due_date'), '%Y-%m-%d')
        new_todo = ToDo(task=data.get('content'), due_date=due_date, user_id=user_id)
        db.session.add(new_todo)
    else:
        return jsonify({"message": "Invalid event type"}), 400

    db.session.commit()
    return jsonify({"message": "Event added successfully"}), 201