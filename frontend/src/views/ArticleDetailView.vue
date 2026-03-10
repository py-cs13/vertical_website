<template>
  <div class="article-detail">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner">
        <div class="spinner"></div>
        <p>正在加载文章...</p>
      </div>
    </div>
    
    <template v-else>
      <!-- 母婴主题装饰 -->
      <div class="theme-decoration">
        <div class="decoration-icon">👶</div>
        <div class="decoration-icon">📚</div>
        <div class="decoration-icon">🎀</div>
      </div>
      
      <!-- 文章头部信息 -->
      <div class="article-header">
        <div class="article-category">
          <span class="category-icon">{{ getCategoryIcon(article.category) }}</span>
          {{ article.category }}
        </div>
        <h1 class="article-title">{{ article.title }}</h1>
        <div class="article-meta">
          <span class="meta-item">
            <i class="icon">📅</i> {{ formatDate(article.created_at) }}
          </span>
          <span class="meta-item">
            <i class="icon">👁️</i> {{ formatNumber(article.view_count) }}
          </span>
          <span class="meta-item">
            <i class="icon">❤️</i> {{ formatNumber(article.likes) }}
          </span>
        </div>
        <div class="article-summary">{{ article.summary }}</div>
      </div>
      
      <!-- 文章正文 -->
      <div class="article-content">
        <!-- 直接渲染API返回的HTML -->
        <div v-html="article.content"></div>
      </div>
      
      <!-- 文章操作区 -->
      <div class="article-actions">
        <Button 
          variant="secondary" 
          size="medium" 
          @click="toggleLike"
          :class="{ 'active': article.liked, 'like-btn': true }"
          :disabled="isLiking"
        >
          <i class="icon">❤️</i> {{ article.liked ? '已点赞' : '点赞' }}
        </Button>
        <Button 
          variant="secondary" 
          size="medium" 
          @click="shareArticle"
          class="share-btn"
        >
          <i class="icon">📤</i> 分享
        </Button>
        <Button 
          variant="secondary" 
          size="medium" 
          @click="toggleCollect"
          :class="{ 'active': article.collected, 'collect-btn': true }"
        >
          <i class="icon">⭐</i> {{ article.collected ? '已收藏' : '收藏' }}
        </Button>
      </div>
      
      <!-- 相关推荐 -->
      <div class="related-content">
        <h3 class="related-title">
          <span class="related-icon">📚</span> 相关推荐
        </h3>
        <div class="related-list">
          <div 
            v-for="item in relatedArticles" 
            :key="item.id" 
            class="related-item"
          >
            <router-link :to="`/article/${item.id}`" class="related-link">
              <div class="related-item-header">
                <span class="related-item-category">
                  <span class="category-icon">{{ getCategoryIcon(item.category) }}</span>
                  {{ item.category }}
                </span>
              </div>
              <h4 class="related-item-title">{{ item.title }}</h4>
              <p class="related-item-summary">{{ item.summary }}</p>
            </router-link>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter, onBeforeRouteUpdate } from 'vue-router'
import { useContentStore, useAuthStore } from '../stores'
import axios from 'axios'
import apiClient from '../utils/api'
import Button from '../components/Button.vue'
import { formatDate, formatNumber } from '../utils/formatters'
import { marked } from 'marked'

const route = useRoute()
const router = useRouter()
const contentStore = useContentStore()
const authStore = useAuthStore()
const articleId = ref(route.params.id) // 使用ref来跟踪路由参数的id值
const loading = ref(true)

// 文章详情
const article = ref({
  id: articleId,
  title: '',
  category: '',
  summary: '',
  content: '',
  created_at: '',
  view_count: 0,
  likes: 0,
  liked: false,
  collected: false
})

// 点赞按钮加载状态
const isLiking = ref(false)

