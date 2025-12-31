import sys
import os
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

# 添加项目根目录到路径
sys.path.append('/Users/shucui/Desktop/vertical_website/backend')

from models import Content
from config import settings

# 获取数据库URL
DATABASE_URL = settings.DATABASE_URL

def check_articles():
    print("检查数据库中的文章数量...")
    
    # 创建数据库引擎
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # 查询所有已发布的文章（排除工具包）
        articles = session.query(Content).filter(
            Content.is_published == True,
            Content.category != "toolkit"
        ).all()
        
        print(f"数据库中已发布的非工具包文章数量: {len(articles)}")
        
        # 显示前10篇文章
        print("\n前10篇文章:")
        for i, article in enumerate(articles[:10], 1):
            print(f"{i}. {article.title} (ID: {article.id}, 分类: {article.category})")
            
        # 检查是否有ID为None的文章
        articles_without_id = [a for a in articles if a.id is None]
        print(f"\n没有ID的文章数量: {len(articles_without_id)}")
        
        # 检查是否有重复ID
        ids = [a.id for a in articles]
        unique_ids = set(ids)
        if len(ids) != len(unique_ids):
            print("\n警告: 发现重复ID的文章!")
            
    except Exception as e:
        print(f"检查失败: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    check_articles()