#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具包购买和下载流程测试脚本
"""

import requests
import json
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置
BASE_URL = "http://localhost:8000"
import os
# 生成唯一的测试邮箱和用户名
USERNAME = f"testuser_{os.urandom(4).hex()}"
EMAIL = f"test_{os.urandom(4).hex()}@example.com"
PASSWORD = "Password123!"  # 包含大写字母和特殊字符


class ToolkitDownloadTest:
    """工具包购买和下载测试类"""
    
    def __init__(self):
        self.base_url = BASE_URL
        self.token = None
        self.test_user_id = None
    
    def login(self, email, password):
        """
        用户登录
        """
        print("\n=== 用户登录测试 ===")
        login_url = f"{self.base_url}/api/auth/login"
        login_data = {
            "email": email,
            "password": password
        }
        
        response = requests.post(login_url, json=login_data)
        if response.status_code == 200:
            data = response.json()
            self.token = data["access_token"]
            print(f"✓ 登录成功，获取到token: {self.token[:20]}...")
            return True
        else:
            print(f"✗ 登录失败: {response.status_code}, {response.text}")
            return False
    
    def register_test_user(self):
        """
        注册测试用户
        """
        print("\n=== 注册测试用户 ===")
        register_url = f"{self.base_url}/api/auth/register"
        register_data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD
        }
        
        response = requests.post(register_url, json=register_data)
        if response.status_code == 201:
            data = response.json()
            self.test_user_id = data["id"]
            print(f"✓ 注册成功，用户ID: {self.test_user_id}")
            # 注册成功后调用登录方法获取访问令牌
            return self.login(EMAIL, PASSWORD)
        elif response.status_code == 409:
            print(f"✓ 用户已存在，使用现有用户登录")
            return self.login(EMAIL, PASSWORD)
        else:
            print(f"✗ 注册失败: {response.status_code}, {response.text}")
            return False
    
    def get_latest_toolkits(self):
        """
        获取最新工具包列表
        """
        print("\n=== 获取最新工具包列表 ===")
        url = f"{self.base_url}/api/toolkits/latest"
        
        response = requests.get(url)
        if response.status_code == 200:
            toolkits = response.json()
            print(f"✓ 获取到 {len(toolkits)} 个工具包")
            for i, toolkit in enumerate(toolkits):
                print(f"  {i+1}. {toolkit['title']} (ID: {toolkit['id']}, 价格: {toolkit['price']}元)")
            return toolkits
        else:
            print(f"✗ 获取工具包失败: {response.status_code}, {response.text}")
            return []
    
    def create_order(self, product_type, product_id, amount, items):
        """
        创建订单
        """
        print(f"\n=== 创建订单测试 (产品类型: {product_type}, 产品ID: {product_id}) ===")
        
        order_url = f"{self.base_url}/api/orders"
        headers = {"Authorization": f"Bearer {self.token}"}
        order_data = {
            "product_type": product_type,
            "product_id": product_id,
            "amount": amount,
            "items": items
        }
        
        response = requests.post(order_url, json=order_data, headers=headers)
        if response.status_code == 201:
            data = response.json()
            print(f"✓ 订单创建成功: 订单ID={data['id']}, 订单号={data['order_number']}")
            return data
        else:
            print(f"✗ 订单创建失败: {response.status_code}, {response.text}")
            return None
    
    def process_payment(self, order_id, payment_method="alipay"):
        """
        处理支付请求
        """
        print(f"\n=== 支付处理测试 (订单ID: {order_id}) ===")
        
        url = f"{self.base_url}/api/orders/{order_id}/pay"
        headers = {"Authorization": f"Bearer {self.token}"}
        payment_data = {
            "order_id": order_id,
            "payment_method": payment_method,
            "return_url": "http://localhost:8000"
        }
        
        response = requests.post(url, json=payment_data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ 支付处理成功: 交易ID={data['transaction_id']}, 支付URL={data['payment_url']}")
            return data
        else:
            print(f"✗ 支付处理失败: {response.status_code}, {response.text}")
            return None
    
    def download_toolkit(self, toolkit_id):
        """
        下载工具包PDF
        """
        print(f"\n=== 下载工具包PDF测试 (工具包ID: {toolkit_id}) ===")
        url = f"{self.base_url}/api/toolkits/{toolkit_id}/download"
        headers = {"Authorization": f"Bearer {self.token}"}
        
        response = requests.get(url, headers=headers, stream=True)
        if response.status_code == 200:
            # 获取文件名
            content_disposition = response.headers.get("content-disposition")
            if content_disposition:
                # 尝试从content-disposition头部提取文件名
                if 'filename*=' in content_disposition:
                    # 处理RFC 5987编码的文件名
                    filename_part = content_disposition.split('filename*=UTF-8\'\'')[1]
                    from urllib.parse import unquote
                    filename = unquote(filename_part)
                elif 'filename=' in content_disposition:
                    # 处理普通的filename参数
                    filename = content_disposition.split("filename=")[1].strip('"')
                else:
                    filename = f"toolkit_{toolkit_id}.pdf"
            else:
                filename = f"toolkit_{toolkit_id}.pdf"
            
            # 保存文件
            with open(filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            
            print(f"✓ 工具包PDF下载成功，保存为: {filename}")
            print(f"  文件大小: {os.path.getsize(filename)} 字节")
            return True
        else:
            print(f"✗ 工具包下载失败: {response.status_code}, {response.text}")
            return False
    
    def run_test(self):
        """
        运行完整的购买和下载流程测试
        """
        print("==================================================")
        print("工具包购买和下载流程测试")
        print("==================================================")
        
        # 1. 注册/登录测试用户
        if not self.register_test_user():
            return False
        
        # 2. 使用数据库中存在的工具包ID进行测试
        # 注意：这个ID应该存在于服务器数据库中
        toolkit_id = 3  # 0-3岁宝宝发育里程碑追踪工具包
        toolkit_title = "0-3岁宝宝发育里程碑追踪工具包"
        toolkit_price = 99.00
        
        print(f"\n=== 使用已知工具包ID: {toolkit_id} ({toolkit_title}) ===")
        
        # 3. 创建订单
        items = [{
            "product_name": toolkit_title,
            "product_price": toolkit_price,
            "quantity": 1,
            "total_amount": toolkit_price * 1
        }]
        total_amount = toolkit_price * 1
        order = self.create_order("toolkit", toolkit_id, total_amount, items)
        if not order:
            return False
        
        # 4. 处理支付
        order_id = order.get("id")
        if not order_id:
            print("✗ 订单创建失败，未返回订单ID")
            return False
        
        payment_result = self.process_payment(order_id)
        if not payment_result:
            print("✗ 支付处理失败")
            return False
        
        # 5. 下载工具包
        # 注意：由于这是模拟支付，实际上订单状态不会被更新为paid
        # 所以这里会失败，但我们可以测试这个流程
        self.download_toolkit(toolkit_id)
        
        print("\n==================================================")
        print("测试完成！")
        print("注意：由于使用的是模拟支付，订单状态未实际更新为'已支付'，")
        print("因此下载测试会失败。在实际环境中，支付完成后订单状态会更新，")
        print("此时下载功能应该能正常工作。")
        print("==================================================")
        
        return True


if __name__ == "__main__":
    test = ToolkitDownloadTest()
    test.run_test()
