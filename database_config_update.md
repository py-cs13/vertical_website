# 全局数据库配置更新方案

## 需求确认
用户要求：
> 不再备份数据，只需要将最新的数据库配置信息进行全局更换，先给出方案，暂时不修改代码。

## 配置信息分析

### 旧数据库配置
- **类型**：PostgreSQL
- **主机**：101.43.177.216（外部IP）
- **端口**：5432
- **数据库名**：vertical_website
- **用户名**：vertical_user
- **密码**：pg123456
- **连接字符串**：`postgresql://vertical_user:pg123456@101.43.177.216:5432/vertical_website`

### 新数据库配置（Docker容器）
- **类型**：PostgreSQL
- **主机**：postgres（Docker容器名）
- **端口**：5432
- **数据库名**：vertical_website
- **用户名**：vertical_user
- **密码**：2Hjh39%&94h
- **连接字符串**：`postgresql://vertical_user:2Hjh39%&94h@postgres:5432/vertical_website`

## 需要更新的配置文件

### 1. 环境变量文件
- **文件**：`/Users/shucui/Desktop/vertical_website/backend/.env`
- **当前内容**：`DATABASE_URL=postgresql://vertical_user:2Hjh39%&94h@101.43.177.216:5432/vertical_website`
- **需要修改**：将主机地址从`101.43.177.216`改为`postgres`

### 2. 主配置文件
- **文件**：`/Users/shucui/Desktop/vertical_website/backend/config.py`
- **当前内容**：`DATABASE_URL: str = "postgresql://vertical_user:2Hjh39%&94h@postgres:5432/vertical_website"`
- **需要修改**：确认配置正确（已使用`postgres`作为主机名）

### 3. 备份配置文件
- **文件**：`/Users/shucui/Desktop/vertical_website/backend/config.py.backup`
- **当前内容**：`DATABASE_URL: str = "postgresql://vertical_user:pg123456@101.43.177.216:5432/vertical_website"`
- **需要修改**：更新为新的连接字符串

### 4. 检查脚本
- **文件**：`/Users/shucui/Desktop/vertical_website/backend/check_db.py`
- **当前内容**：使用环境变量中的数据库配置
- **需要修改**：无需修改，自动使用新的环境变量

### 5. 测试脚本
- **文件**：`/Users/shucui/Desktop/vertical_website/backend/test_db_connection.py`
- **当前内容**：硬编码的数据库连接信息
- **需要修改**：更新为新的连接配置

### 6. 其他脚本
- **文件**：`/Users/shucui/Desktop/vertical_website/backend/simple_backup.py`
- **当前内容**：硬编码的数据库连接信息
- **需要修改**：更新为新的连接配置

## 更新方案

### 步骤1：更新环境变量文件（.env）
```bash
# 将主机地址从101.43.177.216改为postgres
# 密码已经是正确的新密码，不需要修改
```

### 步骤2：检查并更新主配置文件（config.py）
```bash
# 主配置文件已经使用了正确的主机名（postgres）
# 确认密码是否正确
```

### 步骤3：更新备份配置文件（config.py.backup）
```bash
# 更新为新的连接字符串，保持与主配置文件一致
```

### 步骤4：更新测试脚本
```bash
# 更新所有硬编码的测试脚本，使其使用新的数据库配置
```

## 验证方法

### 验证配置更新
```bash
# 检查所有文件是否已更新为新的配置
cd /Users/shucui/Desktop/vertical_website

grep -r "101.43.177.216" backend/  # 应该没有输出或只有需要保留的旧配置

grep -r "postgresql://vertical_user:2Hjh39%&94h@postgres:5432/vertical_website" backend/  # 应该在所有需要的文件中出现
```

### 验证数据库连接
```bash
# 使用新配置连接数据库
cd backend
python -c "from database import engine; from sqlalchemy import text; with engine.connect() as conn: result = conn.execute(text('SELECT 1')); print('数据库连接成功:', result.scalar())"
```

### 验证应用启动
```bash
# 启动后端服务，检查是否能正常连接数据库
uvicorn main:app --reload
```

## 注意事项

1. **密码处理**：新密码`2Hjh39%&94h`包含特殊字符，需要确保在所有配置文件中正确转义

2. **Docker网络**：确保应用容器和PostgreSQL容器在同一个网络（traefik-net）中，这样才能通过`postgres`主机名访问

3. **环境变量优先级**：如果`.env`文件和`config.py`文件都配置了数据库连接，需要确认哪个优先级更高（通常是`.env`文件）

4. **备份配置**：更新配置前，建议备份所有配置文件，以便在出现问题时快速回滚
