#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除数据库中空标题、空摘要或空内容的文章
"""

from database import SessionLocal
from models import Content

db = SessionLocal()

# 查找有问题的文章（标题、摘要或内容为空）
problematic_articles = db.query(Content).filter(
    (Content.title == '') |
    (Content.title == None) |
    (Content.summary == '') |
    (Content.summary == None) |
    (Content.content == '') |
    (Content.content == None)
).all()

print(f"找到 {len(problematic_articles)} 篇有问题的文章")

# 删除这些文章
if problematic_articles:
    print("正在删除有问题的文章...")
    for article in problematic_articles:
        print(f"删除文章: ID={article.id}, 标题={repr(article.title)}")
        db.delete(article)
    
    # 提交更改
    db.commit()
    print(f"已成功删除 {len(problematic_articles)} 篇有问题的文章")
else:
    print("没有发现需要删除的有问题文章")

# 重新检查文章总数
articles = db.query(Content).all()
print(f"当前数据库中文章总数: {len(articles)}")

db.close()
