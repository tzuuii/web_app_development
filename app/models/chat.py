from datetime import datetime
from . import db

class ChatLog(db.Model):
    __tablename__ = 'chat_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'user' or 'ai'
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, user_id, role, content):
        chat_log = cls(user_id=user_id, role=role, content=content)
        db.session.add(chat_log)
        db.session.commit()
        return chat_log

    @classmethod
    def get_by_id(cls, chat_log_id):
        return cls.query.get(chat_log_id)

    @classmethod
    def get_history_by_user(cls, user_id, limit=50):
        # 取得最新的聊天記錄，並由舊到新排序
        logs = cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc()).limit(limit).all()
        return logs[::-1]

    def delete(self):
        db.session.delete(self)
        db.session.commit()
