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

- **布局规范**：
  - **整体页面结构**：采用`header-content-footer`的经典布局，内容区域使用`content-view-sidebar`的双栏布局
  - **导航栏规范**：
    - 使用`.header`类作为导航栏容器
    - 导航栏需要设置较高的z-index以确保不被其他元素覆盖
    - 样式设置为：
      ```css
      .header {
        z-index: 12000; /* 高于其他页面元素的z-index，确保导航栏始终可见 */
      }
      ```
  - **主容器规范**：
    - 使用`.container`类作为页面的最外层容器
    - 容器样式统一设置为：
      ```css
      .container {
        max-width: calc(1200px + 40px); /* 包含左右各20px的边距 */
        margin: 0 auto;
        padding: 0 20px;
      }
      
      @media (min-width: 1200px) {
        .container {
          max-width: calc(1200px + 40px);
          padding: 0;
        }
      }
      ```
  - **内容区域布局**：
    - 使用`.content-wrapper`类包裹主内容区和侧边栏
    - 样式设置为：
      ```css
      .content-wrapper {
        display: flex;
        gap: 30px;
        align-items: flex-start;
        position: relative;
        width: 100%;
      }
      ```
  - **主内容区规范**：
    - 使用`.content-view`类作为主内容区域
    - 样式设置为：
      ```css
      .content-view {
        flex: 1;
        min-width: 0;
        box-sizing: border-box;
      }
      ```
  - **侧边栏规范**：
    - 使用`.sidebar`类作为侧边栏容器
    - 固定宽度为280px（大屏幕），在小屏幕上自动调整
    - 样式设置为：
      ```css
      .sidebar {
        width: 280px;
        flex-shrink: 0;
        padding: 20px;
        background-color: var(--bg-primary);
        box-shadow: var(--shadow-light);
        border-radius: 12px;
        border: 1px solid var(--border-color);
      }
      ```
  - **内容列表布局**：
    - 使用`.content-list`类作为内容列表容器
    - 采用网格布局，大屏幕下每行显示2-3个内容卡片
    - 确保内容在容器内居中分布
    - **工具包卡片特殊设计**：
      - 工具包卡片使用`.content-card-toolkit`类，添加金色边框和渐变背景
      - 卡片顶部显示中文标识"🎁 工具包"，清晰易懂
      - 增加工具包价值标签`.toolkit-value-badge`，使用金色背景和钻石图标标注"实用工具"
      - 价值标签添加鼠标悬停提示，说明"包含可下载的实用工具和专业模板"
      - 卡片悬停时有更明显的上浮和阴影效果，提升用户交互体验
  - **分类标签布局**：
    - 使用`.category-tabs-wrapper`作为外层容器，`.category-tabs-simple`作为内层标签容器
    - "全部"按钮直接作为`.category-tabs-simple`的子元素，始终显示在第一位
    - 其他分类标签使用`.category-tabs-container`容器包裹，默认显示前4个
    - 采用嵌套弹性布局，外层`.category-tabs-simple`使用`flex`布局，内层`.category-tabs-container`使用`flex-wrap: wrap`实现自动换行
    - 点击"全部"按钮可展开/收起所有分类标签
    - 标签按钮样式设置为：
      ```css
      .tab-btn-simple {
        flex-shrink: 0;
        padding: 12px 24px;
        border: 3px solid var(--border-color);
        background-color: var(--bg-primary);
        border-radius: 25px;
        cursor: pointer;
        font-size: 14px;
        font-weight: 500;
        transition: all 0.3s ease;
        color: var(--text-secondary);
        display: flex;
        align-items: center;
        gap: 8px;
        box-shadow: var(--shadow-light);
        min-width: fit-content;
        white-space: nowrap;
        position: relative;
        margin: 0;
        outline: none;
        box-sizing: border-box;
      }
      
      .tab-btn-simple:hover {
        border-color: var(--primary-color);
        color: var(--primary-color);
        box-shadow: var(--shadow-medium);
        background-color: rgba(255, 255, 255, 0.95);
      }
      
      .tab-btn-simple.active {
        background-color: var(--primary-color);
        color: white;
        border-color: var(--primary-color);
        box-shadow: var(--shadow-medium);
      }
      ```
    - 标签容器样式设置为：
      ```css
      .category-tabs-wrapper {
        width: 100%;
        margin-bottom: 20px;
        padding: 10px 0;
        box-sizing: border-box;
        position: relative;
        z-index: 100; /* 降低z-index，确保不覆盖导航栏 */
      }
      
      .category-tabs-simple {
        display: flex;
        gap: 10px;
        padding: 10px 0;
        position: relative;
        z-index: 101; /* 降低z-index，确保不覆盖导航栏 */
        width: 100%;
        contain: content;
        max-width: 100%;
        align-items: flex-start; /* 防止子元素拉伸，解决全部按钮变大问题 */
      }
      
      /* 其他分类标签容器 */
      .category-tabs-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
      }
      ```
    - 功能逻辑要求：
      1. 使用`activeCategory`状态管理当前选中的分类，`isExpanded`状态控制标签展开/收起
      2. 初始状态显示"全部"按钮和前4个分类标签
      3. 点击"全部"按钮时切换`isExpanded`状态，展开显示所有分类标签
      4. 再次点击"全部"按钮时收起额外标签，恢复到初始状态
      5. 点击其他分类标签时，只切换当前选中的分类，不影响展开/收起状态
  - **响应式设计**：
    - 在大屏幕（≥1200px）下，保持双栏布局，确保内容区域和侧边栏的整体平衡
    - 在中等屏幕（992px-1199px）下，调整侧边栏宽度为240px
    - 在小屏幕（≤768px）下，转为垂直布局，侧边栏宽度100%
  - **布局一致性原则**：
    - 所有页面必须遵循统一的布局结构
    - 确保页面在不同屏幕尺寸下左右边距对称
    - 内容区域和侧边栏的间距保持一致（30px）
    - 分类标签和内容列表在容器内居中分布
  - **注意事项**：
    - 严格遵循此布局规范，不得随意修改
    - 如需调整布局或修改分类标签相关逻辑，必须经过团队讨论并得到用户明确同意
    - 修改后必须进行充分测试，确保不影响现有功能
    - 任何涉及分类标签的代码变更都必须先获得用户批准

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
- **收藏管理**：
  - **前端实现**：
    - 收藏列表使用`loadFavorites`方法通过`/api/users/me/favorites`接口获取数据
    - 收藏数据映射为包含`id`、`content_id`、`content`对象和`created_at`的对象数组
    - `content`对象包含`id`、`title`、`category`等字段，用于前端显示收藏内容信息
    - 收藏列表模板使用`v-for`循环遍历`favorites`数组生成收藏项
    - 收藏标题必须使用`<router-link>`组件实现链接功能
    - 链接路径根据`category`动态生成：
      - `agent`类型跳转到`/agent/${item.content_id}`
      - 其他类型跳转到`/article/${item.content_id}`
    - 收藏项包含：标题、摘要、分类、日期和"取消收藏"按钮
  
  - **链接样式规范**：
    - 收藏标题链接使用`.favorite-title-link`类名
    - 基础样式：链接颜色跟随主题色，字重加粗，无下划线
    - 悬停效果：颜色加深，显示下划线，出现轻微上浮效果
    - 下划线动画：从左向右平滑过渡，增强交互反馈
  
  - **后端实现**：
    - 收藏API路径：`GET /api/users/me/favorites`
    - 支持分页参数：`page`（页码）和`page_size`（每页数量，最大50）
    - 返回数据结构：
      ```json
      {
        "status": "success",
        "data": [
          {
            "id": "收藏记录ID",
            "content_id": "内容ID",
            "content": {
              "id": "内容ID",
              "title": "标题",
              "category": "分类",
              "summary": "摘要",
              ...
            },
            "created_at": "收藏时间"
          }
        ],
        "total": "总数"
      }
      ```
    - 取消收藏API：`DELETE /api/content/{content_id}/collect`

  - **文章管理**：
    - 文章必须包含标题、内容、作者、发布时间
    - 文章支持富文本格式
    - 文章可分类和标签化

  - **前端路由规范**：
    - **路由配置**：所有路由在`frontend/src/router/index.js`中定义
    - **路由命名**：
      - 使用kebab-case格式（如：`article-detail`、`user-center`）
      - name属性必须与路由路径保持语义一致
    - **页面路由路径**：
      - 首页：`/`（name: `home`）
      - 登录页：`/login`（name: `login`）
      - 注册页：`/register`（name: `register`）
      - 文章详情页：`/article/:id`（name: `article-detail`）
      - 智能体详情页：`/agent/:id`（name: `agent-detail`）
      - 用户中心：`/user`（name: `user-center`，需要认证）
      - 支付页面：`/payment`（name: `payment`，需要认证）
      - 关于页面：`/about`（name: `about`）
      - 文章列表页：`/articles`（name: `articles`）
      - 智能体列表页：`/agents`（name: `agents`）
      - 联盟推广页：`/affiliate`（name: `affiliate`，需要认证）
      - 管理后台：`/admin`（name: `admin-dashboard`，需要管理员权限）
    - **路由守卫**：
      - 使用`meta.requiresAuth`标记需要认证的路由
      - 使用`meta.requiresAdmin`标记需要管理员权限的路由
      - 未登录用户访问受保护路由时，跳转登录页
      - 非管理员访问管理后台时，显示权限不足提示并跳转首页
    - **组件导入**：使用动态导入（`import()`）实现路由组件懒加载

