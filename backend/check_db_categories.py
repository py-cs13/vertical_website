import json
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入数据库相关模块
from database import SessionLocal, engine
from models import Content

def check_categories():
    """检查数据库中的文章分类分布情况"""
    print("开始查询数据库分类分布...")
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 查询所有分类
        print("\n1. 查询所有文章的分类...")
        categories = db.query(Content.category).distinct().all()
        category_list = [cat[0] for cat in categories]
        print(f"共找到 {len(category_list)} 个不同的分类:")
        for i, category in enumerate(category_list, 1):
            print(f"  {i}. {category}")
        
        # 统计每个分类的文章数量
        print("\n2. 统计每个分类的文章数量...")
        for category in category_list:
            count = db.query(Content).filter(Content.category == category).count()
            print(f"  '{category}': {count} 篇文章")
        
        # 查询总文章数
        total_count = db.query(Content).count()
        print(f"\n3. 总文章数: {total_count}")
        
        # 获取前5篇文章的示例，查看数据结构
        print("\n4. 前5篇文章示例:")
        sample_articles = db.query(Content).limit(5).all()
        for i, article in enumerate(sample_articles, 1):
            print(f"\n  文章 {i}:")
            print(f"    ID: {article.id}")
            print(f"    标题: {article.title}")
            print(f"    分类: '{article.category}'")
            print(f"    创建时间: {article.created_at}")
            print(f"    内容长度: {len(article.content)} 字符")
            
    except Exception as e:
        print(f"查询数据库时出错: {e}")
    finally:
        # 关闭数据库会话
        db.close()
        print("\n数据库会话已关闭")

if __name__ == "__main__":
    check_categories()
