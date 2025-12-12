#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向数据库中添加测试数据的脚本
"""

import os
import sys
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 添加backend目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入模型和配置
from models import Base, User, Content
from config import settings

# 创建数据库引擎和会话
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_test_data():
    """向数据库中添加测试数据"""
    print("开始添加测试数据...")
    
    # 删除所有现有表并重新创建，确保包含新添加的price字段
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 检查是否已经有用户
        user = db.query(User).first()
        if not user:
            # 创建测试用户
            print("创建测试用户...")
            user = User(
                username="test_user",
                email="test@example.com",
                hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # 密码: test123
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # 添加测试文章
        print("添加测试文章...")
        
        # 文章1
        article1 = Content(
            title="如何选择适合宝宝的辅食",
            category="母婴育儿",
            summary="本文将详细介绍如何根据宝宝的年龄和发育阶段选择合适的辅食...",
            content="<h1>如何选择适合宝宝的辅食</h1><p>当宝宝6个月左右时，就可以开始添加辅食了...</p>",
            author_id=user.id,
            is_published=True,
            view_count=100,
            published_at=datetime.now()
        )
        
        # 文章2
        article2 = Content(
            title="新生儿护理的10个关键要点",
            category="母婴育儿",
            summary="新手父母必读！掌握这10个关键要点，轻松应对新生儿护理...",
            content="<h1>新生儿护理的10个关键要点</h1><p>新生儿的到来给家庭带来了欢乐，也带来了挑战...</p>",
            author_id=user.id,
            is_published=True,
            view_count=80,
            published_at=datetime.now()
        )
        
        # 添加测试工具包
        print("添加测试工具包...")
        
        # 工具包1
        toolkit1 = Content(
            title="0-3岁宝宝发育里程碑追踪工具包",
            category="toolkit",
            summary="专业的宝宝发育里程碑追踪工具包，帮助父母轻松记录宝宝的成长过程...",
            content="<h1>0-3岁宝宝发育里程碑追踪工具包</h1><p>本工具包包含详细的发育里程碑检查表...</p>",
            author_id=user.id,
            is_published=True,
            view_count=150,
            published_at=datetime.now(),
            price=99.0
        )
        
        # 工具包2
        toolkit2 = Content(
            title="科学育儿知识手册工具包",
            category="toolkit",
            summary="全面的科学育儿知识手册，涵盖宝宝护理、喂养、教育等各个方面...",
            content="<h1>科学育儿知识手册工具包</h1><p>本工具包收集了最新的科学育儿知识...</p>",
            author_id=user.id,
            is_published=True,
            view_count=120,
            published_at=datetime.now(),
            price=199.0
        )
        
        # 将所有内容添加到数据库
        db.add_all([article1, article2, toolkit1, toolkit2])
        db.commit()
        
        print("测试数据添加完成！")
        print(f"添加了 {db.query(Content).filter(Content.is_published == True).count()} 篇已发布内容")
        
    except Exception as e:
        print(f"添加测试数据时出错: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_test_data()
