# 母婴垂直网站项目规则

## 1. 项目概述
本项目是一个面向母婴群体的垂直网站，提供专业的母婴知识、产品推荐、在线课程和联盟推广系统等功能。

## 2. 技术栈与架构

### 2.1 前端架构
- **框架**：Vue 3 + Composition API
- **构建工具**：Vite
- **状态管理**：Pinia
- **路由管理**：Vue Router
- **HTTP客户端**：Axios
- **UI组件**：自定义组件（Button、FormInput、Header等）
- **工具库**：
  - 日期格式化：自定义formatDate工具
  - 弹窗提示：SweetAlert2

### 2.2 后端架构
- **框架**：FastAPI (Python 3.8+)
- **数据库**：PostgreSQL
- **缓存**：Redis
- **ORM**：SQLAlchemy
- **认证**：JWT (JSON Web Tokens)
- **文件存储**：本地文件系统（头像、工具包等）
- **API风格**：RESTful
- **请求限流**：基于Redis的FastAPILimiter

### 2.3 项目结构
```
vertical_website/
├── backend/              # 后端应用
│   ├── models.py         # 数据库模型
│   ├── schemas.py        # 数据验证和序列化
│   ├── routes.py         # API路由
│   ├── auth.py           # 认证相关
│   ├── main.py           # 应用入口
│   └── static/           # 静态文件存储
└── frontend/             # 前端应用
    ├── src/
    │   ├── components/   # Vue组件
    │   ├── views/        # 页面组件
    │   ├── stores/       # Pinia状态管理
    │   ├── router/       # 路由配置
    │   └── utils/        # 工具函数
    └── index.html        # 入口HTML
```

## 3. 代码风格规范

### 3.1 前端代码风格
- **文件命名**：
  - 组件文件：PascalCase（如：UserCenterView.vue）
  - 工具文件：kebab-case（如：formatters.js）
  - 样式文件：kebab-case

- **命名约定**：
  - 变量名：camelCase（如：userName, affiliateLink）
  - 函数名：camelCase（如：loadUserData, generateAffiliateLink）
  - 组件名：PascalCase（如：<Header />, <Button />）
  - 常量：UPPER_SNAKE_CASE（如：API_BASE_URL）

- **代码格式**：
  - 缩进：2个空格
  - 引号：JavaScript中使用单引号，HTML中使用双引号
  - 每行长度：建议不超过120个字符
  - 代码注释：对复杂逻辑和重要功能添加注释

### 3.2 后端代码风格
- **文件命名**：snake_case（如：auth.py, database.py）
- **命名约定**：
  - 变量名：snake_case（如：user_id, unique_code）
  - 函数名：snake_case（如：get_current_user, generate_affiliate_link）
  - 类名：PascalCase（如：User, AffiliateLink）
  - 常量：UPPER_SNAKE_CASE（如：SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES）

- **代码格式**：
  - 缩进：4个空格（遵循PEP 8）
  - 每行长度：不超过79个字符（遵循PEP 8）
  - 函数注释：使用Google风格的函数文档字符串
  - 类型注解：所有函数参数和返回值必须添加类型注解

## 4. 业务逻辑规则

### 4.1 用户管理
- **注册流程**：
  1. 验证邮箱格式和密码强度
  2. 密码使用bcrypt进行哈希存储
  3. 生成JWT访问令牌
  4. 返回用户信息和令牌

- **认证机制**：
  - 所有需要认证的API请求必须在Authorization头中包含有效的JWT令牌
  - 令牌过期时间：30分钟
  - 令牌无效或过期时返回401错误

### 4.2 内容管理
- **文章管理**：
  - 文章必须包含标题、内容、作者、发布时间
  - 文章支持富文本格式
  - 文章可分类和标签化

- **工具包管理**：
  - 工具包包含名称、描述、价格、文件路径等信息
  - 购买后的工具包支持下载
  - 工具包文件存储在backend/static目录下

### 4.3 支付系统
- **支付流程**：
  1. 创建订单并生成支付链接
  2. 用户完成支付
  3. 回调通知更新订单状态
  4. 发放购买的内容或服务

- **订单状态**：
  - pending: 待支付
  - paid: 已支付
  - cancelled: 已取消
  - refunded: 已退款

### 4.4 联盟推广系统
- **推广链接格式**：`http://localhost:5173?ref={unique_code}`
- **佣金规则**：
  - 佣金比例：订单金额的10%
  - 结算状态：
    - pending: 待结算
    - paid: 已结算
    - cancelled: 已取消
  - 结算周期：每月15日结算上月佣金

- **跟踪机制**：
  - 记录推广链接的点击次数和来源信息
  - 购买转化后自动计算并记录佣金

## 5. API开发规范

### 5.1 前端API调用
- **基础URL**：开发环境为`http://localhost:8000`
- **请求头**：
  - 认证请求：`Authorization: Bearer {token}`
  - Content-Type: `application/json`

- **错误处理**：
  - 统一处理API错误
  - 401错误时清除本地存储并跳转登录页
  - 其他错误显示友好的用户提示

### 5.2 后端API设计
- **路由命名**：使用清晰的资源路径（如：`/api/users/me`, `/api/affiliate/links`）
- **HTTP方法**：
  - GET: 获取资源
  - POST: 创建资源
  - PUT: 更新资源
  - DELETE: 删除资源

- **响应格式**：
  ```json
  {
    "message": "操作描述",
    "data": { /* 响应数据 */ },
    "error": { /* 错误信息（可选） */ }
  }
  ```

