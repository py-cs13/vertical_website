import requests
import json

# 测试用户注册功能
url = "http://localhost:8000/api/auth/register"
headers = {"Content-Type": "application/json"}
data = {
    "username": "testuser_new",
    "email": "test_new@example.com",
    "password": "Password123!"  # 包含大写字母和特殊字符
}

print("Testing user registration...")
try:
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
