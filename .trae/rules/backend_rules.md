# 后端开发规范

## 1. 代码风格规范

### 1.1 文件命名
snake_case（如：auth.py, database.py）

### 1.2 命名约定
- 变量名：snake_case（如：user_id, unique_code）
- 函数名：snake_case（如：get_current_user, generate_affiliate_link）
- 类名：PascalCase（如：User, AffiliateLink）
- 常量：UPPER_SNAKE_CASE（如：SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES）

### 1.3 代码格式
- 缩进：4个空格（遵循PEP 8）
- 每行长度：不超过79个字符（遵循PEP 8）
- 函数注释：使用Google风格的函数文档字符串
- 类型注解：所有函数参数和返回值必须添加类型注解

## 2. 开发环境配置

### 2.1 后端启动
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

### 2.2 环境变量
- 使用.env文件管理环境变量
- 敏感信息（数据库密码、API密钥等）必须通过环境变量配置
- 不要在代码中硬编码敏感信息

## 3. 后端性能优化

### 3.1 数据库索引
为查询频繁的字段添加索引

### 3.2 缓存机制
使用Redis缓存热点数据和会话信息

### 3.3 异步处理
对IO密集型操作使用异步方式

### 3.4 分页处理
大量数据时使用分页查询

### 3.5 请求限流
使用Redis实现API请求限流保护
