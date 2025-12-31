# 第一阶段：构建前端应用
FROM node:18.20.0-slim AS builder

# 设置工作目录
WORKDIR /app

# 安装构建工具
RUN apt-get update && apt-get install -y python3 make g++ git

# 设置npm配置，避免权限问题
RUN npm config set fund false && npm config set audit false

# 复制package.json和package-lock.json
COPY package*.json ./

# 安装所有依赖（包含开发依赖）- 阿里云CICD兼容方案
RUN npm install --production=false

# 复制所有源代码
COPY . .

# 构建生产版本
RUN npm run build

# 第二阶段：使用Nginx部署静态文件（生产环境）
FROM nginx:1.25.0-alpine

# 复制构建产物到Nginx静态目录
COPY --from=builder /app/dist /usr/share/nginx/html

# 暴露Nginx端口
EXPOSE 80

# 启动Nginx服务
CMD ["nginx", "-g", "daemon off;"]