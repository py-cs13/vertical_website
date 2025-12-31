"""
生成10篇母婴文章
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models import Content
from content_generator import DeepSeekGenerator
from datetime import datetime

def generate_articles():
    """生成10篇母婴文章"""
    generator = DeepSeekGenerator()
    
    # 定义文章主题：5个分类，每个分类2篇文章
    article_plan = [
        {
            "category": "婴儿护理",
            "topics": [
                "宝宝打疫苗后的常见反应和护理要点",
                "婴儿肠绞痛的症状识别和缓解方法"
            ]
        },
        {
            "category": "早教启蒙",
            "topics": [
                "如何通过绘本阅读培养宝宝的认知能力",
                "户外活动对宝宝大运动发展的重要性"
            ]
        },
        {
            "category": "孕期指南",
            "topics": [
                "孕期产检时间表和必查项目详解",
                "孕期如何科学控制体重避免过度增长"
            ]
        },
        {
            "category": "产后恢复",
            "topics": [
                "产后盆底肌修复的最佳时间和训练方法",
                "产后避孕那些事：科学避孕保护妈妈健康"
            ]
        },
        {
            "category": "宝宝健康",
            "topics": [
                "宝宝第一次发烧怎么办？新手妈妈必备应对指南",
                "婴儿配方奶的正确冲调和喂养方法"
            ]
        }
    ]
    
    session = SessionLocal()
    count = 0
    
    try:
        for category_info in article_plan:
            category_name = category_info["category"]
            topics = category_info["topics"]
            
            for topic in topics:
                print(f"\n正在生成：{category_name} - {topic}")
                
                try:
                    # 生成文章
                    article = generator.generate_article(topic, category_name)
                    
                    if article:
                        # 保存到数据库
                        content = Content(
                            title=article["title"],
                            content=article["content"],
                            summary=article["summary"],
                            category=category_name,
                            author_id=1,  # 默认作者
                            is_published=True,
                            created_at=datetime.now(),
                            updated_at=datetime.now()
                        )
                        session.add(content)
                        session.commit()
                        
                        print(f"✅ 成功生成文章：{article['title']}")
                        count += 1
                    else:
                        print(f"❌ 生成失败：{topic}")
                        
                except Exception as e:
                    print(f"❌ 生成出错：{topic} - {str(e)}")
                    session.rollback()
                    continue
    
    finally:
        session.close()
    
    print(f"\n🎉 共成功生成 {count} 篇文章")
    return count

if __name__ == "__main__":
    generate_articles()
