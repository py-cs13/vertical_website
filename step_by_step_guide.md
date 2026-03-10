# 母婴垂直网站部署与数据迁移分步指南

## 一、准备工作

### 1. 检查现有服务状态
```bash
# 查看现有服务状态
docker-compose ps

# 检查数据库服务健康
docker-compose logs postgres
docker-compose logs redis
```

### 2. 确认traefik-net网络
```bash
# 检查traefik-net网络是否存在
docker network ls | grep traefik-net
```

### 3. 创建新数据目录
```bash
# 创建新数据目录
mkdir -p /home/ubuntu/docker/data/{postgres,redis,backend/static}

# 设置目录权限
chmod 755 /home/ubuntu/docker/data/{postgres,redis,backend/static}
```

## 二、数据库备份

### 1. PostgreSQL备份
```bash
# 执行PostgreSQL数据库备份（使用正确的容器名称）
# 备份文件将保存到宿主机的/tmp目录
docker exec -it website_postgres pg_dump -U vertical_user -d vertical_website -f /tmp/backup.sql

# 验证备份文件
ls -lh /tmp/backup.sql
```

### 2. Redis备份
```bash
# 执行Redis后台保存（使用正确的容器名称）
docker exec -it website_redis redis-cli -a "Redis2024!@#$Secure" BGSAVE

# 等待备份完成（大约几秒钟）

# 复制Redis数据文件到宿主机
docker cp website_redis:/data/dump.rdb /tmp/redis_dump.rdb

# 验证备份文件
ls -lh /tmp/redis_dump.rdb
```

## 三、启动新的数据库服务

### 1. 启动新PostgreSQL和Redis服务
```bash
# 使用新的Docker Compose文件启动数据库服务
docker-compose -f docker-compose.new.yml up -d postgres redis

# 检查新服务状态（等待服务变为healthy状态）
docker-compose -f docker-compose.new.yml ps
```

### 2. 验证新数据库服务
```bash
# 验证PostgreSQL新服务
PG_CONTAINER_NEW=$(docker-compose -f docker-compose.new.yml ps -q postgres)
docker exec -it $PG_CONTAINER_NEW psql -U vertical_user -d vertical_website -c "SELECT version();"

# 验证Redis新服务
REDIS_CONTAINER_NEW=$(docker-compose -f docker-compose.new.yml ps -q redis)
docker exec -it $REDIS_CONTAINER_NEW redis-cli -a "Redis2024!@#$Secure" PING
```

## 四、数据恢复

### 1. PostgreSQL数据恢复
```bash
# 将备份文件复制到新PostgreSQL容器
PG_CONTAINER_NEW=$(docker-compose -f docker-compose.new.yml ps -q postgres)
docker cp /tmp/backup.sql $PG_CONTAINER_NEW:/tmp/backup.sql

# 执行恢复操作
docker exec -it $PG_CONTAINER_NEW psql -U vertical_user -d vertical_website -f /tmp/backup.sql
```

### 2. Redis数据恢复
```bash
# 停止新Redis服务
docker-compose -f docker-compose.new.yml stop redis

# 将备份文件复制到新Redis容器
REDIS_CONTAINER_NEW=$(docker-compose -f docker-compose.new.yml ps -q redis)
docker cp /tmp/redis_dump.rdb $REDIS_CONTAINER_NEW:/data/dump.rdb

# 启动新Redis服务
docker-compose -f docker-compose.new.yml start redis
```

## 五、数据验证

### 1. PostgreSQL数据验证
```bash
# 验证表数量是否一致
PG_CONTAINER="website_postgres"  # 原容器名称
PG_CONTAINER_NEW=$(docker-compose -f docker-compose.new.yml ps -q postgres)

echo "原数据库表数量："
docker exec -it $PG_CONTAINER psql -U vertical_user -d vertical_website -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';"

echo "新数据库表数量："
docker exec -it $PG_CONTAINER_NEW psql -U vertical_user -d vertical_website -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';"

# 检查关键表数据量（以users表为例）
TABLE_NAME="users"
echo "原数据库$TABLE_NAME表数据量："
docker exec -it $PG_CONTAINER psql -U vertical_user -d vertical_website -c "SELECT COUNT(*) FROM $TABLE_NAME;"

echo "新数据库$TABLE_NAME表数据量："
docker exec -it $PG_CONTAINER_NEW psql -U vertical_user -d vertical_website -c "SELECT COUNT(*) FROM $TABLE_NAME;"
```

### 2. Redis数据验证
```bash
# 验证键数量是否一致
REDIS_CONTAINER="website_redis"  # 原容器名称
REDIS_CONTAINER_NEW=$(docker-compose -f docker-compose.new.yml ps -q redis)

echo "原Redis键数量："
docker exec -it $REDIS_CONTAINER redis-cli -a "Redis2024!@#$Secure" DBSIZE

echo "新Redis键数量："
docker exec -it $REDIS_CONTAINER_NEW redis-cli -a "Redis2024!@#$Secure" DBSIZE
```

## 六、启动完整新服务

### 1. 启动后端和前端服务
```bash
# 启动新的后端和前端服务
docker-compose -f docker-compose.new.yml up -d backend frontend

# 检查所有新服务状态
docker-compose -f docker-compose.new.yml ps
```

### 2. 验证新服务功能
```bash
# 验证后端API健康状态
curl http://localhost:8000/api/health

# 验证前端服务
curl http://localhost:80
```

## 七、切换生产流量

### 1. 更新DNS/负载均衡
将您的域名指向新的前端服务（端口80），或更新负载均衡配置。

### 2. 监控新服务
```bash
# 监控后端服务日志
docker-compose -f docker-compose.new.yml logs -f backend

# 监控前端服务日志
docker-compose -f docker-compose.new.yml logs -f frontend
```

## 八、回滚方案

如果切换过程中出现问题，可以快速回滚到原服务：

1. **恢复DNS/负载均衡**：将流量指向原服务（端口80）

2. **验证原服务**：
```bash
# 检查原服务状态
docker-compose ps

# 检查原服务健康
docker-compose logs backend
```

## 九、清理和维护

在确认新服务稳定运行7天后，可以考虑停止并清理原服务：

```bash
# 停止原服务
docker-compose down
```

**注意**：请在执行任何删除操作前，确保已完成所有数据验证并确认新服务正常运行。

## 十、重要提示

1. 请确保在执行任何操作前备份所有重要数据
2. 在生产环境切换前，请进行充分的测试
3. 请确保您对Docker和数据库操作有一定的了解
4. 如果遇到任何问题，请参考相关日志信息

---

**文档版本**：1.0  
**创建日期**：2026年1月9日  
**作者**：Trae AI Assistant