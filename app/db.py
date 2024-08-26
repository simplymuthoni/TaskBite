"""
Database module for the TaskBite app.

This module provides functions for interacting with the database.
"""
import os
import mariadb
from flask_sqlalchemy import SQLAlchemy
from mariadb import Error

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy()

def create_connection():
    """
    Creates a connection to the database.

    Returns:
        conn (mariadb.Connection): The connection object to the database.
    """
    conn = None
    try:
        conn = mariadb.connect(db)
    except Error as e:
        print(e)
    return conn

def create_tables():
    """
    Creates the tables in the database.

    Returns:
        None
    """
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS user(
                            id CHAR(36) PRIMARY KEY,
                            username VARCHAR(20) NOT NULL,
                            name VARCHAR(30) NOT NULL,
                            password VARCHAR(10) NOT NULL,
                            email VARCHAR(30) NOT NULL);''')

    conn.commit()
    cursor.close()
    conn.close()

def init_db():
    """
    Initializes the database by creating the tables.
    Returns:
        None
    """
create_tables()
