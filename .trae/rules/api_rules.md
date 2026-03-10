# API开发规范

## 1. 后端API设计

### 1.1 路由命名
使用清晰的资源路径（如：`/api/users/me`, `/api/affiliate/links`）

### 1.2 HTTP方法
- GET: 获取资源
- POST: 创建资源
- PUT: 更新资源
- DELETE: 删除资源

### 1.3 响应格式
```json
{
  "message": "操作描述",
  "data": { /* 响应数据 */ },
  "error": { /* 错误信息（可选） */ }
}
```

### 1.4 错误码
- 200: 成功
- 201: 创建成功
- 400: 请求参数错误
- 401: 未授权
- 403: 禁止访问
- 404: 资源不存在
- 500: 服务器内部错误

### 1.5 路由顺序规范（重要）

#### 1.5.1 路由匹配规则
FastAPI按顺序匹配路由，具体路由必须在参数化路由之前定义

#### 1.5.2 正确示例
```python
# 具体路由在前
@router.get("/api/products/recommend", response_model=List[ProductResponse])
def get_recommend_products(...):
    pass

# 参数化路由在后
@router.get("/api/products/{product_id}", response_model=ProductResponse)
def get_product(...):
    pass
```

#### 1.5.3 错误示例
```python
# 参数化路由在前（错误）
@router.get("/api/products/{product_id}", response_model=ProductResponse)
def get_product(...):
    pass

# 具体路由在后（会被错误匹配）
@router.get("/api/products/recommend", response_model=List[ProductResponse])
def get_recommend_products(...):
    pass
```

#### 1.5.4 常见问题
- 如果具体路由在参数化路由之后，FastAPI会尝试将具体路径解析为参数
- 例如：`/api/products/recommend` 会被匹配到 `/api/products/{product_id}`，尝试将"recommend"解析为整数ID而报错

#### 1.5.5 验证方法
- 使用curl命令测试API：`curl -X GET "http://localhost:8000/api/products/recommend?category=育儿用品&limit=2"`
- 检查后端日志确认路由是否正确匹配
- 如果返回参数解析错误，检查路由顺序是否正确

## 2. 前端API调用规范

### 2.1 基础URL
开发环境为`http://localhost:8000`

### 2.2 请求头
- 认证请求：`Authorization: Bearer {token}`
- Content-Type: `application/json`

### 2.3 错误处理
- 统一处理API错误
- 401错误时清除本地存储并跳转登录页
- 其他错误显示友好的用户提示

## 3. 商品推荐API接口

### 3.1 基于浏览历史推荐
#### 3.1.1 接口信息
- 接口路径：`GET /api/products/recommend-by-history`
- 功能描述：根据用户浏览历史推荐商品
- 认证：可选（支持未登录用户）

#### 3.1.2 请求参数
| 参数名 | 类型 | 必需 | 默认值 | 说明 |
|--------|------|------|--------|------|
| limit | int | 否 | 4 | 推荐数量 |

#### 3.1.3 响应数据
```json
[
  {
    "id": 1,
    "name": "商品名称",
    "description": "商品描述",
    "image_url": "图片URL",
    "link_url": "购买链接",
    "price": 99.0,
    "category": "商品分类",
    "click_count": 10
  }
]
```

#### 3.1.4 推荐逻辑
- 已登录用户有浏览历史：基于最近浏览的文章AI分析推荐
- 已登录用户无浏览历史：返回热门商品
- 未登录用户：返回随机推荐

### 3.2 基于文章内容推荐
#### 3.2.1 接口信息
- 接口路径：`GET /api/products/recommend-by-content`
- 功能描述：根据文章内容AI分析推荐商品
- 认证：可选

#### 3.2.2 请求参数
| 参数名 | 类型 | 必需 | 默认值 | 说明 |
|--------|------|------|--------|------|
| article_id | int | 是 | - | 文章ID |
| limit | int | 否 | 2 | 推荐数量 |

#### 3.2.3 响应数据
```json
[
  {
    "id": 1,
    "name": "商品名称",
    "description": "商品描述",
    "image_url": "图片URL",
    "link_url": "购买链接",
    "price": 99.0,
    "category": "商品分类",
    "click_count": 10
  }
]
```

#### 3.2.4 推荐逻辑
- 使用DeepSeek AI模型分析文章内容
- 提取关键词、商品类型、目标人群等信息
- 使用ProductMatcher进行商品匹配
- AI分析失败时降级为基于分类推荐

### 3.3 基于分类推荐（已废弃）
#### 3.3.1 接口信息
- 接口路径：`GET /api/products/recommend`
- 功能描述：根据商品分类推荐商品（已废弃，保留用于兼容）
- 认证：可选

#### 3.3.2 请求参数
| 参数名 | 类型 | 必需 | 默认值 | 说明 |
|--------|------|------|--------|------|
| category | string | 是 | - | 商品分类 |
| limit | int | 否 | 2 | 推荐数量 |

#### 3.3.3 响应数据
```json
[
  {
    "id": 1,
    "name": "商品名称",
    "description": "商品描述",
    "image_url": "图片URL",
    "link_url": "购买链接",
    "price": 99.0,
    "category": "商品分类",
    "click_count": 10
  }
]
```

### 3.4 商品点击记录
#### 3.4.1 接口信息
- 接口路径：`POST /api/products/{product_id}/click`
- 功能描述：记录商品点击次数
- 认证：可选

#### 3.4.2 请求参数
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| product_id | int | 是 | 商品ID（路径参数） |

#### 3.4.3 响应数据
```json
{
  "message": "点击记录成功",
  "click_count": 11
}
```

### 3.5 路由顺序注意事项
商品推荐相关API必须在商品详情API之前定义，避免路由匹配错误：

```python
# 正确顺序
@router.get("/api/products/recommend-by-history", ...)
@router.get("/api/products/recommend-by-content", ...)
@router.get("/api/products/recommend", ...)
@router.get("/api/products/{product_id}", ...)
```