- **错误码**：
  - 200: 成功
  - 201: 创建成功
  - 400: 请求参数错误
  - 401: 未授权
  - 403: 禁止访问
  - 404: 资源不存在
  - 500: 服务器内部错误

## 6. 数据库规范

### 6.1 表设计原则
- 每个表必须有主键
- 使用外键建立表关系
- 字段名使用snake_case
- 为重要字段添加索引
- 添加适当的注释说明字段用途

### 6.2 常用表结构
- **用户表**：存储用户基本信息（id, email, password_hash, nickname等）
- **文章表**：存储文章内容（id, title, content, author_id, created_at等）
- **工具包表**：存储工具包信息（id, name, description, price, file_path等）
- **订单表**：存储订单信息（id, user_id, total_amount, status, created_at等）
- **推广链接表**：存储推广链接（id, user_id, unique_code, is_active等）
- **佣金记录表**：存储佣金信息（id, order_id, affiliate_link_id, amount, status等）

## 7. 部署与测试

### 7.1 开发环境
- **前端**：
  ```bash
  cd frontend
  npm install
  npm run dev
  ```

- **后端**：
  ```bash
  cd backend
  pip install -r requirements.txt
  python -m uvicorn main:app --reload
  ```

### 7.2 生产环境
- **容器化**：使用Docker和docker-compose
- **环境变量**：使用.env.production文件配置
- **静态文件**：使用Nginx或CDN托管
- **数据库**：使用PostgreSQL（与开发环境保持一致）

### 7.3 测试规范
- **单元测试**：对核心功能进行单元测试
- **集成测试**：测试模块间的交互
- **端到端测试**：测试完整的用户流程
- **测试覆盖率**：争取达到80%以上

## 8. 文档规范

### 8.1 代码文档
- **前端组件**：为组件添加props、events、slots的文档
- **后端API**：使用FastAPI的自动文档功能
- **工具函数**：说明函数的用途、参数和返回值

### 8.2 项目文档
- **README**：项目概述、安装说明、使用指南
- **API文档**：使用Swagger UI（FastAPI自动生成）
- **开发日志**：记录开发过程中的重要决策和问题
- **部署文档**：生产环境部署步骤和配置说明

## 9. 安全规范

### 9.1 前端安全
- 防止XSS攻击：对用户输入进行过滤和转义
- 防止CSRF攻击：使用合适的防护措施
- 安全存储：敏感信息不存储在localStorage中

### 9.2 后端安全
- 密码安全：使用bcrypt进行哈希存储
- 认证授权：严格的JWT验证机制
- 输入验证：所有用户输入必须经过验证
- SQL注入防护：使用ORM参数化查询
- 敏感信息保护：不在日志中记录敏感信息

## 10. 开发流程

### 10.1 分支管理
- main：主分支，用于生产环境
- develop：开发分支，整合所有功能
- feature/xxx：特性分支，开发新功能
- bugfix/xxx：修复分支，修复bug

### 10.2 代码审查
- 所有代码必须经过代码审查才能合并到main分支
- 审查重点：代码质量、功能实现、安全性、性能

### 10.3 提交规范
- 提交信息清晰明了，使用中英文混合
- 格式：`类型: 描述`（如：`feat: 添加联盟推广系统`）
- 类型包括：feat（新功能）、fix（修复bug）、docs（文档）、style（代码风格）、refactor（重构）、test（测试）、chore（构建/工具）

## 11. 性能优化

### 11.1 前端优化
- 代码分割：使用动态导入减少初始加载时间
- 图片优化：使用适当的图片格式和大小
- 缓存策略：合理使用浏览器缓存
- 懒加载：对非首屏内容进行懒加载

### 11.2 后端优化
- 数据库索引：为查询频繁的字段添加索引
- 缓存机制：使用Redis缓存热点数据和会话信息
- 异步处理：对IO密集型操作使用异步方式
- 分页处理：大量数据时使用分页查询
- 请求限流：使用Redis实现API请求限流保护

## 12. 其他约定

### 12.1 命名规范
- 变量和函数名应具有描述性，避免使用缩写
- 组件名应反映其功能和用途
- 文件名应与组件或模块的功能一致

### 12.2 注释规范
- 对复杂逻辑添加注释说明
- 注释应简洁明了，使用中文
- 定期更新注释，确保与代码一致

### 12.3 代码复用
- 提取可复用的组件和工具函数
- 避免重复代码
- 遵循DRY（Don't Repeat Yourself）原则

### 12.4 技术扩展与灵活性
- **技术栈扩展**：本项目规则并非一成不变，允许根据业务需求和技术发展引入新的工具、框架或服务
- **评估机制**：引入新技术前，应评估其与现有技术栈的兼容性、学习成本和性能影响
- **文档更新**：引入新技术后，应及时更新项目规则和相关文档
- **团队共识**：重要的技术选型变更应经过团队讨论和共识

### 12.5 Redis使用规范
- **主要用途**：
  - 请求限流：保护API免受恶意请求攻击
  - 缓存：存储热点数据、会话信息和临时状态
  - 队列：用于异步任务处理（如内容生成、邮件发送等）
- **配置管理**：Redis连接信息应通过环境变量或配置文件管理
- **容错处理**：Redis服务不可用时，系统应能降级运行，避免整体服务中断

---

本规则将指导项目的开发和维护，确保代码质量和项目的可扩展性。所有团队成员应严格遵守这些规则。