#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容自动生成服务
通过百度智能云千帆平台集成DeepSeek模型，实现自动化内容生成和发布功能
"""

import os
import logging
import requests
import json
from typing import Optional, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取日志记录器
from logging_config import get_logger
logger = get_logger(__name__)

# 导入配置
from config import settings

# 百度智能云千帆API配置
BAIDU_QIANFAN_API_KEY = settings.DEEPSEEK_API_KEY or ""  # 复用已配置的API密钥
BAIDU_QIANFAN_API_SECRET = None  # 如果需要，可以在.env中添加并从settings获取
BAIDU_QIANFAN_API_BASE_URL = "https://qianfan.baidubce.com/v2/chat/completions"  # 百度智能云千帆平台标准API端点

# 内容生成模板
CONTENT_TEMPLATES = {
    "article": """
你是一位专业的{category}领域内容创作者，请根据以下要求生成一篇高质量的文章：

标题：{title}
关键词：{keywords}

要求：
1. 内容结构清晰，包括引言、正文（分点阐述）、结论
2. 语言专业但通俗易懂，避免使用过于生僻的术语
3. 内容具有实用性和价值，能够帮助读者解决实际问题
4. 文章长度控制在800-1200字之间
5. 避免复制粘贴，保证内容的原创性

请按照以下格式输出：
标题：[文章标题]
摘要：[简短的内容摘要，100字左右]
正文：[完整的文章内容]
""",
    "toolkit": """
你是一位专业的{category}领域专家，请根据以下主题生成一个实用的工具包内容：

主题：{title}
关键词：{keywords}

要求：
1. 内容结构清晰，包括工具包介绍、使用方法、注意事项
2. 内容具有实操性，提供具体的步骤和建议
3. 语言简洁明了，重点突出
4. 内容长度控制在500-800字之间

