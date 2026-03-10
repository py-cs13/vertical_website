#!/usr/bin/env python3
"""
数据库迁移脚本：添加浏览历史表
执行命令：python migrations/add_view_history.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from database import engine, SessionLocal
from models import ViewHistory
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def migrate():
    """
    执行数据库迁移，创建浏览历史表
    """
    try:
        logger.info("开始创建浏览历史表...")
        
        with engine.begin() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS view_history (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    article_id INTEGER NOT NULL REFERENCES contents(id) ON DELETE CASCADE,
                    session_id VARCHAR(100),
                    viewed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    UNIQUE (user_id, article_id)
                )
            """))
            
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS ix_view_history_user_id ON view_history(user_id)
            """))
            
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS ix_view_history_article_id ON view_history(article_id)
            """))
            
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS ix_view_history_session_id ON view_history(session_id)
            """))
            
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS ix_view_history_viewed_at ON view_history(viewed_at)
            """))
        
        logger.info("浏览历史表创建成功！")
        return True
        
    except Exception as e:
        logger.error(f"创建浏览历史表失败: {e}")
        return False


def rollback():
    """
    回滚迁移，删除浏览历史表
    """
    try:
        logger.info("开始回滚，删除浏览历史表...")
        
        with engine.begin() as conn:
            conn.execute(text("DROP TABLE IF EXISTS view_history CASCADE"))
        
        logger.info("浏览历史表删除成功！")
        return True
        
    except Exception as e:
        logger.error(f"删除浏览历史表失败: {e}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="浏览历史表迁移脚本")
    parser.add_argument("--rollback", action="store_true", help="回滚迁移")
    args = parser.parse_args()
    
    if args.rollback:
        success = rollback()
    else:
        success = migrate()
    
    sys.exit(0 if success else 1)
