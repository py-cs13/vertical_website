import requests
import json

# 测试购买API
def test_purchase_api():
    url = "http://localhost:8000/api/orders"
    
    # 准备测试数据
    order_data = {
        "product_type": "toolkit",
        "product_id": 1,
        "amount": 99.0,
        "items": [
            {
                "product_name": "测试工具包",
                "product_price": 99.0,
                "quantity": 1,
                "total_amount": 99.0
            }
        ]
    }
    
    # 添加测试用户token（模拟已登录状态）
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer test_token_123"
    }
    
    print("=== 测试购买API ===")
    print(f"请求URL: {url}")
    print(f"请求数据: {json.dumps(order_data, indent=2)}")
    
    try:
        response = requests.post(url, json=order_data, headers=headers)
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            print("\n✅ 购买API调用成功！")
            return True
        else:
            print(f"\n❌ 购买API调用失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"\n❌ 请求失败: {e}")
        return False

if __name__ == "__main__":
    test_purchase_api()
