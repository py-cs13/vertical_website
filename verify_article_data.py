#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证各分类文章数据统计脚本
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from backend.config import Settings

# 获取配置
settings = Settings()

def main():
    """主函数"""
    print("正在连接数据库...")
    
    # 创建数据库引擎
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        print("\n开始统计各分类文章数量...\n")
        
        # 统计所有分类的文章数量
        result = db.execute(
            text("""
            SELECT category, COUNT(*) as article_count 
            FROM contents 
            WHERE is_published = true 
            GROUP BY category 
            ORDER BY category
            """)
        )
        
        # 获取所有分类列表（根据Sidebar.vue中的定义）
        all_categories = ["母婴育儿", "育儿知识", "营养辅食", "产后恢复", "亲子互动", "成长发育", "健康养生", "早期教育"]
        
        # 打印统计结果
        print(f"{'分类名称':<10} {'文章数量':<10} {'状态':<10}")
        print("-" * 30)
        
        # 创建分类计数字典
        category_counts = {row.category: row.article_count for row in result}
        
        # 打印每个分类的统计信息
        all_good = True
        for category in all_categories:
            count = category_counts.get(category, 0)
            status = "✓ 正常" if count > 0 else "✗ 缺失"
            if count == 0:
                all_good = False
            print(f"{category:<10} {count:<10} {status:<10}")
        
        # 统计总文章数
        total_result = db.execute(
            text("""
            SELECT COUNT(*) as total_count 
            FROM contents 
            WHERE is_published = true
            """)
        )
        total_count = total_result.scalar()
        
        print("-" * 30)
        print(f"{'总计':<10} {total_count:<10}")
        
        if all_good:
            print("\n✅ 所有分类均有文章数据，验证通过！")
        else:
            print("\n❌ 部分分类缺少文章数据，请检查！")
        
    except Exception as e:
        print(f"\n发生错误: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
