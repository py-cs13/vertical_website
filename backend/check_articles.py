#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查数据库中的文章数据
"""

from database import SessionLocal
from models import Content

db = SessionLocal()

# 获取所有文章
articles = db.query(Content).all()

print(f"文章总数: {len(articles)}")
print("\n文章详情:")
print("=" * 60)

for article in articles:
    print(f"ID: {article.id}")
    print(f"标题: {repr(article.title)}")
    print(f"分类: {article.category}")
    print(f"摘要长度: {len(article.summary)}")
    print(f"内容长度: {len(article.content)}")
    print(f"是否为空标题: {article.title is None or article.title.strip() == ''}")
    print(f"是否为空摘要: {article.summary is None or article.summary.strip() == ''}")
    print(f"是否为空内容: {article.content is None or article.content.strip() == ''}")
    print("-" * 60)

db.close()
