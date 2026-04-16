from datetime import datetime
from . import db

class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(50), nullable=True)
    icon = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    notes = db.relationship('Note', backref='subject', lazy=True, cascade="all, delete-orphan")

    @classmethod
    def create(cls, user_id, name, color=None, icon=None):
        subject = cls(user_id=user_id, name=name, color=color, icon=icon)
        db.session.add(subject)
        db.session.commit()
        return subject

    @classmethod
    def get_by_id(cls, subject_id):
        return cls.query.get(subject_id)

    @classmethod
    def get_all_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc()).all()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
