"""
合并分类脚本：将11个分类精简为8个核心分类
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models import Content
from sqlalchemy import text

# 分类映射关系
CATEGORY_MAPPING = {
    # 合并到孕期指南
    "孕期营养": "孕期指南",
    "营养食谱": "孕期指南",
    
    # 产后恢复保持不变
    "产后恢复": "产后恢复",
    
    # 合并到婴儿护理
    "婴儿护理": "婴儿护理",
    "宝宝护理": "婴儿护理",
    
    # 合并到宝宝健康
    "母婴健康": "宝宝健康",
    
    # 合并到早教启蒙
    "幼儿教育": "早教启蒙",
    
    # 亲子游戏保持不变
    "亲子游戏": "亲子游戏",
    
    # 合并到育儿知识
    "育儿知识": "育儿知识",
    "育儿经验": "育儿知识",
    
    # 母婴用品保持不变
    "母婴用品": "母婴用品"
}

def merge_categories():
    """合并分类"""
    session = SessionLocal()
    
    # 显示当前分类统计
    print("📊 当前分类统计：")
    result = session.execute(text("SELECT category, COUNT(*) FROM contents GROUP BY category ORDER BY COUNT(*) DESC"))
    for row in result:
        print(f"  - {row[0]}：{row[1]}篇")
    
    print("\n🔄 开始合并分类...")
    
    updated_count = 0
    for old_cat, new_cat in CATEGORY_MAPPING.items():
        # 查找该分类的文章
        articles = session.query(Content).filter(Content.category == old_cat).all()
        if articles:
            for article in articles:
                article.category = new_cat
            updated_count += len(articles)
            print(f"  ✅ {old_cat} → {new_cat}（{len(articles)}篇）")
    
    session.commit()
    
    # 显示合并后的分类
    print("\n📊 合并后的分类统计：")
    result = session.execute(text("SELECT category, COUNT(*) FROM contents GROUP BY category ORDER BY COUNT(*) DESC"))
    for row in result:
        print(f"  - {row[0]}：{row[1]}篇")
    
    session.close()
    
    print(f"\n🎉 共更新 {updated_count} 篇文章的分类")
    
    # 最终分类数量
    unique_cats = set(CATEGORY_MAPPING.values())
    print(f"📁 从 {len(CATEGORY_MAPPING)} 个分类合并为 {len(unique_cats)} 个核心分类")
    print(f"   核心分类列表：{', '.join(sorted(unique_cats))}")

if __name__ == "__main__":
    merge_categories()
