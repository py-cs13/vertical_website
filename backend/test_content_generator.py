#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化内容生成功能测试脚本
用于验证百度智能云千帆API连接和DeepSeek模型内容生成功能
"""

import sys
import os
from datetime import datetime

# 添加backend目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入配置和内容生成器
from config import settings
from content_generator import DeepSeekGenerator, AutoContentPublisher

# 检查百度智能云千帆API密钥是否配置
if not settings.DEEPSEEK_API_KEY:
    print("❌ 错误: 未配置百度智能云千帆API密钥")
    print("请在.env文件中添加DEEPSEEK_API_KEY=your-baidu-qianfan-api-key")
    sys.exit(1)

# 创建测试数据
test_topics = [
    "婴儿辅食添加的最佳时间和注意事项",
    "产后恢复的5个关键要点",
    "健康饮食：如何合理搭配一日三餐"
]

test_categories = ["母婴育儿"]

def test_deepseek_connection():
    """测试百度智能云千帆API连接"""
    print("\n🔍 测试百度智能云千帆API连接...")
    generator = DeepSeekGenerator()
    
    try:
        # 测试API连接
        response = generator.test_connection()
        if response:
            print("✅ 百度智能云千帆API连接成功!")
            return True
        else:
            print("❌ 百度智能云千帆API连接失败")
            return False
    except Exception as e:
        print(f"❌ 百度智能云千帆API连接异常: {e}")
        return False

def test_content_generation():
    """测试内容生成功能"""
    print("\n📝 测试内容生成功能...")
    generator = DeepSeekGenerator()
    
    try:
        # 直接测试API调用，查看详细响应
        import requests
        import json
        
        topic = test_topics[0]
        category = test_categories[0]
        print(f"\n生成文章: {topic} ({category})")
        
        # 构建测试请求
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {generator.api_key}"
        }
        
        params = {}
        
        payload = {
            "model": "eb-instant",  # 添加模型字段
            "messages": [
                {"role": "system", "content": "你是一位专业的内容创作者，擅长生成高质量、有价值的文章和工具包。"},
                {"role": "user", "content": f"请生成一篇关于'{topic}'的{category}领域文章，包含标题、摘要和正文。"}
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        print(f"直接调用API测试:")
        print(f"URL: {generator.base_url}")
        print(f"请求头: Authorization: Bearer {generator.api_key[:20]}...")
        print(f"请求体: {json.dumps(payload, ensure_ascii=False)[:100]}...")
        
        response = requests.post(generator.base_url, headers=headers, params=params, json=payload, timeout=60)
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        # 然后再测试正常的生成方法
        article = generator.generate_article(topic, category)
        
        if article and "title" in article and "content" in article:
            print("✅ 文章生成成功!")
            print(f"标题: {article['title']}")
            print(f"摘要: {article['summary'][:100]}...")
            print(f"内容长度: {len(article['content'])} 字符")
            print(f"内容预览: {article['content'][:200]}...")
            return True
        else:
            print("❌ 文章生成失败")
            return False
    except Exception as e:
        print(f"❌ 内容生成异常: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_toolkit_generation():
    """测试工具包生成功能"""
    print("\n📦 测试工具包生成功能...")
    generator = DeepSeekGenerator()
    
    try:
        # 测试工具包生成
        topic = test_topics[1]
        category = test_categories[0]
        print(f"\n生成工具包: {topic} ({category})")
        
        toolkit = generator.generate_toolkit(topic, category)
        if toolkit and "title" in toolkit and "content" in toolkit:
            print(f"✅ 工具包生成成功!")
            print(f"标题: {toolkit['title']}")
            print(f"内容长度: {len(toolkit['content'])} 字")
            print(f"摘要: {toolkit['summary'][:100]}...")
            return True
        else:
            print("❌ 工具包生成失败")
            return False
    except Exception as e:
        print(f"❌ 工具包生成异常: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🚀 自动化内容生成功能测试开始")
    print("=" * 50)
    
    # 运行所有测试
    tests = [
        ("百度智能云千帆API连接", test_deepseek_connection),
        ("文章生成功能", test_content_generation),
        ("工具包生成功能", test_toolkit_generation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'=' * 50}")
        print(f"测试: {test_name}")
        print("-" * 50)
        
        if test_func():
            passed += 1
        
    print(f"\n{'=' * 50}")
    print(f"测试结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！自动化内容生成功能正常工作")
    else:
        print("⚠️  部分测试失败，请检查错误信息")
    
    print(f"\n测试完成于: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