// 相关推荐
const relatedArticles = ref([
  { id: 2, title: '如何科学安排孕期饮食', category: '营养辅食', summary: '孕期饮食对胎儿发育至关重要，本文将为您介绍科学的孕期饮食安排。' },
  { id: 3, title: '新生儿护理的10个关键要点', category: '母婴育儿', summary: '新手父母必看，掌握这些新生儿护理技巧，让宝宝健康成长。' },
  { id: 4, title: '亲子互动游戏推荐（0-1岁）', category: '亲子互动', summary: '通过简单的互动游戏，促进宝宝的智力和情感发展。' },
  { id: 5, title: '产后恢复的正确方法', category: '产后恢复', summary: '科学的产后恢复计划，帮助新妈妈快速恢复身体健康。' },
  { id: 6, title: '宝宝辅食添加时间表', category: '营养辅食', summary: '了解宝宝不同阶段的辅食添加建议，让宝宝营养均衡成长。' },
  { id: 7, title: '婴儿睡眠习惯培养指南', category: '母婴育儿', summary: '帮助宝宝建立良好的睡眠习惯，让全家都能睡个好觉。' }
])

// 获取分类对应的图标
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
  return iconMap[categoryName] || '📖'
}

// 将Markdown内容转换为HTML格式的函数 - 简化版，更适合直接显示后端传来的小红书风格内容
const formatContent = (content) => {
  if (!content) return '';
  
  // 直接返回内容，不做任何处理，因为后端已经返回了HTML格式的内容
  return content;
}

