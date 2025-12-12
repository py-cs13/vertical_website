import requests
import json

# 测试用户登录功能
url = "http://localhost:8000/api/auth/login"
headers = {"Content-Type": "application/json"}
data = {
    "email": "test@example.com",
    "password": "test123456"
}

print("Testing user login...")
try:
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # 如果登录成功，保存token用于后续测试
    if response.status_code == 200:
        token = response.json().get("access_token")
        with open("test_token.txt", "w") as f:
            f.write(token)
        print("Token saved to test_token.txt")
        
        # 测试创建订单功能
        order_url = "http://localhost:8000/api/orders"
        order_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        order_data = {
            "toolkit_id": 1,  # 假设toolkit_id为1
            "quantity": 1
        }
        
        print("\nTesting order creation...")
        order_response = requests.post(order_url, headers=order_headers, data=json.dumps(order_data))
        print(f"Status Code: {order_response.status_code}")
        print(f"Response: {order_response.json()}")
        
except Exception as e:
    print(f"Error: {e}")
