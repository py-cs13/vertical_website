<template>
  <div class="home-view">
    <!-- 内容分类标签 -->
    <div class="category-tabs-wrapper">
      <div class="category-tabs-simple">
        <!-- 全部按钮 -->
        <button 
          class="tab-btn-simple all-btn"
          :class="{ active: activeCategory === 0 }"
          @click="toggleAllCategories"
        >
          <span class="tab-icon">📚</span>
          全部
        </button>
        <!-- 其他分类标签容器 -->
        <div class="category-tabs-container">
          <!-- 默认显示的前4个分类标签 -->
          <button 
            v-for="category in categories.filter(c => c.id !== 0 && c.id <= 4)" 
            :key="category.id" 
            class="tab-btn-simple" 
            :class="{ active: activeCategory === category.id }"
            @click="filterContent(category.id)"
          >
            <span class="tab-icon">{{ category.icon }}</span>
            {{ category.name }}
          </button>
          <!-- 剩余分类标签（只有在展开状态下显示） -->
          <button 
            v-for="category in categories.filter(c => c.id > 4)" 
            :key="category.id" 
            class="tab-btn-simple" 
            :class="{ active: activeCategory === category.id }"
            @click="filterContent(category.id)"
            v-if="isExpanded"
          >
            <span class="tab-icon">{{ category.icon }}</span>
            {{ category.name }}
          </button>
        </div>
    
    <!-- 搜索结果提示 -->
    <div v-if="isSearchMode" class="search-result-header">
      <div class="search-result-info">
        <span class="search-icon">🔍</span>
        <span class="search-text">搜索关键词：</span>
        <span class="search-keyword">"{{ searchKeyword }}"</span>
        <span class="search-count">，找到 {{ filteredArticles.length }} 篇相关文章</span>
      </div>
      <button class="clear-search-btn" @click="clearSearch">
        <span>✕</span> 清除搜索
      </button>
    </div>
      </div>
    </div>
    
    <!-- 加载状态：骨架屏 -->
    <div v-if="loading && !hasCachedContent" class="skeleton-container">
      <!-- 文章骨架屏 -->
      <div class="content-section">
        <div class="section-header skeleton">
          <div class="section-title skeleton-text"></div>
          <div class="view-all-link skeleton-text"></div>
        </div>
        <div class="content-list">
          <div v-for="i in 4" :key="'skeleton-article-' + i" class="content-card skeleton-card">
            <div class="card-header skeleton">
              <div class="card-category skeleton-text"></div>
              <div class="card-type skeleton-text"></div>
            </div>
            <div class="card-title skeleton-text"></div>
            <div class="card-summary skeleton-text"></div>
            <div class="card-meta skeleton">
              <div class="meta-item skeleton-text"></div>
              <div class="meta-item skeleton-text"></div>
              <div class="meta-item skeleton-text"></div>
            </div>
            <div class="card-actions skeleton">
              <div class="read-more-btn skeleton-text"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 文章区域 -->
    <div class="content-section">
      <h2 class="section-title">
        <span class="section-icon">{{ isSearchMode ? '🔍' : '📚' }}</span>
        {{ isSearchMode ? '搜索结果' : '文章列表' }}
      </h2>
      
      <div class="content-list">
        <!-- 生成文章卡片 -->
        <div 
          v-for="article in displayedArticles" 
          :key="'article-' + article.id" 
          class="content-card"
        >
          <div class="card-header">
            <div class="card-category">
              <span class="category-icon">{{ getCategoryIcon(article.category) }}</span>
              {{ article.category }}
            </div>
            <div class="card-type">📚 文章</div>
          </div>
          
          <h3 class="card-title">
            <router-link :to="`/article/${article.id}`">
              {{ article.title || '标题加载中...' }}
            </router-link>
          </h3>
          
          <p class="card-summary">{{ article.summary || '内容摘要加载中...' }}</p>
          
          <div class="card-meta">
            <span class="meta-item">
              <i class="icon">📅</i> {{ formatDate(article.created_at || '2024-06-03') }}
            </span>
            <span class="meta-item">
              <i class="icon">👁️‍🗨️</i> {{ article.view_count || 0 }}
            </span>
            <span class="meta-item">
              <i class="icon">❤️</i> {{ article.likes || 0 }}
            </span>
          </div>
          
          <div class="card-actions">
            <router-link 
              :to="`/article/${article.id}`" 
              class="read-more-btn"
            >
              阅读全文 →
            </router-link>
          </div>
        </div>
      </div>
      
      <!-- 加载更多按钮 -->
      <div class="load-more-container">
        <button 
          class="load-more-btn" 
          @click="loadMoreArticles"
          :disabled="loading || !hasMoreArticles"
        >
          <span v-if="loading" class="loading-spinner"></span>
          {{ loading ? '加载中...' : hasMoreArticles ? '加载更多' : '没有更多了' }}
        </button>
      </div>
    </div>
    
    <!-- 空状态显示 -->
    <div v-if="!loading && filteredArticles.length === 0" class="empty-state">
      <div class="empty-icon">📚</div>
      <h3>暂无内容</h3>
      <p>该分类下暂时没有相关内容，换个分类试试吧！</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useContentStore } from '../stores'
