import sys
import os
from sqlalchemy import create_engine, text

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

# 导入数据库配置
from backend.config import Settings

def fix_view_count():
    """修复文章的view_count为NULL的问题"""
    # 获取配置
    settings = Settings()
    
    print("=== 修复文章view_count字段 ===")
    
    # 创建数据库引擎
    engine = create_engine(settings.DATABASE_URL)
    
    try:
        # 连接数据库并创建事务
        with engine.begin() as conn:
            # 更新view_count为NULL的记录
            result = conn.execute(
                text("UPDATE contents SET view_count = 0 WHERE view_count IS NULL")
            )
            
            print(f"成功修复 {result.rowcount} 条记录")
            print("所有文章的view_count字段已设置为0")
    
    except Exception as e:
        print(f"修复过程中发生错误: {e}")

if __name__ == "__main__":
    fix_view_count()