<template>
  <div class="home-view">
    <!-- 母婴主题装饰 -->
    <div class="theme-decoration">
      <div class="decoration-icon">👶</div>
      <div class="decoration-icon">🍼</div>
      <div class="decoration-icon">🎀</div>
    </div>
    
    <!-- 页面副标题 -->
    <p class="page-subtitle main-subtitle">专业的母婴知识分享，陪伴宝贝健康成长每一天</p>
    
    <!-- 第一区块：欢迎内容 -->
    <div class="welcome-section">
      <h1 class="welcome-title">👩‍👧‍👦 欢迎来到母婴知识宝库</h1>
      <p class="welcome-text">
        在这里，我们为每一位新手妈妈和准妈妈提供最专业、最贴心的母婴知识。
        从孕期护理到产后恢复，从婴儿护理到早期教育，我们陪伴您和宝宝一起成长。
      </p>
      
      <!-- 功能导航 -->
      <div class="feature-nav">
        <router-link to="/articles" class="feature-card">
          <div class="feature-icon">📚</div>
          <div class="feature-info">
            <h3>精选文章</h3>
            <p>阅读专业母婴知识</p>
          </div>
        </router-link>
        
        <router-link to="/agents" class="feature-card">
          <div class="feature-icon">🧸</div>
          <div class="feature-info">
            <h3>智能体</h3>
            <p>实用的育儿工具</p>
          </div>
        </router-link>
      </div>
    </div>
    
    <!-- 分隔装饰 -->
    <div class="section-divider">
      <div class="divider-line"></div>
      <div class="divider-icon">✨</div>
      <div class="divider-line"></div>
    </div>
    
    <!-- 第二区块：推荐文章 -->
    <div class="recommended-section" v-if="recommendedArticles.length > 0">
      <h2 class="recommended-title">🔥 热门推荐</h2>
      <div class="recommended-cards">
        <router-link 
          v-for="article in recommendedArticles" 
          :key="article.id"
          :to="`/article/${article.id}`"
          class="recommended-card"
        >
          <div class="recommended-category">{{ article.category }}</div>
          <h3 class="recommended-card-title">{{ article.title }}</h3>
          <p class="recommended-summary">{{ article.summary }}</p>
          <span class="read-more-text">阅读更多 →</span>
        </router-link>
      </div>
    </div>
    
    <!-- 加载中状态 -->
    <div class="loading-recommended" v-else-if="loading">
      <p>加载推荐内容中...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// 推荐文章数据
const recommendedArticles = ref([])
const loading = ref(true)

// 获取推荐文章（获取最新发布的前3篇文章）
const fetchRecommendedArticles = async () => {
  try {
    // 使用专门的最新文章接口
    const token = localStorage.getItem('token')
    console.log('开始获取推荐文章...')
    const response = await axios.get('/api/articles/latest?limit=3', {
      headers: token ? { Authorization: `Bearer ${token}` } : {}
    })
    
    console.log('API响应:', response.data)
    
    if (response.data && response.data.length > 0) {
      // 映射文章数据，去除HTML标签获取纯文本摘要
      recommendedArticles.value = response.data.map(article => ({
        id: article.id,
        title: article.title,
        category: article.category,
        summary: article.summary ? article.summary.replace(/<[^>]*>/g, '').substring(0, 80) + '...' : '',
        created_at: article.created_at
      }))
      console.log('推荐文章数据:', recommendedArticles.value)
    } else {
      console.log('没有获取到推荐文章数据')
    }
  } catch (error) {
    console.error('获取推荐文章失败:', error)
    console.error('错误详情:', error.response?.data || error.message)
  } finally {
    loading.value = false
    console.log('加载状态:', loading.value)
  }
}

onMounted(() => {
  fetchRecommendedArticles()
})
</script>

