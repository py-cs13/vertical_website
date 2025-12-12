#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试工具包API端点的脚本
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_toolkit_api():
    """测试工具包API端点"""
    print("测试工具包API端点...")
    
    # 测试获取最新工具包
    url = f"{BASE_URL}/api/toolkits/latest"
    response = requests.get(url)
    
    print(f"\nAPI请求: {url}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应头: {json.dumps(dict(response.headers), indent=2)}")
    print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    
    if response.status_code == 200:
        toolkits = response.json()
        print(f"\n成功获取到 {len(toolkits)} 个工具包")
    else:
        print(f"\nAPI请求失败，状态码: {response.status_code}")

if __name__ == "__main__":
    test_toolkit_api()