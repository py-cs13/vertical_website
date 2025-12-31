#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成工具包数据脚本
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from backend.config import Settings

# 获取配置
settings = Settings()

# 工具包列表
toolkits = [
    {
        "title": "🎁 新生儿护理工具包",
        "content": "这个工具包包含了新生儿护理的所有必备指南，包括换尿布、洗澡、抚触等技巧。\n\n📋 工具包内容：\n1. 新生儿护理指南PDF\n2. 每日护理记录表模板\n3. 常见问题解答文档\n4. 护理视频教程链接\n\n使用这个工具包，新手爸妈可以轻松掌握新生儿护理的所有要点。",
        "category": "母婴育儿",
        "summary": "包含新生儿护理指南、记录表模板、常见问题解答和视频教程的完整工具包。",
        "price": 19.9
    },
    {
        "title": "🎁 宝宝辅食工具包",
        "content": "这个工具包包含了宝宝辅食添加的所有必备资源，从第一口辅食到多样化饮食的完整指南。\n\n📋 工具包内容：\n1. 6-12个月辅食计划\n2. 辅食食谱集PDF\n3. 辅食添加记录表\n4. 食物过敏应对指南\n\n使用这个工具包，妈妈们可以轻松为宝宝制作营养均衡的辅食。",
        "category": "母婴育儿",
        "summary": "包含辅食计划、食谱集、记录表和过敏应对指南的完整工具包。",
        "price": 24.9
    },
    {
        "title": "🎁 宝宝睡眠工具包",
        "content": "这个工具包包含了改善宝宝睡眠的所有实用资源，帮助宝宝建立良好的睡眠习惯。\n\n📋 工具包内容：\n1. 睡眠训练指南\n2. 睡眠记录表模板\n3. 睡前仪式建议\n4. 常见睡眠问题解决方案\n\n使用这个工具包，爸妈可以帮助宝宝建立规律的睡眠习惯，让全家都能睡个好觉。",
        "category": "母婴育儿",
        "summary": "包含睡眠训练指南、记录表模板、睡前仪式建议和问题解决方案的完整工具包。",
        "price": 29.9
    }
]

def main():
    """主函数"""
    print("正在连接数据库...")
    
    # 创建数据库引擎
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        print("\n开始生成工具包数据...")
        
        # 为每个工具包生成数据
        for toolkit in toolkits:
            print(f"\n正在生成工具包: {toolkit['title']}")
            
            try:
                # 保存到数据库
                db.execute(
                    text("""
                    INSERT INTO contents (title, content, category, summary, author_id, is_published, view_count, published_at, price, created_at, updated_at)
                    VALUES (:title, :content, :category, :summary, :author_id, :is_published, 0, NOW(), :price, NOW(), NOW())
                    """),
                    {
                        "title": toolkit["title"],
                        "content": toolkit["content"],
                        "category": "toolkit",  # 工具包的分类为"toolkit"
                        "summary": toolkit["summary"],
                        "author_id": 1,  # 默认作者ID
                        "is_published": True,
                        "price": toolkit["price"]
                    }
                )
                
                db.commit()
                print(f"✓ 成功生成工具包: {toolkit['title']}")
                
            except Exception as e:
                print(f"✗ 生成工具包失败: {e}")
                db.rollback()
                continue
        
        print("\n工具包生成完成！")
        
    except Exception as e:
        print(f"\n发生错误: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()