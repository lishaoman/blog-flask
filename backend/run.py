# backend/run.py
from app import create_app

app = create_app()

if __name__ == '__main__':
    # 开发模式下启动，开启调试功能
    app.run(debug=True, port=5000)