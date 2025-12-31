<template>
  <aside class="sidebar">
    <!-- 分类导航 -->
    <div class="sidebar-section">
      <h3 class="section-title">内容分类</h3>
      <ul class="category-list">
        <li v-for="category in categories" :key="category.id">
          <a href="#" @click.prevent="filterByCategory(category.name)">
            {{ category.name }}
            <span class="count">({{ category.count }})</span>
          </a>
        </li>
      </ul>
    </div>
    
    <!-- 热门文章 -->
    <div class="sidebar-section">
      <h3 class="section-title">热门文章</h3>
        <ul class="hot-list">
          <li v-for="article in hotArticles" :key="article.id">
            <a href="" @click.prevent="navigateToArticle(article.id)" class="hot-article-link">
              {{ article.title }}
            </a>
          </li>
        </ul>
    </div>
    

    
    <!-- 推广广告 -->
    <div class="sidebar-section">
      <h3 class="section-title">特别推荐</h3>
      <div class="advertisement">
        <div class="ad-content">
          <h4>获取专业工具包</h4>
          <p>9.9元即可获得价值99元的专业工具包</p>
          <button class="ad-btn" @click="buyNow">立即购买</button>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useContentStore } from '../stores/content'

const router = useRouter()
const contentStore = useContentStore()

// 定义事件，用于向父组件传递分类筛选请求
const emit = defineEmits(['filter-category'])

// 分类列表 - 从实际文章数据动态生成
const categories = ref([])
const updateCategoryCounts = () => {
  if (!contentStore.articles || contentStore.articles.length === 0) return
  
  // 从文章数据中获取所有唯一分类
  const articleCategories = contentStore.articles.map(a => a.category)
  const uniqueCategories = [...new Set(articleCategories)]
  
  // 创建分类列表
  categories.value = uniqueCategories.map((cat, index) => ({
    id: index + 1,
    name: cat,
    count: 0
  }))
  
  // 统计每个分类的文章数量
  contentStore.articles.forEach(article => {
    const category = categories.value.find(c => c.name === article.category)
    if (category) {
      category.count++
    }
  })
}

// 热门文章 - 从实际文章数据中获取前5篇
const hotArticles = computed(() => {
  if (!contentStore.articles || contentStore.articles.length === 0) {
    return []
  }
  // 按浏览量或创建时间排序，取前5篇
  return [...contentStore.articles]
    .sort((a, b) => (b.view_count || 0) - (a.view_count || 0))
    .slice(0, 5)
})



// 组件挂载时加载数据并更新分类计数
onMounted(() => {
  // 如果还没有加载文章数据，则加载
  if (contentStore.articles.length === 0) {
    contentStore.fetchLatestArticles()
  }
  
  // 更新分类计数
  updateCategoryCounts()
})

// 监听文章数据变化，更新分类计数
watch(() => contentStore.articles, () => {
  updateCategoryCounts()
}, { deep: true })

// 分类筛选方法
const filterByCategory = (categoryName) => {
  // 向父组件发送分类筛选事件
  emit('filter-category', categoryName)
}

// 导航到文章详情
const navigateToArticle = (articleId) => {
  console.log('navigateToArticle被调用，文章ID:', articleId)
  console.log('当前路由:', router.currentRoute.value)
  console.log('路由实例:', router)
  
  // 尝试使用不同的路由跳转方式
  try {
    // 确保articleId是字符串类型
    const stringId = String(articleId)
    const routePath = `/article/${stringId}`
    console.log('尝试跳转到:', routePath)
    
    // 先记录当前位置
    const currentPath = router.currentRoute.value.path
    console.log('当前路径:', currentPath)
    
    // 使用router.push并监听结果
    router.push(routePath).then(() => {
      console.log('路由跳转成功')
      console.log('跳转后路由:', router.currentRoute.value.path)
    }).catch((error) => {
      console.error('路由跳转失败:', error)
    })
    
    // 立即检查路由变化
    setTimeout(() => {
      console.log('100ms后路由:', router.currentRoute.value.path)
      if (router.currentRoute.value.path === currentPath) {
        console.warn('路由没有发生变化，当前路径:', currentPath)
        // 如果路由没有变化，尝试使用replace方法
        console.log('尝试使用replace方法')
        router.replace(routePath).then(() => {
          console.log('replace跳转成功')
          console.log('replace后路由:', router.currentRoute.value.path)
        }).catch((error) => {
          console.error('replace跳转失败:', error)
        })
      }
    }, 100)
  } catch (error) {
    console.error('navigateToArticle发生异常:', error)
  }
}



