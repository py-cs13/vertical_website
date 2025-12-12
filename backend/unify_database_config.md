# 数据库统一配置说明

## 当前数据库配置情况

### 1. 生产环境数据库
- **数据库类型**：PostgreSQL
- **配置文件**：`config.py` 和 `.env.production`
- **连接信息**：
  - 主机：`101.43.177.216`
  - 端口：`5432`
  - 数据库名：`vertical_website`
  - 用户名：`vertical_user`
  - 密码：`pg123456`
- **连接字符串**：`postgresql://vertical_user:pg123456@101.43.177.216:5432/vertical_website`
- **使用场景**：所有环境统一使用

## 统一数据库配置方案

### 1. 修改默认数据库配置

要将所有数据统一存储到生产环境数据库，需要修改 `config.py` 中的默认配置：

```python
# 数据库配置
DATABASE_URL: str = "postgresql://vertical_user:pg123456@101.43.177.216:5432/vertical_website"
```

这样修改后，无论在什么环境下，都会默认使用生产环境的PostgreSQL数据库。

### 2. 配置环境变量

如果需要保留环境区分，但确保所有环境都使用相同的数据库，可以设置环境变量：

```bash
# 在项目根目录下创建.env文件
cp .env.production .env
```

这样，无论是开发环境还是生产环境，都会加载 `.env` 文件中的配置，使用相同的数据库。

### 3. 验证数据库连接

修改配置后，可以运行以下命令验证数据库连接：

```bash
python -c "from database import engine; from sqlalchemy import text; with engine.connect() as conn: result = conn.execute(text('SELECT 1')); print('数据库连接成功:', result.scalar())"
```

### 4. 重新创建数据库表

如果是第一次使用生产环境数据库，需要重新创建数据库表：

```bash
cd backend
python -c "from database import Base, engine; from models import *; Base.metadata.create_all(bind=engine)"
```

### 5. 导入测试数据（可选）

如果需要导入测试数据到生产环境数据库，可以使用数据库迁移工具或手动导入。

## 统一后的使用方式

修改配置后，所有的API请求、数据存储、数据查询都会自动使用生产环境的PostgreSQL数据库：

- 用户注册/登录数据会存储到生产环境数据库
- 内容数据（包括工具包）会存储到生产环境数据库
- 订单和支付数据会存储到生产环境数据库
- 所有API请求都会从生产环境数据库获取数据

## 注意事项

1. **数据库权限**：确保生产环境数据库用户有足够的权限（创建表、读写数据等）
2. **网络连接**：确保应用服务器能够连接到生产环境数据库服务器
3. **数据备份**：定期备份生产环境数据库，防止数据丢失
4. **性能监控**：监控数据库性能，确保系统稳定运行

通过以上配置，所有数据都会统一存储到生产环境的PostgreSQL数据库中，实现数据的集中管理和使用。