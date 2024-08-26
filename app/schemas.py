"""
marshmallow_schemas.py

This module defines Marshmallow schemas for the User, Note, and ToDo models.

The schemas are used to serialize and deserialize data for these models.

Classes:
    UserSchema: Schema for the User model.
    NoteSchema: Schema for the Note model.
    ToDoSchema: Schema for the ToDo model.

Variables:
    user_schema: Instance of UserSchema for serializing a single user.
    users_schema: Instance of UserSchema for serializing multiple users.
    note_schema: Instance of NoteSchema for serializing a single note.
    notes_schema: Instance of NoteSchema for serializing multiple notes.
    todo_schema: Instance of ToDoSchema for serializing a single todo item.
    todos_schema: Instance of ToDoSchema for serializing multiple todo items.
"""
from marshmallow import Schema, fields

class UserSchema(Schema):
    """
    Schema for the User model.

    Attributes:
        id (str): Unique identifier for the user.
        username (str): Username chosen by the user.
        email (str): Email address of the user.
        name (str): Full name of the user.
        password (str): Password for the user (load_only).
        created_at (datetime): Timestamp when the user was created.
        updated_at (datetime): Timestamp when the user was last updated.
        email_verified (bool): Whether the user's email is verified.

    Example:
        {
            "id": "123",
            "username": "john_doe",
            "email": "john@example.com",
            "name": "John Doe",
            "password": "password123",
            "created_at": "2022-01-01T12:00:00",
            "updated_at": "2022-01-01T12:00:00",
            "email_verified": true
        }
    """
    id = fields.Str(required=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    password = fields.Str(load_only=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
    email_verified = fields.Boolean(required=True)

    class Meta:
        fields = ('id', 'username', 'email', 'name', 'password', 'created_at', 'updated_at', 'email_verified')

class NoteSchema(Schema):
    """
    Schema for the Note model.

    Attributes:
        id (str): Unique identifier for the note.
        content (str): Content of the note.
        created_at (datetime): Timestamp when the note was created.
        user_id (str): ID of the user who created the note.
        user (UserSchema): Nested user schema with id and username.

    Example:
        {
            "id": "123",
            "content": "This is a note",
            "created_at": "2022-01-01T12:00:00",
            "user_id": "123",
            "user": {
                "id": "123",
                "username": "john_doe"
            }
        }
    """
    id = fields.Str(required=True)
    content = fields.Str(required=True)
    created_at = fields.DateTime(required=True)
    user_id = fields.Str(required=True)
    user = fields.Nested(UserSchema, only=['id', 'username'])

    class Meta:
        fields = ('id', 'content', 'created_at', 'user_id', 'user')

class ToDoSchema(Schema):
    """
    Schema for the ToDo model.

    Attributes:
        id (str): Unique identifier for the todo item.
        task (str): Task description.
        priority (str): Priority level of the task.
        due_date (datetime): Due date for the task.
        user_id (str): ID of the user who created the todo item.
        user (UserSchema): Nested user schema with id and username.

    Example:
        {
            "id": "123",
            "task": "Buy milk",
            "priority": "high",
            "due_date": "2022-01-15T12:00:00",
            "user_id": "123",
            "user": {
                "id": "123",
                "username": "john_doe"
            }
        }
    """
    id = fields.Str(required=True)
    task = fields.Str(required=True)
    priority = fields.Str(required=True)
    due_date = fields.DateTime(required=True)
    user_id = fields.Str(required=True)
    user = fields.Nested(UserSchema, only=['id', 'username'])

    class Meta:
        fields = ('id', 'task', 'priority', 'due_date', 'user_id', 'user')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)
todo_schema = ToDoSchema()
todos_schema = ToDoSchema(many=True)
