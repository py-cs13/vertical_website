#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第三批母婴文章生成脚本 (ID: 188-197)
主题覆盖：婴儿抚触、幼儿语言发展、孕期水肿、产后睡眠、宝宝肠胃护理等
"""

import os
import sys
from datetime import datetime
from content_generator import DeepSeekGenerator
from database import SessionLocal
from models import Content

def generate_third_batch_articles():
    """生成第三批10篇母婴文章 (ID: 188-197)"""
    
    # 初始化数据库连接和生成器
    session = SessionLocal()
    generator = DeepSeekGenerator()
    
    # 第三批文章主题配置 (ID: 188-197)
    # 确保覆盖前端指定的8个大类：['母婴育儿', '育儿知识', '营养辅食', '产后恢复', '亲子互动', '成长发育', '早期教育', '健康养生']
    articles_plan = [
        {
            "id": 188,
            "title": "👶宝宝肠胃敏感怎么办？肠道健康守护指南💪",
            "category": "母婴育儿",  # 大类1：母婴育儿
            "prompt": """请生成一篇关于宝宝肠胃护理的专业指南，要求：
            
1. 标题使用emoji，内容专业实用
2. 包含以下内容结构：
   - 宝宝肠胃发育特点
   - 常见肠胃问题及识别
   - 肠胃敏感的护理方法
   - 益生菌和饮食调理
   - 预防肠胃疾病的措施
3. 语言专业可信，给家长信心
4. 提供科学的护理建议
5. 字数控制在800-1200字"""
        },
        {
            "id": 189,
            "title": "👶婴儿抚触按摩全攻略｜促进发育增进亲子关系的温柔时光💕",
            "category": "育儿知识",  # 大类2：育儿知识
            "prompt": """请生成一篇关于婴儿抚触按摩的专业指南，要求：
            
1. 标题使用emoji，内容通俗易懂
2. 包含以下内容结构：
   - 婴儿抚触的科学原理和好处
   - 最佳按摩时间和环境准备
   - 详细的按摩手法和步骤
   - 注意事项和安全提醒
   - 不同月龄的按摩重点
3. 语言亲切自然，适合新手妈妈阅读
4. 突出实用性和可操作性
5. 字数控制在800-1200字"""
        },
        {
            "id": 190,
            "title": "🍎孕期补铁全攻略｜告别贫血让孕期更健康💪",
            "category": "营养辅食",  # 大类3：营养辅食
            "prompt": """请生成一篇关于孕期补铁的专业指南，要求：
            
1. 标题使用emoji，内容科学实用
2. 包含以下内容结构：
   - 孕期缺铁的危害和症状
   - 铁需求量计算和补充时机
   - 富含铁的食物推荐
   - 铁剂补充的注意事项
   - 铁吸收促进和抑制因素
3. 语言专业可信，给孕妇指导
4. 提供实用的补铁方案
5. 字数控制在800-1200字"""
        },
        {
            "id": 191,
            "title": "💤产后失眠怎么办？新手妈妈睡眠修复全攻略🌙",
            "category": "产后恢复",  # 大类4：产后恢复
            "prompt": """请生成一篇关于产后睡眠质量改善的指南，要求：
            
1. 标题使用emoji，内容温暖贴心
2. 包含以下内容结构：
   - 产后失眠的常见原因分析
   - 建立健康睡眠习惯的方法
   - 利用碎片时间休息的技巧
   - 家人支持和分工建议
   - 长期睡眠不足的健康影响
3. 语言理解体贴，给妈妈们温暖
4. 提供实用的睡眠改善方案
5. 字数控制在800-1200字"""
        },
        {
            "id": 192,
            "title": "🤝培养宝宝社交能力｜从小培养人际交往的温柔引导🌈",
            "category": "亲子互动",  # 大类5：亲子互动
            "prompt": """请生成一篇关于幼儿社交能力培养的指南，要求：
            
1. 标题使用emoji，内容温暖实用
2. 包含以下内容结构：
   - 社交能力发展的重要性
   - 不同年龄段的社交特点
   - 创造社交机会的方法
   - 处理冲突和分享的技巧
   - 家长如何引导和支持
3. 语言温柔鼓励，给家长信心
4. 提供具体的培养方法
5. 字数控制在800-1200字"""
        },
        {
            "id": 193,
            "title": "🦷婴儿口腔护理大揭秘｜从出生开始的牙齿保护计划✨",
            "category": "成长发育",  # 大类6：成长发育
            "prompt": """请生成一篇关于婴儿口腔护理的专业指南，要求：
            
1. 标题使用emoji，内容科学细致
2. 包含以下内容结构：
   - 婴儿口腔发育阶段
   - 新生儿口腔清洁方法
   - 出牙期的护理要点
   - 正确的刷牙技巧和工具
   - 口腔疾病预防和处理
