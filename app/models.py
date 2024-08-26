"""
This module defines the database models for the application, including:

1. User: Represents a user in the system.
2. Note: Represents a note created by a user.
3. ToDo: Represents a to-do task created by a user.

Each model includes attributes that map to the columns in the respective database table, 
as well as methods to perform common operations like password hashing and checking.

Usage:
    This module should be imported wherever the models need to be accessed or manipulated.

    Example:
        from your_application.models import User, Note, ToDo

        user = User(username='john_doe', email='john@example.com', name='John Doe')
        user.set_password('mysecretpassword')
        db.session.add(user)
        db.session.commit()

Author: Mugo Patricia
Date: 24th August 2024
"""

from datetime import datetime
import uuid
from sqlalchemy import Enum, DateTime, Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db

Base = declarative_base()

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
        email_verified (bool): Whether the user's email has been verified.

    Examples:
        >>> user = User(username='john_doe', email='john@example.com', name='John Doe')
        >>> user.password = generate_password_hash('mysecretpassword')
        >>> db.session.add(user)
        >>> db.session.commit()
    """

    __tablename__ = 'user'

    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    name = Column(String(30), nullable=False)
    password = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    email_verified = Column(Boolean, default=False)

    def __repr__(self):
        """
        Returns a string representation of the user.

        Returns:
            str: A string in the format '<User username>'.
        """
        return f'<User {self.username}>'

    def set_password(self, password: str) -> None:
        """
        Sets the user's password.

        Args:
            password (str): The new password for the user.
        """
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Checks if the provided password matches the user's password.

        Args:
            password (str): The password to check.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password, password)


class Note(db.Model):
    """
    Represents a note created by a user.

    Attributes:
        id (str): Unique identifier for the note (UUID).
        content (str): The text content of the note.
        created_at (datetime): Timestamp when the note was created.
        user_id (str): Foreign key referencing the user who created the note.
        user (User): The user who created the note.

    Example:
        >>> note = Note(content="Hello, world!", user_id=1)
        >>> db.session.add(note)
        >>> db.session.commit()
    """

    __tablename__ = 'note'

    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
    content = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String(36), ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref='notes')

    def __repr__(self):
        """
        Returns a string representation of the note.

        Returns:
            str: A string in the format '<Note content>'.
        """
        return f'<Note {self.content}>'


class ToDo(db.Model):
    """
    Represents a to-do task created by a user.

    Attributes:
        id (str): Unique identifier for the to-do task (UUID).
        task (str): The text description of the task.
        priority (Enum): The priority of the task (high, medium, low).
        due_date (datetime): Timestamp when the task is due.
        user_id (str): Foreign key referencing the user who created the task.
        user (User): The user who created the task.

    Example:
        >>> todo = ToDo(task="Buy milk", priority="high", due_date=datetime(2023, 3, 15), user_id=1)
        >>> db.session.add(todo)
        >>> db.session.commit()
    """

    __tablename__ = 'todo'

    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
    task = Column(String(100), nullable=False)
    priority = Column(Enum('high', 'medium', 'low'), nullable=False)
    due_date = Column(DateTime, nullable=False)
    user_id = Column(String(36), ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref='todos')

    def __repr__(self):
        """
        Returns a string representation of the to-do task.

        Returns:
            str: A string in the format '<ToDo task>'.
        """
        return f'<ToDo {self.task}>'

engine = create_engine('mariadb+mariadbconnector://mugo:Demo123@localhost/taskbite')

Base.metadata.create_all(engine)
