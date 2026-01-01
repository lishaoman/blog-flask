# backend/config.py
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # 安全密钥，生产环境需要保密并使用复杂随机字符串
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-this'

    # 数据库配置：使用当前目录下的 app.db SQLite 文件
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')

    # 关闭 SQLAlchemy 的事件追踪系统以节省开销
    SQLALCHEMY_TRACK_MODIFICATIONS = False