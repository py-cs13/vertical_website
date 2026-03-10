# 母婴垂直网站数据库迁移方案

## 一、概述

本方案旨在将现有的PostgreSQL和Redis数据库数据迁移到使用traefik-net网络的新数据库服务中。迁移过程将确保数据的完整性和一致性，同时最小化服务中断时间。

## 二、迁移准备

### 2.1 环境检查

1. **确认现有服务状态**：
   ```bash
   # 查看现有服务状态
   docker-compose ps
   
   # 确认数据库服务健康
   docker-compose logs postgres
   docker-compose logs redis
   ```

2. **确认新服务环境**：
   ```bash
   # 检查traefik-net网络是否存在
   docker network ls | grep traefik-net
   
   # 如果不存在，创建网络（如果有必要）
   # docker network create traefik-net
   ```

3. **创建新数据目录**：
   ```bash
   # 创建新数据目录
   mkdir -p /home/ubuntu/docker/data/{postgres,redis,backend/static}
   
   # 设置目录权限
   chmod 755 /home/ubuntu/docker/data/{postgres,redis,backend/static}
   ```

## 三、数据库备份

### 3.1 PostgreSQL备份

**方法1：直接通过容器执行备份**

```bash
# 执行PostgreSQL数据库备份（使用正确的容器名称）
# 备份文件将保存到宿主机的/tmp目录

docker exec -it website_postgres pg_dump -U vertical_user -d vertical_website -f /tmp/backup.sql

# 验证备份文件
ls -lh /tmp/backup.sql
```

**方法2：如果无法直接执行，通过SFTP下载配置文件后操作**

如果您只能通过SFTP访问服务器，可以：
1. 先下载现有docker-compose.yml文件
2. 在本地使用相同的网络配置启动临时容器进行备份

### 3.2 Redis备份

**方法1：直接通过容器执行备份**

```bash
# 执行Redis后台保存（使用正确的容器名称）
# 这将在Redis数据目录中创建dump.rdb文件
docker exec -it website_redis redis-cli -a "Redis2024!@#$Secure" BGSAVE

# 等待备份完成
# 检查备份状态
docker exec -it website_redis redis-cli -a "Redis2024!@#$Secure" LASTSAVE
```

**方法2：直接复制Redis数据文件**

```bash
# 复制Redis数据文件到宿主机（使用正确的容器名称）
# 直接使用容器名称复制dump.rdb文件到宿主机/tmp目录
docker cp website_redis:/data/dump.rdb /tmp/redis_dump.rdb

# 验证备份文件
ls -lh /tmp/redis_dump.rdb
```

## 四、启动新服务

### 4.1 启动新的数据库服务

```bash
# 启动新的数据库服务（仅postgres和redis）
docker-compose -f docker-compose.new.yml up -d postgres redis

# 检查新服务状态
# 等待服务变为healthy状态
docker-compose -f docker-compose.new.yml ps
```

### 4.2 验证新数据库服务

```bash
# 验证PostgreSQL新服务
PG_CONTAINER_NEW=$(docker-compose -f docker-compose.new.yml ps -q postgres)
docker exec -it $PG_CONTAINER_NEW psql -U vertical_user -d vertical_website -c "SELECT version();"

# 验证Redis新服务
REDIS_CONTAINER_NEW=$(docker-compose -f docker-compose.new.yml ps -q redis)
docker exec -it $REDIS_CONTAINER_NEW redis-cli -a "Redis2024!@#$Secure" PING
```

## 五、数据库恢复

### 5.1 PostgreSQL恢复

**方法1：通过docker-compose执行恢复**

```bash
# 将备份文件复制到新的PostgreSQL容器
PG_CONTAINER_NEW=$(docker-compose -f docker-compose.new.yml ps -q postgres)
docker cp /tmp/backup.sql $PG_CONTAINER_NEW:/tmp/backup.sql

# 执行恢复操作
docker exec -it $PG_CONTAINER_NEW psql -U vertical_user -d vertical_website -f /tmp/backup.sql
```

**方法2：通过本地连接执行恢复**

```bash
# 使用psql直接连接到新的PostgreSQL服务
# 新服务使用端口5432
psql -h localhost -p 5432 -U vertical_user -d vertical_website -f /tmp/backup.sql
```

### 5.2 Redis恢复

**方法1：通过复制数据文件恢复**

```bash
# 停止新的Redis服务
docker-compose -f docker-compose.new.yml stop redis

# 将备份的dump.rdb文件复制到新的Redis数据目录
REDIS_CONTAINER_NEW=$(docker-compose -f docker-compose.new.yml ps -q redis)
docker cp /tmp/redis_dump.rdb $REDIS_CONTAINER_NEW:/data/dump.rdb

# 启动新的Redis服务
docker-compose -f docker-compose.new.yml start redis
```

