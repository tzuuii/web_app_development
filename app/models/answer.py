from datetime import datetime
from . import db

class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    
    user_answer = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    topic = db.Column(db.String(100), nullable=False)  # 知識點標籤，用於弱點分析
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, user_id, quiz_id, question_id, user_answer, is_correct, topic):
        answer = cls(
            user_id=user_id,
            quiz_id=quiz_id,
            question_id=question_id,
            user_answer=user_answer,
            is_correct=is_correct,
            topic=topic
        )
        db.session.add(answer)
        db.session.commit()
        return answer

    @classmethod
    def get_by_id(cls, answer_id):
        return cls.query.get(answer_id)

    @classmethod
    def get_all_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc()).all()

    @classmethod
    def get_by_quiz(cls, quiz_id):
        return cls.query.filter_by(quiz_id=quiz_id).all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
