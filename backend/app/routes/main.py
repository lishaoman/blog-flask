# backend/app/routes/main.py
from flask import Blueprint, jsonify

# 创建一个名为 'main' 的蓝图
main_bp = Blueprint('main', __name__)

@main_bp.route('/ping', methods=['GET'])
def ping():
    """
    健康检查接口，用于测试后端是否正常运行
    """
    return jsonify({
        'status': 'success',
        'message': 'Pong! Backend is running successfully.'
    })