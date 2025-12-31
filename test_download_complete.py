#!/usr/bin/env python3
"""
完整测试工具包下载流程，包括用户注册、认证和PDF生成
"""

import sys
import os
import requests
import json

# 添加项目根目录和backend目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

# 设置环境变量，确保能够正确导入模块
os.environ["PYTHONPATH"] = os.path.dirname(os.path.abspath(__file__)) + ":" + os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend") + ":" + os.environ.get("PYTHONPATH", "")

# 配置
BASE_URL = "http://localhost:8000"
REGISTER_ENDPOINT = f"{BASE_URL}/api/auth/register"
LOGIN_ENDPOINT = f"{BASE_URL}/api/auth/login"

# 生成随机测试用户凭据
random_suffix = os.urandom(4).hex()
TEST_USER = {
    "username": f"testuser_{random_suffix}",
    "email": f"test_{random_suffix}@example.com",
    "password": "Password123!"
}

# 创建测试内容
test_content = {
    "title": "母婴护理工具包",
    "content": "# 母婴护理工具包\n\n## 一、新生儿护理指南\n\n### 1. 日常护理\n\n- 每天给宝宝洗澡1-2次\n- 使用温和的婴儿洗发水和沐浴露\n- 保持宝宝皮肤清洁干燥\n\n### 2. 喂养建议\n\n- 母乳喂养最好持续6个月以上\n- 配方奶喂养要按照说明配比\n- 按需喂养，不要强迫宝宝进食\n\n## 二、育儿工具推荐\n\n1. 婴儿体温计\n2. 奶瓶消毒器\n3. 婴儿抚触油\n4. 防溢乳垫\n\n## 三、常见问题解答\n\nQ: 宝宝晚上哭闹怎么办？\nA: 可能是饥饿、尿布湿了或者需要安抚，可以尝试喂奶、更换尿布或轻拍安抚。\n\nQ: 如何判断宝宝是否吃饱？\nA: 观察宝宝的体重增长、尿量和排便情况，吃饱的宝宝通常会自动停止吸吮。\n"
}

def register():
    """注册新用户"""
    print("正在注册新用户...")
    print(f"使用测试邮箱: {TEST_USER['email']}")
    print(f"使用测试用户名: {TEST_USER['username']}")
    try:
        response = requests.post(REGISTER_ENDPOINT, json=TEST_USER)
        if response.status_code == 201:
            print("✅ 用户注册成功！")
            return True
        else:
            print(f"❌ 注册失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ 注册请求失败: {e}")
        return False

def login():
    """登录获取token"""
    print("\n正在登录...")
    try:
        # 只传递email和password用于登录
        login_data = {"email": TEST_USER["email"], "password": TEST_USER["password"]}
        response = requests.post(LOGIN_ENDPOINT, json=login_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            if token:
                print(f"✅ 登录成功！Token: {token[:20]}...")
                return token
        print(f"❌ 登录失败: {response.status_code} - {response.text}")
        return None
    except Exception as e:
        print(f"❌ 登录请求失败: {e}")
        return None

def download_toolkit(token):
    """测试下载工具包"""
    print("\n正在下载工具包...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        # 从数据库获取工具包列表
        from database import get_db
        from models import Content
        
        db = next(get_db())
        toolkits = db.query(Content).filter(Content.category == "toolkit", Content.is_published == True).all()
        db.close()
        
        if not toolkits:
            print("❌ 未找到可用的工具包")
            return False
        
        # 使用第一个工具包进行测试
        toolkit_id = toolkits[0].id
        toolkit_name = toolkits[0].title
        print(f"使用工具包 ID: {toolkit_id}, 名称: {toolkit_name}")
        
        # 先购买工具包
        print("\n正在购买工具包...")
        
        # 从数据库获取工具包的价格信息
        db = next(get_db())
        toolkit = db.query(Content).filter(Content.id == toolkit_id).first()
        db.close()
        
        if not toolkit:
            print("❌ 未找到工具包信息")
            return False
        
        # 设置工具包价格（使用数据库中的价格或默认值）
        price = float(toolkit.price) if toolkit.price else 99.99
        
        # 构造正确的订单数据格式
        purchase_data = {
            "product_type": "toolkit",
            "product_id": toolkit_id,
            "amount": price,
            "items": [
                {
                    "product_name": toolkit.title,
                    "product_price": price,
                    "quantity": 1,
                    "total_amount": price
                }
            ]
        }
        
        # 创建订单
        purchase_response = requests.post(
            f"{BASE_URL}/api/orders",
            headers=headers,
            json=purchase_data
        )
        
        if purchase_response.status_code == 201:
            order_data = purchase_response.json()
            print(f"✅ 订单创建成功！订单ID: {order_data['id']}, 订单号: {order_data['order_number']}")
            
            # 在测试环境下，直接模拟支付完成
            print("\n正在模拟支付完成...")
            pay_url = f"{BASE_URL}/api/orders/{order_data['id']}/pay"
            pay_data = {
                "order_id": order_data['id'],
                "payment_method": "test"
            }
            
            pay_response = requests.post(
                pay_url,
                headers=headers,
                json=pay_data
            )
            
            if pay_response.status_code == 200:
                print("✅ 支付成功！订单已完成")
            else:
                print(f"⚠️  支付请求返回: {pay_response.status_code} - {pay_response.text}")
        else:
            print(f"⚠️  购买请求返回: {purchase_response.status_code} - {purchase_response.text}")
        
        # 构建下载URL
        DOWNLOAD_ENDPOINT = f"{BASE_URL}/api/toolkits/{toolkit_id}/download"
        
        # 发送下载请求
        response = requests.get(DOWNLOAD_ENDPOINT, headers=headers, stream=True)
        if response.status_code == 200:
            # 检查响应头
            content_type = response.headers.get("content-type")
            content_disposition = response.headers.get("content-disposition")
            
            print(f"✅ 下载请求成功！")
            print(f"   状态码: {response.status_code}")
            print(f"   内容类型: {content_type}")
            print(f"   内容处理: {content_disposition}")
            
            # 保存文件
            filename = "downloaded_toolkit.pdf"
            with open(filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            print(f"✅ 文件已保存为: {filename}")
            print(f"   文件大小: {os.path.getsize(filename)} 字节")
            return True
        else:
            print(f"❌ 下载失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ 下载请求失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pdf_generator():
    """测试PDF生成器"""
    print("\n正在测试PDF生成器...")
    
    try:
        from backend.pdf_generator import PDFGenerator
        
        # 创建PDF生成器实例
        pdf_gen = PDFGenerator()
        
        # 生成PDF
        pdf_buffer = pdf_gen.generate_toolkit_pdf(test_content)
        
        # 保存为文件
        output_path = "generated_pdf_test.pdf"
        with open(output_path, 'wb') as f:
            f.write(pdf_buffer.getvalue())
        
        print(f"✅ PDF生成成功！文件保存为: {output_path}")
        print(f"   文件大小: {os.path.getsize(output_path)} 字节")
        return True
    except Exception as e:
        print(f"❌ PDF生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("=== 工具包下载完整测试 ===\n")
    
    # 1. 测试PDF生成器
    test_pdf_generator()
    
    # 2. 测试注册、登录和下载
    register_success = register()
    if register_success:
        token = login()
        if token:
            download_toolkit(token)
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    main()
