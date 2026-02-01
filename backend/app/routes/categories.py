# backend/app/routes/categories.py
from flask import Blueprint, jsonify

from app.extensions import db
from app.models import Category, Post

categories_bp = Blueprint('categories', __name__)


@categories_bp.route('/', methods=['GET'])
def get_categories():
    """
    获取所有分类，每个分类带文章数量统计
    """
    # 使用 SQLAlchemy 的 func.count 来统计每个分类下的文章数量
    from sqlalchemy import func

    # 查询所有分类及其文章数量
    categories_with_count = db.session.query(
        Category.id,
        Category.name,
        func.count(Post.id).label('post_count')
    ).outerjoin(
        Post, Category.id == Post.category_id
    ).group_by(
        Category.id, Category.name
    ).all()

    # 转换为字典列表
    result = [
        {
            'id': cat.id,
            'name': cat.name,
            'post_count': cat.post_count or 0
        }
        for cat in categories_with_count
    ]

    return jsonify(result)


@categories_bp.route('/<int:category_id>', methods=['GET'])
def get_category_by_id(category_id):
    """
    根据ID获取分类详情
    """
    category = Category.query.get_or_404(category_id)
    return jsonify(category.to_dict())


@categories_bp.route('/<int:category_id>/posts', methods=['GET'])
def get_posts_by_category(category_id):
    """
    获取指定分类下的所有文章
    """
    # 验证分类存在
    category = Category.query.get_or_404(category_id)

    # 查询该分类下的所有文章
    posts = Post.query.filter_by(category_id=category_id).order_by(Post.created_at.desc()).all()

    return jsonify({
        'category': category.to_dict(),
        'posts': [post.to_dict() for post in posts]
    })
