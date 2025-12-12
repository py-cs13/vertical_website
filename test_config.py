#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置加载测试脚本
"""

import os
import sys

# 切换到backend目录
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
os.chdir(backend_dir)

# 设置环境变量
os.environ['APP_ENV'] = 'production'

# 确保能导入backend模块
sys.path.insert(0, backend_dir)

# 打印当前目录和文件
print(f"当前工作目录: {os.getcwd()}")
print(f"backend/.env.production存在: {os.path.exists('.env.production')}")
if os.path.exists('.env.production'):
    print("\n.env.production内容:")
    with open('.env.production', 'r') as f:
        print(f.read())

# 导入配置
from config import settings

print("\n=== 配置加载测试 ===")
print(f"APP_ENV: {os.getenv('APP_ENV')}")
print(f"DATABASE_URL: {settings.DATABASE_URL}")
print(f"REDIS_URL: {settings.REDIS_URL}")
print(f"DEBUG: {settings.DEBUG}")
print(f"SECRET_KEY: {settings.SECRET_KEY}")
