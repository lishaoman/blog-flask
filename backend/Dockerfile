# blog-project/backend/Dockerfile

# 使用官方的 Python 镜像作为基础
FROM python:3.9-slim-buster

# 设置工作目录
WORKDIR /app

# 复制依赖文件，并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制整个应用代码
COPY . .

# 暴露端口 (Gunicorn 默认端口)
EXPOSE 5000

# 启动 Gunicorn 服务器，绑定所有网络接口的 5000 端口
# Gunicorn 是生产环境下运行 Flask 的推荐方式，它是一个 WSGI HTTP Server
# -w N 表示启动 N 个 worker 进程
# app:app 表示在 app 模块中找到 app 变量（即 create_app() 返回的 Flask 实例）
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "run:app"]