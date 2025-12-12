<template>
  <div class="home-view">
    <!-- 母婴主题装饰 -->
    <div class="theme-decoration">
      <div class="decoration-icon">👶</div>
      <div class="decoration-icon">🍼</div>
      <div class="decoration-icon">🎀</div>
    </div>
    
    <!-- 页面标题 -->
    <h1 class="page-title">母婴生活内容平台</h1>
    <p class="page-subtitle">专业的母婴知识分享，陪伴宝贝健康成长每一天</p>
    
    <!-- 内容分类标签 -->
    <div class="category-tabs">
      <button 
        v-for="category in categories" 
        :key="category.id" 
        class="tab-btn" 
        :class="{ active: activeCategory === category.id }"
        @click="filterContent(category.id)"
      >
        <span class="tab-icon">{{ getCategoryIcon(category.name) }}</span>
        {{ category.name }}
      </button>
    </div>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner">
        <div class="spinner"></div>
        <p>正在加载内容...</p>
      </div>
    </div>
    
    <!-- 内容列表 -->
    <div v-else-if="filteredContent.length > 0" class="content-list">
      <div 
        v-for="item in filteredContent" 
        :key="item.id" 
        class="content-card"
        :class="{ 'content-card-toolkit': item.type === 'toolkit' }"
      >
        <div class="card-header">
          <div class="card-category">
            <span class="category-icon">{{ getCategoryIcon(item.category) }}</span>
            {{ item.category }}
          </div>
          <div class="card-type">{{ item.type === 'article' ? '📚 文章' : '🎁 工具包' }}</div>
        </div>

        
        <h3 class="card-title">
          <router-link :to="`/${item.type === 'article' ? 'article' : 'toolkit'}/${item.id}`">
            {{ item.title || '标题加载中...' }}
          </router-link>
        </h3>
        
        <p class="card-summary">{{ item.summary || '内容摘要加载中...' }}</p>
        
        <div class="card-meta">
          <span class="meta-item">
            <i class="icon">📅</i> {{ formatDate(item.created_at || '2024-06-03') }}
          </span>
          <span class="meta-item">
            <i class="icon">👁️‍🗨️</i> {{ formatNumber(item.views || 0) }}
          </span>
          <span class="meta-item">
            <i class="icon">❤️</i> {{ formatNumber(item.likes || 0) }}
          </span>
          <span v-if="item.type === 'toolkit'" class="meta-item price">
            <i class="icon">💰</i> ¥{{ item.price || 99.0 }}
          </span>
        </div>
        
        <div class="card-actions">
          <router-link 
            :to="`/${item.type === 'article' ? 'article' : 'toolkit'}/${item.id}`" 
            class="read-more-btn"
          >
            {{ item.type === 'article' ? '阅读全文' : '查看详情' }} →
          </router-link>
          <button v-if="item.type === 'toolkit'" class="buy-btn" @click="buyToolkit(item)">立即购买</button>
        </div>
      </div>
    </div>
    
    <!-- 空状态 -->
    <div v-else class="empty-state">
      <div class="empty-icon">📚</div>
      <h3>暂无内容</h3>
      <p>该分类下暂时没有相关内容，换个分类试试吧！</p>
    </div>
    

    

    
    <!-- 加载更多按钮 -->
    <div class="load-more">
      <button class="load-more-btn" @click="loadMoreContent">加载更多</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onActivated, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useContentStore, useAuthStore } from '../stores'
import { formatDate, formatNumber } from '../utils/formatters'

const contentStore = useContentStore()
const router = useRouter()
const route = useRoute()
const activeCategory = ref(0) // 0表示全部
const activeType = ref(null) // null表示全部，'article'表示文章，'toolkit'表示工具包
const loading = ref(false)

// 模拟分类数据
const categories = ref([
  { id: 0, name: '全部' },
  { id: 1, name: '婴儿护理' },
  { id: 2, name: '育儿知识' },
  { id: 3, name: '营养辅食' },
  { id: 4, name: '产后恢复' },
  { id: 5, name: '亲子互动' },
  { id: 6, name: '成长发育' }
])

// 页面加载时获取内容
onMounted(async () => {
  await loadContent()
})

// 每次进入页面时重新获取内容
onActivated(async () => {
  await loadContent()
})

// 加载内容的函数
const loadContent = async () => {
  loading.value = true
  try {
    await Promise.all([
      contentStore.fetchLatestArticles(),
      contentStore.fetchLatestToolkits()
    ])
    
    // 检查URL参数
    if (route.query.category) {
      if (route.query.category === 'article' || route.query.category === 'toolkit') {
        activeType.value = route.query.category
      }
    }
  } catch (error) {
    console.error('Failed to load content:', error)
  } finally {
    loading.value = false
  }
}

