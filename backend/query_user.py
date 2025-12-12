# 查询用户信息的脚本
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User
from config import settings

# 使用PostgreSQL数据库（与后端实际使用的一致）
DATABASE_URL = settings.DATABASE_URL

# 创建数据库引擎
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# 创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    # 查询所有用户
    users = db.query(User).all()
    
    if users:
        print(f"共有 {len(users)} 个用户:")
        for user in users:
            print(f"\n用户 {user.id}:")
            print(f"邮箱: {user.email}")
            print(f"用户名: {user.username}")
            print(f"密码哈希: {user.hashed_password}")
            print(f"创建时间: {user.created_at}")
            print(f"是否活跃: {user.is_active}")
            print(f"性别: {user.gender}")
            print(f"生日: {user.birthday}")
            print(f"个人简介: {user.bio}")
            print(f"头像: {user.avatar}")
    else:
        print("数据库中没有用户")
finally:
    db.close()