// 立即购买功能
const buyNow = () => {
  // 为广告创建一个模拟的商品对象
  const mockToolkit = {
    id: 999, // 模拟的工具包ID
    title: '专业工具包',
    type: 'toolkit',
    price: 9.9
  }
  
  // 跳转到支付页面，携带商品信息
  router.push({
    path: '/payment',
    query: {
      product_type: mockToolkit.type,
      product_id: mockToolkit.id,
      product_name: mockToolkit.title,
      price: mockToolkit.price
    }
  })
}
</script>

<style scoped>
.sidebar {
  width: 280px;
  padding: 20px;
  background-color: var(--bg-primary);
  box-shadow: var(--shadow-light);
  border-radius: 12px;
  border: 1px solid var(--border-color);
}

.sidebar-section {
  margin-bottom: 25px;
  background-color: var(--bg-secondary);
  padding: 15px;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.sidebar-section:hover {
  box-shadow: var(--shadow-light);
  transform: translateY(-2px);
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 15px;
  color: var(--primary-color);
  padding-bottom: 10px;
  border-bottom: 2px solid var(--bg-accent);
  display: flex;
  align-items: center;
  gap: 8px;
  padding-left: 0;
}

.section-title::before {
  content: "🌸";
  font-size: 16px;
}

/* 分类列表 */
.category-list {
  list-style: none;
  padding-left: 0;
  margin-left: 0;
}

.category-list li {
  margin-bottom: 10px;
  position: relative;
}

.category-list a {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: var(--text-secondary);
  text-decoration: none;
  transition: all 0.3s ease;
  padding: 10px 10px 10px 28px;
  border-radius: 8px;
  font-size: 14px;
  line-height: 1.5;
  width: 100%;
  box-sizing: border-box;
  position: relative;
}

.category-list a::before {
  content: "✨";
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 14px;
  transition: transform 0.3s ease;
}

.category-list a:hover {
  color: var(--primary-color);
  background-color: var(--bg-accent);
  transform: translateX(3px);
}

.category-list a:hover::before {
  transform: translateY(-50%) scale(1.2);
  color: #FFD700;
}

.category-list .count {
  font-size: 12px;
  color: var(--text-light);
  background-color: var(--bg-primary);
  padding: 4px 10px;
  border-radius: 12px;
  border: 1px solid var(--border-color);
  min-width: 35px;
  text-align: center;
  font-weight: 500;
}

/* 热门列表 */
.hot-list {
  list-style: none;
  padding-left: 0;
  margin-left: 0;
}

.hot-list li {
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--border-color);
  position: relative;
  padding-left: 28px;
  min-height: 24px;
  margin-left: 0;
}

.hot-list li::before {
  content: "✨";
  position: absolute;
  left: 8px;
  top: 5px;
  font-size: 14px;
  width: 15px;
  height: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease;
}

.hot-list li:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.hot-list a {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 14px;
  line-height: 1.5;
  transition: all 0.3s ease;
  display: block;
  padding: 2px 0;
  width: 100%;
  box-sizing: border-box;
}

.hot-list a:hover {
  color: var(--primary-color);
  transform: translateX(3px);
}

.hot-list li:hover::before {
  transform: scale(1.2);
  color: #FFD700;
}

/* 广告区域 */
.advertisement {
  background: linear-gradient(135deg, #FFF5F8 0%, #F0F8FF 100%);
  padding: 25px 20px;
  border-radius: 12px;
  text-align: center;
  border: 2px dashed var(--primary-color);
}

.ad-content h4 {
  font-size: 18px;
  margin-bottom: 12px;
  color: var(--primary-color);
  font-weight: 600;
}

.ad-content p {
  font-size: 14px;
  margin-bottom: 18px;
  color: var(--text-secondary);
}

.ad-btn {
  background-color: var(--accent-color);
  color: var(--text-primary);
  border: none;
  padding: 10px 25px;
  border-radius: 25px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 15px;
  box-shadow: var(--shadow-light);
}

.ad-btn:hover {
  background-color: #FFC107;
  transform: translateY(-2px);
  box-shadow: var(--shadow-medium);
}

/* 响应式设计 */
@media (max-width: 992px) {
  .sidebar {
    width: 240px;
    padding: 15px;
  }
  
  .sidebar-section {
    padding: 15px;
    margin-bottom: 20px;
  }
  
  .section-title {
    font-size: 16px;
  }
  
  .section-title::before {
    font-size: 14px;
  }
  
  .hot-list a {
    font-size: 13px;
  }
}

@media (max-width: 768px) {
  .sidebar {
    width: 100%;
    margin-top: 20px;
    padding: 15px;
  }
  
  .sidebar-section {
    margin-bottom: 20px;
    padding: 15px;
  }
  
  .sidebar-section:last-child {
    margin-bottom: 0;
  }
}
</style>