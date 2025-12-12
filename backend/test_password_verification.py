# 测试密码验证功能
from auth import verify_password

def test_password_verification():
    # 从数据库中获取的哈希密码
    hashed_password = "$2b$12$YyhqmKH4MiVGsjOjfIhzsOKs5Qbog3x5e46NS6Rat6GpzA4I7ojre"  # 对应 cs@163.com 的密码哈希
    
    # 测试密码
    test_passwords = [
        "password123",  # 可能的密码
        "123456",      # 简单密码
        "testpassword"  # 测试密码
    ]
    
    print("测试密码验证功能...")
    print(f"哈希密码: {hashed_password}")
    print("\n测试结果:")
    
    for pwd in test_passwords:
        is_valid = verify_password(pwd, hashed_password)
        print(f"密码 '{pwd}' -> {'有效' if is_valid else '无效'}")

if __name__ == "__main__":
    test_password_verification()