// 加载文章详情
const loadArticleDetail = async (id) => {
  loading.value = true
  try {
    // 尝试从store获取文章详情
    const articleData = await contentStore.fetchArticleDetail(id)
    if (articleData) {
      // 调试：打印API返回的content字段
      console.log('API返回的content类型:', typeof articleData.content)
      console.log('API返回的content前100字符:', articleData.content.substring(0, 100))
      // 直接使用后端返回的HTML内容，不需要再用marked解析
      article.value = {
        ...articleData,
        content: articleData.content,
        liked: articleData.liked || false,
        collected: articleData.collected || false
      }
    } else {
      // 如果store没有数据，使用模拟数据
      article.value = {
        id: id,
        title: '新生儿护理的10个重要技巧',
        category: '母婴育儿',
        summary: '作为新手父母，掌握正确的新生儿护理技巧至关重要。本文将为您介绍10个关键的护理要点，帮助您更好地照顾宝宝。',
        content: `<p>作为新手父母，掌握正确的新生儿护理技巧至关重要。本文将为您介绍10个关键的护理要点，帮助您更好地照顾宝宝。</p>\n\n<h2>1. 保持清洁与卫生</h2>\n<p>新生儿的皮肤非常娇嫩，需要特别注意清洁和卫生。每天用温水为宝宝洗澡，避免使用刺激性的沐浴产品。</p>\n\n<h2>2. 正确的喂养方式</h2>\n<p>母乳喂养是最佳的选择，如果无法母乳喂养，可以选择适合宝宝的配方奶粉。喂养时要注意正确的姿势，避免宝宝呛奶。</p>\n\n<h2>3. 充足的睡眠</h2>\n<p>新生儿每天需要大量的睡眠，确保宝宝有一个安静、舒适的睡眠环境，有助于宝宝的生长发育。</p>\n\n<h2>4. 体温调节</h2>\n<p>新生儿的体温调节能力较差，要注意保持室内温度适宜，避免宝宝过热或过冷。</p>\n\n<h2>5. 脐带护理</h2>\n<p>保持宝宝的脐带部位清洁干燥，避免感染。一般情况下，脐带会在出生后1-2周自然脱落。</p>\n\n<h2>6. 观察宝宝的状态</h2>\n<p>密切观察宝宝的饮食、睡眠、大小便等情况，如有异常及时就医。</p>\n\n<h2>7. 避免过度刺激</h2>\n<p>新生儿的神经系统尚未发育完善，要避免过度的噪音、强光等刺激。</p>\n\n<h2>8. 适当的抚触</h2>\n<p>适当的抚触有助于促进宝宝的血液循环和身体发育，增强亲子关系。</p>\n\n<h2>9. 按时接种疫苗</h2>\n<p>按照医生的建议，按时为宝宝接种疫苗，预防各种疾病。</p>\n\n<h2>10. 寻求专业帮助</h2>\n<p>如果您有任何关于新生儿护理的问题，不要犹豫，及时寻求医生或专业人士的帮助。</p>`,
        created_at: new Date().toISOString(),
        views: Math.floor(Math.random() * 1000),
        likes: Math.floor(Math.random() * 100),
        liked: false,
        collected: false
      }
    }
    
    // 如果用户已登录，获取收藏状态和点赞状态
    if (authStore.token) {
      try {
        // 获取收藏状态
        const collectResponse = await apiClient.get(`/content/${id}/collect/status`)
        article.value.collected = collectResponse.data.data.is_collected
        
        // 获取点赞状态
        const likeResponse = await apiClient.get(`/content/${id}/like/status`)
        // 注意：点赞状态接口返回的数据没有包裹data字段
        article.value.liked = likeResponse.data.is_liked
        article.value.likes = likeResponse.data.like_count
      } catch (error) {
        console.error('获取状态失败:', error)
      }
    }
    
  } catch (error) {
    console.error('加载文章详情失败:', error)
    // 使用模拟数据作为备选
    article.value = {
      id: id,
      title: '新生儿护理的10个重要技巧',
      category: '母婴育儿',
      summary: '作为新手父母，掌握正确的新生儿护理技巧至关重要。本文将为您介绍10个关键的护理要点，帮助您更好地照顾宝宝。',
      content: `<p>作为新手父母，掌握正确的新生儿护理技巧至关重要。本文将为您介绍10个关键的护理要点，帮助您更好地照顾宝宝。</p>\n\n<h2>1. 保持清洁与卫生</h2>\n<p>新生儿的皮肤非常娇嫩，需要特别注意清洁和卫生。每天用温水为宝宝洗澡，避免使用刺激性的沐浴产品。</p>\n\n<h2>2. 正确的喂养方式</h2>\n<p>母乳喂养是最佳的选择，如果无法母乳喂养，可以选择适合宝宝的配方奶粉。喂养时要注意正确的姿势，避免宝宝呛奶。</p>\n\n<h2>3. 充足的睡眠</h2>\n<p>新生儿每天需要大量的睡眠，确保宝宝有一个安静、舒适的睡眠环境，有助于宝宝的生长发育。</p>\n\n<h2>4. 体温调节</h2>\n<p>新生儿的体温调节能力较差，要注意保持室内温度适宜，避免宝宝过热或过冷。</p>\n\n<h2>5. 脐带护理</h2>\n<p>保持宝宝的脐带部位清洁干燥，避免感染。一般情况下，脐带会在出生后1-2周自然脱落。</p>\n\n<h2>6. 观察宝宝的状态</h2>\n<p>密切观察宝宝的饮食、睡眠、大小便等情况，如有异常及时就医。</p>\n\n<h2>7. 避免过度刺激</h2>\n<p>新生儿的神经系统尚未发育完善，要避免过度的噪音、强光等刺激。</p>\n\n<h2>8. 适当的抚触</h2>\n<p>适当的抚触有助于促进宝宝的血液循环和身体发育，增强亲子关系。</p>\n\n<h2>9. 按时接种疫苗</h2>\n<p>按照医生的建议，按时为宝宝接种疫苗，预防各种疾病。</p>\n\n<h2>10. 寻求专业帮助</h2>\n<p>如果您有任何关于新生儿护理的问题，不要犹豫，及时寻求医生或专业人士的帮助。</p>`,
      created_at: new Date().toISOString(),
      views: Math.floor(Math.random() * 1000),
      likes: Math.floor(Math.random() * 100),
      liked: false,
      collected: false
    }
  } finally {
    loading.value = false
  }
}

// 监听路由参数变化
onBeforeRouteUpdate((to, from) => {
  if (to.params.id !== from.params.id) {
    articleId.value = to.params.id
    article.value.id = articleId.value
    loadArticleDetail(articleId.value)
  }
})

// 初始加载文章详情
onMounted(async () => {
  await loadArticleDetail(articleId.value)
})

