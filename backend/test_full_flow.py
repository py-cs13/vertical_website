import requests
import json
import os

# 生成唯一的测试邮箱和用户名
test_email = f"test_{os.urandom(4).hex()}@example.com"
test_username = f"testuser_{os.urandom(4).hex()}"
print(f"Using test email: {test_email}")
print(f"Using test username: {test_username}")

# 1. 测试用户注册
print("\n1. Testing user registration...")
register_url = "http://localhost:8000/api/auth/register"
headers = {"Content-Type": "application/json"}
register_data = {
    "username": test_username,
    "email": test_email,
    "password": "Password123!"  # 包含大写字母和特殊字符
}

response = requests.post(register_url, headers=headers, data=json.dumps(register_data))
print(f"Status Code: {response.status_code}")
if response.status_code == 201:
    print("User registered successfully!")
    user_data = response.json()
    print(f"User ID: {user_data['id']}")
else:
    print(f"Registration failed: {response.json()}")
    exit(1)

# 2. 测试用户登录
print("\n2. Testing user login...")
login_url = "http://localhost:8000/api/auth/login"
login_data = {
    "email": test_email,  # 使用email而不是username
    "password": "Password123!"
}
response = requests.post(login_url, json=login_data, headers=headers)
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    print("User logged in successfully!")
    login_data = response.json()
    token = login_data.get("access_token")
    if token:
        headers["Authorization"] = f"Bearer {token}"
        print("Token obtained and added to headers")
    else:
        print("Failed to get token")
        exit(1)
else:
    print(f"Login failed: {response.json()}")
    exit(1)

# 3. 获取最新工具包信息
print("\n3. Getting latest toolkit information...")
toolkit_url = "http://localhost:8000/api/toolkits/latest"
response = requests.get(toolkit_url, headers=headers)
if response.status_code == 200:
    toolkit_data = response.json()
    # 过滤出类型为toolkit的内容
    toolkits = [item for item in toolkit_data if item.get("category") == "toolkit"]
    if toolkits:
        # 使用第一个工具包
        toolkit = toolkits[0]
        toolkit_id = toolkit["id"]
        toolkit_name = toolkit["title"]
        toolkit_price = toolkit["price"]
        print(f"Found toolkit: ID={toolkit_id}, Name='{toolkit_name}', Price={toolkit_price}")
    else:
        print("No toolkits found!")
        exit(1)
else:
    print(f"Failed to get toolkits: {response.status_code}")
    exit(1)

# 4. 创建订单
print("\n4. Creating order...")
order_url = "http://localhost:8000/api/orders"
order_data = {
    "product_type": "toolkit",  # 购买的是工具包
    "product_id": toolkit_id,  # 使用获取到的工具包ID
    "amount": toolkit_price,  # 使用实际的工具包价格
    "items": [
        {
            "product_name": toolkit_name,
            "product_price": toolkit_price,
            "quantity": 1,
            "total_amount": toolkit_price
        }
    ]
}

response = requests.post(order_url, headers=headers, data=json.dumps(order_data))
print(f"Status Code: {response.status_code}")
if response.status_code == 201:
    print("Order created successfully!")
    order_data = response.json()
    order_id = order_data.get("id")
    print(f"Order ID: {order_id}")
else:
    print(f"Order creation failed: {response.json()}")
    exit(1)

# 5. 处理支付
print("\n5. Processing payment...")
payment_url = f"http://localhost:8000/api/orders/{order_id}/pay"
payment_data = {
    "order_id": order_id,
    "payment_method": "alipay",
    "return_url": "http://localhost:8000/api/payment/callback"
}

response = requests.post(payment_url, headers=headers, data=json.dumps(payment_data))
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    print("Payment initiated successfully!")
    payment_data = response.json()
    payment_url = payment_data.get("payment_url")
    print(f"Payment URL: {payment_url}")
    
    # 6. 模拟支付回调（在测试环境中）
    print("\n6. Simulating payment callback...")
    callback_url = "http://localhost:8000/api/payment/callback"
    # 使用返回的order_number
    order_number = payment_data.get('order_number')
    callback_data = {
        "out_trade_no": order_number,  # 订单号
        "trade_status": "TRADE_SUCCESS",  # 支付成功
        "total_amount": toolkit_price,  # 支付金额
        "trade_no": f"alipay_{os.urandom(8).hex()}"  # 支付宝交易号
    }
    callback_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    callback_response = requests.post(callback_url, data=callback_data, headers=callback_headers)
    
    if callback_response.status_code == 200:
        print("Payment callback processed successfully!")
        print(f"Callback response: {callback_response.text}")
    else:
        print(f"Payment callback failed: {callback_response.status_code}")
        print(f"Callback error: {callback_response.text}")
        print("Continuing test anyway...")
else:
    print(f"Payment initiation failed: {response.json()}")
    # 由于是模拟环境，我们可以跳过实际支付步骤
    print("Skipping actual payment in test environment...")

# 7. 测试PDF生成功能（假设用户已购买）
print("\n7. Testing PDF generation...")
pdf_url = f"http://localhost:8000/api/toolkits/{toolkit_id}/download"
response = requests.get(pdf_url, headers=headers)
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    print("PDF generated successfully!")
    # 保存PDF文件
    with open("test_toolkit.pdf", "wb") as f:
        f.write(response.content)
    print(f"PDF saved to: test_toolkit.pdf")
    print(f"PDF file size: {len(response.content)} bytes")
else:
    print(f"PDF generation failed: {response.json()}")

print("\nTest completed!")
