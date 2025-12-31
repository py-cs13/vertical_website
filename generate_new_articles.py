#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成新的小红书风格文章脚本
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from backend.config import Settings
from backend.content_generator import DeepSeekGenerator

# 获取配置
settings = Settings()

# 创建生成器
generator = DeepSeekGenerator()

# 文章主题列表
topics = [
    "婴儿辅食添加指南",
    "新生儿护理的10个关键要点",
    "宝宝睡眠问题全解析",
    "科学的亲子互动方法",
    "宝宝疫苗接种全指南",
    "如何培养宝宝的阅读兴趣",
    "宝宝常见疾病的家庭护理",
    "宝宝衣物选择与护理",
    "0-3岁宝宝发育里程碑追踪",
    "科学育儿知识手册"
]

def main():
    """主函数"""
    print("正在连接数据库...")
    
    # 创建数据库引擎
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        print("\n开始生成小红书风格文章...")
        
        # 为每个主题生成文章
        for topic in topics:
            print(f"\n正在生成主题: {topic}")
            
            # 生成文章
            try:
                article = generator.generate_article(topic, "母婴育儿")
                
                # 保存到数据库
                db.execute(
                    text("""
                    INSERT INTO contents (title, content, category, summary, author_id, is_published, view_count, published_at, price, created_at, updated_at)
                    VALUES (:title, :content, :category, :summary, :author_id, :is_published, 0, NOW(), :price, NOW(), NOW())
                    """),
                    {
                        "title": article["title"],
                        "content": article["content"],
                        "category": "母婴育儿",
                        "summary": article["content"][:150] + "...",
                        "author_id": 1,  # 默认作者ID
                        "is_published": True,
                        "price": 9.9
                    }
                )
                
                db.commit()
                print(f"✓ 成功生成文章: {article['title']}")
                
            except Exception as e:
                print(f"✗ 生成文章失败: {e}")
                db.rollback()
                continue
        
        print("\n文章生成完成！")
        
    except Exception as e:
        print(f"\n发生错误: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