- **小红书风格文章格式规范**（重要）：
  所有生成的文章必须严格遵循以下格式要求，确保内容符合母婴群体的阅读习惯和审美偏好：
  
  #### 4.2.1 标题规范
  - **格式要求**：
    - 标题必须使用中文标点符号（，。！？：；""）
    - 标题开头必须带emoji表情符号（如👶、💕、🍼、👩等）
    - 标题长度建议在15-35字之间
    - 标题应使用疑问句、感叹句或陈述句，增强吸引力
    - 标题应体现实用性和价值感，如"必看""攻略""指南""技巧"等
  
  - **示例**：
    - ✅「👶 新生儿黄疸怎么办？新手妈妈必看的应对指南」
    - ✅「💕 宝宝哭闹不止？快速安抚方法大公开」
    - ❌「新生儿黄疸的医学知识和护理方法」（无emoji、过于正式）
  
  #### 4.2.2 内容结构规范
  - **整体结构**：
    - 采用「开头引入 → 问题分析 → 解决方案 → 注意事项 → 总结」的五段式结构
    - 总字数控制在800-1200字之间
    - 内容层次清晰，逻辑连贯
  
  - **段落标题规范**：
    - 使用HTML `<h3>` 标签作为段落标题
    - 标题必须以emoji开头，增强视觉吸引力
    - 每篇文章包含3-6个段落标题
    - 标题之间要有逻辑递进关系
  
  - **段落内容规范**：
    - 使用HTML `<p>` 标签作为段落容器
    - 内容语言口语化、亲和自然，像和朋友聊天
    - 适当使用「姐妹们」「妈妈们」「大家」等称呼
    - 适当使用emoji表情符号增加亲和力
  
  - **列表规范**：
    - 使用HTML `<ul>` 和 `<li>` 标签创建无序列表
    - 每个列表项使用 `<li><strong>标题</strong>：内容</li>` 格式
    - 列表项控制在3-7个之间
    - 列表用于呈现步骤、方法、注意事项等内容
  
  - **示例结构**：
    ```html
    <h3>👶 标题emoji + 简短描述性文字</h3>
    <p>引入段落，用2-3句话引入话题，建立共鸣。</p>
    <p>展开说明，提供背景信息或问题分析。</p>
    <h3>💡 具体解决方法或步骤</h3>
    <p>详细说明方法或步骤，语言要具体可操作。</p>
    <ul>
      <li><strong>第一步</strong>：具体操作内容</li>
      <li><strong>第二步</strong>：具体操作内容</li>
      <li><strong>第三步</strong>：具体操作内容</li>
    </ul>
    <h3>⚠️ 注意事项或常见误区</h3>
    <ul>
      <li><strong>注意事项1</strong>：具体说明</li>
      <li><strong>注意事项2</strong>：具体说明</li>
    </ul>
    <h3>💕 鼓励性总结</h3>
    <p>用温暖鼓励的语言结束文章，增强情感连接。</p>
    ```
  
  #### 4.2.3 表情符号使用规范
  - **常用emoji分类**：
    - 人物类：👶、👩、🤱、👨‍👩‍👧、👵
    - 情绪类：💕、😊、😢、🤔、😉
    - 物品类：🍼、🛏️、👶、🧸
    - 动作类：💪、💆‍♀️、🧠、👀
    - 标记类：✅、❌、💡、⚠️、📊、🔍
  
  - **使用原则**：
    - 每个段落标题必须带1个emoji
    - 每个重点内容前可适当添加emoji
    - 全文emoji数量控制在5-15个之间
    - 避免在同一段落中连续使用多个emoji
  
  #### 4.2.4 语言风格规范
  - **语气**：
    - 亲切、温暖、像朋友聊天
    - 适度使用「呀」「啦」「呢」等语气词
    - 避免过于正式、学术化的表达
  
  - **人称**：
    - 使用第二人称「你」「您」
    - 使用「妈妈们」「姐妹们」等群体称呼
    - 避免使用「用户」「客户」等商业化称呼
  
  - **句式**：
    - 适当使用疑问句引发共鸣
    - 适当使用感叹句增强情感
    - 短句为主，避免长篇大论
  
  - **示例对比**：
    - ❌「新生儿黄疸是一种常见的生理现象，需要家长注意观察」
    - ✅「👶 新手妈妈别慌！黄疸其实没那么可怕」
    - ❌「建议产妇在产后多休息，保持良好的饮食习惯」
    - ✅「💕 产后恢复是一个漫长的过程，不要急于求成」

  #### 4.2.5 内容质量要求
  - **实用性**：
    - 每个建议都要具体可操作
    - 提供的方法要有数据或经验支持
    - 包含常见问题的解决方案
  
  - **真实性**：
    - 经验分享要真实可信
    - 适当加入个人经历或案例
    - 承认局限性，不要夸大效果
  
  - **安全性**：
    - 医疗健康建议要保守、建议就医
    - 产品推荐要客观公正
    - 避免传播未经验证的偏方
  
  - **完整性**：
    - 问题分析要全面
    - 解决方案要完整
    - 注意事项要详尽
  
  #### 4.2.6 内容生成器集成
  - **backend/content_generator.py** 中的 `CONTENT_TEMPLATES` 必须严格遵循上述格式规范
  - 任何文章生成脚本（如 `generate_articles.py`、`manual_articles.py`）都必须使用符合小红书风格的模板
  - 手动添加文章时必须检查格式是否符合规范
  - 使用 `verify_xiaohongshu_format.py` 验证文章格式
  
  #### 4.2.7 格式验证清单
  生成或添加文章后，必须检查以下项目：
  - [ ] 标题以emoji开头
  - [ ] 标题使用中文标点
  - [ ] 内容使用HTML标签（`<h3>`、`<p>`、`<ul>`、`<li>`）
  - [ ] 每个段落标题都有emoji
  - [ ] 语言风格亲切、口语化
  - [ ] 使用第二人称「你/您」
  - [ ] 包含「妈妈们」「姐妹们」等称呼
  - [ ] 字数在800-1200字之间
  - [ ] 有明确的结构层次
  - [ ] 内容实用、可操作

