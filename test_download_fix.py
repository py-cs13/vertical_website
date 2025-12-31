#!/usr/bin/env python3
"""
测试脚本：验证工具包下载权限问题

该脚本用于诊断用户支付成功后无法下载工具包的问题。
主要检查：
1. 用户订单状态是否正确更新为"paid"
2. 订单产品ID与工具包ID是否匹配
3. 当前用户ID与订单用户ID是否匹配
"""

import requests
import json
import sys

# 配置
BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:5174"

# 用户输入区（请根据实际情况修改）
TOOLKIT_ID = 1  # 要下载的工具包ID
USER_EMAIL = "user@example.com"  # 用户注册邮箱
USER_PASSWORD = "password123"  # 用户密码


def login(email, password):
    """用户登录获取token"""
    print("\n=== 用户登录 ===")
    url = f"{BASE_URL}/api/auth/login"
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        print("✅ 登录成功")
        return response.json()
    else:
        print(f"❌ 登录失败: {response.status_code}")
        print(f"错误信息: {response.text}")
        return None


def get_user_orders(token):
    """获取用户订单列表"""
    print("\n=== 获取用户订单 ===")
    url = f"{BASE_URL}/api/orders"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        orders = response.json()
        print(f"✅ 获取订单成功，共 {len(orders)} 个订单")
        return orders
    else:
        print(f"❌ 获取订单失败: {response.status_code}")
        print(f"错误信息: {response.text}")
        return None


def check_order_status(orders, toolkit_id):
    """检查订单状态和产品ID匹配情况"""
    print("\n=== 检查订单状态 ===")
    found_matching_order = False
    
    for order in orders:
        print(f"\n订单ID: {order['id']}")
        print(f"订单状态: {order['status']}")
        print(f"产品类型: {order['product_type']}")
        print(f"产品ID: {order['product_id']}")
        print(f"支付时间: {order['paid_at'] if order['paid_at'] else '未支付'}")
        
        # 检查是否有匹配的工具包订单
        if order['product_type'] == 'toolkit' and order['product_id'] == toolkit_id:
            found_matching_order = True
            
            if order['status'] == 'paid':
                print("✅ 找到匹配的已支付订单！")
                return True
            else:
                print(f"⚠️  找到匹配订单，但状态为: {order['status']}")
                
    if not found_matching_order:
        print(f"❌ 未找到产品类型为'toolkit'且产品ID为{toolkit_id}的订单")
        print("可能的原因:")
        print("1. 订单产品ID与工具包ID不匹配")
        print("2. 订单产品类型不是'toolkit'")
        print("3. 订单可能是其他用户创建的")
    
    return False


def test_download(token, toolkit_id):
    """测试下载工具包"""
    print("\n=== 测试工具包下载 ===")
    url = f"{BASE_URL}/api/toolkits/{toolkit_id}/download"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers, allow_redirects=False)
    
    if response.status_code == 200 or response.status_code == 302:
        print("✅ 下载请求成功！")
        if response.status_code == 302:
            print(f"重定向到下载地址: {response.headers['Location']}")
        return True
    else:
        print(f"❌ 下载请求失败: {response.status_code}")
        try:
            error_data = response.json()
            print(f"错误信息: {error_data.get('detail', '未知错误')}")
        except:
            print(f"错误信息: {response.text}")
        return False


def check_user_info(token):
    """获取当前用户信息"""
    print("\n=== 获取当前用户信息 ===")
    url = f"{BASE_URL}/api/users/me"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        user_info = response.json()
        print(f"✅ 获取用户信息成功")
        print(f"用户ID: {user_info['id']}")
        print(f"用户邮箱: {user_info['email']}")
        return user_info
    else:
        print(f"❌ 获取用户信息失败: {response.status_code}")
        print(f"错误信息: {response.text}")
        return None


def main():
    """主函数"""
    print("🔍 开始诊断工具包下载权限问题...")
    
    # 1. 用户登录
    login_result = login(USER_EMAIL, USER_PASSWORD)
    if not login_result:
        print("\n❌ 登录失败，无法继续诊断")
        return
    
    token = login_result["access_token"]
    
    # 2. 获取当前用户信息
    user_info = check_user_info(token)
    if not user_info:
        print("\n❌ 获取用户信息失败，无法继续诊断")
        return
    
    # 3. 获取用户订单
    orders = get_user_orders(token)
    if not orders:
        print("\n❌ 获取订单失败，无法继续诊断")
        return
    
    # 4. 检查订单状态
    order_check_passed = check_order_status(orders, TOOLKIT_ID)
    
    # 5. 测试下载
    download_passed = test_download(token, TOOLKIT_ID)
    
    # 6. 总结
    print("\n" + "="*50)
    print("🔍 诊断总结")
    print("="*50)
    
    if order_check_passed and download_passed:
        print("✅ 诊断完成，未发现问题！")
        print("可能的原因：前端缓存问题，请尝试刷新页面或清除浏览器缓存")
    else:
        print("❌ 诊断发现问题：")
        
        if not order_check_passed:
            print("- 订单状态或产品ID不匹配")
            print("  建议：检查支付回调是否正常工作，订单状态是否正确更新为'paid'")
        
        if not download_passed:
            print("- 下载请求失败")
            print("  建议：检查后端download API实现和权限验证逻辑")
    
    print("\n" + "="*50)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  程序被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 程序执行出错: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
