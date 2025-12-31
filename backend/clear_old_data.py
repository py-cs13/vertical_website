#!/usr/bin/env python3
"""
清除数据库中的旧文章和工具包数据
"""

import logging
from sqlalchemy.orm import Session
from models import Content, User
from database import engine

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def clear_old_data():
    """清除数据库中的旧内容数据"""
    logger.info("开始清除旧数据...")
    
    with Session(engine) as session:
        try:
            # 统计现有数据
            old_content_count = session.query(Content).count()
            
            logger.info(f"当前数据库中有 {old_content_count} 条内容数据")
            
            # 删除所有内容数据
            session.query(Content).delete()
            session.commit()
            
            logger.info("旧数据清除完成！")
            logger.info(f"共删除了 {old_content_count} 条内容数据")
            
        except Exception as e:
            logger.error(f"清除数据时发生错误: {e}")
            session.rollback()
            raise

if __name__ == "__main__":
    clear_old_data()
