# 母婴垂直网站迁移实施步骤

## 一、迁移前准备

### 1.1 检查现有服务状态
```bash
# 查看现有服务状态
docker-compose ps

# 检查数据库服务日志
docker-compose logs postgres
```

### 1.2 确认traefik-net网络
```bash
# 检查traefik-net网络是否存在
docker network ls | grep traefik-net
```

### 1.3 创建新数据目录
```bash
# 创建新数据目录
mkdir -p /home/ubuntu/docker/data/{postgres,redis,backend/static}

# 设置目录权限
chmod 755 /home/ubuntu/docker/data/{postgres,redis,backend/static}
```

## 二、数据库备份

### 2.1 PostgreSQL备份
```bash
# 执行PostgreSQL备份（使用正确的容器名称）
docker exec -it website_postgres pg_dump -U vertical_user -d vertical_website -f /tmp/backup.sql

# 验证备份文件
ls -lh /tmp/backup.sql
```

### 2.2 Redis备份
```bash
# 执行Redis后台保存（使用正确的容器名称）
docker exec -it website_redis redis-cli -a "Redis2024!@#$Secure" BGSAVE

# 复制Redis数据文件到宿主机（使用正确的容器名称）
docker cp website_redis:/data/dump.rdb /tmp/redis_dump.rdb

# 验证备份文件
ls -lh /tmp/redis_dump.rdb
```

## 三、启动新服务

### 3.1 启动新数据库服务
```bash
# 启动新的PostgreSQL和Redis服务
docker-compose -f docker-compose.new.yml up -d postgres redis

# 检查新服务状态
docker-compose -f docker-compose.new.yml ps
```

### 3.2 验证新数据库服务
```bash
# 验证PostgreSQL新服务
PG_CONTAINER_NEW=$(docker-compose -f docker-compose.new.yml ps -q postgres)
docker exec -it $PG_CONTAINER_NEW psql -U vertical_user -d vertical_website -c "SELECT version();"

# 验证Redis新服务
REDIS_CONTAINER_NEW=$(docker-compose -f docker-compose.new.yml ps -q redis)
docker exec -it $REDIS_CONTAINER_NEW redis-cli -a "Redis2024!@#$Secure" PING
```

## 四、数据恢复

### 4.1 PostgreSQL恢复
```bash
# 将备份文件复制到新PostgreSQL容器
PG_CONTAINER_NEW=$(docker-compose -f docker-compose.new.yml ps -q postgres)
docker cp /tmp/backup.sql $PG_CONTAINER_NEW:/tmp/backup.sql

# 执行恢复
docker exec -it $PG_CONTAINER_NEW psql -U vertical_user -d vertical_website -f /tmp/backup.sql
```

### 4.2 Redis恢复
```bash
# 停止新Redis服务
docker-compose -f docker-compose.new.yml stop redis

# 复制备份文件到新Redis容器
REDIS_CONTAINER_NEW=$(docker-compose -f docker-compose.new.yml ps -q redis)
docker cp /tmp/redis_dump.rdb $REDIS_CONTAINER_NEW:/data/dump.rdb

# 启动新Redis服务
docker-compose -f docker-compose.new.yml start redis
```

## 五、数据验证

### 5.1 PostgreSQL数据验证
```bash
# 检查表数量（使用正确的容器名称）
PG_CONTAINER="website_postgres"
PG_CONTAINER_NEW=$(docker-compose -f docker-compose.new.yml ps -q postgres)

echo "原数据库表数量："
docker exec -it $PG_CONTAINER psql -U vertical_user -d vertical_website -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';"

echo "新数据库表数量："
docker exec -it $PG_CONTAINER_NEW psql -U vertical_user -d vertical_website -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';"
```

### 5.2 Redis数据验证
```bash
# 检查键数量（使用正确的容器名称）
REDIS_CONTAINER="website_redis"
REDIS_CONTAINER_NEW=$(docker-compose -f docker-compose.new.yml ps -q redis)

echo "原Redis键数量："
docker exec -it $REDIS_CONTAINER redis-cli -a "Redis2024!@#$Secure" DBSIZE

echo "新Redis键数量："
docker exec -it $REDIS_CONTAINER_NEW redis-cli -a "Redis2024!@#$Secure" DBSIZE
```

## 六、启动完整新服务

### 6.1 启动后端和前端服务
```bash
# 启动新的后端和前端服务
docker-compose -f docker-compose.new.yml up -d backend frontend

# 检查所有新服务状态
docker-compose -f docker-compose.new.yml ps
```

### 6.2 验证新服务功能
```bash
# 验证后端API健康状态
curl http://localhost:8000/api/health

# 验证前端服务
curl http://localhost:80
```

## 七、切换生产流量

### 7.1 测试新服务
在正式切换前，建议进行充分的功能测试和性能测试。

### 7.2 正式切换
1. 更新DNS或负载均衡配置，将流量指向新服务（端口80）

2. 监控新服务：
```bash
# 监控后端服务日志
docker-compose -f docker-compose.new.yml logs -f backend

# 监控前端服务日志
docker-compose -f docker-compose.new.yml logs -f frontend
```

## 八、回滚方案

如果切换出现问题，可快速回滚到原服务：

1. 恢复DNS或负载均衡配置，将流量指向原服务（端口80）

2. 监控原服务：
```bash
docker-compose logs -f backend
```

## 九、清理和维护

在确认新服务稳定运行7天后，可以考虑清理原服务：

```bash
# 停止原服务
docker-compose down
```

**注意**：请在执行任何删除操作前，确保已完成所有数据验证并确认新服务正常运行。
