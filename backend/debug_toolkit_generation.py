#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试工具包生成功能的脚本
"""

import os
import sys
import requests
import json

# 添加backend目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import settings
from content_generator import DeepSeekGenerator

def debug_toolkit_generation():
    """调试工具包生成功能"""
    print("调试工具包生成功能")
    print("=" * 50)
    
    # 初始化生成器
    generator = DeepSeekGenerator()
    
    if not generator.api_key:
        print("❌ API密钥未配置")
        return
    
    # 测试数据
    topic = "科学育儿知识手册工具包"
    category = "母婴育儿"
    keywords = "科学育儿,育儿知识,育儿手册"
    
    # 直接使用模板内容
    toolkit_template = """
你是一位专业的小红书母婴领域专家，擅长生成符合小红书平台风格的实用工具包内容。请根据以下主题生成一个小红书风格的HTML格式工具包：

主题：{title}
关键词：{keywords}
分类：{category}

小红书风格要求：
1. **标题**：使用吸引人的标题，可适当使用emoji，突出工具包的价值和实用性
2. **开头**：使用亲切的语气介绍工具包的用途、价值和适用人群
3. **结构**：采用清晰的多层结构，包含以下部分：
   - 工具包概述：介绍工具包的核心价值和解决问题
   - 核心工具集合：详细列出5-8个核心工具或资源，每个工具包含：
     * 工具名称和用途
     * 具体内容描述
     * 使用方法和步骤
     * 下载链接和格式说明（如Excel、PDF、文档等）
   - 详细使用指南：每个工具的具体使用场景和操作步骤
   - 实际应用案例：3-4个真实场景的应用示例，包含完整的使用流程
   - 常见问题解答：6-8个用户可能遇到的问题和详细解决方案
4. **要点**：每个工具、方法或步骤使用<li>标签标记，方便阅读和操作
5. **语言**：口语化、实用、具体，避免过于专业的术语，确保普通用户能轻松理解
6. **表情符号**：适当使用emoji增强亲和力，但不超过内容的10%
7. **格式**：直接生成HTML格式，包含适当的HTML标签（如<h2>、<h3>、<p>、<ul>、<li>、<table>等）
8. **长度**：控制在2500-3500字之间，确保内容丰富全面
9. **实用性**：确保内容具有高度实操性，能够帮助读者解决实际问题
10. **价值体现**：突出工具包的独特价值和使用后的效果，包含具体的量化收益（如节省时间、提高效率等）

请严格按照以下格式输出，不要添加任何额外内容：
标题：[小红书风格的工具包名称]
摘要：[简短的工具包介绍，100字左右，不使用emoji]
内容：[符合小红书风格的完整HTML格式工具包内容，包含适当emoji和HTML标签]
"""
    
    prompt = toolkit_template.format(
        title=topic,
        keywords=keywords,
        category=category
    )
    
    print(f"生成提示词:\n{prompt}")
    print("\n" + "=" * 50)
    
    # 构建API请求
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {generator.api_key}"
    }

    print("\n=== API Request Details ===")
    print(f"API Key: {generator.api_key}")
    print(f"Base URL: {generator.base_url}")
    print(f"Prompt: {prompt}")
    print(f"Headers: {headers}")
    
    # 构建payload
    payload = {
        "model": "deepseek-v3.1-250821",
        "messages": [
            {
                "role": "system",
                "content": "你是一位专业的内容创作者，擅长生成高质量、有价值的文章和工具包。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    print(f"Payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")
    print("\n=== Sending API Request... ===")

    try:
        # 使用与content_generator.py中相同的请求方式
        response = requests.request("POST", generator.base_url, headers=headers, data=json.dumps(payload), timeout=120)  # 增加超时时间到120秒
        print(f"\n=== API Response ===")
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        response_text = response.text
        print(f"Response Text: {response_text}")
        
        # 尝试解析JSON响应
        try:
            response_json = response.json()
            print(f"\nResponse JSON: {json.dumps(response_json, ensure_ascii=False, indent=2)}")
        except json.JSONDecodeError:
            print(f"\nFailed to parse response as JSON")

        # 检查是否有错误
        if "error" in response_json:
            print(f"\nAPI Error: {response_json['error']['code']} - {response_json['error']['message']}")
            return

        # 处理响应
        if "choices" in response_json and response_json["choices"]:
            content = response_json["choices"][0]["message"]["content"]
            print(f"\n=== Generated Content ===")
            print(content)
            
            # 解析生成的内容
            parsed = _parse_generated_content(content)
            print(f"\n=== Parsed Content ===")
            print(f"Title: {parsed.get('title')}")
            print(f"Summary: {parsed.get('summary')}")
            print(f"Content: {parsed.get('content')}")
            print(f"Content Length: {len(parsed.get('content', ''))} characters")
        else:
            print(f"\nResponse format unexpected: {response_json}")

    except requests.exceptions.RequestException as e:
        print(f"\nAPI Request Failed: {str(e)}")
    except Exception as e:
        print(f"\nUnexpected Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_toolkit_generation()
