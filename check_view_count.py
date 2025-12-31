import sys
import os
from sqlalchemy import create_engine, text

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

# 导入数据库配置
from backend.config import Settings

def check_view_count():
    """检查文章的view_count字段值"""
    # 获取配置
    settings = Settings()
    
    print("=== 检查文章view_count字段 ===")
    
    # 创建数据库引擎
    engine = create_engine(settings.DATABASE_URL)
    
    try:
        # 连接数据库
        with engine.connect() as conn:
            # 查询所有文章的view_count值
            result = conn.execute(
                text("SELECT id, title, view_count FROM contents ORDER BY id DESC")
            )
            
            print("\n文章view_count详情:")
            has_null = False
            
            for row in result:
                print(f"ID: {row.id}, 标题: {row.title}, view_count: {row.view_count} (类型: {type(row.view_count).__name__})")
                if row.view_count is None:
                    has_null = True
            
            if has_null:
                print("\n警告: 发现view_count为NULL的记录！")
            else:
                print("\n所有文章的view_count字段都有有效值")
                
    except Exception as e:
        print(f"检查过程中发生错误: {e}")

if __name__ == "__main__":
    check_view_count()