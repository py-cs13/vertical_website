#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查数据库中的用户信息
"""

import sys
import os

# 添加backend目录到系统路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import settings
from models import Base, User
from auth import verify_password

def check_database_users():
    """
    检查数据库中的用户信息
    """
    print("检查数据库中的用户信息...")
    
    try:
        # 创建数据库引擎
        engine = create_engine(settings.DATABASE_URL)
        
        # 创建会话
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # 查询所有用户
        users = db.query(User).all()
        
        if not users:
            print("数据库中没有用户信息")
            return
        
        print(f"数据库中共有 {len(users)} 个用户:")
        print("-" * 50)
        
        for user in users:
            print(f"用户ID: {user.id}")
            print(f"用户名: {user.username}")
            print(f"邮箱: {user.email}")
            print(f"是否激活: {user.is_active}")
            print(f"是否管理员: {user.is_admin}")
            print(f"创建时间: {user.created_at}")
            print(f"密码哈希: {user.hashed_password}")
            print("-" * 50)
            
            # 测试密码验证
            if user.email == "test@example.com":
                is_password_correct = verify_password("test1234", user.hashed_password)
                print(f"测试密码 'test1234' 是否正确: {is_password_correct}")
                print("-" * 50)
                
    except Exception as e:
        print(f"检查用户信息时发生错误: {e}")
    finally:
        if 'db' in locals():
            db.close()

def main():
    """
    主函数
    """
    check_database_users()

if __name__ == "__main__":
    main()
