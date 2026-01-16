# backend/app/models.py
from datetime import datetime
from app.extensions import db

# 1. 标签与文章的关联表 (多对多辅助表)
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id', name='fk_post_tags_post_id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id', name='fk_post_tags_tag_id'), primary_key=True)
)

# 2. 分类模型
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    # 反向关联：通过 category.posts 可以找到该分类下所有文章
    posts = db.relationship('Post', backref='category', lazy=True)

    def to_dict(self):
        return {'id': self.id, 'name': self.name}

# 3. 标签模型
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'name': self.name}

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False, default='')
    # 新增：外键关联分类 (一对多)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', name='fk_post_category_id'), nullable=True)
    # 新增：关联标签 (多对多)
    tags = db.relationship('Tag', secondary=post_tags, lazy='subquery', backref=db.backref('posts', lazy=True))
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
            # 序列化时带上分类名和标签列表
            'category': self.category.name if self.category else '未分类',
            'tags': [tag.name for tag in self.tags],
            'created_at': self.created_at.isoformat() + 'Z',
            'updated_at': self.updated_at.isoformat() + 'Z'
        }