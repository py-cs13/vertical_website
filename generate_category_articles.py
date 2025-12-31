#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为所有分类生成高质量文章脚本
"""

import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from backend.config import Settings
from backend.content_generator import DeepSeekGenerator

# 获取配置
settings = Settings()

# 创建生成器
generator = DeepSeekGenerator()

# 每个分类的主题列表，确保覆盖所有分类且文章质量高
category_topics = {
    "母婴育儿": [
        "新生儿护理的10个关键要点",
        "如何建立良好的亲子依恋关系",
        "宝宝常见睡眠问题及解决方法",
        "新手父母必知的育儿误区",
        "科学应对宝宝哭闹的方法",
        "宝宝安全防护全攻略",
        "婴儿抚触的好处与正确方法",
        "如何选择合适的婴儿用品"
    ],
    "育儿知识": [
        "正面管教的核心原则与实践",
        "培养孩子良好习惯的科学方法",
        "如何提高孩子的专注力",
        "儿童情绪管理技巧",
        "亲子沟通的艺术",
        "挫折教育对孩子成长的重要性",
        "如何培养孩子的自信心",
        "家风建设对孩子的影响"
    ],
    "营养辅食": [
        "6个月宝宝辅食添加全指南",
        "不同月龄宝宝的辅食食谱推荐",
        "宝宝辅食的科学搭配原则",
        "如何预防宝宝挑食偏食",
        "宝宝缺铁性贫血的饮食调理",
        "婴儿便秘的辅食解决方案",
        "宝宝辅食制作工具推荐",
        "过敏宝宝的辅食添加注意事项"
    ],
    "产后恢复": [
        "科学的产后恢复计划",
        "产后盆底肌修复的重要性与方法",
        "产后饮食调理与营养补充",
        "产后情绪管理与心理健康",
        "产后身材恢复的科学方法",
        "哺乳期常见问题及解决方法",
        "产后性生活的恢复与注意事项",
        "新手妈妈的时间管理技巧"
    ],
    "亲子互动": [
        "0-1岁宝宝的亲子互动游戏推荐",
        "培养亲子关系的日常活动",
        "如何通过游戏促进孩子的智力发展",
        "亲子阅读的正确方法与推荐书单",
        "户外亲子活动的好处与推荐",
        "家庭亲子手工制作项目",
        "亲子旅行的准备与注意事项",
        "如何与孩子建立良好的沟通模式"
    ],
    "成长发育": [
        "0-3岁宝宝发育里程碑追踪",
        "儿童语言发育的关键时期",
        "孩子运动能力发展的培养",
        "儿童认知发展的规律与促进",
        "如何识别孩子的发育迟缓",
        "孩子社交能力的培养方法",
        "儿童性别认知的发展与引导",
        "青少年心理健康与成长"
    ],
    "健康养生": [
        "宝宝常见疾病的家庭护理",
        "儿童免疫力的科学提升方法",
        "孩子用眼健康与视力保护",
        "儿童口腔护理全攻略",
        "预防儿童肥胖的科学方法",
        "孩子呼吸道疾病的预防与护理",
        "儿童皮肤护理的注意事项",
        "家庭急救知识与技能"
    ],
    "早期教育": [
        "蒙特梭利教育法的核心理念",
        "0-6岁儿童敏感期的把握",
        "如何培养孩子的阅读兴趣",
        "儿童艺术启蒙的正确方法",
        "数学启蒙的趣味方法",
        "科学启蒙从家庭开始",
        "如何选择合适的早教机构",
        "幼小衔接的准备与过渡"
    ]
}

def main():
    """主函数"""
    print("正在连接数据库...")
    
    # 创建数据库引擎
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        print("\n开始为所有分类生成高质量文章...")
        
        # 为每个分类生成文章
        for category, topics in category_topics.items():
            print(f"\n正在处理分类: {category}")
            
            # 为该分类的每个主题生成文章
            for topic in topics:
                print(f"  正在生成主题: {topic}")
                
                # 生成文章
                try:
                    article = generator.generate_article(topic, category)
                    
                    # 保存到数据库
                    db.execute(
                        text("""
                        INSERT INTO contents (title, content, category, summary, author_id, is_published, view_count, published_at, price, created_at, updated_at)
                        VALUES (:title, :content, :category, :summary, :author_id, :is_published, 0, NOW(), :price, NOW(), NOW())
                        """),
                        {
                            "title": article["title"],
                            "content": article["content"],
                            "category": category,
                            "summary": article["content"][:150] + "...",
                            "author_id": 1,  # 默认作者ID
                            "is_published": True,
                            "price": 9.9
                        }
                    )
                    
                    db.commit()
                    print(f"  ✓ 成功生成文章: {article['title']}")
                    
                    # 避免请求过于频繁，添加适当延迟
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"  ✗ 生成文章失败: {e}")
                    db.rollback()
                    continue
        
        print("\n所有分类文章生成完成！")
        
    except Exception as e:
        print(f"\n发生错误: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
