#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证文章内容格式是否已更新为小红书风格
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'backend', '.env.production'))

# 添加backend目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

# 导入配置
from config import settings

def main():
    """验证文章内容格式"""
    try:
        # 使用配置中的DATABASE_URL直接连接
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            # 获取最新的文章
            result = conn.execute(
                text("SELECT id, title, content FROM contents ORDER BY id DESC LIMIT 5")
            )
            articles = result.fetchall()
            
            print(f"\n找到 {len(articles)} 篇最新文章:")
            print("=" * 50)
            
            for article in articles:
                article_id, title, content = article
                
                print(f"\n文章ID: {article_id}")
                print(f"标题: {title}")
                print(f"内容预览 (前500字符):")
                print(content[:500] + "...")
                print("-" * 50)
                
                # 检查是否包含小红书风格元素
                import re
                has_emoji = bool(re.search(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002700-\U000027BF]', title))
                has_newlines = '\n' in content
                has_short_paragraphs = content.count('\n\n') > 2
                
                print(f"小红书风格特征检测:")
                print(f"- 标题包含emoji: {'是' if has_emoji else '否'}")
                print(f"- 内容包含换行: {'是' if has_newlines else '否'}")
                print(f"- 内容包含多段落: {'是' if has_short_paragraphs else '否'}")
                
                print("=" * 50)
                
    except Exception as e:
        print(f"连接数据库失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()