// 切换点赞状态
const toggleLike = async () => {
  const token = authStore.token
  if (!token) {
    alert('请先登录再点赞')
    return
  }
  
  // 防止重复点击
  if (isLiking.value) return
  isLiking.value = true
  
  // 乐观更新：先切换本地状态
  const wasLiked = article.value.liked
  article.value.liked = !wasLiked
  article.value.likes += wasLiked ? -1 : 1
  
  try {
    const response = await apiClient.post(`/content/${articleId.value}/like`)
    
    // 使用后端返回的点赞状态和数量
    if (response.data) {
      article.value.liked = response.data.is_liked
      article.value.likes = response.data.like_count
    }
  } catch (error) {
    console.error('点赞失败:', error)
    // 回滚乐观更新
    article.value.liked = wasLiked
    article.value.likes += wasLiked ? 1 : -1
    
    if (error.response?.status === 401) {
      alert('请先登录后再点赞')
    } else {
      alert(error.response?.data?.detail || '点赞失败，请稍后重试')
    }
  } finally {
    isLiking.value = false
  }
}

// 切换收藏状态
const toggleCollect = async () => {
  const token = authStore.token
  if (!token) {
    alert('请先登录再收藏')
    return
  }
  
  // 乐观更新：先切换本地状态
  const wasCollected = article.value.collected
  article.value.collected = !wasCollected
  
  try {
    const response = await apiClient.post(`/content/${articleId.value}/collect`)
    
    // 兼容两种响应格式：
    // 1. 收藏成功时：response.data 是 {id, user_id, content_id, created_at}
    // 2. 取消收藏时：response.data.data 是 {id, user_id, content_id, created_at}
    if (response.data.status) {
      // 取消收藏成功，返回的是status格式
      article.value.collected = false
    } else {
      // 收藏成功，返回的是直接的favorite对象
      article.value.collected = true
    }
  } catch (error) {
    console.error('收藏失败:', error)
    // 回滚乐观更新
    article.value.collected = wasCollected
    
    if (error.response?.status === 401) {
      alert('请先登录后再收藏')
    } else {
      alert(error.response?.data?.detail || '收藏失败，请稍后重试')
    }
  }
}

// 分享文章
const shareArticle = () => {
  // 实际项目中这里会调用分享API
  alert('分享功能开发中...')
}

</script>

<style scoped>
.article-detail {
  max-width: 100%;
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

/* 文章头部信息 - 小红书风格 */
.article-header {
  margin-bottom: 40px;
  background-color: #fff;
  padding: 32px;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  position: relative;
  overflow: hidden;
}

/* 小红书风格装饰 */
.article-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 6px;
  background: linear-gradient(90deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
}

/* 可爱的背景装饰 */
.article-header::after {
  content: '🌸';
  position: absolute;
  top: 20px;
  right: 20px;
  font-size: 48px;
  opacity: 0.08;
  transform: rotate(15deg);
}

.article-category {
  font-size: 14px;
  color: #ff9a9e;
  font-weight: 700;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  background-color: #fff5f5;
  padding: 8px 16px;
  border-radius: 20px;
  width: fit-content;
  box-shadow: 0 2px 8px rgba(255, 154, 158, 0.15);
}

.category-icon {
  font-size: 18px;
}

.article-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 24px;
  line-height: 1.3;
  color: #333;
  position: relative;
  z-index: 1;
}

.article-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  font-size: 13px;
  color: #999;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  background-color: #fafafa;
  padding: 6px 14px;
  border-radius: 16px;
  transition: all 0.3s ease;
}

.meta-item:hover {
  background-color: #fff5f5;
  color: #ff9a9e;
}

.article-summary {
  font-size: 17px;
  line-height: 1.8;
  color: #666;
  background-color: #fafafa;
  padding: 22px;
  border-radius: 16px;
  border-left: 4px solid #fecfef;
  position: relative;
  z-index: 1;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

/* 母婴主题装饰 - 优化 */
.theme-decoration {
  display: flex;
  justify-content: center;
  gap: 25px;
  margin-bottom: 25px;
  animation: float 3s ease-in-out infinite;
}

.decoration-icon {
  font-size: 36px;
  filter: drop-shadow(0 4px 8px rgba(255, 154, 158, 0.2));
  transform: rotate(-12deg);
}

.decoration-icon:nth-child(2) {
  font-size: 40px;
  transform: rotate(0deg);
  animation-delay: 0.5s;
}

.decoration-icon:nth-child(3) {
  font-size: 32px;
  transform: rotate(12deg);
  animation-delay: 1s;
}

/* 文章正文 - 小红书风格优化 */
.article-content {
  margin-bottom: 40px;
  font-size: 16px;
  line-height: 2.2;
  color: #333;
  background-color: #fff;
  padding: 36px;
  border-radius: 20px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.06);
  position: relative;
  overflow: hidden;
}