import { formatDate } from '../utils/formatters'

const contentStore = useContentStore()
const router = useRouter()
const route = useRoute()

// 分类标签相关状态
const categories = ref([])
const activeCategory = ref(0)
const loading = ref(false)
const currentArticleDisplayCount = ref(6)
const isExpanded = ref(false)

// 搜索相关状态
const searchKeyword = ref('')

// 动态生成分类列表
const updateCategories = () => {
  const articleCategories = contentStore.articles.map(a => a.category)
  const uniqueCategories = [...new Set(articleCategories)]
  
  // 创建分类列表
  const newCategories = [
    { id: 0, name: '全部', icon: '📚' }
  ]
  
  uniqueCategories.forEach((cat, index) => {
    newCategories.push({
      id: index + 1,
      name: cat,
      icon: getCategoryIcon(cat)
    })
  })
  
  categories.value = newCategories
}

// 根据分类名称获取图标
const getCategoryIcon = (categoryName) => {
  const iconMap = {
    '孕期指南': '🤰',
    '新生照顾': '👶',
    '幼儿发展': '🌱',
    '亲子互动': '👨‍👩‍👧',
    '早期教育': '🎓',
    '营养健康': '🍎',
    '产后恢复': '🏥',
    '育儿用品': '🛍️'
  }
  return iconMap[categoryName] || '📚'
}

// 组件挂载时加载内容
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
    
    // 检查搜索参数
    const urlSearch = route.query.search
    if (urlSearch) {
      searchKeyword.value = urlSearch
    }
  } catch (error) {
    console.error('加载内容失败:', error)
  } finally {
    loading.value = false
  }
})

// 筛选后的文章
const filteredArticles = computed(() => {
  let articles = contentStore.articles
  
  // 分类筛选
  if (activeCategory.value !== 0) {
    const category = categories.value.find(cat => cat.id === activeCategory.value)
    if (category) {
      articles = articles.filter(article => article.category === category.name)
    }
  }
  
  // 搜索筛选
  if (searchKeyword.value.trim()) {
    const keyword = searchKeyword.value.trim().toLowerCase()
    articles = articles.filter(article => 
      (article.title && article.title.toLowerCase().includes(keyword)) ||
      (article.summary && article.summary.toLowerCase().includes(keyword)) ||
      (article.category && article.category.toLowerCase().includes(keyword))
    )
  }
  
  return articles
})

// 显示的文章
const displayedArticles = computed(() => {
  return filteredArticles.value.slice(0, currentArticleDisplayCount.value)
})

// 是否有更多文章
const hasMoreArticles = computed(() => {
  return displayedArticles.value.length < filteredArticles.value.length
})

// 是否有缓存内容
const hasCachedContent = computed(() => {
  return contentStore.articles.length > 0
})

