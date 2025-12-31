#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接连接数据库测试用户密码的脚本
"""

import sys
import os
from sqlalchemy import create_engine, text
from passlib.context import CryptContext

# 添加backend目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# 从配置中获取数据库连接信息
from config import settings

# 创建密码哈希上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 测试函数
def test_db_and_password():
    print("开始测试数据库和密码验证...")
    
    try:
        # 创建数据库引擎
        engine = create_engine(settings.DATABASE_URL)
        print(f"数据库连接成功: {settings.DATABASE_URL}")
        
        # 连接数据库
        with engine.connect() as conn:
            # 查询测试用户
            result = conn.execute(text("SELECT * FROM users WHERE email = 'test@example.com'"))
            user = result.fetchone()
            
            if user:
                print("\n找到测试用户:")
                print(f"ID: {user.id}")
                print(f"用户名: {user.username}")
                print(f"邮箱: {user.email}")
                print(f"密码哈希: {user.hashed_password}")
                print(f"是否激活: {user.is_active}")
                
                # 测试密码验证
                test_passwords = ["test123", "wrong_password"]
                for pwd in test_passwords:
                    is_valid = pwd_context.verify(pwd, user.hashed_password)
                    print(f"\n验证密码 '{pwd}': {'成功' if is_valid else '失败'}")
            else:
                print("\n未找到测试用户")
                # 查看所有用户
                result = conn.execute(text("SELECT id, username, email FROM users"))
                users = result.fetchall()
                print("\n数据库中的所有用户:")
                for u in users:
                    print(f"ID: {u.id}, 用户名: {u.username}, 邮箱: {u.email}")
                    
    except Exception as e:
        print(f"\n测试失败: {e}")

if __name__ == "__main__":
    test_db_and_password()