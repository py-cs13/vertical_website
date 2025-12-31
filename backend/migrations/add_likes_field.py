# 数据库迁移脚本：添加likes字段
# 运行方式: python migrations/add_likes_field.py

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import engine
from sqlalchemy import text

def migrate():
    """添加likes字段到contents表"""
    print("开始数据库迁移：添加likes字段...")
    
    try:
        # 检查字段是否已存在
        check_sql = text("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name='contents' AND column_name='likes'
        """)
        with engine.connect() as conn:
            result = conn.execute(check_sql)
            existing = result.fetchone()
            
            if existing:
                print("✅ likes字段已存在，无需迁移")
                return
            
        # 添加likes字段
        alter_sql = text("""
            ALTER TABLE contents ADD COLUMN likes INTEGER DEFAULT 0 NOT NULL
        """)
        with engine.connect() as conn:
            conn.execute(alter_sql)
            conn.commit()
            print("✅ likes字段添加成功！")
            
    except Exception as e:
        print(f"❌ 迁移失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    migrate()
