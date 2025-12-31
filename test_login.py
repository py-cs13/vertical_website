#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试登录功能的脚本
"""

import requests
import json

def test_login():
    """
    测试登录功能
    """
    print("测试登录功能...")
    
    # 登录API地址
    login_url = "http://localhost:8000/api/auth/login"
    
    # 测试用户凭证
    test_credentials = {
        "email": "test@example.com",
        "password": "test1234"
    }
    
    try:
        # 发送登录请求
        response = requests.post(
            login_url,
            json=test_credentials,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"登录请求状态码: {response.status_code}")
        print(f"登录请求响应: {response.text}")
        
        if response.status_code == 200:
            print("登录成功！")
            
            # 获取访问令牌
            login_data = response.json()
            access_token = login_data.get("access_token")
            
            if access_token:
                print(f"获取到访问令牌: {access_token[:20]}...")
                
                # 测试使用令牌访问受保护的API
                test_protected_api(access_token)
        else:
            print("登录失败！")
            
    except Exception as e:
        print(f"测试登录功能时发生错误: {e}")

def test_protected_api(access_token):
    """
    测试使用令牌访问受保护的API
    """
    print("\n测试访问受保护的API...")
    
    # 受保护的API地址
    protected_url = "http://localhost:8000/api/auth/me"
    
    try:
        # 发送请求
        response = requests.get(
            protected_url,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )
        
        print(f"受保护API请求状态码: {response.status_code}")
        print(f"受保护API请求响应: {response.text}")
        
        if response.status_code == 200:
            print("访问受保护API成功！")
        else:
            print("访问受保护API失败！")
            
    except Exception as e:
        print(f"测试受保护API时发生错误: {e}")

def main():
    """
    主函数
    """
    test_login()

if __name__ == "__main__":
    main()
