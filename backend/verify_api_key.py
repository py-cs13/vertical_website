#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度智能云千帆API密钥验证工具
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

# 百度智能云千帆平台API端点列表
# 不同模型可能有不同的端点
API_ENDPOINTS = {
    "eb-instant": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant",
    "ernie-bot": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-bot",
    "ernie-bot-turbo": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-bot-turbo"
}

# 获取API密钥
api_key = get_api_key()

if not api_key:
    print("❌ 未找到API密钥，请在.env文件中配置DEEPSEEK_API_KEY")
    exit(1)

print("=" * 60)
print("百度智能云千帆API密钥验证工具")
print("=" * 60)
print(f"使用API密钥: {api_key[:10]}...{api_key[-10:]}")

# 测试每个API端点
for model, endpoint in API_ENDPOINTS.items():
    print(f"\n🧪 测试模型: {model}")
    print(f"📌 端点URL: {endpoint}")
    
    try:
        params = {
            "access_token": api_key
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "messages": [
                {"role": "user", "content": "Hello, 请回复一个简单的问候。"}
            ],
            "max_tokens": 50
        }
        
        response = requests.post(
            endpoint,
            headers=headers,
            params=params,
            json=payload,
            timeout=30
        )
        
        print(f"🔍 响应状态码: {response.status_code}")
        
        try:
            result = response.json()
            print(f"📋 响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            if response.status_code == 200:
                if "error_code" in result:
                    if result["error_code"] == 0:
                        print("✅ API密钥有效，请求成功！")
                        if "result" in result:
                            print(f"💬 模型回复: {result['result'][:100]}...")
                    else:
                        print(f"❌ API错误: {result['error_code']} - {result.get('error_msg')}")
                        print("📚 错误说明:")
                        if result["error_code"] == 110:
                            print("   - 错误码110: API密钥无效或已过期")
                            print("   - 请检查API密钥是否正确，或重新生成API密钥")
                        elif result["error_code"] == 111:
                            print("   - 错误码111: API密钥过期")
                            print("   - 请重新生成API密钥")
                        elif result["error_code"] == 112:
                            print("   - 错误码112: API密钥被禁用")
                            print("   - 请联系百度智能云客服")
                else:
                    print("✅ API请求成功，响应格式与预期不同")
            else:
                print(f"❌ HTTP请求失败: {response.status_code}")
                
        except json.JSONDecodeError:
            print(f"❌ 响应不是有效的JSON格式: {response.text[:200]}...")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求异常: {e}")
    except Exception as e:
        print(f"❌ 未知错误: {e}")

print(f"\n{'-'*60}")
print("测试完成！")
print("如果所有模型都返回错误码110，请检查:")
print("1. API密钥是否正确")
print("2. API密钥是否已过期")
print("3. API密钥是否有调用相应模型的权限")
print("4. 是否已在百度智能云控制台激活服务")