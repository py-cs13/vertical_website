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
            <i class="icon">👁️</i> {{ formatNumber(article.views) }}
          </span>
          <span class="meta-item">
            <i class="icon">❤️</i> {{ formatNumber(article.likes) }}
          </span>
        </div>
        <div class="article-summary">{{ article.summary }}</div>
      </div>
      
      <!-- 文章正文 -->
      <div class="article-content">
        <!-- 使用 v-html 渲染富文本内容 -->
        <div v-html="article.content"></div>
      </div>
      
      <!-- 文章操作区 -->
      <div class="article-actions">
        <Button 
          variant="secondary" 
          size="medium" 
          @click="toggleLike"
          :class="{ 'active': article.liked, 'like-btn': true }"
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
import { useRoute, useRouter } from 'vue-router'
import { useContentStore } from '../stores'
import Button from '../components/Button.vue'
import { formatDate, formatNumber } from '../utils/formatters'

const route = useRoute()
const router = useRouter()
const contentStore = useContentStore()
const articleId = parseInt(route.params.id)
const loading = ref(true)

// 文章详情
const article = ref({
  id: articleId,
  title: '',
  category: '',
  summary: '',
  content: '',
  created_at: '',
  views: 0,
  likes: 0,
  liked: false,
  collected: false
})

// 相关推荐
const relatedArticles = ref([
  { id: 2, title: '如何科学安排孕期饮食', category: '营养辅食', summary: '孕期饮食对胎儿发育至关重要，本文将为您介绍科学的孕期饮食安排。' },
  { id: 3, title: '新生儿护理的10个关键要点', category: '婴儿护理', summary: '新手父母必看，掌握这些新生儿护理技巧，让宝宝健康成长。' },
  { id: 4, title: '亲子互动游戏推荐（0-1岁）', category: '亲子互动', summary: '通过简单的互动游戏，促进宝宝的智力和情感发展。' },
  { id: 5, title: '产后恢复的正确方法', category: '产后恢复', summary: '科学的产后恢复计划，帮助新妈妈快速恢复身体健康。' },
  { id: 6, title: '宝宝辅食添加时间表', category: '营养辅食', summary: '了解宝宝不同阶段的辅食添加建议，让宝宝营养均衡成长。' },
  { id: 7, title: '婴儿睡眠习惯培养指南', category: '婴儿护理', summary: '帮助宝宝建立良好的睡眠习惯，让全家都能睡个好觉。' }
])

// 获取分类对应的图标
const getCategoryIcon = (categoryName) => {
  const iconMap = {
    '婴儿护理': '👶',
    '育儿知识': '📚',
    '营养辅食': '🍼',
    '产后恢复': '🤰',
    '亲子互动': '👨‍👩‍👧',
    '成长发育': '🌱',
    '健康养生': '💊',
    '母婴育儿': '👪'
  }
  return iconMap[categoryName] || '📖'
}