3. 语言专业温和，消除家长焦虑
4. 提供详细的护理步骤
5. 字数控制在800-1200字"""
        },
        {
            "id": 194,
            "title": "🌟幼儿语言发展黄金期｜从咿呀学语到流利表达的实用指南💬",
            "category": "早期教育",  # 大类7：早期教育
            "prompt": """请生成一篇关于幼儿语言发展的实用指南，要求：
            
1. 标题使用emoji，内容科学实用
2. 包含以下内容结构：
   - 语言发展的关键里程碑
   - 0-3岁语言发展阶段详解
   - 促进语言发展的有效方法
   - 创造丰富的语言环境
   - 常见语言发展问题及应对
3. 语言温暖鼓励，给家长信心
4. 提供具体的互动游戏和方法
5. 字数控制在800-1200字"""
        },
        {
            "id": 195,
            "title": "🧴宝宝皮肤护理全攻略｜呵护娇嫩肌肤远离湿疹困扰👶",
            "category": "健康养生",  # 大类8：健康养生
            "prompt": """请生成一篇关于宝宝皮肤护理的专业指南，要求：
            
1. 标题使用emoji，内容专业细致
2. 包含以下内容结构：
   - 宝宝皮肤特点和保护需求
   - 日常皮肤护理的正确方法
   - 湿疹等皮肤问题的处理
   - 护肤品选择和使用指南
   - 环境因素对皮肤的影响
3. 语言专业温和，给家长指导
4. 提供详细的护理步骤
5. 字数控制在800-1200字"""
        },
        {
            "id": 196,
            "title": "🤰孕期水肿难受？这些缓解方法让你孕期更舒适✨",
            "category": "营养辅食",  # 大类3：营养辅食（额外一篇）
            "prompt": """请生成一篇关于孕期水肿缓解方法的指南，要求：
            
1. 标题使用emoji，内容贴心实用
2. 包含以下内容结构：
   - 孕期水肿的原因和症状
   - 预防水肿的日常护理
   - 有效的缓解方法和技巧
   - 饮食调理和生活习惯
   - 何时需要就医的警示信号
3. 语言关怀体贴，理解孕妇辛苦
4. 提供简单易行的缓解方法
5. 字数控制在800-1200字"""
        },
        {
            "id": 197,
            "title": "⚖️产后体重管理秘籍｜健康恢复拒绝身材焦虑🌸",
            "category": "产后恢复",  # 大类4：产后恢复（额外一篇）
            "prompt": """请生成一篇关于产后体重管理的指南，要求：
            
1. 标题使用emoji，内容温暖鼓励
2. 包含以下内容结构：
   - 产后体重变化规律
   - 科学的减重时间安排
   - 健康饮食和运动计划
   - 哺乳期的特殊考虑
   - 心理调适和自信建立
3. 语言温暖鼓励，给妈妈们信心
4. 提供健康可持续的管理方法
5. 字数控制在800-1200字"""
        }
    ]
    
    print(f"🎯 开始生成第三批母婴文章 (ID: 188-197)")
    print(f"📅 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 生成每篇文章
    for article_plan in articles_plan:
        try:
            print(f"\n📝 正在生成文章 {article_plan['id']}: {article_plan['title'][:50]}...")
            
            # 生成文章内容
            article_content = generator.generate_article(
                topic=article_plan['title'],
                category=article_plan['category'],
                keywords=article_plan['title']  # 使用标题作为关键词
            )
            
            if article_content and 'content' in article_content:
                # 检查ID是否已存在，存在则删除旧记录
                existing_article = session.query(Content).filter(Content.id == article_plan['id']).first()
                if existing_article:
                    print(f"🗑️  已存在ID为{article_plan['id']}的文章，正在删除...")
                    session.delete(existing_article)
                    session.commit()
                
                # 创建文章对象
                article = Content(
                    id=article_plan['id'],
                    title=article_plan['title'],
                    content=article_content['content'],
                    category=article_plan['category'],
                    summary=article_content.get('summary', article_plan['title'][:100] + "..."),
                    author_id=1,  # 使用ID为1的默认作者
                    is_published=True,
                    published_at=datetime.now(),
                    view_count=0,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
            else:
                print(f"❌ 文章内容生成失败")
                continue
            
            # 保存到数据库
            session.add(article)
            session.commit()
            
            print(f"✅ 文章 {article_plan['id']} 生成完成: {article_plan['category']}")
            
        except Exception as e:
            print(f"❌ 文章 {article_plan['id']} 生成失败: {str(e)}")
            session.rollback()
            continue
    
    # 关闭数据库连接
    session.close()
    
    print("\n" + "=" * 60)
    print(f"🎉 第三批文章生成完成！")
    print(f"📊 新增文章: 10篇 (ID: 188-197)")
    print(f"📅 完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 显示文章概览
    print(f"\n📋 文章概览:")
    for article_plan in articles_plan:
        print(f"   ID {article_plan['id']}: {article_plan['category']} - {article_plan['title'][:40]}...")

if __name__ == "__main__":
    generate_third_batch_articles()