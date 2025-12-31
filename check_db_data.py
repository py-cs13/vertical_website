import sys
import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

# 导入数据库配置和模型
from backend.database import Base, engine, get_db
from backend.models import Content

def check_db_data():
    """检查数据库中的文章和工具包数据"""
    # 创建会话
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = Session()
    
    try:
        print("=== 检查数据库中的文章和工具包数据 ===")
        
        # 查询所有已发布的内容
        all_contents = db.query(Content).filter(Content.is_published == True).order_by(Content.created_at.desc()).all()
        
        print(f"\n已发布内容总数: {len(all_contents)}")
        
        # 分类统计
        articles_count = 0
        toolkits_count = 0
        
        print("\n内容详情:")
        for content in all_contents:
            if content.category == 'toolkit':
                toolkits_count += 1
                content_type = "工具包"
            else:
                articles_count += 1
                content_type = "文章"
            
            print(f"ID: {content.id}, 标题: {content.title}, 类型: {content_type}, 分类: {content.category}, 发布状态: {content.is_published}")
        
        print(f"\n统计结果:")
        print(f"文章数量: {articles_count}")
        print(f"工具包数量: {toolkits_count}")
        
    except Exception as e:
        print(f"查询数据库时发生错误: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_db_data()