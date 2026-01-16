# 问题排查记录

## 问题：本地运行时前端 API 请求返回 HTML 而非 JSON

### 问题描述

- **症状**：博客首页一直显示"加载中..."，浏览器控制台报错：
  ```
  Uncaught (in promise) TypeError: Cannot read properties of undefined (reading 'substring')
  ```

- **环境差异**：
  - 使用 `docker-compose` 部署时：各页面功能正常
  - 本地启动 Flask 后端 + Vite 前端时：出现上述问题

- **API 响应异常**：获取博客列表接口返回的是 Vite 的 HTML 页面而非 JSON 数据：
  ```html
  <!doctype html>
  <html lang="en">
    <head>
      <script type="module" src="/@vite/client"></script>
      ...
    </head>
    <body>
      <div id="app"></div>
      ...
    </body>
  </html>
  ```

### 根本原因

| 部署方式 | 请求路径 | 响应来源 | 结果 |
|----------|----------|----------|------|
| Docker (Nginx) | Frontend → Nginx → Backend | 后端 Flask | ✅ 正确返回 JSON |
| 本地开发 | Frontend → Vite Dev Server | Vite 开发服务器 | ❌ 返回 Vite HTML |

**原因**：`frontend/src/api/index.js` 中使用相对路径 `baseURL: ''`，在 Nginx 环境下由 Nginx 进行转发，但本地运行时 Vite 开发服务器没有代理配置，导致 `/api/*` 请求被 Vite 自己拦截并返回了 index.html。

### 解决方案

在 `frontend/vite.config.js` 中添加 Vite 代理配置：

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',  // Flask 后端地址
        changeOrigin: true,
        // 如果 Flask 路由是 @app.route('/posts') 而非 @app.route('/api/posts')，
        // 需要取消下面注释来去掉 /api 前缀
        // rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
```

### 工作原理

配置后，Vite 开发服务器会将 `/api` 开头的请求自动转发到后端：

| 前端请求 | Vite 代理转发到 |
|----------|-----------------|
| `/api/posts` | `http://localhost:5000/api/posts` |
| `/api/posts/1` | `http://localhost:5000/api/posts/1` |

### 注意事项

1. **端口匹配**：确保 `target` 中的端口与 Flask 后端实际运行端口一致（默认 5000）
2. **路由前缀**：
   - Flask 使用 `@app.route('/api/posts')` → 不需要 `rewrite`
   - Flask 使用 `@app.route('/posts')` → 需要添加 `rewrite` 去掉 `/api` 前缀
3. **热重载**：修改 `vite.config.js` 后需要重启 Vite 开发服务器

---

*记录日期：2026-01-14*
