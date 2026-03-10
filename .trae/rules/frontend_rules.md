# 前端开发规范

## 1. 代码风格规范

### 1.1 文件命名
- 组件文件：PascalCase（如：UserCenterView.vue）
- 工具文件：kebab-case（如：formatters.js）
- 样式文件：kebab-case

### 1.2 命名约定
- 变量名：camelCase（如：userName, affiliateLink）
- 函数名：camelCase（如：loadUserData, generateAffiliateLink）
- 组件名：PascalCase（如：<Header />, <Button />）
- 常量：UPPER_SNAKE_CASE（如：API_BASE_URL）

### 1.3 代码格式
- 缩进：2个空格
- 引号：JavaScript中使用单引号，HTML中使用双引号
- 每行长度：建议不超过120个字符
- 代码注释：对复杂逻辑和重要功能添加注释

## 2. 布局规范

### 2.1 整体页面结构
采用`header-content-footer`的经典布局，内容区域使用`content-view-sidebar`的双栏布局

### 2.2 导航栏规范
使用`.header`类作为导航栏容器
导航栏需要设置较高的z-index以确保不被其他元素覆盖

```css
.header {
  z-index: 12000; /* 高于其他页面元素的z-index，确保导航栏始终可见 */
}
```

### 2.3 主容器规范
使用`.container`类作为页面的最外层容器

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

### 2.4 内容区域布局
使用`.content-wrapper`类包裹主内容区和侧边栏

```css
.content-wrapper {
  display: flex;
  gap: 30px;
  align-items: flex-start;
  position: relative;
  width: 100%;
}
```

### 2.5 主内容区规范
使用`.content-view`类作为主内容区域

```css
.content-view {
  flex: 1;
  min-width: 0;
  box-sizing: border-box;
}
```

### 2.6 侧边栏规范
使用`.sidebar`类作为侧边栏容器，固定宽度为280px（大屏幕），在小屏幕上自动调整

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

### 2.7 内容列表布局
使用`.content-list`类作为内容列表容器，采用网格布局，大屏幕下每行显示2-3个内容卡片，确保内容在容器内居中分布

### 2.8 智能体卡片特殊设计
智能体卡片使用`.content-card-agent`类，添加金色边框和渐变背景
卡片顶部显示中文标识"🤖 智能体"，清晰易懂
增加智能体价值标签`.agent-value-badge`，使用金色背景和钻石图标标注"AI辅助"
价值标签添加鼠标悬停提示，说明"包含可下载的AI智能体和专业模板"
卡片悬停时有更明显的上浮和阴影效果，提升用户交互体验

### 2.9 分类标签布局
使用`.category-tabs-wrapper`作为外层容器，`.category-tabs-simple`作为内层标签容器
"全部"按钮直接作为`.category-tabs-simple`的子元素，始终显示在第一位
其他分类标签使用`.category-tabs-container`容器包裹，默认显示前4个
采用嵌套弹性布局，外层`.category-tabs-simple`使用`flex`布局，内层`.category-tabs-container`使用`flex-wrap: wrap`实现自动换行
点击"全部"按钮可展开/收起所有分类标签

#### 标签按钮样式
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

#### 标签容器样式
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

#### 功能逻辑要求
1. 使用`activeCategory`状态管理当前选中的分类，`isExpanded`状态控制标签展开/收起
2. 初始状态显示"全部"按钮和前4个分类标签
3. 点击"全部"按钮时切换`isExpanded`状态，展开显示所有分类标签
4. 再次点击"全部"按钮时收起额外标签，恢复到初始状态
5. 点击其他分类标签时，只切换当前选中的分类，不影响展开/收起状态

### 2.10 响应式设计
- 在大屏幕（≥1200px）下，保持双栏布局，确保内容区域和侧边栏的整体平衡
- 在中等屏幕（992px-1199px）下，调整侧边栏宽度为240px
- 在小屏幕（≤768px）下，转为垂直布局，侧边栏宽度100%

### 2.11 布局一致性原则
- 所有页面必须遵循统一的布局结构
- 确保页面在不同屏幕尺寸下左右边距对称
- 内容区域和侧边栏的间距保持一致（30px）
- 分类标签和内容列表在容器内居中分布

