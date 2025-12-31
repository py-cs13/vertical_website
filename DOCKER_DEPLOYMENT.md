# Docker 部署指南 - 垂直网站项目

## 📋 项目概述

本项目是一个面向母婴群体的垂直网站，包含以下组件：
- **前端**: Vue 3 + Vite + Nginx
- **后端**: FastAPI + Python + PostgreSQL + Redis
- **数据库**: PostgreSQL 15
- **缓存**: Redis 7

## 🚀 快速部署

### 1. 使用部署脚本（推荐）

```bash
# 给部署脚本执行权限（如果还没有）
chmod +x docker-up.sh

# 运行部署脚本
./docker-up.sh
```

### 2. 手动部署

```bash
# 创建 Docker 网络
docker network create website_backend-net

# 构建并启动所有服务
docker compose up -d --build

# 查看服务状态
docker compose ps

# 查看日志
docker compose logs -f
```

## 📁 新的文件结构

```
vertical_website/
├── frontend/
│   ├── Dockerfile.new          # 新的前端Dockerfile
│   ├── nginx.conf              # Nginx配置
│   └── Dockerfile              # 已更新（备份：Dockerfile.backup）
├── backend/
│   ├── Dockerfile.new          # 新的后端Dockerfile
│   └── Dockerfile              # 已更新（备份：Dockerfile.backup）
├── docker-compose.new.yml      # 新的Docker Compose配置
├── docker-compose.yml          # 已更新（备份：docker-compose.yml.backup）
├── docker-up.sh                # 部署脚本
└── DOCKER_DEPLOYMENT.md        # 本文档
```

## 🔧 新Dockerfile特性

### 前端 Dockerfile.new 改进
- ✅ 使用多阶段构建减小镜像大小
- ✅ 使用 Alpine Linux 基础镜像
- ✅ 包含完整的 Nginx 配置
- ✅ 支持 API 代理到后端
- ✅ 静态资源缓存优化
- ✅ Gzip 压缩配置

### 后端 Dockerfile.new 改进
- ✅ 多阶段构建
- ✅ 安全用户创建（非root用户）
- ✅ 健康检查配置
- ✅ 优化的Python依赖安装
- ✅ 正确的环境变量设置
- ✅ 系统依赖优化安装

## 🌐 访问地址

部署完成后，可通过以下地址访问：

- **前端应用**: http://localhost:80
- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs
- **数据库**: localhost:5432
- **Redis**: localhost:6379

## 📊 服务监控

```bash
# 查看所有服务状态
docker compose ps

# 查看服务日志
docker compose logs -f [service_name]

# 实时监控服务
docker compose logs -f

# 重启特定服务
docker compose restart [service_name]

# 停止所有服务
docker compose down

# 完全清理（包括数据卷）
docker compose down -v
```

## 🔍 故障排除

### 1. 构建失败
```bash
# 清理 Docker 缓存
docker system prune -a

# 重新构建特定服务
docker compose build --no-cache [service_name]
```

### 2. 端口冲突
如果80端口被占用，修改 `docker-compose.yml` 中的端口映射：
```yaml
frontend:
  ports:
    - "8080:80"  # 使用8080端口代替80
```

### 3. 数据库连接问题
检查环境变量和数据库服务状态：
```bash
# 检查数据库连接
docker compose exec postgres psql -U vertical_user -d vertical_website

# 查看数据库日志
docker compose logs postgres
```

### 4. 权限问题
```bash
# 修复文件权限
sudo chown -R $USER:$USER .

# 给脚本执行权限
chmod +x docker-up.sh
```

## 🔒 生产环境配置

### 环境变量设置
在生产环境中，请修改以下环境变量：

```bash
# 修改 docker-compose.yml 中的环境变量
SECRET_KEY=your_very_secure_secret_key_here
POSTGRES_PASSWORD=your_secure_database_password
REDIS_PASSWORD=your_secure_redis_password
```

### SSL/TLS 配置
生产环境建议配置 HTTPS：
1. 使用 Nginx 配置 SSL 证书
2. 或使用 Traefik 等反向代理

### 数据备份
```bash
# 备份 PostgreSQL 数据
docker compose exec postgres pg_dump -U vertical_user vertical_website > backup.sql

# 恢复 PostgreSQL 数据
docker compose exec -T postgres psql -U vertical_user vertical_website < backup.sql
```

## 📈 性能优化

### 前端优化
- ✅ 静态资源缓存
- ✅ Gzip 压缩
- ✅ 代码分割（Vite 自动处理）

### 后端优化
- ✅ 连接池配置
- ✅ Redis 缓存
- ✅ 健康检查

### 数据库优化
- ✅ PostgreSQL 配置优化
- ✅ 索引优化
- ✅ 连接池设置

## 🛡️ 安全配置

### 1. 网络安全
- 使用 Docker 网络隔离
- 只暴露必要的端口

### 2. 镜像安全
- 使用非 root 用户运行
- 最小化镜像大小
- 定期更新基础镜像

### 3. 密钥管理
- 使用环境变量管理敏感信息
- 避免在代码中硬编码密钥

## 📞 技术支持

如果遇到问题，请检查：
1. Docker 和 Docker Compose 版本
2. 系统资源（内存、磁盘空间）
3. 端口占用情况
4. 服务日志输出

## 🎯 下一步

部署成功后，可以：
1. 测试所有功能模块
2. 配置域名和SSL证书
3. 设置监控和日志收集
4. 配置自动化部署

---

**注意**: 首次部署可能需要几分钟时间下载镜像和构建服务，请耐心等待。