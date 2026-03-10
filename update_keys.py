#!/usr/bin/env python3
"""
密钥更新脚本
用于生成安全的SECRET_KEY并更新到配置文件中
"""

import secrets
import os
import re

def generate_secure_key():
    """生成安全的密钥"""
    return secrets.token_urlsafe(64)

def update_docker_compose_key(file_path):
    """更新Docker Compose文件中的SECRET_KEY"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 生成新密钥
    new_key = generate_secure_key()
    
    # 替换SECRET_KEY
    updated_content = re.sub(r'SECRET_KEY: "[^"]+"', f'SECRET_KEY: "{new_key}"', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    return new_key

def update_env_file_key(file_path):
    """更新.env文件中的SECRET_KEY"""
    if not os.path.exists(file_path):
        print(f"文件 {file_path} 不存在")
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 生成新密钥
    new_key = generate_secure_key()
    
    # 替换SECRET_KEY
    updated_content = re.sub(r'SECRET_KEY=[^\n]+', f'SECRET_KEY={new_key}', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    return new_key

def main():
    print("=== 密钥更新脚本 ===")
    print()
    
    # 更新Docker Compose文件
    docker_compose_path = "./docker-compose.new.yml"
    if os.path.exists(docker_compose_path):
        new_key = update_docker_compose_key(docker_compose_path)
        print(f"✓ Docker Compose文件已更新，新密钥: {new_key}")
    else:
        print(f"✗ 未找到Docker Compose文件: {docker_compose_path}")
    
    print()
    
    # 更新后端.env.production文件
    env_file_path = "./backend/.env.production"
    if os.path.exists(env_file_path):
        new_key = update_env_file_key(env_file_path)
        if new_key:
            print(f"✓ 后端环境配置文件已更新，新密钥: {new_key}")
    else:
        print(f"✗ 未找到后端环境配置文件: {env_file_path}")
    
    print()
    print("=== 更新完成 ===")
    print("注意：")
    print("1. 请确保在生产环境中使用安全的密钥")
    print("2. 更新密钥后，所有已存在的JWT令牌将失效，用户需要重新登录")
    print("3. 建议定期更新密钥以提高安全性")

if __name__ == "__main__":
    main()