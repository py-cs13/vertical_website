#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新测试用户的密码为test1234
"""

import sys
import os

# 添加backend目录到系统路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings
from models import User
from auth import get_password_hash

def update_test_user_password():
    """
    更新测试用户的密码为test1234
    """
    print("更新测试用户密码...")
    
    try:
        # 创建数据库引擎
        engine = create_engine(settings.DATABASE_URL)
        
        # 创建会话
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # 查找测试用户
        test_user = db.query(User).filter(User.email == "test@example.com").first()
        
        if test_user:
            print(f"找到测试用户: {test_user.email}")
            
            # 更新密码
            test_user.hashed_password = get_password_hash("test1234")
            db.commit()
            db.refresh(test_user)
            
            print(f"测试用户密码已更新为 'test1234'")
        else:
            print("未找到测试用户，正在创建新的测试用户...")
            
            # 创建新的测试用户
            new_test_user = User(
                username="test_user",
                email="test@example.com",
                hashed_password=get_password_hash("test1234"),
                is_active=True
            )
            
            db.add(new_test_user)
            db.commit()
            db.refresh(new_test_user)
            
            print(f"新测试用户创建成功: {new_test_user.email}")
            print(f"密码: test1234")
            
    except Exception as e:
        print(f"更新用户密码时发生错误: {e}")
    finally:
        if 'db' in locals():
            db.close()

def main():
    """
    主函数
    """
    update_test_user_password()

if __name__ == "__main__":
    main()