// 是否为搜索模式
const isSearchMode = computed(() => {
  return searchKeyword.value.trim() !== ''
})

// 获取当前分类名称
const getCurrentCategoryName = () => {
  const category = categories.value.find(c => c.id === activeCategory.value)
  return category ? category.name : ''
}

// 清除搜索
const clearSearch = () => {
  searchKeyword.value = ''
  // 清除URL参数
  router.push({ path: '/articles', query: {} })
}

// 分类筛选
const filterContent = (categoryId) => {
  activeCategory.value = categoryId
  // 切换分类时重置显示数量
  currentArticleDisplayCount.value = 6
  
  // 更新URL查询参数
  if (categoryId === 0) {
    router.push({ path: '/articles', query: {} })
  } else {
    const category = categories.value.find(c => c.id === categoryId)
    if (category) {
      router.push({ path: '/articles', query: { category: category.name } })
    }
  }
}

// 切换展开/收起所有分类
const toggleAllCategories = () => {
  isExpanded.value = !isExpanded.value
  activeCategory.value = 0 // 切换到全部分类
  // 更新URL查询参数
  router.push({ path: '/articles', query: {} })
  // 重置显示数量
  currentArticleDisplayCount.value = 6
}

// 监听路由参数变化，更新分类筛选
watch(() => route.query.category, (newCategory) => {
  if (newCategory) {
    // 找到对应的分类ID
    const category = categories.value.find(c => c.name === newCategory)
    if (category) {
      activeCategory.value = category.id
    } else {
      activeCategory.value = 0
    }
  } else {
    activeCategory.value = 0
  }
  // 切换分类时重置显示数量
  currentArticleDisplayCount.value = 6
}, { immediate: true })

// 监听搜索参数变化
watch(() => route.query.search, (newSearch) => {
  if (newSearch) {
    searchKeyword.value = newSearch
    // 重置显示数量
    currentArticleDisplayCount.value = 6
  } else {
    searchKeyword.value = ''
  }
}, { immediate: true })

// 加载更多文章
const loadMoreArticles = () => {
  // 只有当有更多文章时才增加显示数量
  if (hasMoreArticles.value) {
    currentArticleDisplayCount.value += 4
  }
}
</script>

<style scoped>
/* 全局样式 */
.home-view {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  box-sizing: border-box;
}

a {
  text-decoration: none;
  color: inherit;
}

/* 分类标签样式 */
.category-tabs-wrapper {
  margin-bottom: 20px;
  padding: 10px 0;
  position: relative;
  z-index: 50;
}

/* 搜索结果提示样式 */
.search-result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(135deg, #FFF5F5 0%, #FFF0F0 100%);
  border-radius: 12px;
  border: 2px solid #FFB4B4;
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(255, 107, 139, 0.15);
}

.search-result-info {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.search-icon {
  font-size: 20px;
}

.search-text {
  color: #666;
  font-size: 14px;
}

.search-keyword {
  color: #FF6B8B;
  font-weight: 600;
  font-size: 16px;
  background: rgba(255, 107, 139, 0.1);
  padding: 4px 12px;
  border-radius: 20px;
}

.search-count {
  color: #999;
  font-size: 14px;
}

.clear-search-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: white;
  border: 2px solid #ddd;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  color: #666;
  transition: all 0.3s ease;
}

.clear-search-btn:hover {
  background: #FF6B8B;
  border-color: #FF6B8B;
  color: white;
}

.clear-search-btn span {
  font-size: 12px;
}

.category-tabs-simple {
  display: flex;
  gap: 10px;
  padding: 10px 0;
  position: relative;
  z-index: 101;
  width: 100%;
  contain: content;
  max-width: 100%;
  align-items: flex-start;
}

.tab-btn-simple {
  flex-shrink: 0;
  padding: 12px 24px;
  border: 3px solid #e0e0e0;
  background-color: white;
  border-radius: 25px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  color: #666;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  min-width: fit-content;
  white-space: nowrap;
  position: relative;
  margin: 0;
  outline: none;
  box-sizing: border-box;
}

