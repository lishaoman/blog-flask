// frontend/src/api/index.js
import axios from 'axios'

// 创建一个 axios 实例
const api = axios.create({
  // 后端服务的地址 (注意：如果你的后端端口不是 5000，请修改这里)
  // baseURL: 'http://127.0.0.1:5000',
  baseURL: '', // 使用相对路径，交给 Nginx 转发
  timeout: 5000, // 请求超时时间
  headers: {
    'Content-Type': 'application/json'
  }
})

// 可以在这里添加拦截器 (Interceptors)，比如统一处理错误，目前暂时不需要

export default api