<style scoped>
.home-view {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

/* 母婴主题装饰 */
.theme-decoration {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
}

.decoration-icon {
  font-size: 32px;
  opacity: 0.7;
}

/* 页面副标题 */
.page-subtitle {
  text-align: center;
  margin-bottom: 20px;
  color: #666;
  font-size: 16px;
}

.main-subtitle {
  font-size: 18px;
  font-weight: 500;
  color: #333;
}

/* 欢迎区域 */
.welcome-section {
  background: linear-gradient(135deg, #fff5f5 0%, #fff 100%);
  border-radius: 20px;
  padding: 60px 40px;
  text-align: center;
  margin-top: 30px;
  box-shadow: 0 4px 20px rgba(255, 107, 139, 0.1);
}

.welcome-title {
  font-size: 36px;
  color: #333;
  margin-bottom: 20px;
  font-weight: 700;
}

.welcome-text {
  font-size: 18px;
  color: #666;
  line-height: 1.8;
  max-width: 800px;
  margin: 0 auto 40px;
}

/* 功能导航 */
.feature-nav {
  display: flex;
  justify-content: center;
  gap: 30px;
  flex-wrap: wrap;
}

.feature-card {
  display: flex;
  align-items: center;
  gap: 20px;
  background: white;
  padding: 30px 40px;
  border-radius: 16px;
  text-decoration: none;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.feature-card:hover {
  transform: translateY(-5px);
  border-color: #FF6B8B;
  box-shadow: 0 8px 25px rgba(255, 107, 139, 0.2);
}

.feature-icon {
  font-size: 48px;
}

.feature-info h3 {
  font-size: 20px;
  color: #333;
  margin-bottom: 5px;
  font-weight: 600;
}

.feature-info p {
  font-size: 14px;
  color: #666;
  margin: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .welcome-section {
    padding: 40px 20px;
  }
  
  .welcome-title {
    font-size: 28px;
  }
  
  .welcome-text {
    font-size: 16px;
  }
  
  .feature-nav {
    flex-direction: column;
    align-items: center;
  }
  
  .feature-card {
    width: 100%;
    max-width: 300px;
    justify-content: center;
  }
}

/* 分隔装饰 */
.section-divider {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  margin: 40px 0;
}

.divider-line {
  flex: 1;
  max-width: 200px;
  height: 2px;
  background: linear-gradient(90deg, transparent, #FF6B8B, transparent);
}

.divider-icon {
  font-size: 20px;
  color: #FF6B8B;
}

/* 推荐文章区域 */
.recommended-section {
  background: linear-gradient(135deg, #fff5f5 0%, #fff 100%);
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 4px 20px rgba(255, 107, 139, 0.1);
}

.recommended-title {
  font-size: 24px;
  color: #333;
  margin-bottom: 25px;
  text-align: center;
  font-weight: 600;
}

.recommended-cards {
  display: flex;
  gap: 25px;
  justify-content: center;
  flex-wrap: wrap;
}

.recommended-card {
  flex: 1;
  min-width: 280px;
  max-width: 350px;
  background: white;
  border-radius: 16px;
  padding: 25px;
  text-decoration: none;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border: 2px solid transparent;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.recommended-card:hover {
  transform: translateY(-8px);
  border-color: #FF6B8B;
  box-shadow: 0 8px 30px rgba(255, 107, 139, 0.2);
}

.recommended-category {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #FF6B8B;
  font-weight: 500;
}

.recommended-card-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0;
  line-height: 1.5;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.recommended-summary {
  font-size: 14px;
  color: #666;
  line-height: 1.7;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  flex-grow: 1;
}

.read-more-text {
  font-size: 14px;
  color: #FF6B8B;
  font-weight: 500;
  margin-top: auto;
  transition: all 0.3s ease;
}

.recommended-card:hover .read-more-text {
  transform: translateX(5px);
}

.loading-recommended {
  text-align: center;
  padding: 40px 0;
  color: #666;
}

/* 响应式 - 推荐卡片 */
@media (max-width: 992px) {
  .recommended-cards {
    flex-direction: column;
    align-items: center;
  }
  
  .recommended-card {
    width: 100%;
    max-width: 500px;
  }
}

@media (max-width: 768px) {
  .section-divider {
    margin: 30px 0;
  }
  
  .divider-line {
    max-width: 100px;
  }
  
  .recommended-section {
    padding: 30px 20px;
  }
}
</style>