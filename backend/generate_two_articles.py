"""
生成两篇高质量母婴文章并保存到数据库
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content_generator import DeepSeekGenerator
from database import SessionLocal
from models import Content
from datetime import datetime

def main():
    # 初始化生成器
    print("🚀 初始化内容生成器...")
    generator = DeepSeekGenerator()
    
    # 测试API连接
    print("\n🔗 测试百度智能云千帆API连接...")
    if not generator.test_connection():
        print(f"❌ API连接失败")
        return
    print("✅ API连接成功！")
    
    # 定义两篇文章的主题（贴近母婴群体需求）
    article_topics = [
        {
            "title": "宝宝多大可以吃盐？99%妈妈都做错了",
            "description": "关于宝宝吃盐的正确时间、用量建议，以及辅食调味品的科学使用方法，帮助新手妈妈避开误区",
            "category": "育儿知识"
        },
        {
            "title": "宝宝红屁屁反复发作？可能是你护理方法不对",
            "description": "宝宝红屁屁（尿布疹）的原因分析、预防方法和护理技巧，让宝宝远离红屁屁困扰",
            "category": "宝宝护理"
        }
    ]
    
    # 生成并保存文章
    print("\n📝 开始生成文章...")
    for i, topic in enumerate(article_topics, 1):
        print(f"\n{'='*50}")
        print(f"📖 文章 {i}/{len(article_topics)}: {topic['title']}")
        print(f"{'='*50}")
        
        # 调用生成器生成文章内容
        article = generator.generate_article(
            topic=topic['title'],
            category=topic['category'],
            keywords=f"{topic['category']}, {topic['title']}, 母婴, 育儿"
        )
        
        if article and "title" in article and "content" in article:
            title = article.get("title", topic['title'])
            summary = article.get("summary", f"关于{topic['category']}的专业知识分享")
            content_html = article.get("content", "")
            
            # 保存到数据库
            db = SessionLocal()
            try:
                content = Content(
                    title=title,
                    category=topic['category'],
                    summary=summary,
                    content=content_html,
                    author_id=1,  # 假设管理员ID为1
                    is_published=True,
                    published_at=datetime.now(),
                    view_count=0,
                    likes=0,
                    price=0.00  # 免费文章
                )
                db.add(content)
                db.commit()
                db.refresh(content)
                
                print(f"\n✅ 文章生成并保存成功！")
                print(f"   ID: {content.id}")
                print(f"   标题: {title}")
                print(f"   分类: {topic['category']}")
                print(f"   摘要: {summary[:100]}...")
                print(f"   字数: {len(content_html)} 字符")
                
            except Exception as e:
                db.rollback()
                print(f"❌ 保存文章到数据库失败: {e}")
            finally:
                db.close()
        else:
            print(f"❌ 文章生成失败")
    
    print(f"\n{'='*50}")
    print("🎉 两篇文章生成完成！")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
