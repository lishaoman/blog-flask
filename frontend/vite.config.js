import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    // === 新增配置开始 ===
    proxy: {
      '/api': {
        target: 'http://localhost:5000', // 这里填你本地 Flask 启动的地址和端口
        changeOrigin: true,
        // 如果你的 Flask 路由本身就包含 /api (例如 @app.route('/api/posts'))，则不需要 rewrite
        // 如果你的 Flask 路由是 @app.route('/posts')，则需要取消下面这行的注释来要把 /api 去掉
        // rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
    // === 新增配置结束 ===
  }
})