### 2.12 注意事项
- 严格遵循此布局规范，不得随意修改
- 如需调整布局或修改分类标签相关逻辑，必须经过团队讨论并得到用户明确同意
- 修改后必须进行充分测试，确保不影响现有功能
- 任何涉及分类标签的代码变更都必须先获得用户批准

## 3. 前端路由规范

### 3.1 路由配置
所有路由在`frontend/src/router/index.js`中定义

### 3.2 路由命名
使用kebab-case格式（如：`article-detail`、`user-center`）
name属性必须与路由路径保持语义一致

### 3.3 页面路由路径
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

### 3.4 路由守卫
- 使用`meta.requiresAuth`标记需要认证的路由
- 使用`meta.requiresAdmin`标记需要管理员权限的路由
- 未登录用户访问受保护路由时，跳转登录页
- 非管理员访问管理后台时，显示权限不足提示并跳转首页

### 3.5 组件导入
使用动态导入（`import()`）实现路由组件懒加载

## 5. 前端API调用规范

### 5.1 基础URL
开发环境为`http://localhost:8000`

### 5.2 请求头
- 认证请求：`Authorization: Bearer {token}`
- Content-Type: `application/json`

### 5.3 错误处理
- 统一处理API错误
- 401错误时清除本地存储并跳转登录页
- 其他错误显示友好的用户提示

## 6. 商品推荐组件规范

### 6.1 推荐位置规则
- **侧边栏推荐**：所有页面（首页、文章列表页、文章详情页）的侧边栏"热门文章"模块下方显示1-2个商品推荐
- **精选好物页面**：整个页面都是商品展示，保持现状
- **禁止位置**：除精选好物页面外，其他所有页面的正文下方禁止放置商品推荐区块

### 6.2 推荐策略
#### 6.2.1 首页和文章列表页
- **已登录用户有浏览历史**：基于用户最近浏览的文章进行AI分析，推荐相关商品
- **已登录用户无浏览历史**：返回热门商品（按点击次数排序）
- **未登录用户**：返回随机推荐商品

#### 6.2.2 文章详情页
- 基于当前文章内容进行AI分析
- 提取关键词、商品类型、目标人群等信息
- 使用商品匹配器精准匹配相关商品
- AI分析失败时降级为基于分类推荐

### 6.3 组件使用方式
#### 6.3.1 侧边栏推荐（所有页面）
```vue
<ProductRecommendation 
  mode="history"
  :limit="2"
/>
```

#### 6.3.2 文章详情页推荐（侧边栏）
```vue
<ProductRecommendation 
  mode="ai"
  :article-id="article.id"
  :limit="2"
/>
```

### 6.4 Props参数
- `mode`（必需）：推荐模式，可选值：
  - `history`：基于用户浏览历史推荐（首页、文章列表页）
  - `ai`：基于文章内容AI推荐（文章详情页）
  - `category`：基于分类推荐（已废弃）
- `articleId`（可选）：文章ID，用于AI模式
- `category`（可选）：商品分类，已废弃
- `limit`（可选）：推荐数量，默认2
- `layout`（可选）：布局方式，可选值：`list`（列表）、`grid`（网格），默认`list`

### 6.5 组件功能
- 根据mode参数选择不同的推荐策略
- 显示商品图片、名称、描述、价格和购买链接
- 支持加载状态和空状态显示
- 点击商品时记录点击次数

### 6.6 API调用
#### 6.6.1 基于浏览历史推荐
- 使用`apiClient.get('/products/recommend-by-history')`调用后端API
- 传递参数：`{ limit }`
- 响应数据为商品数组

#### 6.6.2 基于文章内容推荐
- 使用`apiClient.get('/products/recommend-by-content')`调用后端API
- 传递参数：`{ article_id, limit }`
- 响应数据为商品数组

### 6.7 注意事项
- 商品图片链接为示例链接，可能无法正常显示
- 组件会自动监听mode和articleId属性变化并重新加载商品
- AI分析失败时会自动降级为基于分类推荐
- 未登录用户会返回随机推荐商品
- 禁止在正文下方添加商品推荐区块（精选好物页面除外）

## 7. 前端性能优化

### 7.1 代码分割
使用动态导入减少初始加载时间

### 7.2 图片优化
使用适当的图片格式和大小

### 7.3 缓存策略
合理使用浏览器缓存

### 7.4 懒加载
对非首屏内容进行懒加载
