#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成4个高质量工具包的脚本
满足用户需求：高质量、实用性强、价格合理、有购买欲
"""

import sys
import os
from datetime import datetime
from typing import Optional, Dict

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入相关模块
from content_generator import DeepSeekGenerator
from database import get_db
from models import Content, User
from sqlalchemy.orm import Session
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 高质量工具包主题列表
high_quality_toolkits = [
    {
        "title": "宝宝睡眠作息工具包",
        "keywords": "宝宝睡眠,作息规律,婴儿睡眠,睡眠训练,哄睡技巧",
        "category": "母婴工具",
        "price": 19.9  # 合理的价格设置
    },
    {
        "title": "婴儿辅食制作工具包",
        "keywords": "婴儿辅食,辅食食谱,辅食制作,宝宝营养,6月龄辅食",
        "category": "宝宝食谱",
        "price": 24.9  # 合理的价格设置
    },
    {
        "title": "新生儿护理技能工具包",
        "keywords": "新生儿护理,婴儿护理,脐带护理,洗澡技巧,婴儿抚触",
        "category": "婴儿护理",
        "price": 29.9  # 合理的价格设置
    },
    {
        "title": "亲子游戏互动工具包",
        "keywords": "亲子游戏,婴儿游戏,早教游戏,互动游戏,智力开发",
        "category": "育儿经验",
        "price": 14.9  # 合理的价格设置
    }
]

def generate_toolkits():
    """生成4个高质量工具包"""
    logger.info("开始生成4个高质量工具包...")
    
    # 初始化内容生成器
    generator = DeepSeekGenerator()
    
    # 测试API连接
    if not generator.test_connection():
        logger.error("百度智能云千帆API连接失败，无法生成工具包")
        return False
    
    # 获取数据库会话
    db = next(get_db())
    
    try:
        # 获取默认作者（ID为1的用户）
        author = db.query(User).filter(User.id == 1).first()
        if not author:
            logger.error("未找到ID为1的用户，无法设置工具包作者")
            return False
        
        # 生成工具包
        generated_count = 0
        for i, toolkit_info in enumerate(high_quality_toolkits, 1):
            logger.info(f"正在生成第{i}个工具包: {toolkit_info['title']}")
            
            # 生成工具包内容
            toolkit_content = generator.generate_toolkit(
                topic=toolkit_info['title'],
                category=toolkit_info['category'],
                keywords=toolkit_info['keywords']
            )
            
            if not toolkit_content:
                logger.error(f"第{i}个工具包生成失败: {toolkit_info['title']}")
                continue
            
            # 检查生成的内容格式
            if 'title' not in toolkit_content or 'summary' not in toolkit_content or 'content' not in toolkit_content:
                logger.error(f"第{i}个工具包内容格式错误: {toolkit_info['title']}")
                continue
            
            # 创建工具包内容对象
            new_toolkit = Content(
                title=toolkit_content['title'],
                category=toolkit_info['category'],
                summary=toolkit_content['summary'],
                content=toolkit_content['content'],
                author_id=author.id,
                is_published=True,
                price=toolkit_info['price'],
                published_at=datetime.now()
            )
            
            # 保存到数据库
            db.add(new_toolkit)
            db.commit()
            db.refresh(new_toolkit)
            
            logger.info(f"✅ 第{i}个工具包生成成功并保存到数据库")
            logger.info(f"   ID: {new_toolkit.id}")
            logger.info(f"   标题: {new_toolkit.title}")
            logger.info(f"   价格: ¥{new_toolkit.price}")
            logger.info(f"   分类: {new_toolkit.category}")
            
            generated_count += 1
        
        logger.info(f"\n🎉 工具包生成完成！共生成 {generated_count} 个工具包")
        return True
        
    except Exception as e:
        logger.error(f"生成工具包时发生错误: {str(e)}")
        db.rollback()
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    generate_toolkits()
