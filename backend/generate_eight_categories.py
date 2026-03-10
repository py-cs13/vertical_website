#!/usr/bin/env python3
"""
为8大分类中的每个分类生成1~3篇文章
"""

from database import get_db
from models import Content
from content_generator import generator_service
import random
import logging
from logging_config import setup_logging

# 设置日志
setup_logging()
logger = logging.getLogger(__name__)

# 定义8大分类及其对应的主题模板
EIGHT_CATEGORIES = {
    '孕期指南': [
        '🤰 孕期营养补充指南：哪些营养素是必需的？',
        '🤰 孕期运动：适合孕妇的安全运动方式',
        '🤰 孕期常见不适症状及缓解方法'
    ],
    '新生照顾': [
        '👶 新生儿黄疸：原因、症状及护理方法',
        '👶 新生儿睡眠习惯培养：建立良好的睡眠规律',
        '👶 新生儿日常护理：洗澡、换尿布、脐带护理'
    ],
    '幼儿发展': [
        '🌱 1-2岁幼儿语言发展关键期：如何促进语言能力',
        '🌱 幼儿行为习惯培养：如何让孩子学会自己吃饭',
        '🌱 幼儿情绪管理：帮助孩子识别和表达情绪'
    ],
    '亲子互动': [
        '👨‍👩‍👧 0-1岁亲子游戏：促进亲子关系的简单游戏',
        '👨‍👩‍👧 家庭阅读时光：如何培养孩子的阅读兴趣',
        '👨‍👩‍👧 亲子沟通技巧：有效倾听和回应孩子的需求'
    ],
    '早期教育': [
        '🎓 0-3岁早期教育：如何培养孩子的认知能力',
        '🎓 幼儿创造力培养：通过游戏激发孩子的想象力',
        '🎓 数学启蒙：让孩子在生活中学习数学'
    ],
    '营养健康': [
        '🍎 幼儿饮食金字塔：如何搭配均衡的膳食',
        '🍎 儿童常见食物过敏：症状和预防方法',
        '🍎 春季儿童保健：预防感冒和过敏的方法'
    ],
    '产后恢复': [
        '🏥 产后盆底肌修复：为什么重要？如何进行？',
        '🏥 产后情绪管理：预防和应对产后抑郁',
        '🏥 产后饮食：促进身体恢复的营养建议'
    ],
    '育儿用品': [
        '🛍️ 婴儿奶瓶选购指南：玻璃vs塑料，哪种更好？',
        '🛍️ 安全座椅选购：如何选择适合孩子的型号',
        '🛍️ 婴儿衣物选择：舒适和安全的重要性'
    ]
}

def generate_articles_per_category():
    """为每个分类生成1~3篇文章"""
    db = next(get_db())
    
    try:
        # 为每个分类生成文章
        for category, topics in EIGHT_CATEGORIES.items():
            logger.info(f'开始为分类 {category} 生成文章')
            
            # 随机选择1~3个主题
            num_topics = random.randint(1, 3)
            selected_topics = random.sample(topics, num_topics)
            
            # 为每个选定的主题生成文章
            for topic in selected_topics:
                try:
                    # 生成文章
                    logger.info(f'生成文章: {topic}')
                    generated = generator_service.generate_content(
                        template_type='article',
                        category=category,
                        title=topic,
                        keywords=topic.split('：')[0].strip('🤰👶🌱👨‍👩‍👧🎓🍎🏥🛍️ ')
                    )
                    
                    if not generated:
                        logger.error(f'文章生成失败: {topic}')
                        continue
                    
                    # 检查文章是否已存在
                    existing_article = db.query(Content).filter(Content.title == generated['title']).first()
                    if existing_article:
                        logger.warning(f'文章已存在: {generated["title"]}')
                        continue
                    
                    # 检查ID是否已存在并生成新ID
                    max_id = db.query(Content.id).order_by(Content.id.desc()).first()
                    new_id = (max_id[0] if max_id else 0) + 1
                    
                    # 创建新文章
                    new_article = Content(
                        id=new_id,
                        title=generated['title'],
                        category=category,
                        summary=generated['summary'],
                        content=generated['content'],
                        author_id=1,  # 默认作者
                        is_published=True
                    )
                    
                    # 添加到数据库
                    db.add(new_article)
                    db.commit()
                    
                    logger.info(f'✅ 文章生成成功: ID={new_id}, 标题={generated["title"]}, 分类={category}')
                    
                except Exception as e:
                    logger.error(f'生成文章时出错: {topic}, 错误信息: {e}')
                    db.rollback()
                    continue
            
            logger.info(f'完成分类 {category} 的文章生成')
        
        logger.info('所有分类的文章生成完成')
        
    except Exception as e:
        logger.error(f'程序执行出错: {e}')
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    logger.info('开始为8大分类生成文章')
    generate_articles_per_category()
    logger.info('文章生成程序结束')