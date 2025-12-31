#!/usr/bin/env python3
"""
为母婴用品分类生成8篇高质量文章
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models import Content
from content_generator import DeepSeekGenerator
from datetime import datetime

def generate_mother_baby_product_articles():
    """为母婴用品分类生成8篇高质量文章"""
    
    print("🍼 开始为母婴用品分类生成8篇高质量文章")
    print("=" * 60)
    
    # 初始化数据库会话
    session = SessionLocal()
    generator = DeepSeekGenerator()
    
    # 母婴用品分类的文章主题
    article_topics = [
        {
            "title": "👶 新生儿必备用品清单｜新手妈妈必看的实用购物指南",
            "keywords": "新生儿用品,必备清单,购物指南,新手妈妈"
        },
        {
            "title": "🍼 宝宝奶瓶选择全攻略｜如何挑选最适合的奶瓶品牌",
            "keywords": "奶瓶选择,宝宝喂养,奶瓶品牌,新手妈妈"
        },
        {
            "title": "👗 婴儿服装选购指南｜如何为宝宝选择安全舒适的衣物",
            "keywords": "婴儿服装,选购指南,宝宝衣物,安全材质"
        },
        {
            "title": "🛁 婴儿洗护用品推荐｜温和无刺激的宝宝专用产品",
            "keywords": "婴儿洗护,宝宝护肤,洗护用品,温和产品"
        },
        {
            "title": "🛏️ 婴儿床品选购指南｜打造安全舒适的睡眠环境",
            "keywords": "婴儿床,床品选购,宝宝睡眠,睡眠安全"
        },
        {
            "title": "🚼 婴儿推车选购攻略｜如何选择适合的出行工具",
            "keywords": "婴儿推车,出行工具,选购攻略,宝宝推车"
        },
        {
            "title": "🧸 婴儿玩具安全指南｜如何选择益智又安全的玩具",
            "keywords": "婴儿玩具,安全玩具,益智玩具,玩具选择"
        },
        {
            "title": "🏥 家庭婴儿护理用品清单｜必备的医疗和护理用品",
            "keywords": "婴儿护理,护理用品,家庭护理,婴儿医疗"
        }
    ]
    
    generated_ids = []
    
    for i, topic_config in enumerate(article_topics, 1):
        try:
            print(f"\n📝 正在生成第{i}篇文章...")
            print(f"   标题: {topic_config['title']}")
            print(f"   分类: 母婴用品")
            
            # 生成文章内容
            article = generator.generate_article(
                topic=topic_config['title'],
                category="母婴用品",
                keywords=topic_config['keywords']
            )
            
            if article and article.get('content'):
                # 创建文章对象
                new_article = Content(
                    title=topic_config['title'],
                    content=article['content'],
                    category="母婴用品",
                    summary=article.get('summary', f"关于{topic_config['title'][2:]}的详细指南"),
                    author_id=1,
                    is_published=True,
                    published_at=datetime.now(),
                    view_count=0,
                    price=9.90,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                
                session.add(new_article)
                session.commit()
                
                generated_ids.append(new_article.id)
                print(f"   ✅ 文章ID: {new_article.id} 生成成功")
                
            else:
                print(f"   ❌ 文章生成失败")
                
        except Exception as e:
            print(f"   ❌ 生成第{i}篇文章时出错: {str(e)}")
            session.rollback()
    
    session.close()
    
    print("\n" + "=" * 60)
    print(f"🎉 母婴用品分类文章生成完成！")
    print(f"📊 共生成 {len(generated_ids)} 篇文章")
    print(f"📂 分类: 母婴用品")
    print(f"🆔 文章ID列表: {generated_ids}")
    
    # 显示更新后的分类统计
    print(f"\n📈 更新后的母婴用品分类统计:")
    session = SessionLocal()
    from sqlalchemy import text
    result = session.execute(text(
        "SELECT COUNT(*) FROM contents WHERE category = '母婴用品'"
    ))
    count = result.scalar()
    print(f"   母婴用品分类现在共有 {count} 篇文章")
    session.close()
    
    return generated_ids

if __name__ == "__main__":
    generate_mother_baby_product_articles()