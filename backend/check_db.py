# 检查PostgreSQL数据库中的用户表结构和数据
import sys
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from config import settings

# 从配置中获取数据库连接信息
db_url = settings.DATABASE_URL
print(f"数据库连接URL: {db_url}")

try:
    # 连接到PostgreSQL数据库
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    print("成功连接到数据库")
    
    # 检查用户表结构
    cursor.execute("SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = 'users'")
    table_structure = cursor.fetchall()
    print("\n用户表结构:")
    for col in table_structure:
        print(f"  {col['column_name']}: {col['data_type']} {'NOT NULL' if col['is_nullable'] == 'NO' else ''}")
    
    # 查询用户数据
    cursor.execute("SELECT id, username, email, hashed_password, created_at, is_active FROM users")
    users = cursor.fetchall()
    
    print(f"\n共有 {len(users)} 个用户:")
    for user in users:
        print(f"\n用户 {user['id']}:")
        print(f"  邮箱: {user['email']}")
        print(f"  用户名: {user['username']}")
        print(f"  密码哈希: {user['hashed_password']}")
        print(f"  创建时间: {user['created_at']}")
        print(f"  是否活跃: {user['is_active']}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"数据库操作失败: {str(e)}")
    import traceback
    traceback.print_exc()