请按照以下格式输出：
标题：[工具包名称]
摘要：[简短的工具包介绍，50字左右]
内容：[完整的工具包内容]
"""
}

class DeepSeekGenerator:
    """
    百度智能云千帆平台DeepSeek模型内容生成器
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化DeepSeek生成器
        
        Args:
            api_key: 百度智能云千帆API密钥
        """
        self.api_key = api_key or BAIDU_QIANFAN_API_KEY
        self.api_secret = BAIDU_QIANFAN_API_SECRET
        self.base_url = BAIDU_QIANFAN_API_BASE_URL
        
        if not self.api_key:
            logger.warning("未配置百度智能云千帆API密钥，内容生成功能将不可用")
    
    def generate_content(self, template_type: str, **kwargs) -> Optional[Dict[str, str]]:
        """
        使用百度智能云千帆API调用DeepSeek模型生成内容
        
        Args:
            template_type: 模板类型 (article/toolkit)
            **kwargs: 模板参数
                - category: 内容分类
                - title: 内容标题
                - keywords: 关键词
        
        Returns:
            Dict[str, str]: 生成的内容，包含title、summary、content
            None: 生成失败时返回
        """
        if not self.api_key:
            logger.error("百度智能云千帆API密钥未配置，无法生成内容")
            return None
        
        # 验证模板类型
        if template_type not in CONTENT_TEMPLATES:
            logger.error(f"不支持的模板类型: {template_type}")
            return None
        
        try:
            # 构建提示词
            prompt = CONTENT_TEMPLATES[template_type].format(**kwargs)
            
            # 调用百度智能云千帆API（使用用户提供的模板格式）
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": "deepseek-v3.1-250821",  # 使用用户提供的模型
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
            
            logger.info(f"调用百度智能云千帆API生成内容: {kwargs.get('title')}")
            # 使用用户提供的模板方式发送请求
            response = requests.request("POST", self.base_url, headers=headers, data=json.dumps(payload), timeout=60)
            response.raise_for_status()
            
            # 解析API响应
            result = response.json()
            
            # 检查是否有错误
            if "error" in result:
                logger.error(f"百度智能云千帆API错误: {result['error']['code']} - {result['error']['message']}")
                return None
            
            # 最新的API响应格式：{"choices": [{"message": {"role": "assistant", "content": "内容"}}], ...}
            if "choices" in result and result["choices"]:
                content = result["choices"][0]["message"]["content"]
                # 解析生成的内容
                generated_content = self._parse_generated_content(content)
            else:
                logger.error(f"百度智能云千帆API响应格式不符合预期: {result}")
                return None
            logger.info(f"内容生成成功: {generated_content.get('title')}")
            
            return generated_content
            
        except requests.exceptions.RequestException as e:
            logger.error(f"调用百度智能云千帆API失败: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"内容生成失败: {str(e)}")
            return None
    
    def test_connection(self) -> bool:
        """
        测试百度智能云千帆API连接
        
        Returns:
            bool: 连接成功返回True，失败返回False
        """
        if not self.api_key:
            return False
        
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": "deepseek-v3.1-250821",  # 使用用户提供的模型
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant."
                    },
                    {
                        "role": "user",
                        "content": "测试连接"
                    }
                ]
            }
            
            # 使用用户提供的模板方式发送请求
            response = requests.request("POST", self.base_url, headers=headers, data=json.dumps(payload), timeout=30)
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"百度智能云千帆API连接测试失败: {str(e)}")
            return False
    
    def generate_article(self, topic: str, category: str, keywords: str = "") -> Optional[Dict[str, str]]:
        """
        生成文章内容
        
        Args:
            topic: 文章主题
            category: 文章分类
            keywords: 关键词（可选）
        
        Returns:
            Dict[str, str]: 生成的文章内容
            None: 生成失败时返回
        """
        if not keywords:
            keywords = topic
        
        return self.generate_content(
            template_type="article",
            category=category,
            title=topic,
            keywords=keywords
        )
    
    def generate_toolkit(self, topic: str, category: str, keywords: str = "") -> Optional[Dict[str, str]]:
        """
        生成工具包内容
        
        Args:
            topic: 工具包主题
            category: 工具包分类
            keywords: 关键词（可选）
        
        Returns:
            Dict[str, str]: 生成的工具包内容
            None: 生成失败时返回
        """
        if not keywords:
            keywords = topic
        
        return self.generate_content(
            template_type="toolkit",
            category=category,
            title=topic,
            keywords=keywords
        )
    
    def _parse_generated_content(self, content: str) -> Dict[str, str]:
        """
        解析生成的内容
        
        Args:
            content: 生成的原始内容
            
        Returns:
            Dict[str, str]: 解析后的内容，包含title、summary、content
        """
        parsed = {
            "title": "",
            "summary": "",
            "content": ""
        }
        
        # 解析标题
        title_start = content.find("标题：")
        if title_start != -1:
            title_end = content.find("摘要：", title_start)
            if title_end != -1:
                parsed["title"] = content[title_start + 3:title_end].strip()
        
        # 解析摘要
        summary_start = content.find("摘要：")
        if summary_start != -1:
            content_start = content.find("正文：", summary_start)
            if content_start == -1:
                content_start = content.find("内容：", summary_start)
            if content_start != -1:
                parsed["summary"] = content[summary_start + 3:content_start].strip()
        
        # 解析正文/内容
        content_start = content.find("正文：")
        if content_start == -1:
            content_start = content.find("内容：")
        if content_start != -1:
            parsed["content"] = content[content_start + 3:].strip()
        
        return parsed

class AutoContentPublisher:
    """
    自动内容发布器
    """
    
    def __init__(self, db_session):
        """
        初始化自动发布器
        
        Args:
            db_session: 数据库会话
        """
        self.db = db_session
        self.generator = DeepSeekGenerator()
    
    def generate_and_publish(self, category: str, title: str, keywords: str, 
                            template_type: str = "article", author_id: int = 1) -> Optional[Dict[str, Any]]:
        """
        自动生成并发布内容
        
        Args:
            category: 内容分类
            title: 内容标题
            keywords: 关键词
            template_type: 模板类型 (article/toolkit)
            author_id: 作者ID，默认1
            
        Returns:
            Dict[str, Any]: 发布的内容信息
            None: 生成或发布失败时返回
        """
        try:
            # 生成内容
            generated = self.generator.generate_content(
                template_type=template_type,
                category=category,
                title=title,
                keywords=keywords
            )
            
            if not generated:
                logger.error("内容生成失败，无法发布")
                return None
            
            # 导入Content模型（避免循环导入）
            from models import Content
            
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
            self.db.add(content)
            self.db.commit()
            self.db.refresh(content)
            
            logger.info(f"内容自动发布成功: {content.title} (ID: {content.id})")
            
            return {
                "id": content.id,
                "title": content.title,
                "category": content.category,
                "published_at": content.published_at.isoformat()
            }
            
        except Exception as e:
            logger.error(f"自动发布失败: {str(e)}")
            self.db.rollback()
            return None

# 内容生成服务实例
generator_service = DeepSeekGenerator()
