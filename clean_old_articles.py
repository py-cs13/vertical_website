#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除旧格式文章脚本
只保留符合小红书风格的新格式文章
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from backend.config import Settings
import re

# 获取配置
settings = Settings()

def main():
    """主函数"""
    print("正在连接数据库...")
    
    # 创建数据库引擎
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # 查询所有文章
        result = db.execute(text("SELECT id, title, content, created_at FROM contents ORDER BY created_at DESC"))
        articles = result.fetchall()
        
        print(f"\n共发现 {len(articles)} 篇文章")
        
        # 分析文章格式
        old_format_count = 0
        new_format_count = 0
        old_article_ids = []
        
        print("\n开始分析文章格式...")
        for article in articles:
            article_id, title, content, created_at = article
            
            # 判断是否为新格式（小红书风格）
            # 新格式特征：标题有emoji，内容有自然换行，没有Markdown标签
            has_emoji = bool(re.search(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002700-\U000027BF]', title))
            has_clean_format = not ('####' in content or '---' in content)
            has_proper_newlines = content.count('\n\n') >= 2
            
            is_new_format = has_emoji and has_clean_format and has_proper_newlines
            
            if is_new_format:
                new_format_count += 1
                print(f"✓ 文章 {article_id} ({title[:20]}...) 是新格式")
            else:
                old_format_count += 1
                old_article_ids.append(article_id)
                print(f"✗ 文章 {article_id} ({title[:20]}...) 是旧格式")
        
        print(f"\n分析结果：")
        print(f"- 新格式文章: {new_format_count} 篇")
        print(f"- 旧格式文章: {old_format_count} 篇")
        
        # 确认删除
        if old_article_ids:
            confirm = input(f"\n是否删除 {len(old_article_ids)} 篇旧格式文章？(y/n): ")
            if confirm.lower() == 'y':
                print("\n开始删除旧格式文章...")
                # 批量删除
                for article_id in old_article_ids:
                    db.execute(text("DELETE FROM contents WHERE id = :id"), {"id": article_id})
                
                db.commit()
                print(f"成功删除 {len(old_article_ids)} 篇旧格式文章")
            else:
                print("取消删除操作")
        else:
            print("\n没有旧格式文章需要删除")
            
    except Exception as e:
        print(f"\n发生错误: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
