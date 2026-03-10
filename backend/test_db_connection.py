#!/usr/bin/env python3
"""
PostgreSQL数据库连接测试脚本
用于验证与生产环境PostgreSQL数据库的连接是否正常
"""

import os
import sys
import logging
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError, ProgrammingError

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """测试数据库连接"""
    try:
        # 获取数据库连接字符串
        # 优先从环境变量获取
        from config import Settings
        settings = Settings()
        
        if hasattr(settings, 'DATABASE_URL'):
            database_url = settings.DATABASE_URL
            logger.info(f"正在使用配置文件中的数据库连接字符串: {database_url}")
        else:
            logger.error("配置文件中未找到DATABASE_URL配置")
            return 1
        
        # 创建数据库引擎
        logger.info("正在创建数据库引擎...")
        engine = create_engine(database_url)
        
        # 测试连接
        logger.info("正在测试数据库连接...")
        with engine.connect() as connection:
            # 执行简单查询
            result = connection.execute("SELECT version()")
            version = result.scalar()
            logger.info(f"✅ 数据库连接成功！PostgreSQL版本: {version}")
            
            # 尝试列出数据库表
            try:
                result = connection.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
                tables = [row[0] for row in result]
                if tables:
                    logger.info(f"📋 数据库中存在的表: {tables}")
                else:
                    logger.info("📋 数据库中暂无表")
            except ProgrammingError as e:
                logger.warning(f"⚠️  无法列出表: {e}")
        
        return 0
        
    except OperationalError as e:
        logger.error(f"❌ 数据库连接失败: {e}")
        logger.error("可能的原因：")
        logger.error("1. 数据库服务器未运行")
        logger.error("2. 用户名或密码错误")
        logger.error("3. 网络连接问题")
        logger.error("4. 防火墙阻止连接")
        return 1
    except Exception as e:
        logger.error(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())