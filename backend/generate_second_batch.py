#!/usr/bin/env python3
"""
生成第二批10篇高质量母婴文章脚本（ID 178-187）
"""
import sys
import os
from datetime import datetime
from typing import List

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from content_generator import DeepSeekGenerator
from database import SessionLocal
from models import Content

def generate_second_batch_articles() -> List[int]:
    """
    生成第二批10篇高质量文章 (ID 178-187)
    
    Returns:
        List[int]: 生成的文章ID列表
    """
    db = SessionLocal()
    generator = DeepSeekGenerator()
    published_ids = []
    
    # 定义第二批10篇精心挑选的文章主题
    article_topics = [
        # 婴儿护理类
        ("宝宝出牙期的护理攻略：缓解疼痛的实用方法和注意事项", "婴儿护理", "出牙期,护理,疼痛缓解,注意事项,婴儿"),
        ("婴儿湿疹的识别与护理：科学方法告别宝宝肌肤问题", "婴儿护理", "婴儿湿疹,识别,护理,肌肤问题,科学方法"),
        
        # 幼儿教育类
        ("如何培养宝宝的自理能力：从穿衣吃饭到如厕训练的进阶指南", "幼儿教育", "自理能力,穿衣吃饭,如厕训练,培养,进阶"),
        ("音乐启蒙对宝宝的重要性：培养节奏感与创造力的科学方法", "幼儿教育", "音乐启蒙,节奏感,创造力,科学方法,培养"),
        
        # 孕期营养类
        ("孕期必需营养素详解：叶酸、铁、钙、DHA的补充时机与方法", "孕期营养", "孕期营养素,叶酸,铁钙DHA,补充时机,科学方法"),
        ("孕期血糖管理：妊娠糖尿病的预防和饮食控制指南", "孕期营养", "孕期血糖,妊娠糖尿病,预防,饮食控制,管理"),
        
        # 产后恢复类
        ("产后抑郁的识别与应对：新手妈妈的心理健康指南", "产后恢复", "产后抑郁,识别,应对,心理健康,新手妈妈"),
        ("产后重返职场准备：哺乳、育儿和工作平衡的实用建议", "产后恢复", "产后重返职场,哺乳,育儿,工作平衡,实用建议"),
        
        # 宝宝健康类
        ("宝宝过敏体质识别：常见过敏原和预防措施全解析", "宝宝健康", "宝宝过敏,过敏体质,过敏原,预防措施,识别"),
        ("儿童疫苗接种全攻略：接种时间表和注意事项详解", "宝宝健康", "儿童疫苗,接种时间表,注意事项,疫苗接种,全攻略")
    ]
    
    try:
        for i, (topic, category, keywords) in enumerate(article_topics, 1):
            print(f"正在生成第{i}篇文章: {topic} ({category})...")
            
            # 生成文章
            generated = generator.generate_article(
                topic=topic,
                category=category,
                keywords=keywords
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
                author_id=1,  # 使用默认作者ID
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
            print("=" * 80)
            
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
    print("开始生成第二批10篇高质量母婴文章...")
    print("=" * 80)
    
    # 生成文章
    generated_ids = generate_second_batch_articles()
    
    print("\n" + "=" * 80)
    print(f"🎉 第二批文章生成完成！")
    print(f"   共生成 {len(generated_ids)} 篇文章")
    print(f"   文章ID列表: {generated_ids}")
    print(f"   生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    return generated_ids

if __name__ == "__main__":
    main()