# backend/app/routes/posts.py
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Post

# 创建一个名为 'posts' 的蓝图
posts_bp = Blueprint('posts', __name__)


# 1. 创建文章 API
@posts_bp.route('/', methods=['POST'])
def create_post():
    data = request.get_json()

    # 简单的验证
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({'error': 'Title and content are required'}), 400

    new_post = Post(title=data['title'], content=data['content'])

    # 保存到数据库
    db.session.add(new_post)
    db.session.commit()

    return jsonify(new_post.to_dict()), 201


# 2. 获取文章列表 API
@posts_bp.route('/', methods=['GET'])
def get_posts():
    # 查询所有文章，按创建时间倒序排列 (最新的在最前)
    posts = Post.query.order_by(Post.created_at.desc()).all()

    # 将对象列表转换为字典列表
    return jsonify([post.to_dict() for post in posts])


# 3. 获取单篇文章详情 API
@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    # 根据 ID 查找，如果找不到返回 404
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())


# 4. 更新文章 API (Update)
@posts_bp.route('/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # 更新字段，如果没传则保持原样
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)

    db.session.commit()
    return jsonify(post.to_dict())


# 5. 删除文章 API (Delete)
@posts_bp.route('/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return jsonify({'message': 'Post deleted successfully'})