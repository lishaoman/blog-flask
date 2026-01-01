# backend/app/models.py
from datetime import datetime
from app.extensions import db

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # 自动记录创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # 自动记录更新时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Post {self.title}>'

    # 辅助方法：将模型对象转换为字典，方便 API 返回 JSON 数据
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat() + 'Z',
            'updated_at': self.updated_at.isoformat() + 'Z'
        }