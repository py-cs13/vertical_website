# 自动化内容生成系统使用说明

## 功能概述

本系统实现了基于DeepSeek API的自动化内容生成和发布功能，能够为垂直领域网站自动生成高质量的文章和工具包内容。

## 技术架构

- **后端框架**: FastAPI
- **AI引擎**: DeepSeek3 API
- **数据存储**: PostgreSQL
- **缓存**: Redis

## 快速开始

### 1. 配置百度智能云千帆API密钥

在`.env`文件中添加您的百度智能云千帆API密钥：

```env
# DeepSeek API配置（通过百度智能云千帆平台）
DEEPSEEK_API_KEY=your-baidu-qianfan-api-key-here
DEEPSEEK_API_BASE_URL=https://qianfan.baidubce.com/v2/chat/completions
```

**获取API密钥步骤**：
1. 登录百度智能云控制台
2. 进入千帆AI应用开发者中心
3. 创建或选择已有的应用
4. 在应用详情页获取API密钥
5. 确保已开通DeepSeek模型的使用权限

### 2. 安装依赖

```bash
cd /Users/shucui/Desktop/vertical_website/backend
pip install -r requirements.txt
```

### 3. 启动服务

```bash
uvicorn main:app --reload
```

### 4. 测试功能

运行测试脚本验证功能：

```bash
python test_content_generator.py
```

## API接口

### 1. 生成内容草稿

**POST** `/api/content/generate`

**请求参数**:
```json
{
  "topic": "婴儿辅食添加的最佳时间",
  "category": "母婴育儿",
  "content_type": "article"  # article 或 toolkit
}
```

**响应**:
```json
{
  "id": "content-uuid",
  "title": "婴儿辅食添加的最佳时间和注意事项",
  "category": "母婴育儿",
  "summary": "本文介绍了婴儿辅食添加的最佳时间...",
  "content": "详细内容...",
  "status": "draft",
  "created_at": "2023-12-01T10:00:00Z"
}
```

### 2. 自动生成并发布内容

**POST** `/api/content/auto-publish`

**请求参数**:
```json
{
  "topic": "产后恢复的5个关键要点",
  "category": "母婴育儿",
  "content_type": "article"
}
```

**响应**:
```json
{
  "id": "content-uuid",
  "title": "产后恢复的5个关键要点",
  "category": "母婴育儿",
  "status": "published",
  "published_at": "2023-12-01T10:00:00Z",
  "message": "内容已成功生成并发布"
}
```

## 使用示例

### 生成文章

```python
from content_generator import DeepSeekGenerator

generator = DeepSeekGenerator()
article = generator.generate_article(
    topic="婴儿辅食添加的最佳时间",
    category="母婴育儿"
)
print(f"生成的文章标题: {article['title']}")
print(f"文章内容: {article['content']}")
```

### 自动发布内容

```python
from content_generator import AutoContentPublisher

publisher = AutoContentPublisher()
result = publisher.generate_and_publish(
    topic="健康饮食：如何合理搭配一日三餐",
    category="健康养生",
    content_type="article"
)
print(f"发布结果: {result}")
```

## 内容模板

系统使用预定义的模板生成内容：

### 文章模板
- 包含标题、摘要、正文（分章节）、结尾
- 适合垂直领域的专业内容

### 工具包模板
- 包含标题、简介、目录、详细内容、使用建议
- 适合实用工具和指南类内容

## 错误处理

系统包含完善的错误处理机制：
- API连接失败重试
- 内容生成超时处理
- 输入参数验证
- 数据库操作异常捕获

## 性能优化

- 使用Redis进行请求限流
- 异步处理内容生成任务
- 批量内容生成支持

## 注意事项

1. 请确保您的DeepSeek API密钥有效且有足够的配额
2. 生成内容的质量取决于输入的主题和类别
3. 建议在生产环境中配置适当的日志和监控
4. 定期更新内容模板以保持内容质量

## 开发计划

- [ ] 支持自定义内容模板
- [ ] 添加内容审核功能
- [ ] 实现定时自动发布任务
- [ ] 支持多语言内容生成
- [ ] 添加内容质量评估指标
