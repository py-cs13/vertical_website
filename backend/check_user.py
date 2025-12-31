#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查数据库中是否存在用户ID为1的用户
"""

from database import SessionLocal
from models import User

# 创建数据库会话
db = SessionLocal()

print("检查数据库中是否存在用户ID为1的用户...")

# 检查用户是否存在
user = db.query(User).filter(User.id == 1).first()

if user:
    print(f"✅ 用户存在: ID={user.id}, 用户名={user.username}, 邮箱={user.email}")
else:
    print(f"❌ 用户ID=1不存在")
    print("正在创建用户ID=1...")
    
    # 创建一个默认用户
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    new_user = User(
        username="admin",
        email="admin@example.com",
        hashed_password=pwd_context.hash("admin123"),
        is_active=True,
        is_admin=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    print(f"✅ 用户创建成功: ID={new_user.id}, 用户名={new_user.username}, 邮箱={new_user.email}")

# 关闭数据库会话
db.close()