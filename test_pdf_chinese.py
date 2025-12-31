import requests
import json
import os

# 测试配置
BASE_URL = "http://localhost:8000"
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "Testpassword123!"

# 注册测试用户
def register_user():
    print("注册测试用户...")
    url = f"{BASE_URL}/api/auth/register"
    payload = {
        "username": "test_chinese_pdf_2",
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    response = requests.post(url, json=payload)
    if response.status_code == 201:
        print("用户注册成功")
        return True
    elif response.status_code == 400:
        print("用户已存在，跳过注册")
        return True
    else:
        print(f"注册失败: {response.status_code}")
        print(f"错误信息: {response.text}")
        return False

# 登录获取JWT令牌
def login():
    print("\n登录获取令牌...")
    url = f"{BASE_URL}/api/auth/login"
    payload = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("登录成功，获取令牌")
        return token
    else:
        print(f"登录失败: {response.status_code}")
        print(f"错误信息: {response.text}")
        return None

# 获取最新工具包
def get_latest_toolkits(token):
    print("\n获取最新工具包...")
    url = f"{BASE_URL}/api/toolkits/latest"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        toolkits = response.json()
        print(f"获取到{len(toolkits)}个工具包")
        return toolkits
    else:
        print(f"获取工具包失败: {response.status_code}")
        return []

# 下载工具包
def download_toolkit(token, toolkit_id, toolkit_title):
    print(f"\n下载工具包: {toolkit_title} (ID: {toolkit_id})...")
    url = f"{BASE_URL}/api/toolkits/{toolkit_id}/download"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, stream=True)
    
    if response.status_code == 200:
        # 提取文件名
        content_disposition = response.headers.get("Content-Disposition", "")
        filename = f"toolkit_{toolkit_id}.pdf"
        
        # 保存文件
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"工具包下载成功，保存为: {filename}")
        print(f"文件大小: {os.path.getsize(filename)} bytes")
        return filename
    else:
        print(f"下载失败: {response.status_code}")
        print(f"错误信息: {response.text}")
        return None

# 主测试函数
def main():
    # 注册用户
    if not register_user():
        return
    
    # 登录获取令牌
    token = login()
    if not token:
        return
    
    # 获取工具包列表
    toolkits = get_latest_toolkits(token)
    if not toolkits:
        return
    
    # 选择第一个工具包
    toolkit = toolkits[0]
    
    # 创建订单
    print(f"\n创建订单: {toolkit['title']} (ID: {toolkit['id']})...")
    order_url = f"{BASE_URL}/api/orders"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    order_payload = {
        "product_type": "toolkit",
        "product_id": toolkit["id"],
        "product_name": toolkit["title"],
        "product_price": float(toolkit["price"]),
        "quantity": 1
    }
    
    order_response = requests.post(order_url, headers=headers, json=order_payload)
    if order_response.status_code != 201:
        print(f"创建订单失败: {order_response.status_code}")
        print(f"错误信息: {order_response.text}")
        return
    
    order_data = order_response.json()
    order_id = order_data["id"]
    print(f"订单创建成功: ID={order_id}")
    
    # 模拟支付
    print(f"\n模拟支付订单: {order_id}...")
    pay_url = f"{BASE_URL}/api/orders/{order_id}/pay"
    pay_response = requests.post(pay_url, headers=headers)
    if pay_response.status_code != 200:
        print(f"支付失败: {pay_response.status_code}")
        print(f"错误信息: {pay_response.text}")
        return
    
    pay_data = pay_response.json()
    print(f"订单支付成功: 状态={pay_data['status']}")
    
    # 下载工具包
    filename = download_toolkit(token, toolkit["id"], toolkit["title"])
    
    if filename:
        print(f"\n测试完成！下载的文件: {os.path.abspath(filename)}")
        print("请打开该文件检查中文是否正常显示")

if __name__ == "__main__":
    main()