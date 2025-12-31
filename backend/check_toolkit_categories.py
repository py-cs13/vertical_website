#!/usr/bin/env python3
"""
检查数据库中工具包的分类
"""

from database import get_db
from models import Content

if __name__ == "__main__":
    db = next(get_db())
    
    # 查询所有分类为toolkit的内容
    toolkits = db.query(Content).filter(Content.category == "toolkit").all()
    print(f"分类为'toolkit'的工具包数量: {len(toolkits)}")
    for t in toolkits:
        print(f"ID: {t.id}, 标题: {t.title}, 分类: {t.category}, 已发布: {t.is_published}")
    
    # 查询所有内容，查看实际的分类值
    print("\n所有内容的分类:")
    contents = db.query(Content).all()
    for c in contents:
        print(f"ID: {c.id}, 标题: {c.title}, 分类: {c.category}, 已发布: {c.is_published}")
    
    db.close()