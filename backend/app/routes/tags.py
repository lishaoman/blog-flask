# backend/app/routes/tags.py
from flask import Blueprint, jsonify

from app.extensions import db
from app.models import Tag, Post, post_tags

tags_bp = Blueprint('tags', __name__)


@tags_bp.route('/', methods=['GET'])
def get_tags():
    """
    获取所有标签，每个标签带文章数量统计
    """
    from sqlalchemy import func

    # 查询所有标签及其文章数量
    tags_with_count = db.session.query(
        Tag.id,
        Tag.name,
        func.count(Post.id).label('post_count')
    ).join(
        post_tags, Tag.id == post_tags.c.tag_id
    ).join(
        Post, post_tags.c.post_id == Post.id
    ).group_by(
        Tag.id, Tag.name
    ).all()

    # 转换为字典列表
    result = [
        {
            'id': tag.id,
            'name': tag.name,
            'post_count': tag.post_count or 0
        }
        for tag in tags_with_count
    ]

    return jsonify(result)


@tags_bp.route('/<int:tag_id>', methods=['GET'])
def get_tag_by_id(tag_id):
    """
    根据ID获取标签详情
    """
    tag = Tag.query.get_or_404(tag_id)
    return jsonify(tag.to_dict())


@tags_bp.route('/<int:tag_id>/posts', methods=['GET'])
def get_posts_by_tag(tag_id):
    """
    获取指定标签下的所有文章
    """
    # 验证标签存在
    tag = Tag.query.get_or_404(tag_id)

    # 查询拥有该标签的所有文章
    posts = Post.query.filter(Post.tags.any(id=tag_id)).order_by(Post.created_at.desc()).all()

    return jsonify({
        'tag': tag.to_dict(),
        'posts': [post.to_dict() for post in posts]
    })
