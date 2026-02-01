# backend/app/__init__.py
from flask import Flask
from config import Config
from app.extensions import db, migrate, cors

def create_app(config_class=Config):
    """
    应用工厂函数：负责创建并配置 Flask 应用实例
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 1. 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    # 配置 CORS，允许来自任意域名的 /api/* 请求 (开发环境方便，生产环境需限制)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    # 2. 注册蓝图 (路由)
    from app.routes.main import main_bp
    app.register_blueprint(main_bp, url_prefix='/api')

    # === 新增：注册文章蓝图 ===
    from app.routes.posts import posts_bp
    # 访问路径将是 /api/posts
    app.register_blueprint(posts_bp, url_prefix='/api/posts')

    # === 新增：注册分类蓝图 ===
    from app.routes.categories import categories_bp
    app.register_blueprint(categories_bp, url_prefix='/api/categories')

    # === 新增：注册标签蓝图 ===
    from app.routes.tags import tags_bp
    app.register_blueprint(tags_bp, url_prefix='/api/tags')

    # 3. 导入模型 (确保 Flask-Migrate 能识别到模型变化)
    from app import models

    return app