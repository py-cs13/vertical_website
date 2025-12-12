#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试百度智能云千帆API端点
"""

import requests
import json
import os

# 从环境变量获取API密钥
def get_api_key():
    # 尝试从环境变量获取
    api_key = os.environ.get('DEEPSEEK_API_KEY')
    
    # 如果环境变量不存在，尝试从.env文件读取
    if not api_key and os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if line.strip() and '=' in line:
                    key, value = line.strip().split('=', 1)
                    if key.strip() == 'DEEPSEEK_API_KEY':
                        api_key = value.strip().strip('"\'')
                        break
    
    return api_key

# 从环境变量获取API密钥和密钥
# 注意：根据文档，可能需要同时使用API Key和Secret Key来获取access token
def get_api_credentials():
    api_key = None
    secret_key = None
    
    # 尝试从.env文件读取
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if line.strip() and '=' in line:
                    key, value = line.strip().split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"\'')
                    if key == 'DEEPSEEK_API_KEY':
                        api_key = value
                    elif key == 'DEEPSEEK_API_SECRET':
                        secret_key = value
    
    # 尝试从环境变量获取
    if not api_key:
        api_key = os.environ.get('DEEPSEEK_API_KEY')
    if not secret_key:
        secret_key = os.environ.get('DEEPSEEK_API_SECRET')
    
    return api_key, secret_key

# 获取百度智能云access token
def get_access_token(api_key, secret_key):
    """
    使用API Key和Secret Key获取百度智能云access token
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": secret_key
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result.get("access_token")
    except Exception as e:
        print(f"❌ 获取access token失败: {e}")
        return None

# 百度智能云千帆平台API端点（使用用户提供的模板）
API_URL = "https://qianfan.baidubce.com/v2/chat/completions"

# 获取API密钥和密钥
api_key, secret_key = get_api_credentials()

if not api_key:
    print("❌ 未找到API密钥，请在.env文件中配置DEEPSEEK_API_KEY")
    exit(1)

# 如果有密钥，先获取access token
access_token = None
if secret_key:
    print(f"使用API密钥: {api_key[:10]}...")
    print(f"使用API密钥: {secret_key[:10]}...")
    access_token = get_access_token(api_key, secret_key)
    if access_token:
        print(f"成功获取access token: {access_token[:10]}...")
else:
    # 如果没有密钥，直接使用API密钥
    access_token = api_key
    print(f"直接使用API密钥: {access_token[:10]}...")

if not access_token:
    print("❌ 无法获取有效的access token")
    exit(1)

# 测试API连接
try:
    # 根据最新文档，使用Authorization头进行认证
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    payload = {
        "model": "deepseek-v3.1-250821",  # 使用用户提供的模型
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Hello"
            }
        ]
    }
    
    print(f"\n测试API端点: {API_URL}")
    print(f"请求头: Authorization: Bearer {api_key[:10]}...")
    print(f"请求体: {json.dumps(payload, ensure_ascii=False)}")
    
    # 使用用户提供的模板方式发送请求
    response = requests.request(
        "POST",
        API_URL,
        headers=headers,
        data=json.dumps(payload),
        timeout=30
    )
    
    print(f"\n响应状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    
    if response.status_code == 200:
        print("✅ API调用成功")
        # 解析并打印响应结构
        try:
            result = response.json()
            print(f"\n响应JSON结构:")
            print(f"- 错误码: {result.get('error_code')}")
            print(f"- 错误信息: {result.get('error_msg')}")
            print(f"- 结果: {result.get('result')}")
            print(f"- 请求ID: {result.get('request_id')}")
            print(f"- 所有键: {list(result.keys())}")
            
            # 提供错误建议
            if result.get('error_code') == 110:
                print("\n💡 错误建议：")
                print("1. API密钥可能无效或已过期，请检查并获取新的密钥")
                print("2. 请确认您已在百度智能云控制台启用了相关模型的访问权限")
                print("3. 请确保使用正确的认证方式（Bearer Token或access_token参数）")
            elif result.get('error_code') == 3:
                print("\n💡 错误建议：")
                print("1. API端点可能不正确，请检查端点URL")
                print("2. 请确认您使用的是支持的API方法")
        except json.JSONDecodeError:
            print("❌ 响应不是有效的JSON格式")
    else:
        print(f"❌ API调用失败: {response.status_code}")
        
except Exception as e:
    print(f"❌ API调用异常: {e}")