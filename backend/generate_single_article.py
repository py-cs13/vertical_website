#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为用户生成一篇示例文章
"""

import os
import sys
from datetime import datetime
from content_generator import DeepSeekGenerator
from database import SessionLocal
from models import Content

def generate_single_article():
    """生成一篇婴儿辅食添加指南文章"""
    
    # 初始化数据库连接和生成器
    session = SessionLocal()
    generator = DeepSeekGenerator()
    
    # 文章配置
    article_config = {
        "id": 188,
        "title": "🍼婴儿辅食添加全攻略｜新手妈妈必备！从泥状到颗粒状的科学喂养指南👶",
        "category": "婴儿护理",
        "prompt": """请生成一篇关于婴儿辅食添加的专业指南，要求：
        
1. 标题使用emoji，内容通俗易懂
2. 包含以下内容结构：
   - 辅食添加的最佳时机和信号
   - 辅食添加的正确顺序和原则
   - 不同月龄的辅食种类和做法
   - 辅食添加过程中的注意事项
   - 常见问题和解决方案
3. 语言亲切自然，像朋友聊天
4. 突出实用性和可操作性
5. 字数控制在800-1200字
6. 严格遵循小红书风格，使用HTML格式"""
    }
    
    try:
        print(f"🎯 正在生成文章: {article_config['title']}")
        print(f"📅 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # 生成文章内容
        result = generator.generate_article(
            topic=article_config['title'], 
            category=article_config['category'],
            keywords="婴儿辅食, 添加指南, 喂养方法, 育儿知识"
        )
        
        if result:
            # 解析生成的内容
            parsed_content = generator._parse_generated_content(result['content'])
            
            # 创建文章对象
            article = Content(
                id=article_config['id'],
                title=article_config['title'],
                content=parsed_content['content'],
                category=article_config['category'],
                author_id=1,  # 默认作者ID
                is_published=True,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                view_count=0,
                published_at=datetime.now(),
                price=9.90,
                summary=parsed_content.get('summary', parsed_content['content'][:200] + "...")
            )
            
            # 保存到数据库
            session.add(article)
            session.commit()
            
            print(f"✅ 文章生成完成!")
            print(f"📝 文章ID: {article_config['id']}")
            print(f"📂 分类: {article_config['category']}")
            print(f"📄 字数: {len(parsed_content['content'])} 字符")
            print(f"💾 已保存到数据库")
            
            # 显示内容摘要
            print(f"\n📖 内容预览:")
            print(f"摘要: {parsed_content.get('summary', '无摘要')}")
            print(f"\n内容开头:")
            print(parsed_content['content'][:300] + "...")
            
        else:
            print("❌ 文章生成失败")
            
    except Exception as e:
        print(f"❌ 生成过程中出现错误: {str(e)}")
        session.rollback()
    finally:
        # 关闭数据库连接
        session.close()
        
        print("\n" + "=" * 60)
        print(f"🎉 文章生成任务完成!")

if __name__ == "__main__":
    generate_single_article()