**方法2：通过Redis命令恢复**

```bash
# 如果使用Redis 6+，可以使用RESTORE命令
# 但对于完整备份，建议使用文件复制方法
```

## 六、数据验证

### 6.1 PostgreSQL数据验证

```bash
# 验证数据完整性
# 1. 检查表数量
PG_CONTAINER="website_postgres"
PG_CONTAINER_NEW=$(docker-compose -f docker-compose.new.yml ps -q postgres)

echo "原数据库表数量："
docker exec -it $PG_CONTAINER psql -U vertical_user -d vertical_website -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';"

echo "新数据库表数量："
docker exec -it $PG_CONTAINER_NEW psql -U vertical_user -d vertical_website -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';"

# 2. 检查关键表数据量
# 示例：检查用户表数据量
TABLE_NAME="users"  # 根据实际情况修改
echo "原数据库$TABLE_NAME表数据量："
docker exec -it $PG_CONTAINER psql -U vertical_user -d vertical_website -c "SELECT COUNT(*) FROM $TABLE_NAME;"

echo "新数据库$TABLE_NAME表数据量："
docker exec -it $PG_CONTAINER_NEW psql -U vertical_user -d vertical_website -c "SELECT COUNT(*) FROM $TABLE_NAME;"
```

### 6.2 Redis数据验证

```bash
# 验证Redis数据
REDIS_CONTAINER="website_redis"
REDIS_CONTAINER_NEW=$(docker-compose -f docker-compose.new.yml ps -q redis)

echo "原Redis键数量："
docker exec -it $REDIS_CONTAINER redis-cli -a "Redis2024!@#$Secure" DBSIZE

echo "新Redis键数量："
docker exec -it $REDIS_CONTAINER_NEW redis-cli -a "Redis2024!@#$Secure" DBSIZE

# 检查特定键是否存在
KEY_NAME="example_key"  # 根据实际情况修改
docker exec -it $REDIS_CONTAINER redis-cli -a "Redis2024!@#$Secure" GET $KEY_NAME
docker exec -it $REDIS_CONTAINER_NEW redis-cli -a "Redis2024!@#$Secure" GET $KEY_NAME
```

## 七、启动完整新服务

### 7.1 启动后端和前端服务

```bash
# 启动新的后端和前端服务
docker-compose -f docker-compose.new.yml up -d backend frontend

# 检查所有新服务状态
docker-compose -f docker-compose.new.yml ps
```

### 7.2 验证新服务功能

```bash
# 验证后端API健康状态
curl http://localhost:8000/api/health

# 验证前端服务
curl http://localhost:80
```

## 八、切换生产流量

### 8.1 测试阶段

在正式切换前，建议进行充分测试：

1. **功能测试**：测试网站的核心功能
2. **性能测试**：确保新服务性能满足要求
3. **安全测试**：检查服务的安全性

### 8.2 正式切换

1. **更新DNS/负载均衡**：
   - 将域名指向新的前端服务（端口80）
   - 或更新负载均衡配置

2. **监控新服务**：
   ```bash
   # 监控新服务日志
docker-compose -f docker-compose.new.yml logs -f backend
docker-compose -f docker-compose.new.yml logs -f frontend
   ```

### 8.3 回滚计划

如果切换过程中出现问题，可快速回滚到原服务：

1. **恢复DNS/负载均衡**：将域名指向原服务（端口80）
2. **监控原服务**：确保原服务正常运行

## 九、清理和维护

### 9.1 数据备份保留

建议在迁移完成后保留原数据库备份至少7天，以应对可能的数据问题。

### 9.2 原服务清理

在确认新服务稳定运行7天后，可以考虑停止并清理原服务：

```bash
# 停止原服务
docker-compose down

# 如果需要，删除原数据卷（谨慎操作！）
# docker volume rm vertical_website_postgres_data vertical_website_redis_data vertical_website_backend_static
```

## 十、注意事项

1. **备份重要性**：在执行任何迁移操作前，务必确保已完成数据库备份
2. **服务中断**：Redis数据迁移可能会导致短暂的缓存失效
3. **权限问题**：确保所有命令以适当的权限执行
4. **网络问题**：确保新服务能够正常访问traefik-net网络
5. **密码安全**：所有包含密码的命令应妥善保管，避免泄露

## 十一、紧急联系人

如果在迁移过程中遇到问题，请联系系统管理员或技术支持团队。

---

**文档版本**：1.0
**创建日期**：2024年12月
**作者**：Trae AI Assistant
