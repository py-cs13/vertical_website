#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细的下载功能测试脚本，用于诊断401错误
"""

import requests
import json
import base64
import sys
from datetime import datetime

# 配置
BASE_URL = "http://localhost:8000"

# 获取用户输入的token
def get_token():
    """从用户输入获取token"""
    token = input("请输入从浏览器获取的token: ").strip()
    if not token:
        print("错误：token不能为空")
        sys.exit(1)
    return token

# 解析JWT令牌（不验证签名，仅用于查看payload）
def decode_jwt(token):
    """解码JWT令牌的payload部分"""
    try:
        # JWT令牌由三部分组成：header.payload.signature
        parts = token.split('.')
        if len(parts) != 3:
            return None
        
        # 解码payload（需要处理base64 URL安全编码）
        payload = parts[1]
        # 确保payload长度是4的倍数
        payload += '=' * (-len(payload) % 4)
        # 解码
        payload_bytes = base64.urlsafe_b64decode(payload)
        payload_dict = json.loads(payload_bytes.decode('utf-8'))
        return payload_dict
    except Exception as e:
        print(f"解码JWT令牌失败: {e}")
        return None

# 测试token有效性
def test_token_validity(token):
    """测试token是否有效"""
    print(f"\n=== 测试Token有效性 ===")
    
    # 解析令牌
    payload = decode_jwt(token)
    if payload:
        print(f"✓ 令牌格式正确")
        print(f"  用户ID: {payload.get('sub')}")
        
        # 检查过期时间
        exp = payload.get('exp')
        if exp:
            exp_time = datetime.fromtimestamp(exp)
            now = datetime.now()
            print(f"  过期时间: {exp_time}")
            print(f"  当前时间: {now}")
            print(f"  令牌状态: {'已过期' if exp_time < now else '有效'}")
        else:
            print(f"  警告: 令牌没有过期时间")
    else:
        print(f"✗ 令牌格式错误")
        return False
    
    return True

# 测试用户信息API
def test_user_info(token):
    """测试获取用户信息API"""
    print(f"\n=== 测试用户信息API ===")
    url = f"{BASE_URL}/api/users/me"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    print(f"请求URL: {url}")
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ 获取用户信息成功")
        print(f"  用户名: {data.get('username')}")
        print(f"  邮箱: {data.get('email')}")
        print(f"  用户ID: {data.get('id')}")
        return True
    else:
        print(f"✗ 获取用户信息失败")
        print(f"  错误详情: {response.text}")
        return False

# 获取可用的工具包列表
def get_available_toolkits(token):
    """获取可用的工具包列表"""
    print(f"\n=== 获取可用工具包列表 ===")
    url = f"{BASE_URL}/api/toolkits"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    print(f"请求URL: {url}")
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        toolkits = response.json()
        print(f"✓ 获取工具包列表成功，共 {len(toolkits)} 个工具包")
        
        for i, toolkit in enumerate(toolkits[:3], 1):  # 只显示前3个
            print(f"  {i}. {toolkit.get('title')} (ID: {toolkit.get('id')})")
            print(f"     分类: {toolkit.get('category')}")
            print(f"     价格: {toolkit.get('price')} 元")
        
        if len(toolkits) > 3:
            print(f"     ... 还有 {len(toolkits) - 3} 个工具包")
        
        return toolkits
    else:
        print(f"✗ 获取工具包列表失败")
        print(f"  错误详情: {response.text}")
        return None

# 测试下载工具包
def test_download_toolkit(token, toolkit_id):
    """测试下载工具包"""
    print(f"\n=== 测试下载工具包 (ID: {toolkit_id}) ===")
    url = f"{BASE_URL}/api/toolkits/{toolkit_id}/download"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers, stream=True)
    print(f"请求URL: {url}")
    print(f"状态码: {response.status_code}")
    print(f"响应头: {dict(response.headers)}")
    
    if response.status_code == 200:
        # 获取文件名
        content_disposition = response.headers.get("content-disposition")
        if content_disposition:
            filename = content_disposition.split("filename=")[1].strip('"')
        else:
            filename = f"toolkit_{toolkit_id}.pdf"
        
        # 保存文件
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        
        print(f"✓ 工具包下载成功，保存为: {filename}")
        return True
    else:
        print(f"✗ 工具包下载失败")
        print(f"  错误详情: {response.text}")
        return False

# 主函数
def main():
    print("🚀 开始详细测试下载功能")
    print(f"📅 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 后端地址: {BASE_URL}")
    
    # 获取token
    token = get_token()
    
    # 步骤1: 测试token有效性
    if not test_token_validity(token):
        sys.exit(1)
    
    # 步骤2: 测试用户信息API
    if not test_user_info(token):
        print("\n❌ 测试失败：无法获取用户信息，可能是token无效")
        sys.exit(1)
    
    # 步骤3: 获取可用工具包
    toolkits = get_available_toolkits(token)
    if not toolkits:
        sys.exit(1)
    
    # 步骤4: 选择一个工具包进行下载测试
    toolkit_id = input(f"\n请选择要下载的工具包ID (1-{len(toolkits)}): ").strip()
    try:
        index = int(toolkit_id) - 1
        if 0 <= index < len(toolkits):
            selected_toolkit = toolkits[index]
            test_download_toolkit(token, selected_toolkit.get('id'))
        else:
            print(f"❌ 无效的工具包ID")
            sys.exit(1)
    except ValueError:
        print(f"❌ 无效的工具包ID")
        sys.exit(1)
    
    print(f"\n🎉 测试完成")

if __name__ == "__main__":
    main()