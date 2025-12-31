#!/bin/bash

# Docker 部署脚本 - 垂直网站项目
echo "🚀 开始部署垂直网站项目..."

# 检查 Docker 和 Docker Compose 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

# 创建网络（如果不存在）
echo "📡 创建 Docker 网络..."
docker network create website_backend-net 2>/dev/null || echo "网络已存在"

# 停止并删除现有容器
echo "🛑 停止现有容器..."
docker-compose -f docker-compose.yml down 2>/dev/null || echo "无现有容器"

# 使用新的 docker-compose 文件启动服务
echo "🔄 使用新配置启动服务..."
docker-compose -f docker-compose.new.yml up -d --build

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "📊 检查服务状态..."
docker-compose -f docker-compose.new.yml ps

echo "✅ 部署完成！"
echo "🌐 前端访问地址: http://localhost:80"
echo "🔧 后端 API 访问地址: http://localhost:8000"
echo "🗄️  数据库连接: localhost:5432"
echo "🗂️  Redis 连接: localhost:6379"

# 显示日志命令
echo ""
echo "📝 查看日志命令:"
echo "  查看所有日志: docker-compose -f docker-compose.new.yml logs -f"
echo "  查看后端日志: docker-compose -f docker-compose.new.yml logs -f backend"
echo "  查看前端日志: docker-compose -f docker-compose.new.yml logs -f frontend"