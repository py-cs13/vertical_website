#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查数据库中的内容，包括文章和工具包
"""

from database import get_db
from models import Content
import datetime

# 获取数据库会话
db = next(get_db())

print("检查数据库中的内容...")

# 定义工具包分类列表
toolkit_categories = ["宝宝食谱", "育儿计划", "母婴工具"]

# 查询所有工具包
all_toolkits = db.query(Content).filter(Content.category.in_(toolkit_categories)).order_by(Content.created_at.desc()).all()

print(f"\n✅ 数据库中共有 {len(all_toolkits)} 条工具包内容")

if all_toolkits:
    print("\n所有工具包列表:")
    print("=" * 50)
    
    for i, content in enumerate(all_toolkits, 1):
        print(f"\n{i}. ")
        print(f"   ID: {content.id}")
        if content.title:
            print(f"   标题: {content.title}")
        print(f"   分类: {content.category}")
        
        # 内容类型为工具包
        content_type = "工具包"
        
        print(f"   类型: {content_type}")
        print(f"   作者ID: {content.author_id}")
        print(f"   发布时间: {content.published_at}")
        print(f"   价格: ¥{content.price}")
        print(f"   内容长度: {len(content.content)} 字符")
        
        # 检查内容是否包含HTML
        if content.content and (content.content.startswith('<') or '<p>' in content.content or '<ul>' in content.content or '<div>' in content.content or '<h' in content.content):
            print("   内容格式: HTML ✅")
        else:
            print("   内容格式: 纯文本 ❌")