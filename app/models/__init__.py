from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Ensure all models are imported here so Flask-SQLAlchemy can detect them
# They must be imported after db is defined to avoid circular imports.
from .user import User
from .subject import Subject
from .note import Note
from .quiz import Quiz, Question
from .answer import Answer
from .chat import ChatLog
