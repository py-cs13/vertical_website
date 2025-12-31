#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统计各分类下的文章数量
"""

from database import SessionLocal
from models import Content

# 创建数据库会话
db = SessionLocal()

# 获取所有已发布的非工具包文章
articles = db.query(Content).filter(
    Content.is_published == True,
    Content.category != "toolkit"
).all()

print(f"已发布的非工具包文章总数: {len(articles)}")
print("\n各分类文章数量统计:")
print("=" * 60)

# 统计每个分类的文章数量
category_counts = {}
for article in articles:
    if article.category in category_counts:
        category_counts[article.category] += 1
    else:
        category_counts[article.category] = 1

# 按分类名称排序并打印
for category, count in sorted(category_counts.items()):
    print(f"{category}: {count} 篇")

# 检查前端中使用的分类是否存在
frontend_categories = ['母婴育儿', '育儿知识', '营养辅食', '产后恢复', '亲子互动', '成长发育', '早期教育', '健康养生']
print("\n前端分类与数据库实际情况对比:")
print("=" * 60)

for category in frontend_categories:
    if category in category_counts:
        print(f"{category}: 数据库中有 {category_counts[category]} 篇文章")
    else:
        print(f"{category}: 数据库中无此分类的文章")

db.close()