- **工具包管理**：
  - 工具包包含名称、描述、价格、文件路径等信息
  - 购买后的工具包支持下载
  - 工具包文件存储在backend/static目录下

- **页面显示规则**：
  - **首页**：
    - 文章列表固定显示4个卡片
    - 工具包列表固定显示2个卡片
    - 无论分类页面如何操作，首页显示数量始终保持不变
  - **文章分类页面**：
    - 初始显示6个文章卡片
    - 支持"加载更多"功能，每次加载4个文章卡片
    - 显示数量与首页无关，独立管理
  - **工具包分类页面**：
    - 初始显示6个工具包卡片
    - 支持"加载更多"功能，每次加载2个工具包卡片
    - 显示数量与首页无关，独立管理
  - **注意事项**：
    - 此显示规则为核心业务逻辑，未经用户明确同意不得修改
    - 首页与分类页面的显示数量必须严格分离，不得互相影响
    - 修改任何显示逻辑前必须与用户沟通并获得批准

- **路由参数筛选与时序问题**：
  - **问题场景**：当使用URL参数（如`/articles?category=孕期营养`）进行内容筛选时，需要确保数据加载完成后再处理筛选逻辑
  - **时序问题**：Vue的`watch`监听器使用`immediate: true`时会立即执行，但如果依赖的动态数据（如从API获取的分类列表）尚未生成，会导致筛选失败
  - **解决方案**：在`onMounted`钩子中，**确保先加载数据并生成分类列表**，然后再检查URL参数并设置筛选状态
  - **代码模式**：
    ```javascript
    onMounted(async () => {
      loading.value = true
      try {
        await contentStore.fetchLatestArticles()
        // 数据加载完成后动态生成分类列表
        updateCategories()
        
        // 分类列表生成后，检查URL参数并设置筛选状态
        const urlCategory = route.query.category
        if (urlCategory) {
          const category = categories.value.find(c => c.name === urlCategory)
          if (category) {
            activeCategory.value = category.id
          }
        }
      } catch (error) {
        console.error('加载内容失败:', error)
      } finally {
        loading.value = false
      }
    })
    ```
  - **关键点**：
    - 1. 先执行数据加载和分类列表生成
    - 2. 再检查URL参数并设置activeCategory状态
    - 3. 确保`categories`数组已填充后再进行查找匹配
  - **适用场景**：所有需要从URL参数读取并同步页面状态的场景（如分类筛选、搜索关键词等）

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

