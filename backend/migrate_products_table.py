#!/usr/bin/env python3
# 创建products表迁移脚本

import logging
from logging_config import setup_logging, get_logger
setup_logging()
logger = get_logger(__name__)

from database import engine
import sqlalchemy

# 连接到数据库
conn = engine.connect()

try:
    logger.info("开始创建products表...")
    
    # 创建products表的SQL语句
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name VARCHAR(200) NOT NULL,
        description TEXT,
        image_url VARCHAR(500) NOT NULL,
        link_url VARCHAR(500) NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        category VARCHAR(50) NOT NULL,
        is_active BOOLEAN DEFAULT TRUE,
        click_count INTEGER DEFAULT 0,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """
    
    conn.execute(create_table_sql)
    
    # 创建索引
    logger.info("创建索引...")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_products_is_active ON products(is_active);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_products_created_at ON products(created_at);")
    
    logger.info("products表创建成功")
    
except Exception as e:
    logger.error(f"创建products表失败: {str(e)}")
finally:
    conn.close()