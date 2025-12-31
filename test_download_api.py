import requests
import json
import random

# 测试下载API的脚本

def test_download_api():
    # 生成随机用户名，避免重复
    random_suffix = random.randint(1000, 9999)
    test_email = f"testuser{random_suffix}@example.com"
    test_password = "TestPassword123!"  # 符合密码要求：包含大写字母和特殊字符
    
    # 1. 首先注册一个测试用户
    register_url = "http://localhost:8000/api/auth/register"
    register_data = {
        "email": test_email,
        "password": test_password,
        "confirm_password": test_password,
        "username": f"testuser{random_suffix}"
    }
    
    print("正在注册测试用户...")
    register_response = requests.post(register_url, json=register_data)
    print(f"注册状态码: {register_response.status_code}")
    print(f"注册响应: {register_response.text}")
    
    if register_response.status_code != 201:
        print("注册失败，无法测试下载功能")
        return
    
    # 2. 然后进行用户登录
    login_url = "http://localhost:8000/api/auth/login"
    login_data = {
        "email": test_email,
        "password": test_password
    }
    
    print("\n正在登录...")
    login_response = requests.post(login_url, json=login_data)
    print(f"登录状态码: {login_response.status_code}")
    print(f"登录响应: {login_response.text}")
    
    if login_response.status_code != 200:
        print("登录失败，无法测试下载功能")
        return
    
    # 3. 获取JWT令牌
    token = login_response.json().get("access_token")
    if not token:
        print("无法获取令牌")
        return
    
    # 4. 获取工具包列表
    toolkits_url = "http://localhost:8000/api/toolkits"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    print("\n正在获取工具包列表...")
    toolkits_response = requests.get(toolkits_url, headers=headers)
    print(f"工具包列表状态码: {toolkits_response.status_code}")
    print(f"工具包列表响应: {toolkits_response.text}")
    
    toolkits = toolkits_response.json()
    if not isinstance(toolkits, list) or not toolkits:
        print("没有找到工具包")
        return
    
    # 5. 选择第一个工具包进行测试
    toolkit = toolkits[0]
    toolkit_id = toolkit["id"]
    toolkit_name = toolkit["title"]
    toolkit_price = toolkit.get("price", 0.01)  # 获取工具包价格
    print(f"\n选择测试工具包: {toolkit_name} (ID: {toolkit_id}, 价格: {toolkit_price})")
    
    # 6. 创建订单
    order_url = "http://localhost:8000/api/orders"
    order_data = {
        "product_type": "toolkit",
        "product_id": toolkit_id,
        "amount": toolkit_price,
        "items": [
            {
                "product_name": toolkit_name,
                "product_price": toolkit_price,
                "quantity": 1,
                "total_amount": toolkit_price
            }
        ]
    }
    
    print("\n正在创建订单...")
    order_response = requests.post(order_url, json=order_data, headers=headers)
    print(f"创建订单状态码: {order_response.status_code}")
    print(f"创建订单响应: {order_response.text}")
    
    if order_response.status_code != 201:
        print("创建订单失败，无法测试下载功能")
        return
    
    order = order_response.json()
    order_id = order.get("id")
    if not order_id:
        print("无法获取订单ID")
        return
    
    # 7. 支付订单
    pay_url = f"http://localhost:8000/api/orders/{order_id}/pay"
    pay_data = {
        "order_id": order_id,
        "payment_method": "alipay",
        "amount": toolkit_price
    }
    
    print("\n正在支付订单...")
    pay_response = requests.post(pay_url, json=pay_data, headers=headers)
    print(f"支付订单状态码: {pay_response.status_code}")
    print(f"支付订单响应: {pay_response.text}")
    
    if pay_response.status_code != 200:
        print("支付订单失败，无法测试下载功能")
        return
    
    # 8. 测试下载API
    download_url = f"http://localhost:8000/api/toolkits/{toolkit_id}/download"
    
    print(f"\n正在测试下载API: {download_url}")
    try:
        download_response = requests.get(download_url, headers=headers, stream=True)
        print(f"下载状态码: {download_response.status_code}")
        print(f"响应头: {json.dumps(dict(download_response.headers), indent=2)}")
        
        if download_response.status_code == 200:
            # 保存文件
            content_disposition = download_response.headers.get("content-disposition")
            if content_disposition and "filename\*=UTF-8''" in content_disposition:
                filename = content_disposition.split("filename\*=UTF-8''")[1].strip()
                filename = filename.encode('latin-1').decode('utf-8')
            else:
                filename = f"{toolkit_name}.pdf"
            
            with open(filename, "wb") as f:
                for chunk in download_response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            print(f"文件下载成功，保存为: {filename}")
        else:
            print(f"下载失败，错误内容: {download_response.text}")
            
    except Exception as e:
        print(f"下载过程中出现异常: {str(e)}")

if __name__ == "__main__":
    test_download_api()
