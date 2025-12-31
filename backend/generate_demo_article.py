#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为用户生成一篇高质量的演示文章
"""

import os
import sys
from datetime import datetime
from database import SessionLocal
from models import Content

def generate_demo_article():
    """生成一篇婴儿辅食添加指南演示文章"""
    
    # 初始化数据库连接
    session = SessionLocal()
    
    # 文章内容 - 符合小红书风格
    demo_content = """
<h3>🍼 新手妈妈必看！宝宝辅食添加全攻略</h3>
<p>姐妹们！今天想和大家分享宝宝辅食添加的超全攻略。作为两个宝宝的妈妈，我深知新手妈妈对辅食添加的困惑和担心。希望这篇笔记能帮到你们！</p>

<h3>📅 什么时候开始添加辅食？</h3>
<p>根据儿科医生的建议，宝宝6个月左右就可以开始添加辅食了。但是每个宝宝发育情况不同，我们可以观察这些信号：</p>
<ul>
<li><strong>生理准备</strong>：能够坐立，颈部支撑力充足</li>
<li><strong>兴趣信号</strong>：对食物表现出浓厚兴趣，看到大人吃饭会流口水</li>
<li><strong>发育信号</strong>：体重达到出生时的2倍，且不少于6公斤</li>
</ul>

<h3>🥄 辅食添加的正确顺序</h3>
<p>辅食添加要循序渐进，不能急于求成。我的经验是按照这个顺序：</p>
<ul>
<li><strong>第一阶段（6-7个月）</strong>：高铁米粉 → 蔬菜泥（胡萝卜、南瓜、土豆）</li>
<li><strong>第二阶段（7-8个月）</strong>：水果泥（苹果、香蕉、梨）→ 蛋黄泥 → 肉泥</li>
<li><strong>第三阶段（8-10个月）</strong>：烂面条、小米粥、软米饭</li>
<li><strong>第四阶段（10-12个月）</strong>：小颗粒食物、手指食物</li>
</ul>

<h3>⚠️ 添加辅食的注意事项</h3>
<p>这些坑我踩过，你们千万别再踩了：</p>
<ul>
<li><strong>不要加盐</strong>：1岁前的宝宝肾脏发育不完善，不能吃盐</li>
<li><strong>单一食材</strong>：每次只添加一种新食物，观察3天无过敏反应再加下一种</li>
<li><strong>温度适宜</strong>：食物温度控制在37-40度，不要太烫</li>
<li><strong>循序渐进</strong>：从少到多，从稀到稠，从细到粗</li>
</ul>

<h3>🍎 实用辅食制作方法</h3>
<p>分享几个简单易做的辅食制作方法：</p>
<ul>
<li><strong>胡萝卜泥</strong>：蒸熟后用勺子压成泥，加少量温水调成糊状</li>
<li><strong>苹果泥</strong>：去皮蒸熟打成泥，也可以用研磨碗压碎</li>
<li><strong>蛋黄泥</strong>：水煮蛋取蛋黄，用温水调成糊状</li>
</ul>

<h3>💕 给妈妈们的建议</h3>
<p>添加辅食是一个过程，不要给自己太大压力。每个宝宝的接受能力不同，有的宝宝可能需要多次尝试才会接受新食物。保持耐心，多尝试不同的做法，相信宝宝会健康成长的！</p>

<p>有什么问题可以评论区交流哦，我们一起分享育儿经验！</p>
"""
    
    try:
        print(f"🎯 正在创建演示文章...")
        print(f"📅 创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # 手动创建文章对象
        article = Content(
            id=188,  # 更新现有文章
            title="🍼婴儿辅食添加全攻略｜新手妈妈必备！从泥状到颗粒状的科学喂养指南👶",
            content=demo_content,
            category="婴儿护理",
            author_id=1,
            is_published=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            view_count=0,
            published_at=datetime.now(),
            price=9.90,
            summary="详细介绍了婴儿辅食添加的最佳时机、正确顺序、制作方法和注意事项，帮助新手妈妈科学喂养宝宝。涵盖从6个月到12个月的完整辅食添加指南。"
        )
        
        # 先删除现有文章
        existing = session.query(Content).filter(Content.id == 188).first()
        if existing:
            session.delete(existing)
            session.commit()
            print("🗑️ 已删除旧文章")
        
        # 保存新文章
        session.add(article)
        session.commit()
        
        print(f"✅ 演示文章创建完成!")
        print(f"📝 文章ID: 188")
        print(f"📂 分类: 婴儿护理")
        print(f"📄 字数: {len(demo_content)} 字符")
        print(f"💾 已保存到数据库")
        
        # 显示内容摘要
        print(f"\n📖 文章特色:")
        print("• 符合小红书风格：标题带emoji，语言亲切自然")
        print("• 内容结构清晰：5个主要段落，逻辑分明")
        print("• 实用性强：包含具体的操作步骤和注意事项")
        print("• 专业可信：基于育儿经验和科学建议")
        print("• HTML格式：包含h3、p、ul、li等标签，便于前端展示")
        
    except Exception as e:
        print(f"❌ 创建过程中出现错误: {str(e)}")
        session.rollback()
    finally:
        # 关闭数据库连接
        session.close()
        
        print("\n" + "=" * 60)
        print(f"🎉 演示文章创建完成!")

if __name__ == "__main__":
    generate_demo_article()