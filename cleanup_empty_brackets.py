#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理文章内容中的空括号脚本
适用于小红书风格的内容格式
"""

import sys
import os
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 添加backend目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from models import Content
from config import settings

# 创建数据库连接
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def cleanup_content(content: str) -> str:
    """
    清理文章内容，主要处理空括号并保持小红书风格的换行结构
    
    Args:
        content: 原始文章内容
        
    Returns:
        清理后的文章内容
    """
    if not content:
        return content
    
    # 1. 清理空括号（保持换行结构）
    # 使用正则表达式匹配空括号，包括括号内有空格的情况
    cleaned = re.sub(r'\s*\(\s*\)\s*', ' ', content)
    
    # 2. 清理每行内的多余空格，保持换行结构
    lines = cleaned.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # 清理行内的连续空格
        cleaned_line = re.sub(r'\s+', ' ', line).strip()
        # 如果是空行，保持空行
        if not line.strip():
            cleaned_lines.append('')
        elif cleaned_line:
            cleaned_lines.append(cleaned_line)
    
    # 3. 重新组合内容
    cleaned_content = '\n'.join(cleaned_lines)
    
    # 4. 清理多余的空行（保留最多两个连续空行）
    cleaned_content = re.sub(r'\n{3,}', '\n\n', cleaned_content)
    
    # 5. 移除首尾的换行符
    cleaned_content = cleaned_content.strip()
    
    return cleaned_content

def cleanup_empty_brackets():
    """清理所有文章内容中的空括号"""
    db = SessionLocal()
    try:
        # 获取所有文章
        contents = db.query(Content).all()
        print(f"找到 {len(contents)} 篇文章")
        
        updated_count = 0
        for content in contents:
            if content.content:
                original_content = content.content
                
                # 使用新的清理函数处理内容
                cleaned_content = cleanup_content(original_content)
                
                if cleaned_content != original_content:
                    content.content = cleaned_content
                    updated_count += 1
                    print(f"更新文章: {content.title} (ID: {content.id})")
        
        # 提交更改
        db.commit()
        print(f"清理完成，共更新了 {updated_count} 篇文章")
        
    except Exception as e:
        print(f"清理过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_empty_brackets()