.tab-btn-simple:hover {
  border-color: #FF6B8B;
  color: #FF6B8B;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: rgba(255, 255, 255, 0.95);
}

.tab-btn-simple.active {
  background-color: #FF6B8B;
  color: white;
  border-color: #FF6B8B;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* "全部"按钮样式 */
.all-btn {
  z-index: 102;
}

/* 其他分类标签容器 */
.category-tabs-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

/* 内容区域 */
.content-section {
  margin-bottom: 40px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

.section-icon {
  font-size: 28px;
}

.content-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

/* 内容卡片 */
.content-card {
  background-color: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 3px solid #f98b88;
  display: flex;
  flex-direction: column;
  gap: 16px;
  position: relative;
  overflow: hidden;
}

.content-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6px;
  background: linear-gradient(90deg, #f98b88, #ffcccb, #f98b88);
  opacity: 1;
}

.content-card:hover {
  transform: translateY(-12px);
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.2);
  border-color: #f77572;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.card-category {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: #666;
  font-weight: 500;
}

.category-icon {
  font-size: 14px;
}

.card-type {
  font-size: 12px;
  color: #666;
  font-weight: 500;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  color: #333;
}

.card-title a:hover {
  color: #FF6B8B;
}

.card-summary {
  font-size: 14px;
  line-height: 1.8;
  color: #666;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.card-meta {
  display: flex;
  gap: 15px;
  font-size: 12px;
  color: #666;
  margin-top: auto;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.card-actions {
  display: flex;
  justify-content: flex-end;
}

.read-more-btn {
  padding: 8px 16px;
  background-color: #FF6B8B;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  text-decoration: none;
}

.read-more-btn:hover {
  background-color: #FF4785;
}

/* 加载更多按钮 */
.load-more-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.load-more-btn {
  padding: 12px 32px;
  background-color: white;
  border: 2px solid #FF6B8B;
  color: #FF6B8B;
  border-radius: 25px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 10px;
}

.load-more-btn:hover:not(:disabled) {
  background-color: #FF6B8B;
  color: white;
  transform: translateY(-2px);
}

.load-more-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 骨架屏 */
.skeleton-container {
  margin-bottom: 40px;
}

.skeleton-card {
  opacity: 0.6;
}

.skeleton-text {
  background-color: #e0e0e0;
  border-radius: 4px;
  animation: skeleton-loading 1.5s infinite;
}

.skeleton .card-header {
  display: flex;
  justify-content: space-between;
}

.skeleton .card-category .skeleton-text {
  width: 80px;
  height: 16px;
}

.skeleton .card-type .skeleton-text {
  width: 60px;
  height: 16px;
}

.skeleton .card-title .skeleton-text {
  width: 100%;
  height: 24px;
  margin-bottom: 10px;
}

.skeleton .card-summary .skeleton-text {
  width: 100%;
  height: 60px;
  margin-bottom: 10px;
}

.skeleton .card-meta {
  display: flex;
  gap: 15px;
}

.skeleton .card-meta .skeleton-text {
  width: 70px;
  height: 16px;
}

.skeleton .card-actions .skeleton-text {
  width: 100px;
  height: 32px;
}

@keyframes skeleton-loading {
  0% { opacity: 0.4; }
  50% { opacity: 0.7; }
  100% { opacity: 0.4; }
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  margin-bottom: 30px;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.2;
}

.empty-state h3 {
  font-size: 20px;
  color: #333;
  margin-bottom: 8px;
  font-weight: 600;
}

.empty-state p {
  font-size: 14px;
  color: #666;
  max-width: 400px;
  margin: 0 auto 20px;
}

/* 加载动画 */
.loading-spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 107, 139, 0.3);
  border-top: 3px solid #FF6B8B;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .content-list {
    grid-template-columns: 1fr;
  }
  
  .category-tabs-simple {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .tab-btn-simple {
    width: 100%;
    justify-content: center;
  }
  
  .category-tabs-container {
    width: 100%;
  }
}
</style>
