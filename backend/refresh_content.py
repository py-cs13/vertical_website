#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容刷新脚本
用于删除数据库中的老内容并生成新的HTML格式内容
"""

import os
import sys
import logging
import time
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Content, User
from content_generator import DeepSeekGenerator, AutoContentPublisher

# 配置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def delete_old_content(db: Session, category: str = None) -> int:
    """
    删除数据库中的老内容
    
    Args:
        db: 数据库会话
        category: 可选，指定要删除的内容分类
        
    Returns:
        int: 删除的记录数量
    """
    try:
        if category:
            # 删除指定分类的内容
            delete_count = db.query(Content).filter(Content.category == category).delete()
        else:
            # 删除所有内容
            delete_count = db.query(Content).delete()
        
        db.commit()
        logger.info(f"成功删除 {delete_count} 条老内容")
        return delete_count
    except Exception as e:
        logger.error(f"删除老内容时出错: {str(e)}")
        db.rollback()
        raise

def generate_new_content(db: Session):
    """
    生成新的HTML格式内容
    
    Args:
        db: 数据库会话
    """
    try:
        logger.info("="*50)
        logger.info("开始生成新内容")
        logger.info("="*50)
        
        # 创建内容发布器
        publisher = AutoContentPublisher(db)
        logger.info(f"内容发布器创建完成")
        logger.info(f"文章分类列表: {publisher.article_categories}")
        logger.info(f"工具包分类列表: {publisher.toolkit_categories}")
        
        # 生成5篇文章
        logger.info("\n" + "="*30)
        logger.info("开始生成5篇文章")
        logger.info("="*30)
        article_success_count = 0
        article_fail_count = 0
        for i in range(5):
            logger.info(f"\n[文章 {i+1}/5] 开始生成...")
            result = publisher.publish_article()
            if result:
                logger.info(f"[文章 {i+1}/5] ✅ 发布成功: {result['title']} (ID: {result['id']})")
                article_success_count += 1
            else:
                logger.warning(f"[文章 {i+1}/5] ⚠️  发布失败")
                article_fail_count += 1
            time.sleep(2)  # 避免API请求过于频繁
        logger.info(f"\n文章生成完成: 成功 {article_success_count} 篇, 失败 {article_fail_count} 篇")
        
        logger.info("\n" + "="*50)
        logger.info("所有新内容生成完成！")
        logger.info(f"总计: 文章 {article_success_count} 篇")
        logger.info("="*50)
        return True
    except Exception as e:
        logger.error(f"生成新内容时出错: {str(e)}")
        raise

def main():
    """
    主函数
    """
    logger.info("===== 内容刷新脚本开始执行 =====")
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 直接生成新的HTML格式内容，不删除老内容
        generate_new_content(db)
        
        logger.info("===== 内容刷新脚本执行完成！ =====")
        return 0
    except Exception as e:
        logger.error(f"脚本执行失败: {str(e)}")
        return 1
    finally:
        # 关闭数据库会话
        db.close()

if __name__ == "__main__":
    sys.exit(main())