from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Enum
from flask import flash
from sqlalchemy.types import DateTime as TimezoneAwareDateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
import uuid

class User(db.Model):
    """
    Represents a user in the database.

    Attributes:
        id (str): Unique identifier for the user (UUID).
        username (str): Username chosen by the user.
        email (str): Email address of the user.
        name (str): Full name of the user.
        password (str): Hashed password for the user.
        created_at (datetime): Timestamp when the user was created.
        updated_at (datetime): Timestamp when the user was last updated.

    Examples:
        >>> user = User(username='john_doe', email='john@example.com', name='John Doe')
        >>> user.password = generate_password_hash('mysecretpassword')
        >>> db.session.add(user)
        >>> db.session.commit()
    """

    __tablename__ = 'user'
    
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    email_verified = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        """
        Returns a string representation of the user.

        Returns:
            str: A string in the format '<User username>'.
        """
        return f'<User {self.username}>'