// 加载文章详情
onMounted(async () => {
  loading.value = true
  try {
    // 尝试从store获取文章详情
    const articleData = await contentStore.fetchArticleDetail(articleId)
    if (articleData) {
      article.value = {
        ...articleData,
        liked: false,
        collected: false
      }
    } else {
      // 如果store没有数据，使用模拟数据
      article.value = {
        id: articleId,
        title: '新生儿护理的10个重要技巧',
        category: '婴儿护理',
        summary: '作为新手父母，掌握正确的新生儿护理技巧至关重要。本文将为您介绍10个关键的护理要点，帮助您更好地照顾宝宝。',
        content: `
          <p>欢迎阅读这篇关于新生儿护理的文章！作为新手父母，照顾刚出生的宝宝可能会感到紧张和不知所措。别担心，只要掌握了一些基本的护理知识和技巧，您就能成为一位出色的父母。</p>
          
          <h2>1. 正确的抱姿</h2>
          <p>新生儿的颈部肌肉还没有发育完全，所以抱宝宝时一定要支撑好他的头部和颈部。可以使用"摇篮抱"或者"足球抱"的方式，确保宝宝感到安全和舒适。</p>
          
          <h2>2. 脐带护理</h2>
          <p>新生儿的脐带需要保持清洁和干燥，直到自然脱落（通常需要1-2周时间）。每天用酒精棉擦拭脐带根部，避免感染。</p>
          
          <h2>3. 洗澡时间</h2>
          <p>给新生儿洗澡时，水温要控制在37-38℃左右。可以使用专门的婴儿浴盆，注意不要让水进入宝宝的耳朵和眼睛。洗澡时间不宜过长，5-10分钟即可。</p>
          
          <h2>4. 睡眠安全</h2>
          <p>为了降低SIDS（婴儿猝死综合征）的风险，建议让宝宝仰卧睡觉，避免使用过软的床垫和枕头。宝宝的睡眠环境要保持安静和舒适。</p>
          
          <h2>5. 喂养技巧</h2>
          <p>无论是母乳喂养还是配方奶喂养，都要注意正确的姿势和频率。新生儿通常每2-3小时需要喂一次奶，每次喂养时间在15-20分钟左右。</p>
          
          <h2>6. 换尿布</h2>
          <p>及时更换尿布可以预防尿布疹的发生。换尿布时要用温水清洗宝宝的臀部，然后擦干，必要时可以涂抹护臀霜。</p>
          
          <h2>7. 体温监测</h2>
          <p>新生儿的体温调节能力较弱，所以要经常监测宝宝的体温。正常体温范围在36.5-37.5℃之间。</p>
          
          <h2>8. 哭闹安抚</h2>
          <p>新生儿哭闹是表达需求的方式，可能是饿了、累了、尿布湿了或者需要安抚。可以尝试轻轻摇晃、抚摸或者唱歌来安抚宝宝。</p>
          
          <h2>9. 疫苗接种</h2>
          <p>按照医生的建议，及时为宝宝接种疫苗，预防各种传染病。</p>
          
          <h2>10. 观察异常情况</h2>
          <p>要密切观察宝宝的身体状况，如果出现发热、呕吐、腹泻、呼吸急促等异常情况，要及时就医。</p>
          
          <p>希望这些护理技巧能够帮助您更好地照顾宝宝！记住，每个宝宝都是独特的，您需要根据自己宝宝的情况调整护理方式。如果有任何疑问，不要犹豫，及时咨询医生或专业人士。</p>
        `,
        created_at: '2024-06-03',
        views: 1567,
        likes: 123,
        liked: false,
        collected: false
      }
    }
  } catch (error) {
    console.error('Failed to load article:', error)
  } finally {
    loading.value = false
  }
})

// 切换点赞状态
const toggleLike = () => {
  article.value.liked = !article.value.liked
  article.value.likes += article.value.liked ? 1 : -1
}

// 切换收藏状态
const toggleCollect = () => {
  article.value.collected = !article.value.collected
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

/* 文章头部信息 */
.article-header {
  margin-bottom: 40px;
  padding-bottom: 25px;
  border-bottom: 2px solid var(--border-color);
  background-color: var(--bg-primary);
  padding: 25px;
  border-radius: 16px;
  box-shadow: var(--shadow-medium);
  position: relative;
  overflow: hidden;
}

.article-header::before {
  content: "👶";
  position: absolute;
  top: 15px;
  right: 15px;
  font-size: 40px;
  opacity: 0.1;
  transform: rotate(15deg);
}

.article-category {
  font-size: 14px;
  color: var(--primary-color);
  font-weight: 600;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  background-color: var(--bg-secondary);
  padding: 6px 12px;
  border-radius: 15px;
  width: fit-content;
}

.category-icon {
  font-size: 16px;
}

.article-title {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 20px;
  line-height: 1.3;
  color: var(--text-primary);
}

.article-meta {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  font-size: 14px;
  color: var(--text-light);
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  background-color: var(--bg-secondary);
  padding: 4px 12px;
  border-radius: 12px;
}

.article-summary {
  font-size: 16px;
  line-height: 1.7;
  color: var(--text-secondary);
  background-color: var(--bg-secondary);
  padding: 18px;
  border-radius: 12px;
  border-left: 4px solid var(--primary-color);
}

/* 文章正文 */
.article-content {
  margin-bottom: 40px;
  font-size: 16px;
  line-height: 1.8;
  color: var(--text-primary);
  background-color: var(--bg-primary);
  padding: 30px;
  border-radius: 16px;
  box-shadow: var(--shadow-medium);
}

.article-content h2 {
  font-size: 24px;
  font-weight: 600;
  margin: 35px 0 20px;
  color: var(--primary-color);
  padding-bottom: 8px;
  border-bottom: 2px solid var(--border-color);
}

.article-content h2:first-child {
  margin-top: 0;
}

.article-content p {
  margin-bottom: 25px;
  text-align: justify;
}

.article-content ul, .article-content ol {
  margin-left: 25px;
  margin-bottom: 25px;
  padding-left: 10px;
}

.article-content li {
  margin-bottom: 12px;
  padding-left: 8px;
}

.article-content ul li::marker {
  color: var(--primary-color);
  font-size: 18px;
}

.article-content ol li::marker {
  color: var(--primary-color);
  font-weight: 600;
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
  
  .article-content h2 {
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
  
  .article-content h2 {
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
  
  .article-content h2 {
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