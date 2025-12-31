#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查看最近生成的4个工具包的详细信息
"""

from database import get_db
from models import Content

def view_recent_toolkits():
    # 获取数据库会话
    db = next(get_db())
    
    # 查询最近生成的4个工具包
    recent_toolkits = db.query(Content).filter(Content.category.in_(['母婴工具', '宝宝食谱', '婴儿护理'])).order_by(Content.created_at.desc()).limit(4).all()
    
    print("最近生成的4个工具包详细信息：")
    print("=" * 60)
    
    for i, toolkit in enumerate(recent_toolkits, 1):
        print(f"\n工具包 {i}：")
        print(f"ID: {toolkit.id}")
        print(f"标题: {toolkit.title}")
        print(f"分类: {toolkit.category}")
        print(f"价格: ¥{toolkit.price}")
        print(f"内容长度: {len(toolkit.content)} 字符")
        print(f"发布时间: {toolkit.published_at}")
        print("内容预览:")
        print("-" * 30)
        # 预览前200个字符
        preview = toolkit.content[:200]
        print(preview)
        if len(toolkit.content) > 200:
            print("...")
        print("-" * 30)

if __name__ == "__main__":
    view_recent_toolkits()
