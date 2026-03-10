#!/usr/bin/env python3
"""
检查数据库表结构和数据的脚本
"""

import sys
import os

# 添加backend目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.database import get_db
from backend.models import User, Content, Like, Favorite
from sqlalchemy import inspect, func

def check_database():
    """检查数据库结构和数据"""
    print('🔍 开始检查数据库...')
    
    db = next(get_db())
    
    try:
        # 检查表是否存在
        inspector = inspect(db.bind)
        table_names = inspector.get_table_names()
        print('\n📊 数据库中的表:')
        for table_name in table_names:
            print(f'   ✅ {table_name}')
        
        # 检查Content表的字段
        print('\n📝 Content表的主要字段:')
        content_columns = inspector.get_columns('contents')
        for column in content_columns:
            if column['name'] in ['id', 'title', 'likes', 'is_published', 'category']:
                print(f'   {column["name"]}: {column["type"]}')
        
        # 检查Like表的字段
        print('\n❤️ Like表的字段:')
        like_columns = inspector.get_columns('likes')
        for column in like_columns:
            print(f'   {column["name"]}: {column["type"]}')
        
        # 检查Favorite表的字段
        print('\n⭐ Favorite表的字段:')
        favorite_columns = inspector.get_columns('favorites')
        for column in favorite_columns:
            print(f'   {column["name"]}: {column["type"]}')
        
        # 检查是否存在article_likes表
        if 'article_likes' in table_names:
            print('\n📝 article_likes表的字段:')
            article_likes_columns = inspector.get_columns('article_likes')
            for column in article_likes_columns:
                print(f'   {column["name"]}: {column["type"]}')
        
        # 检查用户数据
        users = db.query(User).all()
        print(f'\n👥 用户数量: {len(users)}')
        if users:
            print(f'   第一个用户: ID={users[0].id}, 用户名={users[0].username}')
        
        # 检查内容数据
        articles = db.query(Content).limit(3).all()
        print(f'\n📚 内容数量: {db.query(Content).count()}')
        print('   前3篇文章:')
        for article in articles:
            print(f'   ID: {article.id}, 标题: {article.title}, 点赞数: {article.likes}')
        
        # 检查点赞和收藏数据
        likes = db.query(Like).all()
        favorites = db.query(Favorite).all()
        print(f'\n❤️ 点赞记录数量: {len(likes)}')
        print(f'⭐ 收藏记录数量: {len(favorites)}')
        
        # 检查点赞状态
        if likes:
            print('   点赞记录示例:')
            for like in likes[:2]:
                print(f'   用户ID: {like.user_id}, 内容ID: {like.content_id}')
        
        if favorites:
            print('   收藏记录示例:')
            for favorite in favorites[:2]:
                print(f'   用户ID: {favorite.user_id}, 内容ID: {favorite.content_id}')
        
        print('\n✅ 数据库检查完成')
        
    except Exception as e:
        print(f'\n❌ 数据库检查失败: {e}')
    finally:
        db.close()

if __name__ == '__main__':
    check_database()
