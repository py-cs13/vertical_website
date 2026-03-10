#!/usr/bin/env python3
"""
更新文章分类为优化后的8个大类
"""

from database import get_db
from models import Content

# 分类映射关系
CATEGORY_MAPPING = {
    '母婴育儿': '新生照顾',
    '育儿知识': '幼儿发展',
    '营养辅食': '营养健康',
    '产后恢复': '产后恢复',
    '亲子互动': '亲子互动',
    '亲子游戏': '亲子互动',
    '成长发育': '幼儿发展',
    '早期教育': '早期教育',
    '早教启蒙': '早期教育',
    '健康养生': '营养健康',
    '婴儿护理': '新生照顾',
    '宝宝健康': '新生照顾',
    '母婴用品': '育儿用品',
    '孕期指南': '孕期指南'
}

if __name__ == "__main__":
    db = next(get_db())
    
    # 获取所有文章
    all_articles = db.query(Content).all()
    print(f'总共有 {len(all_articles)} 篇文章')
    
    # 更新分类
    updated_count = 0
    for article in all_articles:
        if article.category in CATEGORY_MAPPING:
            old_category = article.category
            new_category = CATEGORY_MAPPING[old_category]
            article.category = new_category
            updated_count += 1
            print(f'更新文章 {article.id}: {old_category} -> {new_category}')
    
    # 提交更改
    db.commit()
    print(f'\n✅ 成功更新了 {updated_count} 篇文章的分类')
    
    # 验证更新结果
    print('\n📊 更新后的分类分布:')
    from sqlalchemy import func
    category_counts = db.query(Content.category, func.count(Content.id)).group_by(Content.category).all()
    for category, count in category_counts:
        print(f'   {category}: {count} 篇')
    
    db.close()