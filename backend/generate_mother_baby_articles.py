#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
母婴垂直网站内容生成脚本
用于生成真实的母婴相关文章并发布到数据库
"""

import sys
import os
from datetime import datetime

# 添加backend目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入配置和内容生成器
from config import settings
from content_generator import AutoContentPublisher
from database import SessionLocal

# 检查百度智能云千帆API密钥是否配置
if not settings.DEEPSEEK_API_KEY:
    print("❌ 错误: 未配置百度智能云千帆API密钥")
    print("请在.env文件中添加DEEPSEEK_API_KEY=your-baidu-qianfan-api-key")
    sys.exit(1)

# 母婴主题列表
mother_baby_topics = [
    # 孕期护理
    "怀孕初期的注意事项和饮食建议",
    "孕期常见不适症状及缓解方法",
    "孕期运动的好处和安全指南",
    "产检时间表及重要检查项目详解",
    "孕期情绪管理：如何保持心理健康",
    
    # 产后恢复
    "产后恢复的关键时期和注意事项",
    "产后饮食调理：促进身体恢复和乳汁分泌",
    "产后盆底肌修复的重要性和训练方法",
    "产后瘦身：健康有效的体重管理",
    "产后抑郁症的识别和应对策略",
    
    # 新生儿护理
    "新生儿日常护理指南（洗澡、换尿布等）",
    "新生儿喂养技巧：母乳喂养vs配方奶喂养",
    "新生儿睡眠规律建立和常见问题解决",
    "新生儿黄疸的认识和护理方法",
    "新生儿疫苗接种时间表和注意事项",
    
    # 婴儿成长发育
    "婴儿发育里程碑：0-12个月各阶段特点",
    "婴儿辅食添加的最佳时间和方法",
    "婴儿爬行和行走训练的技巧",
    "婴儿语言发展：如何促进宝宝说话",
    "婴儿精细动作和大动作发育训练",
    
    # 育儿经验
    "科学育儿的基本原则和误区",
    "如何培养宝宝良好的睡眠习惯",
    "宝宝哭闹的原因和安抚方法",
    "幼儿分离焦虑的应对策略",
    "家庭环境对宝宝成长的影响",
    
    # 儿童健康
    "儿童常见疾病的预防和护理",
    "儿童营养需求：如何保证均衡饮食",
    "儿童口腔健康：刷牙习惯养成",
    "儿童视力保护：预防近视的方法",
    "儿童运动发育：适合不同年龄的运动",
    
    # 亲子关系
    "如何建立良好的亲子依恋关系",
    "有效沟通：与宝宝建立情感连接",
    "亲子游戏：促进宝宝全面发展",
    "如何正确表扬和鼓励孩子",
    "家庭和谐对孩子成长的重要性"
]

# 分类设置
category = "母婴育儿"

def generate_articles():
    """生成并发布母婴相关文章"""
    print("🚀 开始生成母婴垂直网站文章")
    print(f"📅 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 创建数据库会话
    db = SessionLocal()
    publisher = AutoContentPublisher(db)
    
    try:
        # 生成文章
        total_topics = len(mother_baby_topics)
        generated_count = 0
        failed_count = 0
        
        for index, topic in enumerate(mother_baby_topics, 1):
            print(f"\n{index}/{total_topics} 生成文章: {topic}")
            
            try:
                # 生成并发布文章
                result = publisher.generate_and_publish(
                    category=category,
                    title=topic,
                    keywords=topic,
                    template_type="article",
                    author_id=1  # 默认作者ID
                )
                
                if result:
                    print(f"✅ 发布成功: {result['title']} (ID: {result['id']})")
                    generated_count += 1
                else:
                    print("❌ 发布失败")
                    failed_count += 1
                    
            except Exception as e:
                print(f"❌ 处理失败: {e}")
                failed_count += 1
        
        # 输出统计信息
        print("\n" + "=" * 60)
        print("📊 内容生成统计")
        print(f"总主题数: {total_topics}")
        print(f"成功发布: {generated_count}")
        print(f"发布失败: {failed_count}")
        print(f"成功率: {generated_count/total_topics*100:.1f}%")
        
    except Exception as e:
        print(f"\n❌ 脚本执行出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 关闭数据库会话
        db.close()

if __name__ == "__main__":
    generate_articles()