/* 小红书风格装饰元素 */
.article-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 8px;
  background: linear-gradient(90deg, #ff9a9e 0%, #fecfef 50%, #ff9a9e 100%);
}

/* 标题样式优化 - 增强层级感 */
.article-content :deep(h1) {
  font-size: 26px;
  font-weight: 700;
  margin: 40px 0 22px;
  color: #333;
  padding-left: 12px;
  border-left: 4px solid #ff9a9e;
  background: linear-gradient(45deg, #fff5f5, #ffffff);
  padding: 10px 18px;
  border-radius: 12px;
}

.article-content :deep(h2) {
  font-size: 22px;
  font-weight: 700;
  margin: 35px 0 20px;
  color: #333;
  padding-left: 14px;
  background: linear-gradient(45deg, #fff5f5, #ffffff);
  padding: 8px 18px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
  border-left: 3px solid #ff9a9e;
}

.article-content :deep(h3) {
  font-size: 19px;
  font-weight: 600;
  margin: 30px 0 16px;
  color: #444;
  padding-left: 10px;
  border-left: 3px solid #fecfef;
}

.article-content :deep(h2:first-child),
.article-content :deep(h1:first-child) {
  margin-top: 0;
}

/* 段落样式优化 - 增强可读性 */
.article-content :deep(p) {
  margin-bottom: 32px;
  text-align: left;
  color: #555;
  font-size: 16px;
  padding: 0 8px;
  text-indent: 2em;
  background-color: rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
}

.article-content :deep(p:hover) {
  background-color: #fff5f5;
  border-radius: 8px;
  padding: 8px 12px;
}

/* 首段特殊样式 */
.article-content :deep(p:first-child) {
  font-size: 17px;
  color: #333;
  font-weight: 500;
  background-color: #fafafa;
  padding: 20px;
  border-radius: 12px;
}

/* 列表样式优化 - 小红书风格 */
.article-content :deep(ul), .article-content :deep(ol) {
  margin-left: 0;
  margin-bottom: 35px;
  padding-left: 0;
  background-color: #fff5f5;
  padding: 22px 25px;
  border-radius: 16px;
  border: 1px solid #ffe4e1;
  box-shadow: 0 2px 10px rgba(255, 154, 158, 0.1);
  list-style: none;
}

.article-content :deep(li) {
  margin-bottom: 22px;
  padding-left: 45px;
  position: relative;
  line-height: 2.0;
  color: #444;
  font-size: 16px;
  background-color: white;
  padding: 12px 16px 12px 45px;
  border-radius: 12px;
  border-left: 3px solid #ff9a9e;
  transition: all 0.3s ease;
}

.article-content :deep(li:hover) {
  transform: translateX(5px);
  box-shadow: 0 3px 12px rgba(255, 154, 158, 0.15);
}

/* 无序列表样式 - 小红书风格优化 */
.article-content :deep(ul li)::before {
  content: '🎀';
  position: absolute;
  left: 12px;
  top: 14px;
  color: #ff69b4;
  font-size: 18px;
  filter: drop-shadow(0 2px 4px rgba(255, 105, 180, 0.3));
}

/* 有序列表样式 - 小红书风格优化 */
.article-content :deep(ol) {
  counter-reset: list-counter;
  background-color: #fff0f5;
}

.article-content :deep(ol li)::before {
  content: counter(list-counter);
  counter-increment: list-counter;
  position: absolute;
  left: 12px;
  top: 16px;
  background-color: #ff69b4;
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  box-shadow: 0 2px 6px rgba(255, 105, 180, 0.4);
}

/* 强调文本样式优化 */
.article-content :deep(strong) {
  color: #ff69b4;
  font-weight: 700;
  background-color: rgba(255, 105, 180, 0.1);
  padding: 2px 8px;
  border-radius: 6px;
  margin: 0 2px;
  box-shadow: 0 2px 4px rgba(255, 105, 180, 0.2);
}

/* 粗体和斜体组合样式 */
.article-content :deep(strong em),
.article-content :deep(em strong) {
  background-color: rgba(255, 154, 158, 0.2);
  color: #ff1493;
  border-radius: 6px;
  padding: 3px 10px;
  font-style: italic;
}

/* 文本链接样式优化 */
.article-content :deep(a) {
  color: #ff9a9e;
  text-decoration: none;
  border-bottom: 2px solid #ff9a9e;
  padding-bottom: 1px;
  transition: all 0.3s ease;
  font-weight: 500;
}

.article-content :deep(a:hover) {
  color: #ff69b4;
  background-color: rgba(255, 105, 180, 0.1);
  border-bottom-color: #ff69b4;
  padding: 2px 6px;
  border-radius: 4px;
}

/* 引用样式 */
.article-content :deep(blockquote) {
  margin: 25px 0;
  padding: 16px 20px;
  background-color: #fafafa;
  border-radius: 8px;
  font-style: normal;
  color: #666;
}

/* 分隔线样式 */
.article-content :deep(hr) {
  border: none;
  height: 1px;
  background: linear-gradient(90deg, transparent, #fecfef, transparent);
  margin: 40px 0;
}

/* 小红书风格自定义类样式 - 优化版本 */
.article-content :deep(.xiaohongshu-title) {
  font-size: 26px;
  font-weight: 700;
  margin: 45px 0 25px;
  color: #333;
  padding: 14px 24px;
  background: linear-gradient(45deg, #fff5f5, #ffffff);
  border-radius: 12px;
  border-left: 4px solid #ff9a9e;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 4px 15px rgba(255, 154, 158, 0.1);
}

.article-content :deep(.xiaohongshu-subtitle) {
  font-size: 22px;
  font-weight: 600;
  margin: 38px 0 20px;
  color: #444;
  padding: 12px 20px;
  background: linear-gradient(45deg, #fef0f5, #ffffff);
  border-radius: 10px;
  border-left: 3px solid #fecfef;
  display: flex;
  align-items: center;
  gap: 10px;
}

.article-content :deep(.xiaohongshu-list-item) {
  margin-bottom: 22px;
  text-align: left;
  color: #444;
  font-size: 16px;
  padding-left: 40px;
  line-height: 2.0;
  position: relative;
}

.article-content :deep(.xiaohongshu-list-item::before) {
  content: '🎀';
  position: absolute;
  left: 8px;
  top: 4px;
  color: #ff69b4;
  font-size: 18px;
}

.article-content :deep(.xiaohongshu-quote) {
  margin: 30px 0;
  padding: 22px 28px;
  background: linear-gradient(135deg, #fff0f5, #ffffff);
  border-radius: 12px;
  font-style: normal;
  color: #555;
  font-size: 16px;
  line-height: 2.1;
  border-left: 4px solid #ff9a9e;
  box-shadow: 0 4px 15px rgba(255, 154, 158, 0.08);
}

.article-content :deep(.xiaohongshu-paragraph) {
  margin-bottom: 32px;
  text-align: left;
  color: #555;
  font-size: 16px;
  line-height: 2.2;
  text-indent: 2em;
  padding: 0 8px;
}

.article-content :deep(.xiaohongshu-highlight) {
  color: #ff69b4;
  font-weight: 700;
  background-color: rgba(255, 105, 180, 0.15);
  padding: 3px 10px;
  border-radius: 6px;
  margin: 0 3px;
  box-shadow: 0 2px 6px rgba(255, 105, 180, 0.2);
}

.article-content :deep(.xiaohongshu-pink) {
  color: #ff69b4;
  font-weight: 700;
  background-color: rgba(255, 105, 180, 0.1);
  padding: 2px 8px;
  border-radius: 5px;
}

.article-content :deep(.xiaohongshu-bow) {
  color: #ff1493;
  font-weight: 700;
  background: linear-gradient(45deg, #fff5f5, #ffe4e1);
  padding: 4px 12px;
  border-radius: 8px;
  border: 1px solid #ffb6c1;
  box-shadow: 0 2px 8px rgba(255, 105, 180, 0.2);
  margin: 0 5px;
}

/* 文章操作区 */
.article-actions {
  display: flex;
  gap: 15px;
  margin-bottom: 40px;
  padding: 25px;
  background-color: var(--bg-primary);
  border-radius: 16px;
  box-shadow: var(--shadow-medium);
  flex-wrap: wrap;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border: 2px solid var(--border-color);
  background-color: var(--bg-secondary);
  border-radius: 28px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  color: var(--text-secondary);
  box-shadow: var(--shadow-light);
}

.action-btn:hover {
  background-color: var(--bg-primary);
  transform: translateY(-2px);
  box-shadow: var(--shadow-medium);
}

.action-btn.active {
  border-color: var(--primary-color);
  color: var(--primary-color);
  background-color: var(--bg-secondary);
}

.like-btn:hover, .like-btn.active {
  border-color: var(--accent-color);
  color: var(--accent-color);
}

.share-btn:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.collect-btn:hover, .collect-btn.active {
  border-color: var(--secondary-color);
  color: var(--secondary-color);
}

/* 相关推荐 */
.related-content {
  margin-top: 40px;
}

.related-title {
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 25px;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 10px;
}

.related-icon {
  font-size: 24px;
  color: var(--primary-color);
}

.related-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 25px;
}

.related-item {
  padding: 25px;
  background-color: var(--bg-primary);
  border-radius: 16px;
  box-shadow: var(--shadow-medium);
  transition: all 0.3s ease;
  border-left: 4px solid var(--primary-color);
  position: relative;
  overflow: hidden;
}

.related-item::before {
  content: "📚";
  position: absolute;
  top: 15px;
  right: 15px;
  font-size: 24px;
  opacity: 0.1;
  transform: rotate(15deg);
}

.related-item:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-large);
}

.related-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.related-item-header {
  margin-bottom: 12px;
}

.related-item-category {
  font-size: 12px;
  color: var(--primary-color);
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
  background-color: var(--bg-secondary);
  padding: 4px 10px;
  border-radius: 12px;
  width: fit-content;
}

.related-item-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 10px;
  color: var(--text-primary);
  line-height: 1.4;
}

.related-item-summary {
  font-size: 14px;
  line-height: 1.5;
  color: var(--text-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

/* 响应式设计 */
@media (max-width: 992px) {
  .article-title {
    font-size: 28px;
  }
  
  .article-content {
    padding: 25px;
  }
  
  .article-content :deep(h2) {
    font-size: 22px;
  }
  
  .related-list {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
  }
  
  .theme-decoration {
    gap: 20px;
  }
  
  .decoration-icon {
    font-size: 28px;
  }
}

@media (max-width: 768px) {
  .article-header {
    padding: 20px;
  }
  
  .article-title {
    font-size: 24px;
  }
  
  .article-meta {
    gap: 10px;
  }
  
  .article-content {
    padding: 20px;
    font-size: 15px;
  }
  
  .article-content :deep(h2) {
    font-size: 20px;
  }
  
  .article-actions {
    gap: 10px;
    padding: 20px;
  }
  
  .action-btn {
    padding: 10px 20px;
    font-size: 13px;
  }
  
  .related-title {
    font-size: 20px;
  }
  
  .related-list {
    grid-template-columns: 1fr;
    gap: 18px;
  }
  
  .related-item {
    padding: 20px;
  }
  
  .theme-decoration {
    gap: 15px;
  }
  
  .decoration-icon {
    font-size: 24px;
  }
}

@media (max-width: 480px) {
  .article-title {
    font-size: 20px;
  }
  
  .article-summary {
    font-size: 14px;
  }
  
  .article-content {
    font-size: 14px;
  }
  
  .article-content :deep(h2) {
    font-size: 18px;
  }
  
  .action-btn {
    padding: 8px 16px;
    font-size: 12px;
  }
  
  .related-item-title {
    font-size: 15px;
  }
}
</style>