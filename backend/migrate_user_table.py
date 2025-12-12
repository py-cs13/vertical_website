#!/usr/bin/env python3
# 手动迁移User表，添加母婴特色字段

import logging
from logging_config import setup_logging, get_logger
setup_logging()
logger = get_logger(__name__)

from database import engine
import sqlalchemy

# 连接到数据库
conn = engine.connect()

# 直接添加字段，使用IF NOT EXISTS

try:
    # 定义要添加的字段
    fields_to_add = [
        'baby_name VARCHAR(255) NULL',
        'baby_birthday DATE NULL',
        'baby_gender VARCHAR(10) NULL',
        'baby_milestones TEXT NULL'
    ]
    
    for field_def in fields_to_add:
        # 提取字段名
        field_name = field_def.split()[0]
        
        # 使用IF NOT EXISTS添加字段（PostgreSQL语法）
        logger.info(f"添加字段: {field_name}")
        conn.execute(f"ALTER TABLE users ADD COLUMN IF NOT EXISTS {field_def}")
    
    logger.info("数据库表迁移完成")
except Exception as e:
    logger.error(f"数据库迁移失败: {str(e)}")
finally:
    conn.close()