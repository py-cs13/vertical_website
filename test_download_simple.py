#!/usr/bin/env python3
"""
简单测试脚本：验证下载工具包401错误
"""

import requests
import json

# 配置
BASE_URL = "http://localhost:8000"
TOOLKIT_ID = 1

# 从前端获取token（需要手动从浏览器控制台复制）
# 在浏览器控制台执行: localStorage.getItem('token')
TOKEN = input("请输入从浏览器获取的token: ").strip()

print(f"\n测试工具包下载接口...")
print(f"工具包ID: {TOOLKIT_ID}")
print(f"Token: {TOKEN[:20]}...")

# 测试1: 验证token是否有效
try:
    print(f"\n测试1: 验证token有效性")
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    response = requests.get(f"{BASE_URL}/api/users/me", headers=headers)
    print(f"用户信息接口响应: {response.status_code}")
    if response.status_code == 200:
        user_data = response.json()
        print(f"用户ID: {user_data['id']}, 邮箱: {user_data['email']}")
        print("✓ Token有效")
    else:
        print(f"✗ Token无效: {response.text}")
except Exception as e:
    print(f"✗ 测试1失败: {e}")

# 测试2: 测试下载接口
try:
    print(f"\n测试2: 测试下载接口")
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    response = requests.get(f"{BASE_URL}/api/toolkits/{TOOLKIT_ID}/download", 
                          headers=headers, 
                          stream=True)
    
    print(f"下载接口响应: {response.status_code}")
    print(f"响应头: {dict(response.headers)}")
    
    if response.status_code == 200:
        print("✓ 下载成功")
        print(f"文件大小: {response.headers.get('Content-Length', '未知')} bytes")
        print(f"文件类型: {response.headers.get('Content-Type', '未知')}")
    elif response.status_code == 401:
        print("✗ 下载失败: 401未授权")
        print(f"响应内容: {response.text}")
    elif response.status_code == 403:
        print("✗ 下载失败: 403禁止访问（可能未购买）")
        print(f"响应内容: {response.text}")
    elif response.status_code == 404:
        print("✗ 下载失败: 404工具包不存在")
        print(f"响应内容: {response.text}")
    else:
        print(f"✗ 下载失败: {response.status_code}")
        print(f"响应内容: {response.text}")
except Exception as e:
    print(f"✗ 测试2失败: {e}")

# 测试3: 测试未购买的工具包（如果有）
print(f"\n测试3: 检查工具包是否存在")
try:
    response = requests.get(f"{BASE_URL}/api/toolkits/{TOOLKIT_ID}")
    print(f"工具包信息接口响应: {response.status_code}")
    if response.status_code == 200:
        toolkit = response.json()
        print(f"工具包名称: {toolkit.get('title', '未知')}")
        print(f"发布状态: {'已发布' if toolkit.get('is_published') else '未发布'}")
        print(f"分类: {toolkit.get('category', '未知')}")
    else:
        print(f"✗ 工具包不存在或无法访问")
except Exception as e:
    print(f"✗ 测试3失败: {e}")

print(f"\n测试完成！")
