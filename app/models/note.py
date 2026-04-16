import json
from datetime import datetime
from . import db

class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    
    original_content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    key_points = db.Column(db.Text, nullable=True)  # JSON encoded string
    keywords = db.Column(db.Text, nullable=True)    # JSON encoded string
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    quizzes = db.relationship('Quiz', backref='note', lazy=True, cascade="all, delete-orphan")

    def get_key_points_list(self):
        if self.key_points:
            try:
                return json.loads(self.key_points)
            except:
                return []
        return []

    def get_keywords_list(self):
        if self.keywords:
            try:
                return json.loads(self.keywords)
            except:
                return []
        return []

    @classmethod
    def create(cls, user_id, subject_id, original_content, summary, key_points=None, keywords=None):
        if isinstance(key_points, list):
            key_points = json.dumps(key_points)
        if isinstance(keywords, list):
            keywords = json.dumps(keywords)
            
        note = cls(
            user_id=user_id,
            subject_id=subject_id,
            original_content=original_content,
            summary=summary,
            key_points=key_points,
            keywords=keywords
        )
        db.session.add(note)
        db.session.commit()
        return note

    @classmethod
    def get_by_id(cls, note_id):
        return cls.query.get(note_id)

    @classmethod
    def get_all_by_subject(cls, subject_id):
        return cls.query.filter_by(subject_id=subject_id).order_by(cls.created_at.desc()).all()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                if key in ['key_points', 'keywords'] and isinstance(value, list):
                    setattr(self, key, json.dumps(value))
                else:
                    setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