### 12.6 已完成功能保护规则（软封闭）
- **默认不修改原则**：对于已完成并通过测试的功能模块，默认不进行修改
- **修改前告知**：如需对已完成功能进行修改，必须提前告知用户具体修改的模块、原因、内容及可能的影响范围
- **用户确认机制**：所有对已完成功能的修改必须经过用户明确同意后才能执行
- **修改后测试**：修改完成后必须进行充分测试，确保原有功能正常运行且未引入新的bug
- **例外情况**：当必须进行联动优化以确保系统整体性能或安全性时，应详细说明情况并征得用户同意

### 12.7 修改范围控制规则（核心原则）
- **严格遵循用户指令**：用户要求什么就做什么，不多改也不少改
- **禁止额外添加**：不得未经用户允许添加任何装饰、样式、功能或逻辑
- **保持现有代码**：修改时保持原有代码和逻辑不变，不随意调整
- **明确修改范围**：只修改与用户请求直接相关的代码，不扩展到其他模块
- **禁止主观发挥**：不根据个人判断添加"可能有用"的功能或样式
- **变更前必须确认**：如果需要修改现有功能或添加额外内容，必须先获得用户明确同意
- **验证方法**：修改后使用open_preview工具验证页面效果，确保没有引入意外的视觉或功能变化

**示例**：
- ✅ 用户要求"添加路由"，正确做法：只添加路由配置，不修改任何页面内容
- ✅ 用户要求"修复bug"，正确做法：只修复指定的bug，不改变其他功能
- ❌ 用户要求"添加路由"，错误做法：添加路由后又修改了页面样式和逻辑
- ❌ 用户要求"修复登录"，错误做法：修复登录后又优化了其他不相关功能

---

本规则将指导项目的开发和维护，确保代码质量和项目的可扩展性。所有团队成员应严格遵守这些规则。