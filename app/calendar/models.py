from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from app.extensions import db
from sqlalchemy import Column, Integer, String, Enum
from flask import flash
from sqlalchemy.types import DateTime as TimezoneAwareDateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
import uuid

# Example models for Note and ToDo
class Note(db.Model):

    __tablename__ = 'note'
    
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    content = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class ToDo(db.Model):

    __tablename__ ='todo'

    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    task = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)