// 监听路由参数变化
watch(() => route.query.category, (newCategory) => {
  if (newCategory === 'article' || newCategory === 'toolkit') {
    activeType.value = newCategory
  } else {
    activeType.value = null
  }
})

// 获取分类对应的图标
const getCategoryIcon = (categoryName) => {
  const iconMap = {
    '全部': '🏠',
    '婴儿护理': '👶',
    '育儿知识': '📚',
    '营养辅食': '🍼',
    '产后恢复': '🤰',
    '亲子互动': '👨‍👩‍👧',
    '成长发育': '🌱'
  }
  return iconMap[categoryName] || '📖'
}

// 合并文章和工具包数据
const allContent = computed(() => {
  const articlesWithType = contentStore.articles.map(article => ({
    ...article,
    type: 'article',
    category: article.category || '母婴育儿'
  }))
  
  const toolkitsWithType = contentStore.toolkits.map(toolkit => ({
    ...toolkit,
    type: 'toolkit',
    category: toolkit.category || '育儿工具'
  }))
  
  return [...articlesWithType, ...toolkitsWithType]
})

// 筛选后的内容
const filteredContent = computed(() => {
  let filtered = allContent.value
  
  // 按类型筛选
  if (activeType.value) {
    filtered = filtered.filter(item => item.type === activeType.value)
  }
  
  // 按分类筛选
  if (activeCategory.value !== 0) {
    // 根据分类ID筛选内容
    const categoryMap = {
      1: ['婴儿护理', '健康养生'],
      2: ['育儿知识', '母婴育儿'],
      3: ['营养辅食', '饮食营养'],
      4: ['产后恢复'],
      5: ['亲子互动'],
      6: ['成长发育']
    }
    
    const categoriesToShow = categoryMap[activeCategory.value] || []
    filtered = filtered.filter(item => categoriesToShow.includes(item.category))
  }
  
  return filtered
})

// 分类筛选
const filterContent = (categoryId) => {
  activeCategory.value = categoryId
}

// 加载更多内容
const loadMoreContent = async () => {
  // 这里可以实现分页加载逻辑
  console.log('Load more content...')
}

// 测试点击事件
const testClick = () => {
  console.log('测试点击事件触发了！')
  alert('测试点击事件触发了！')
}

// 测试路由跳转
const testRouter = () => {
  console.log('测试路由跳转...')
  router.push('/about')
}



// 购买工具包
const buyToolkit = async (item) => {
  try {
    console.log('=== 立即购买按钮点击事件开始 ===')
    console.log('点击的商品：', item)
    
    // 检查商品数据完整性
    if (!item || !item.id || !item.title) {
      console.error('商品数据不完整：', item)
      alert('商品数据不完整，请刷新页面后重试')
      return
    }
    
    // 直接跳转到支付页面，携带商品信息
    router.push({
      path: '/payment',
      query: {
        product_type: item.type,
        product_id: item.id,
        product_name: item.title,
        price: item.price || 99.0
      }
    })
    console.log('路由跳转命令已执行，跳转到支付页面')
  } catch (error) {
    console.error('=== 购买工具包时发生错误 ===')
    console.error('错误类型：', typeof error)
    console.error('错误消息：', error.message)
    console.error('错误堆栈：', error.stack)
    alert('购买失败：' + error.message)
  }
}
</script>

<style scoped>
.home-view {
  max-width: 100%;
  position: relative;
}

/* 母婴主题装饰 */
.theme-decoration {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-bottom: 20px;
  animation: float 3s ease-in-out infinite;
}

.decoration-icon {
  font-size: 32px;
  filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1));
  transform: rotate(-10deg);
}

.decoration-icon:nth-child(2) {
  font-size: 36px;
  transform: rotate(0deg);
  animation-delay: 0.5s;
}

.decoration-icon:nth-child(3) {
  font-size: 30px;
  transform: rotate(10deg);
  animation-delay: 1s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 10px;
  color: var(--primary-color);
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.page-title::before,
.page-title::after {
  content: "🎀";
  font-size: 20px;
  color: var(--accent-color);
}

.page-subtitle {
  font-size: 16px;
  color: var(--text-secondary);
  margin-bottom: 30px;
  text-align: center;
  background-color: var(--bg-primary);
  padding: 12px 20px;
  border-radius: 20px;
  display: inline-block;
  margin-left: auto;
  margin-right: auto;
  box-shadow: var(--shadow-light);
}

/* 分类标签 */
.category-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 30px;
  justify-content: center;
}

.tab-btn {
  padding: 10px 20px;
  border: 2px solid var(--border-color);
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
}

.tab-btn:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow: var(--shadow-medium);
}

.tab-btn.active {
  background-color: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
  box-shadow: var(--shadow-medium);
}

.tab-icon {
  font-size: 16px;
}

/* 内容列表 */
.content-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 25px;
  margin-bottom: 30px;
}

