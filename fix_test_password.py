#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复测试用户密码的脚本
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
def fix_test_password():
    print("开始修复测试用户密码...")
    
    try:
        # 创建数据库引擎
        engine = create_engine(settings.DATABASE_URL)
        print(f"数据库连接成功: {settings.DATABASE_URL}")
        
        # 生成新的密码哈希
        password = "test123"
        hashed_password = pwd_context.hash(password)
        print(f"\n新的密码哈希: {hashed_password}")
        
        # 连接数据库并更新密码
        with engine.begin() as conn:
            # 更新测试用户密码
            conn.execute(
                text("UPDATE users SET hashed_password = :hashed_password WHERE email = 'test@example.com'"),
                {"hashed_password": hashed_password}
            )
            print("\n测试用户密码已更新")
            
            # 验证更新后的密码
            result = conn.execute(text("SELECT hashed_password FROM users WHERE email = 'test@example.com'"))
            user = result.fetchone()
            
            if user:
                is_valid = pwd_context.verify(password, user.hashed_password)
                print(f"验证新密码: {'成功' if is_valid else '失败'}")
            
    except Exception as e:
        print(f"\n修复失败: {e}")

if __name__ == "__main__":
    fix_test_password()