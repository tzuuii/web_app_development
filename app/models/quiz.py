import json
from datetime import datetime
from . import db

class Quiz(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    note_id = db.Column(db.Integer, db.ForeignKey('notes.id'), nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)  # easy, medium, hard
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade="all, delete-orphan")
    answers = db.relationship('Answer', backref='quiz', lazy=True, cascade="all, delete-orphan")

    @classmethod
    def create(cls, user_id, note_id, total_questions, difficulty):
        quiz = cls(user_id=user_id, note_id=note_id, total_questions=total_questions, difficulty=difficulty)
        db.session.add(quiz)
        db.session.commit()
        return quiz

    @classmethod
    def get_by_id(cls, quiz_id):
        return cls.query.get(quiz_id)

    @classmethod
    def get_all_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc()).all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    options = db.Column(db.Text, nullable=True)  # JSON encoded list for multiple choice
    correct_answer = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    answers = db.relationship('Answer', backref='question', lazy=True, cascade="all, delete-orphan")

    def get_options_list(self):
        if self.options:
            try:
                return json.loads(self.options)
            except:
                return []
        return []

    @classmethod
    def create(cls, quiz_id, question_text, correct_answer, options=None, explanation=None):
        if isinstance(options, list):
            options = json.dumps(options)
            
        question = cls(
            quiz_id=quiz_id,
            question_text=question_text,
            correct_answer=correct_answer,
            options=options,
            explanation=explanation
        )
        db.session.add(question)
        db.session.commit()
        return question

    @classmethod
    def get_by_id(cls, question_id):
        return cls.query.get(question_id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
