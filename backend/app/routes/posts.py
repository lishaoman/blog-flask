# backend/app/routes/posts.py
from flask import Blueprint, request, jsonify
from sqlalchemy import or_

from app.extensions import db
from app.models import Post, Category, Tag

# 创建一个名为 'posts' 的蓝图
posts_bp = Blueprint('posts', __name__)


# 1. 创建文章 API
@posts_bp.route('/', methods=['POST'])
def create_post():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    # 获取前端传来的分类名和标签数组
    category_name = data.get('category', '').strip()  # 例如 "技术"
    tag_names = data.get('tags', [])  # 例如 ["Python", "Vue"]

    # 简单的验证
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({'error': 'Title and content are required'}), 400

    # 1. 处理分类 (如果存在则获取，不存在则创建)
    category = None
    if category_name:
        category = Category.query.filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            db.session.add(category)

    # 2. 处理标签 (如果存在则获取，不存在则创建)
    tags_objects = []
    for name in tag_names:
        name = name.strip()
        if name:
            tag = Tag.query.filter_by(name=name).first()
            if not tag:
                tag = Tag(name=name)
                db.session.add(tag)
            tags_objects.append(tag)

    # 3. 创建文章并关联
    new_post = Post(title=data['title'], content=data['content'], category=category, tags=tags_objects)

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


@posts_bp.route('/search', methods=['GET'])
def search_posts():
    # 1. 获取前端传来的搜索关键词
    query_str = request.args.get('q', '').strip()

    if not query_str:
        return jsonify([])  # 如果关键词为空，直接返回空列表

    # 2. 执行全文搜索逻辑 (标题或内容中包含关键词)
    # 使用 or_ 实现多字段搜索，contains 实现模糊匹配
    results = Post.query.filter(
        or_(
            Post.title.contains(query_str),
            Post.content.contains(query_str)
        )
    ).order_by(Post.created_at.desc()).all()

    # 3. 序列化并返回
    # 这里的 to_dict() 是你之前模型中定义的方法
    return jsonify([post.to_dict() for post in results])