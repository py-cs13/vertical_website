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
    
    # 安全检查：防止意外删除生产数据
    print("⚠️  警告：此操作将删除数据库中所有现有表并重新创建！")
    print(f"正在连接的数据库URL: {settings.DATABASE_URL}")
    print("请确认这是测试数据库，不是生产数据库！")
    
    # 要求用户确认
    confirmation = input("是否继续执行？(输入 'yes' 确认执行，其他键取消): ")
    if confirmation.lower() != 'yes':
        print("操作已取消")
        return
    
    # 删除所有现有表并重新创建，确保包含新添加的price字段
    print("执行删除现有表并重新创建...")
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
        
        # 文章3
        article3 = Content(
            title="宝宝睡眠问题全解析",
            category="婴儿护理",
            summary="解决宝宝睡眠问题的实用技巧和方法...",
            content="<h1>宝宝睡眠问题全解析</h1><p>宝宝的睡眠问题是困扰很多父母的常见问题...</p>",
            author_id=user.id,
            is_published=True,
            view_count=120,
            published_at=datetime.now()
        )
        
        # 文章4
        article4 = Content(
            title="科学的亲子互动方法",
            category="亲子互动",
            summary="建立良好亲子关系的科学方法和技巧...",
            content="<h1>科学的亲子互动方法</h1><p>亲子互动对宝宝的成长发育至关重要...</p>",
            author_id=user.id,
            is_published=True,
            view_count=90,
            published_at=datetime.now()
        )
        
        # 文章5
        article5 = Content(
            title="宝宝疫苗接种全指南",
            category="婴儿护理",
            summary="详细介绍宝宝疫苗接种的时间表和注意事项...",
            content="<h1>宝宝疫苗接种全指南</h1><p>疫苗接种是保护宝宝健康的重要措施...</p>",
            author_id=user.id,
            is_published=True,
            view_count=150,
            published_at=datetime.now()
        )
        
        # 文章6
        article6 = Content(
            title="如何培养宝宝的阅读兴趣",
            category="早期教育",
            summary="从小培养宝宝阅读兴趣的实用方法...",
            content="<h1>如何培养宝宝的阅读兴趣</h1><p>阅读是宝宝学习和成长的重要方式...</p>",
            author_id=user.id,
            is_published=True,
            view_count=110,
            published_at=datetime.now()
        )
        
        # 文章7
        article7 = Content(
            title="宝宝常见疾病的家庭护理",
            category="婴儿护理",
            summary="宝宝常见疾病的识别和家庭护理方法...",
            content="<h1>宝宝常见疾病的家庭护理</h1><p>当宝宝生病时，正确的家庭护理非常重要...</p>",
            author_id=user.id,
            is_published=True,
            view_count=130,
            published_at=datetime.now()
        )
        
        # 文章8
        article8 = Content(
            title="宝宝衣物选择与护理",
            category="婴儿护理",
            summary="如何为宝宝选择合适的衣物以及正确的护理方法...",
            content="<h1>宝宝衣物选择与护理</h1><p>宝宝的皮肤娇嫩，衣物选择需要特别注意...</p>",
            author_id=user.id,
            is_published=True,
            view_count=95,
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
        
        # 工具包3
        toolkit3 = Content(
            title="宝宝辅食食谱工具包",
            category="toolkit",
            summary="包含数百种适合不同年龄段宝宝的辅食食谱...",
            content="<h1>宝宝辅食食谱工具包</h1><p>本工具包提供了丰富多样的宝宝辅食食谱...</p>",
            author_id=user.id,
            is_published=True,
            view_count=200,
            published_at=datetime.now(),
            price=129.0
        )
        
        # 工具包4
        toolkit4 = Content(
            title="孕期健康管理工具包",
            category="toolkit",
            summary="帮助孕妇进行全面的健康管理和孕期护理...",
            content="<h1>孕期健康管理工具包</h1><p>本工具包包含孕期健康管理的各种工具和指南...</p>",
            author_id=user.id,
            is_published=True,
            view_count=180,
            published_at=datetime.now(),
            price=159.0
        )
        
        # 工具包5
        toolkit5 = Content(
            title="宝宝成长记录工具包",
            category="toolkit",
            summary="帮助父母记录宝宝成长的各种工具和模板...",
            content="<h1>宝宝成长记录工具包</h1><p>本工具包提供了丰富的宝宝成长记录模板...</p>",
            author_id=user.id,
            is_published=True,
            view_count=160,
            published_at=datetime.now(),
            price=89.0
        )
        
        # 工具包6
        toolkit6 = Content(
            title="育儿时间管理工具包",
            category="toolkit",
            summary="帮助父母合理安排育儿时间的实用工具...",
            content="<h1>育儿时间管理工具包</h1><p>本工具包包含各种时间管理工具和技巧...</p>",
            author_id=user.id,
            is_published=True,
            view_count=140,
            published_at=datetime.now(),
            price=79.0
        )
        
        # 工具包7
        toolkit7 = Content(
            title="宝宝教育资源工具包",
            category="toolkit",
            summary="包含丰富的宝宝教育资源和学习材料...",
            content="<h1>宝宝教育资源工具包</h1><p>本工具包提供了各种宝宝教育资源和学习材料...</p>",
            author_id=user.id,
            is_published=True,
            view_count=220,
            published_at=datetime.now(),
            price=199.0
        )
        
        # 工具包8
        toolkit8 = Content(
            title="产后恢复指导工具包",
            category="toolkit",
            summary="帮助新妈妈进行产后恢复的全面指导...",
            content="<h1>产后恢复指导工具包</h1><p>本工具包包含产后恢复的各种指导和建议...</p>",
            author_id=user.id,
            is_published=True,
            view_count=170,
            published_at=datetime.now(),
            price=149.0
        )
        
        # 将所有内容添加到数据库
        db.add_all([article1, article2, article3, article4, article5, article6, article7, article8, 
                    toolkit1, toolkit2, toolkit3, toolkit4, toolkit5, toolkit6, toolkit7, toolkit8])
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
