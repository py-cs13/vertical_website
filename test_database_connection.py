#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库连接测试脚本
用于测试PostgreSQL和Redis数据库连接是否正常
"""

import sys
import psycopg2
import redis
from psycopg2 import OperationalError

# PostgreSQL数据库连接信息
PG_HOST = "101.43.177.216"
PG_PORT = 5432
PG_DATABASE = "vertical_website"
PG_USER = "vertical_user"
PG_PASSWORD = "pg123456"

# Redis数据库连接信息
REDIS_HOST = "101.43.177.216"
REDIS_PORT = 6379
REDIS_PASSWORD = "redis123456"
REDIS_DB = 0


def test_postgresql_connection():
    """测试PostgreSQL数据库连接"""
    print("\n=== 测试PostgreSQL数据库连接 ===")
    try:
        # 建立连接
        connection = psycopg2.connect(
            host=PG_HOST,
            port=PG_PORT,
            database=PG_DATABASE,
            user=PG_USER,
            password=PG_PASSWORD
        )
        
        print(f"✓ 成功连接到PostgreSQL数据库")
        print(f"  主机: {PG_HOST}:{PG_PORT}")
        print(f"  数据库: {PG_DATABASE}")
        print(f"  用户: {PG_USER}")
        
        # 创建游标
        cursor = connection.cursor()
        
        # 执行简单查询
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()[0]
        print(f"  PostgreSQL版本: {db_version}")
        
        # 执行表查询
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = cursor.fetchall()
        if tables:
            print(f"  数据库中的表: {[table[0] for table in tables]}")
        else:
            print("  数据库中没有表")
        
        # 关闭连接
        cursor.close()
        connection.close()
        print("✓ PostgreSQL连接测试通过")
        return True
        
    except OperationalError as e:
        print(f"✗ PostgreSQL连接失败: {e}")
        return False
    except Exception as e:
        print(f"✗ PostgreSQL连接测试发生错误: {e}")
        return False


def test_redis_connection():
    """测试Redis数据库连接"""
    print("\n=== 测试Redis数据库连接 ===")
    try:
        # 建立连接
        r = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            db=REDIS_DB,
            decode_responses=True
        )
        
        # 测试连接
        ping_response = r.ping()
        if ping_response:
            print(f"✓ 成功连接到Redis数据库")
            print(f"  主机: {REDIS_HOST}:{REDIS_PORT}")
            print(f"  数据库: {REDIS_DB}")
            
            # 获取Redis信息
            info = r.info()
            print(f"  Redis版本: {info.get('redis_version')}")
            print(f"  已使用内存: {info.get('used_memory_human')}")
            print(f"  客户端连接数: {info.get('connected_clients')}")
            
            # 测试数据操作
            test_key = "test_connection_key"
            test_value = "Hello, Redis!"
            
            # 设置键值对
            r.set(test_key, test_value)
            print(f"✓ 成功设置键: {test_key} = {test_value}")
            
            # 获取键值对
            retrieved_value = r.get(test_key)
            print(f"✓ 成功获取键: {test_key} = {retrieved_value}")
            
            # 删除测试键
            r.delete(test_key)
            print(f"✓ 成功删除测试键: {test_key}")
            
            print("✓ Redis连接测试通过")
            return True
        else:
            print("✗ Redis连接失败: ping响应为False")
            return False
            
    except redis.ConnectionError as e:
        print(f"✗ Redis连接失败: {e}")
        return False
    except Exception as e:
        print(f"✗ Redis连接测试发生错误: {e}")
        return False


if __name__ == "__main__":
    print("数据库连接测试工具")
    print("=" * 40)
    
    # 检查是否安装了必要的依赖
    try:
        import psycopg2
        import redis
    except ImportError as e:
        print(f"✗ 缺少必要的依赖包: {e}")
        print("请先安装依赖:")
        print("pip install psycopg2-binary redis")
        sys.exit(1)
    
    # 测试PostgreSQL连接
    pg_success = test_postgresql_connection()
    
    # 测试Redis连接
    redis_success = test_redis_connection()
    
    print("\n" + "=" * 40)
    print("测试结果汇总:")
    print(f"PostgreSQL: {'✓ 通过' if pg_success else '✗ 失败'}")
    print(f"Redis: {'✓ 通过' if redis_success else '✗ 失败'}")
    
    if pg_success and redis_success:
        print("\n🎉 所有数据库连接测试都通过了!")
        sys.exit(0)
    else:
        print("\n❌ 部分数据库连接测试失败")
        sys.exit(1)
