#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成单个高质量工具包
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from content_generator import generator_service
from database import get_db
from models import Content
from datetime import datetime

def generate_high_quality_toolkit():
    """生成高质量工具包"""
    # 获取数据库会话
    db = next(get_db())
    
    # 定义工具包信息
    theme = "宝宝睡眠作息工具包"
    category = "母婴工具"
    price = 19.90  # 设置合理价格
    
    print(f"正在生成 {theme}...")
    
    # 生成工具包内容
    content = generator_service.generate_toolkit(theme, category)
    
    if content:
        # 将生成的内容保存到数据库
        new_content = Content(
            title=content['title'],
            summary=content['summary'],
            content=content['content'],
            category=category,
            author_id=1,  # 默认作者ID
            price=price,
            is_published=True,
            published_at=datetime.now()
        )
        
        db.add(new_content)
        db.commit()
        db.refresh(new_content)
        
        print(f"✅ 工具包生成成功！")
        print(f"   ID: {new_content.id}")
        print(f"   标题: {new_content.title}")
        print(f"   分类: {new_content.category}")
        print(f"   价格: ¥{new_content.price}")
        print(f"   内容长度: {len(new_content.content)} 字符")
    else:
        print("❌ 工具包生成失败")

if __name__ == "__main__":
    generate_high_quality_toolkit()
