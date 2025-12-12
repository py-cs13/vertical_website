#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查数据库中工具包数据的脚本
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Content
from config import settings

def check_toolkit_data():
    """检查数据库中的工具包数据"""
    # 创建数据库连接
    engine = create_engine(settings.DATABASE_URL)
    Session = sessionmaker(bind=engine)
    db = Session()
    
    try:
        # 查询所有工具包类型的内容
        toolkits = db.query(Content).filter(Content.category == 'toolkit').all()
        
        print(f"数据库中共有 {len(toolkits)} 个工具包类型的内容")
        print("\n工具包列表：")
        for i, toolkit in enumerate(toolkits, 1):
            print(f"{i}. 标题: {toolkit.title}")
            print(f"   分类: {toolkit.category}")
            print(f"   已发布: {toolkit.is_published}")
            print(f"   价格: {toolkit.price}")
            print(f"   发布时间: {toolkit.published_at}")
            print(f"   查看次数: {toolkit.view_count}")
            print("   " + "-" * 40)
        
        # 检查所有已发布的内容
        all_published = db.query(Content).filter(Content.is_published == True).all()
        print(f"\n所有已发布内容数量: {len(all_published)}")
        
    except Exception as e:
        print(f"查询数据时出错: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_toolkit_data()