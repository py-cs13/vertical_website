# 数据库规范

## 1. 表设计原则
- 每个表必须有主键
- 使用外键建立表关系
- 字段名使用snake_case
- 为重要字段添加索引
- 添加适当的注释说明字段用途

## 2. 常用表结构
- **用户表**：存储用户基本信息（id, email, password_hash, nickname等）
- **文章表**：存储文章内容（id, title, content, author_id, created_at等）
- **智能体表**：存储智能体信息（id, name, description, price, file_path等）
- **订单表**：存储订单信息（id, user_id, total_amount, status, created_at等）
- **推广链接表**：存储推广链接（id, user_id, unique_code, is_active等）
- **佣金记录表**：存储佣金信息（id, order_id, affiliate_link_id, amount, status等）
