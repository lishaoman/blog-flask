# backend/app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# 初始化数据库 ORM
db = SQLAlchemy()
# 初始化数据库迁移工具
migrate = Migrate()
# 初始化跨域资源共享 (允许前端访问后端 API)
cors = CORS()