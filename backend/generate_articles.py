#!/usr/bin/env python3
"""
生成高质量母婴文章脚本
"""
import sys
import os
from datetime import datetime
from typing import List

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from content_generator import DeepSeekGenerator, AutoContentPublisher
from database import SessionLocal
from models import Content

def generate_high_quality_articles(category: str, topics: List[str], author_id: int = 1) -> List[int]:
    """
    生成高质量文章
    
    Args:
        category: 文章分类
        topics: 文章主题列表
        author_id: 作者ID
        
    Returns:
        List[int]: 生成的文章ID列表
    """
    db = SessionLocal()
    generator = DeepSeekGenerator()
    published_ids = []
    
    try:
        for topic in topics:
            print(f"正在生成文章: {topic} ({category})...")
            
            # 生成文章
            generated = generator.generate_article(
                topic=topic,
                category=category,
                keywords=f"{category}, {topic}, 母婴, 育儿"
            )
            
            if not generated:
                print(f"❌ 文章生成失败: {topic}")
                continue
            
            # 创建内容记录
            content = Content(
                title=generated["title"],
                category=category,
                summary=generated["summary"],
                content=generated["content"],
                author_id=author_id,
                is_published=True,
                published_at=datetime.now()
            )
            
            # 保存到数据库
            db.add(content)
            db.commit()
            db.refresh(content)
            
            published_ids.append(content.id)
            print(f"✅ 文章生成成功: {generated['title']} (ID: {content.id})")
            print(f"   摘要: {generated['summary'][:100]}...")
            print("=" * 50)
            
    except Exception as e:
        print(f"❌ 生成过程中发生错误: {str(e)}")
        db.rollback()
    finally:
        db.close()
    
    return published_ids

def main():
    """
    主函数
    """
    print("开始生成高质量母婴文章...")
    print("=" * 50)
    
    # 定义高质量文章主题
    article_topics = {
        "婴儿护理": [
            "新生儿护理全攻略：从出生第一天到满月",
            "婴儿睡眠训练：让宝宝安睡整夜的实用方法",
            "宝宝辅食添加指南：何时加、怎么加、加什么",
            "婴儿常见疾病护理：感冒、发烧、腹泻应对方法",
            "宝宝皮肤护理：湿疹、尿布疹预防与治疗"
        ],
        "幼儿教育": [
            "0-3岁宝宝早期教育：关键阶段与发展重点",
            "培养宝宝的语言能力：从牙牙学语到流利表达",
            "宝宝社交能力培养：如何让孩子学会与人相处",
            "幼儿专注力训练：提升注意力的有效游戏",
            "培养宝宝的创造力：激发想象力的艺术活动"
        ],
        "孕期营养": [
            "孕期饮食指南：每个阶段的营养需求",
            "孕期补剂选择：叶酸、DHA、钙铁锌怎么补",
            "孕期体重管理：健康增重与胎儿发育",
            "缓解孕吐的饮食方法：哪些食物能减轻不适",
            "孕期禁忌食物：这些东西千万不能吃"
        ],
        "产后恢复": [
            "产后身体恢复：子宫收缩、伤口护理与恶露排出",
            "产后盆底肌修复：预防漏尿与脱垂的训练方法",
            "产后身材恢复：科学减肥与塑形",
            "产后心理调节：预防产后抑郁的有效方法",
            "产后性生活：恢复时间与注意事项"
        ],
        "育儿经验": [
            "新手父母必知的育儿技巧：避免常见误区",
            "亲子沟通技巧：如何与孩子建立良好的关系",
            "宝宝行为习惯培养：吃饭、睡觉、刷牙好习惯",
            "应对宝宝哭闹：了解哭声背后的需求",
            "育儿压力缓解：平衡工作与照顾孩子"
        ]
    }
    
    total_generated = 0
    
    # 生成所有分类的文章
    for category, topics in article_topics.items():
        print(f"\n📚 开始生成【{category}】分类文章...")
        generated_ids = generate_high_quality_articles(category, topics)
        total_generated += len(generated_ids)
    
    print("\n" + "=" * 50)
    print(f"🎉 文章生成完成！")
    print(f"   共生成 {total_generated} 篇高质量母婴文章")
    print(f"   生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

if __name__ == "__main__":
    main()
