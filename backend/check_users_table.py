# 检查数据库中users表的实际结构
from database import engine
from sqlalchemy import text

print("检查数据库中users表的实际结构...")

with engine.connect() as conn:
    # 查询表结构
    result = conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'users' ORDER BY ordinal_position"))
    
    print("\nusers表的实际字段:")
    for row in result:
        print(f"  {row[0]}: {row[1]}")

    # 查询用户记录
    print("\nusers表中的记录:")
    result = conn.execute(text("SELECT id, username, email, hashed_password, is_active FROM users"))
    
    for row in result:
        print(f"\n用户ID: {row[0]}")
        print(f"  用户名: {row[1]}")
        print(f"  邮箱: {row[2]}")
        print(f"  密码哈希: {row[3]}")
        print(f"  是否活跃: {row[4]}")
