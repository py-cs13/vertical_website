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
          <a :href="`/article/${article.id}`" @click.prevent="navigateToArticle(article.id)">
            {{ article.title }}
          </a>
        </li>
      </ul>
    </div>
    
    <!-- 热门工具包 -->
    <div class="sidebar-section">
      <h3 class="section-title">热门工具包</h3>
      <ul class="hot-list">
        <li v-for="toolkit in hotToolkits" :key="toolkit.id">
          <a :href="`/toolkit/${toolkit.id}`" @click.prevent="navigateToToolkit(toolkit.id)">
            {{ toolkit.title }}
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 模拟分类数据
const categories = ref([
  { id: 1, name: '健康养生', count: 25 },
  { id: 2, name: '母婴育儿', count: 18 },
  { id: 3, name: '运动健身', count: 12 },
  { id: 4, name: '饮食营养', count: 20 },
  { id: 5, name: '心理疏导', count: 8 },
  { id: 6, name: '睡眠管理', count: 15 }
])

// 模拟热门文章数据
const hotArticles = ref([
  { id: 1, title: '10个简单的养生小技巧' },
  { id: 2, title: '如何科学安排孕期饮食' },
  { id: 3, title: '上班族必看：缓解颈椎疼痛的方法' },
  { id: 4, title: '营养早餐搭配指南' },
  { id: 5, title: '如何改善睡眠质量' }
])

// 模拟热门工具包数据
const hotToolkits = ref([
  { id: 1, title: '家庭健康管理工具包' },
  { id: 2, title: '新生儿护理工具包' },
  { id: 3, title: '减肥健身计划工具包' },
  { id: 4, title: '营养膳食搭配工具包' },
  { id: 5, title: '心理健康测试工具包' }
])

// 分类筛选方法
const filterByCategory = (categoryName) => {
  // 实际项目中这里会调用API获取对应分类的内容
  console.log(`Filter by category: ${categoryName}`)
}

// 导航到文章详情
const navigateToArticle = (articleId) => {
  router.push(`/article/${articleId}`)
}

// 导航到工具包详情
const navigateToToolkit = (toolkitId) => {
  router.push(`/toolkit/${toolkitId}`)
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
  
  console.log('=== 立即购买按钮点击事件开始 ===')
  console.log('点击的商品：', mockToolkit)
  
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
  console.log('路由跳转命令已执行，跳转到支付页面')
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
  padding: 18px;
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
}

.section-title::before {
  content: "🌸";
  font-size: 16px;
}

/* 分类列表 */
.category-list {
  list-style: none;
}

.category-list li {
  margin-bottom: 12px;
}

.category-list a {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: var(--text-secondary);
  text-decoration: none;
  transition: all 0.3s ease;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 15px;
}

.category-list a:hover {
  color: var(--primary-color);
  background-color: var(--bg-accent);
  transform: translateX(5px);
}

.category-list .count {
  font-size: 12px;
  color: var(--text-light);
  background-color: var(--bg-primary);
  padding: 3px 8px;
  border-radius: 12px;
  border: 1px solid var(--border-color);
}

/* 热门列表 */
.hot-list {
  list-style: none;
}

.hot-list li {
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--border-color);
  position: relative;
  padding-left: 20px;
}

.hot-list li::before {
  content: "✨";
  position: absolute;
  left: 0;
  top: 5px;
  font-size: 12px;
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
  line-height: 1.6;
  transition: all 0.3s ease;
  display: block;
}

.hot-list a:hover {
  color: var(--primary-color);
  transform: translateX(5px);
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