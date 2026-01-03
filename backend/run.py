# backend/run.py
from app import create_app

# create_app() 返回的 Flask 实例
# Gunicorn 会使用这个 app 变量来启动服务
app = create_app()

if __name__ == '__main__':
    # 在开发环境运行时仍然使用 app.run()，方便本地调试
    # 生产环境则由 gunicorn 调用 app
    app.run(debug=True, port=5000)