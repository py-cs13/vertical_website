#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查看最新生成的工具包详情
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db
from models import Content

def view_latest_toolkits():
    """查看最新生成的工具包详情"""
    # 获取数据库会话
    db = next(get_db())
    
    try:
        # 查询最新生成的4个工具包（ID 17-20）
        toolkits = db.query(Content).filter(Content.id >= 17, Content.id <= 20).order_by(Content.id).all()
        
        if not toolkits:
            print("未找到ID 17-20的工具包")
            return
        
        print("最新生成的工具包详情:")
        print("=" * 70)
        
        for toolkit in toolkits:
            print(f"ID: {toolkit.id}")
            print(f"标题: {toolkit.title}")
            print(f"分类: {toolkit.category}")
            print(f"价格: ¥{toolkit.price:.2f}")
            print(f"摘要: {toolkit.summary[:150]}...")
            print(f"内容长度: {len(toolkit.content)} 字符")
            print(f"发布时间: {toolkit.published_at}")
            print("=" * 70)
            print()
            
            # 查看第一个工具包的详细内容
            if toolkit.id == 17:
                print("\n" + "=" * 70)
                print("第一个工具包（宝宝睡眠作息工具包）详细内容:")
                print("=" * 70)
                print(toolkit.content)
                print("\n" + "=" * 70)
                print()
                
    except Exception as e:
        print(f"查看工具包详情时发生错误: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    view_latest_toolkits()