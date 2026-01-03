# blog-project/frontend/Dockerfile

# 1. 构建阶段: 使用 Node.js 镜像构建 Vue 应用
FROM node:22-alpine as builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .
RUN npm run build

# 2. 运行阶段: 使用 Nginx 镜像托管静态文件
FROM nginx:alpine

# 移除默认的 Nginx 配置
RUN rm /etc/nginx/conf.d/default.conf

# 复制 Nginx 配置文件 (稍后创建)
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# 复制构建好的 Vue 静态文件到 Nginx 默认的静态文件目录
COPY --from=builder /app/dist /usr/share/nginx/html

# 暴露 Nginx 默认端口
EXPOSE 8080

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]