.content-card {
  background-color: var(--bg-primary);
  border-radius: 16px;
  padding: 25px;
  box-shadow: var(--shadow-medium);
  transition: all 0.3s ease;
  border-left: 5px solid var(--primary-color);
  position: relative;
  overflow: hidden;
}

.content-card::before {
  content: "👶";
  position: absolute;
  top: 15px;
  right: 15px;
  font-size: 24px;
  opacity: 0.1;
  transform: rotate(15deg);
  pointer-events: none;
}

.content-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-large);
}

.content-card-toolkit {
  border-left-color: var(--accent-color);
  background-color: var(--bg-accent);
}

.content-card-toolkit::before {
  content: "🎁";
  font-size: 28px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.card-category {
  font-size: 12px;
  color: var(--primary-color);
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
  background-color: var(--bg-secondary);
  padding: 4px 10px;
  border-radius: 12px;
}

.category-icon {
  font-size: 14px;
}

.card-type {
  font-size: 12px;
  color: var(--text-secondary);
  background-color: var(--bg-secondary);
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 5px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 15px;
  line-height: 1.5;
  color: var(--text-primary);
}

.card-title a {
  color: var(--text-primary);
  text-decoration: none;
  transition: color 0.3s ease;
}

.card-title a:hover {
  color: var(--primary-color);
}

.card-summary {
  font-size: 14px;
  line-height: 1.8;
  color: var(--text-secondary);
  margin-bottom: 20px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  background-color: var(--bg-secondary);
  padding: 12px;
  border-radius: 8px;
}

.card-meta {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  font-size: 12px;
  color: var(--text-light);
  
  .price {
    color: var(--accent-color);
    font-weight: 600;
    font-size: 14px;
  }

  background-color: var(--bg-secondary);
  padding: 10px;
  border-radius: 8px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.card-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
}

.read-more-btn {
  color: var(--primary-color);
  text-decoration: none;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 8px 16px;
  border-radius: 12px;
  background-color: var(--bg-secondary);
}

.read-more-btn:hover {
  color: white;
  background-color: var(--primary-color);
  transform: translateX(5px);
}

.buy-btn {
  background-color: var(--accent-color);
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: var(--shadow-medium);
}

.buy-btn:hover {
  background-color: #FFC107;
  transform: translateY(-2px);
  box-shadow: var(--shadow-medium);
}

/* 加载更多按钮 */
.load-more {
  text-align: center;
}



.load-more-btn {
  padding: 0.75rem 2rem;
  background-color: var(--accent-color);
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.load-more-btn:hover {
  background-color: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow: var(--shadow-medium);
}

/* 响应式设计 */
@media (max-width: 992px) {
  .content-list {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
  }
  
  .page-title {
    font-size: 24px;
  }
  
  .page-title::before,
  .page-title::after {
    font-size: 18px;
  }
  
  .card-title {
    font-size: 16px;
  }
  
  .theme-decoration {
    gap: 20px;
  }
  
  .decoration-icon {
    font-size: 28px;
  }
}

@media (max-width: 768px) {
  .page-title {
    font-size: 20px;
    flex-direction: column;
    gap: 8px;
  }
  
  .page-title::before,
  .page-title::after {
    content: "";
  }
  
  .page-subtitle {
    font-size: 14px;
    padding: 10px 15px;
    font-weight: 500;
  }
  
  .category-tabs {
    gap: 8px;
  }
  
  .tab-btn {
    padding: 8px 16px;
    font-size: 13px;
    gap: 6px;
  }
  
  .content-list {
    grid-template-columns: 1fr;
    gap: 18px;
  }
  
  .content-card {
    padding: 20px;
  }
  
  .card-actions {
    flex-direction: column;
    gap: 15px;
    align-items: stretch;
  }
  
  .buy-btn {
    justify-content: center;
  }
  
  .theme-decoration {
    gap: 15px;
  }
  
  .decoration-icon {
    font-size: 24px;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 18px;
  }
  
  .page-subtitle {
    font-size: 13px;
  }
  
  .tab-btn {
    padding: 6px 12px;
    font-size: 12px;
  }
  
  .card-title {
    font-size: 15px;
  }
  
  .card-summary {
    font-size: 13px;
  }
}

/* 加载状态样式 */
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  padding: 40px;
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid var(--bg-secondary);
  border-top: 4px solid var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-spinner p {
  font-size: 16px;
  color: var(--text-secondary);
  font-weight: 500;
}

/* 空状态样式 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  padding: 40px;
  text-align: center;
  background-color: var(--bg-primary);
  border-radius: 16px;
  box-shadow: var(--shadow-medium);
  margin-bottom: 30px;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.2;
}

.empty-state h3 {
  font-size: 20px;
  color: var(--text-primary);
  margin-bottom: 8px;
  font-weight: 600;
}

.empty-state p {
  font-size: 14px;
  color: var(--text-secondary);
  max-width: 400px;
}
</style>