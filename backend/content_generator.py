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
from datetime import datetime
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取日志记录器
from logging_config import get_logger
logger = get_logger(__name__)

# 导入配置
from config import settings

# 百度智能云千帆API配置
BAIDU_QIANFAN_API_KEY = settings.DEEPSEEK_API_KEY  # 从配置文件获取API密钥
BAIDU_QIANFAN_API_SECRET = None  # 百度智能云千帆API密钥(可选，当前配置不需要)
BAIDU_QIANFAN_API_BASE_URL = settings.DEEPSEEK_API_BASE_URL  # 从配置文件获取API端点

# 内容生成模板 - 小红书风格HTML
CONTENT_TEMPLATES = {
    "article": """
你是一位专业的小红书母婴领域内容创作者，擅长生成符合小红书平台风格的高质量HTML格式文章。请根据以下要求生成一篇小红书风格的HTML文章：

主题：{title}
关键词：{keywords}
分类：{category}

小红书风格要求：
1. **标题**：使用吸引人的标题，可适当使用emoji，长度适中（15-25字）
2. **开头**：使用亲切的第一人称，直接与读者建立联系，引发共鸣
3. **结构**：采用分段式写作，每段简短（1-3句话）
4. **要点**：重要信息使用<li>标签标记，提高可读性
5. **语言**：口语化、亲切、温暖，使用母婴领域常用术语
6. **表情符号**：适当使用emoji增强情感表达，但不超过内容的10%
7. **结尾**：总结要点，给出鼓励或行动建议
8. **格式**：直接生成HTML格式，包含适当的HTML标签（如<p>、<ul>、<li>等）
9. **长度**：控制在800-1200字之间
10. **原创性**：避免复制粘贴，保证内容的原创性和实用性

请严格按照以下格式输出，不要添加任何额外内容：
标题：[小红书风格的文章标题]
摘要：[简短的内容摘要，100字左右，不使用emoji]
正文：[符合小红书风格的完整HTML格式文章内容，包含适当emoji和HTML标签]
""",
    "agent": """
你是一位专业的小红书母婴领域专家，擅长生成符合小红书平台风格的智能体内容。请根据以下主题生成一个小红书风格的HTML格式智能体：

主题：{title}
关键词：{keywords}
分类：{category}

小红书风格要求：
1. **标题**：使用吸引人的标题，可适当使用emoji，突出智能体的价值和实用性
2. **开头**：使用亲切的语气介绍智能体的用途、价值和适用人群
3. **结构**：采用清晰的多层结构，包含以下部分：
   - 智能体概述：详细介绍智能体的核心价值、解决问题和使用方法
   - 核心功能集合：**必须详细列出6个**核心功能或资源，每个功能包含：
     * 功能名称和用途（1-2句话）
     * 具体内容描述（详细说明智能体包含什么，如何使用）
     * 使用方法和步骤（分步骤说明如何使用这个功能）
     * 下载链接和格式说明（如Excel、PDF、文档等）
   - 详细使用指南：每个功能的具体使用场景和操作步骤（每个功能至少3-4步）
   - 实际应用案例：**必须提供3个**真实场景的应用示例，每个案例包含：
     * 案例背景（宝宝的情况）
     * 使用的功能和方法
     * 完整的操作流程（至少5-6步）
     * 最终效果和改进
   - 常见问题解答：**必须提供6个**用户可能遇到的问题和详细解决方案（每个解答至少2-3句话）
4. **要点**：每个功能、方法或步骤使用<li>标签标记，方便阅读和操作
5. **语言**：口语化、实用、具体，避免过于专业的术语，确保普通用户能轻松理解
6. **表情符号**：适当使用emoji增强亲和力，但不超过内容的10%
7. **格式**：直接生成HTML格式，包含适当的HTML标签（如<h2>、<h3>、<p>、<ul>、<li>、<table>等）
8. **长度**：**必须严格控制在2500-3500字之间**，确保内容丰富全面
9. **实用性**：确保内容具有高度实操性，能够帮助读者解决实际问题
10. **价值体现**：突出智能体的独特价值和使用后的效果，包含具体的量化收益（如节省时间、提高效率等）

请严格按照以下格式输出，不要添加任何额外内容：
标题：[小红书风格的智能体名称]
摘要：[简短的智能体介绍，100字左右，不使用emoji]
内容：[符合小红书风格的完整HTML格式智能体内容，包含适当emoji和HTML标签]
""",
    "agent_conversation": """
你是一位专业的母婴智能体助手，擅长根据用户需求生成个性化的母婴智能体。请基于用户的当前请求、对话历史和智能体主题，生成专业、友好的回应。

用户当前请求：{current_request}
对话历史：{conversation_history}
智能体主题：{agent_topic}

要求：
1. 保持对话的连贯性和友好性
2. 理解用户的真实需求
3. 如果用户需要具体的智能体内容，请生成一个完整的HTML格式智能体
4. 智能体应包含：标题、概述、核心功能、使用指南、案例等部分
5. 如果不需要生成智能体，直接用自然语言回应用户

请严格按照以下格式输出：
如果生成智能体：
[AGENT]
标题：[个性化智能体标题]
内容：[完整的HTML格式智能体内容]
[/AGENT]

否则：
[RESPONSE]
[你的自然语言回应]
[/RESPONSE]
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
        self.model = "deepseek-v3.1-250821"  # 设置模型名称
        self.system_prompt = "你是一位专业的内容创作者，擅长生成高质量、有价值的文章和工具包。"  # 设置系统提示词
        self.CONTENT_TEMPLATES = CONTENT_TEMPLATES  # 将全局模板字典作为实例属性
        
        if not self.api_key:
            logger.warning("未配置百度智能云千帆API密钥，内容生成功能将不可用")
    
    def generate_content(self, template_type: str, **kwargs) -> Optional[Dict[str, str]]:
        """
        生成内容
        
        Args:
            template_type: 模板类型
            **kwargs: 模板参数
            
        Returns:
            Dict[str, str]: 生成的内容
            None: 生成失败时返回
        """
        try:
            # 获取模板内容
            template = self.CONTENT_TEMPLATES.get(template_type, "")
            if not template:
                logger.error(f"模板类型不存在: {template_type}")
                return None
            
            # 填充模板参数
            prompt = template.format(**kwargs)
            
            # 构建请求
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 5000,
                "temperature": 0.7
            }
            
            # 调用API
            logger.debug(f"调用百度智能云千帆API，模板类型: {template_type}")
            response = requests.post(
                self.base_url, 
                headers=headers, 
                json=payload,
                timeout=120  # 增加超时时间到120秒
            )
            
            # 检查响应状态
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            choices = result.get("choices", [])
            if not choices or not isinstance(choices, list):
                logger.error(f"API返回结果不符合预期: {result}")
                return None
            generated_content = choices[0].get("message", {}).get("content", "")
            
            # 解析生成的内容
            parsed_content = self._parse_generated_content(generated_content)
            
            logger.debug(f"内容生成成功: {parsed_content.get('title', '无标题')}")
            return parsed_content
            
        except requests.Timeout as e:
            logger.error(f"百度智能云千帆API请求超时: {str(e)}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"百度智能云千帆API请求失败: {str(e)}")
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
    
    def generate_agent(self, topic: str, category: str, keywords: str = "") -> Optional[Dict[str, str]]:
        """
        生成智能体内容
        
        Args:
            topic: 智能体主题
            category: 智能体分类
            keywords: 关键词（可选）
        
        Returns:
            Dict[str, str]: 生成的智能体内容
            None: 生成失败时返回
        """
        if not keywords:
            keywords = topic
        
        return self.generate_content(
            template_type="agent",
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
        
        # 移除代码块标记（如果有）
        if parsed["content"].startswith("```html"):
            parsed["content"] = parsed["content"][7:]
        if parsed["content"].endswith("```"):
            parsed["content"] = parsed["content"][:-3]
        parsed["content"] = parsed["content"].strip()
        
        return parsed

import datetime
from typing import Dict, Any, Optional

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
        # 默认分类列表
        self.article_categories = ["婴儿护理", "幼儿教育", "孕期营养", "产后恢复", "育儿经验"]
        self.agent_categories = ["宝宝食谱", "育儿计划", "母婴工具"]
        
    def publish_article(self, author_id: int = 1) -> Optional[Dict[str, Any]]:
        """
        自动生成并发布一篇文章
        
        Args:
            author_id: 作者ID，默认1
            
        Returns:
            Dict[str, Any]: 发布的文章信息
            None: 生成或发布失败时返回
        """
        import random
        
        # 随机选择一个分类
        category = random.choice(self.article_categories)
        
        # 生成随机标题（示例）
        article_titles = [
            "宝宝辅食添加指南",
            "婴儿睡眠习惯培养",
            "产后妈妈的恢复技巧",
            "幼儿早期教育方法",
            "母乳喂养常见问题解答",
            "宝宝感冒护理小常识",
            "孕期饮食营养搭配",
            "新生儿护理注意事项",
            "宝宝湿疹护理方法",
            "亲子互动游戏推荐"
        ]
        
        title = random.choice(article_titles)
        keywords = f"{category}, {title}"
        
        return self.generate_and_publish(category, title, keywords, "article", author_id)
    
    def publish_agent(self, author_id: int = 1) -> Optional[Dict[str, Any]]:
        """
        自动生成并发布一个智能体
        
        Args:
            author_id: 作者ID，默认1
            
        Returns:
            Dict[str, Any]: 发布的智能体信息
            None: 生成或发布失败时返回
        """
        import random
        
        # 随机选择一个分类
        category = random.choice(self.agent_categories)
        
        # 生成随机标题（示例）
        agent_titles = [
            "宝宝辅食食谱大全",
            "育儿时间管理工具",
            "孕期检查时间表",
            "婴儿发育里程碑追踪",
            "产后恢复运动计划",
            "宝宝疫苗接种指南",
            "幼儿阅读书单推荐",
            "母婴用品清单",
            "宝宝成长记录模板",
            "育儿费用预算表"
        ]
        
        title = random.choice(agent_titles)
        keywords = f"{category}, {title}"
        
        return self.generate_and_publish(category, title, keywords, "agent", author_id)
    
    def generate_and_publish(self, category: str, title: str, keywords: str, 
                            template_type: str = "article", author_id: int = 1) -> Optional[Dict[str, Any]]:
        """
        自动生成并发布内容
        
        Args:
            category: 内容分类
            title: 内容标题
            keywords: 关键词
            template_type: 模板类型 (article/agent)
            author_id: 作者ID，默认1
            
        Returns:
            Dict[str, Any]: 发布的内容信息
            None: 生成或发布失败时返回
        """
        try:
            # 确保使用正确的datetime类
            from datetime import datetime
            
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

class Agent:
    """
    智能体类，用于处理智能体的对话和内容生成
    """
    
    def __init__(self):
        """
        初始化智能体
        """
        self.generator = DeepSeekGenerator()
        
    def converse(self, agent_topic: str, current_request: str, conversation_history: list) -> dict:
        """
        与智能体进行对话
        
        Args:
            agent_topic: 智能体主题
            current_request: 当前用户请求
            conversation_history: 对话历史列表，包含用户和智能体的消息
            
        Returns:
            dict: 包含智能体响应的字典
        """
        try:
            # 构建对话历史字符串
            history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
            
            # 调用内容生成服务
            response = self.generator.generate_content(
                template_type="agent_conversation",
                current_request=current_request,
                conversation_history=history_str,
                agent_topic=agent_topic
            )
            
            if not response:
                return {
                    "content": "抱歉，我暂时无法处理您的请求，请稍后重试。",
                    "success": False
                }
            
            generated_content = response.get("content", "")
            
            # 解析响应格式
            if "[AGENT]" in generated_content and "[/AGENT]" in generated_content:
                # 提取智能体内容
                agent_part = generated_content.split("[AGENT]")[1].split("[/AGENT]")[0]
                
                # 提取标题
                title_start = agent_part.find("标题：")
                title_end = agent_part.find("\n", title_start)
                title = agent_part[title_start + 3:title_end].strip() if title_start != -1 else agent_topic
                
                # 提取内容
                content_start = agent_part.find("内容：")
                content = agent_part[content_start + 3:].strip() if content_start != -1 else agent_part
                
                return {
                    "content": "已为您生成个性化智能体！",
                    "generated_agent": content,
                    "agent_title": title,
                    "success": True,
                    "is_agent": True
                }
            elif "[RESPONSE]" in generated_content and "[/RESPONSE]" in generated_content:
                # 提取普通响应
                response_part = generated_content.split("[RESPONSE]")[1].split("[/RESPONSE]")[0]
                return {
                    "content": response_part.strip(),
                    "success": True,
                    "is_agent": False
                }
            else:
                # 处理格式不规范的响应
                return {
                    "content": generated_content.strip(),
                    "success": True,
                    "is_agent": False
                }
                
        except Exception as e:
            logger.error(f"智能体对话失败: {str(e)}")
            return {
                "content": "抱歉，处理您的请求时发生错误，请稍后重试。",
                "success": False
            }

# 智能体服务实例
agent_service = Agent()