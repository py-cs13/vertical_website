<template>
  <div class="toolkit-detail">
    <!-- 工具包头部信息 -->
    <div class="toolkit-header">
      <div class="toolkit-category">{{ toolkit.category }}</div>
      <h1 class="toolkit-title">{{ toolkit.title }}</h1>
      <div class="toolkit-meta">
        <span class="meta-item">
          <i class="icon">📅</i> {{ formatDate(toolkit.created_at) }}
        </span>
        <span class="meta-item">
          <i class="icon">👁️</i> {{ formatNumber(toolkit.views) }}
        </span>
        <span class="meta-item">
          <i class="icon">❤️</i> {{ formatNumber(toolkit.likes) }}
        </span>
      </div>
      <div class="toolkit-summary">{{ toolkit.summary }}</div>
      
      <!-- 价格和购买按钮 -->
      <div class="toolkit-price-section">
        <div class="price-info">
          <span class="current-price">¥{{ toolkit.price }}</span>
          <span v-if="toolkit.original_price" class="original-price">¥{{ toolkit.original_price }}</span>
        </div>
        <Button variant="primary" size="large" @click="buyNow" class="buy-now-btn">立即购买</Button>
        <Button variant="secondary" size="large" @click="addToCart" class="add-cart-btn">加入购物车</Button>
      </div>
    </div>
    
    <!-- 工具包详情内容 -->
    <div class="toolkit-content">
      <!-- 使用 v-html 渲染富文本内容 -->
      <div v-html="toolkit.content"></div>
    </div>
    
    <!-- 工具包包含内容 -->
    <div class="toolkit-includes">
      <h3 class="section-title">工具包包含</h3>
      <ul class="includes-list">
        <li v-for="(item, index) in toolkit.includes" :key="index" class="include-item">
          <i class="icon">✅</i> {{ item }}
        </li>
      </ul>
    </div>
    
    <!-- 用户评价 -->
    <div class="toolkit-reviews">
      <h3 class="section-title">用户评价</h3>
      <div class="reviews-list">
        <div v-for="review in toolkit.reviews" :key="review.id" class="review-item">
          <div class="review-header">
            <span class="reviewer-name">{{ review.user_name }}</span>
            <div class="review-rating">
              <span v-for="star in 5" :key="star" class="star">
                {{ star <= review.rating ? '⭐' : '☆' }}
              </span>
            </div>
            <span class="review-date">{{ formatDate(review.created_at) }}</span>
          </div>
          <p class="review-content">{{ review.content }}</p>
        </div>
      </div>
    </div>
    
    <!-- 相关推荐 -->
    <div class="related-content">
      <h3 class="related-title">相关推荐</h3>
      <div class="related-list">
        <div 
          v-for="item in relatedToolkits" 
          :key="item.id" 
          class="related-item"
        >
          <router-link :to="`/toolkit/${item.id}`" class="related-link">
            <h4 class="related-item-title">{{ item.title }}</h4>
            <p class="related-item-summary">{{ item.summary }}</p>
            <div class="related-item-price">¥{{ item.price }}</div>
          </router-link>
        </div>
      </div>
    </div>
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
const toolkitId = parseInt(route.params.id)

// 工具包详情
const toolkit = ref({
  id: toolkitId,
  title: '',
  category: '',
  summary: '',
  content: '',
  created_at: '',
  views: 0,
  likes: 0,
  price: 0,
  original_price: 0,
  includes: [],
  reviews: []
})

// 相关推荐
const relatedToolkits = ref([
  { id: 2, title: '新生儿护理工具包', summary: '全面的新生儿护理知识和实用工具', price: 19.9 },
  { id: 3, title: '减肥健身计划工具包', summary: '科学的减肥健身计划和饮食指导', price: 29.9 },
  { id: 4, title: '营养膳食搭配工具包', summary: '健康营养的膳食搭配方案', price: 15.9 }
])

// 加载工具包详情
onMounted(() => {
  // 在实际项目中，这里会调用API获取工具包详情
  // contentStore.fetchToolkitDetail(toolkitId)
  
  // 模拟数据
  toolkit.value = {
    id: toolkitId,
    title: '家庭健康管理工具包',
    category: '健康养生',
    summary: '全面的家庭健康管理知识和实用工具，帮助您管理家人的健康。',
    content: `
      <p>家庭健康管理是现代生活中非常重要的一部分，一个好的家庭健康管理工具包可以帮助您更好地照顾家人的健康。</p>
      
      <h2>工具包特点</h2>
      <p>本工具包包含了丰富的家庭健康管理资源，包括：</p>
      <ul>
        <li>家庭健康档案模板</li>
        <li>常见疾病预防指南</li>
        <li>家庭急救知识手册</li>
        <li>儿童生长发育监测表</li>
        <li>老年人健康管理指南</li>
      </ul>
      
      <h2>使用方法</h2>
      <p>1. 下载工具包中的所有资源文件</p>
      <p>2. 按照说明填写家庭健康档案</p>
      <p>3. 根据指南制定家庭健康计划</p>
      <p>4. 定期更新健康数据，监测家人健康状况</p>
      
      <h2>适用人群</h2>
      <p>本工具包适合所有关注家庭健康的人群，特别是有老人和儿童的家庭。</p>
    `,
    created_at: '2025-01-10',
    views: 892,
    likes: 67,
    price: 9.9,
    original_price: 99,
    includes: [
      '家庭健康档案Excel模板',
      '常见疾病预防指南PDF',
      '家庭急救知识手册PDF',
      '儿童生长发育监测表Excel',
      '老年人健康管理指南PDF',
      '家庭健康管理视频教程'
    ],
    reviews: [
      { id: 1, user_name: '健康达人', rating: 5, created_at: '2025-01-12', content: '工具包非常实用，包含了很多有用的健康管理资源。' },
      { id: 2, user_name: '快乐妈妈', rating: 4, created_at: '2025-01-11', content: '儿童生长发育监测表很实用，帮助我更好地了解孩子的成长情况。' },
      { id: 3, user_name: '爱心爸爸', rating: 5, created_at: '2025-01-10', content: '家庭急救知识手册很全面，值得购买。' }
    ]
  }
})

// 购买按钮点击事件
const buyNow = () => {
  // 跳转到支付页面
  router.push({
    name: 'payment',
    query: {
      product_type: 'toolkit',
      product_id: toolkit.value.id,
      product_name: toolkit.value.title,
      price: toolkit.value.price
    }
  })
}



// 加入购物车
const addToCart = () => {
  // 实际项目中这里会调用加入购物车API
  alert('已加入购物车')
}
</script>

<style scoped>
/* 主题装饰 */
.theme-decoration {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-bottom: 20px;
}

.decoration-icon {
  font-size: 32px;
  animation: float 3s ease-in-out infinite;
  filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1));
  transform: rotate(-10deg);
}

.decoration-icon:nth-child(2) {
  font-size: 36px;
  animation-delay: 0.5s;
  transform: rotate(0deg);
}

.decoration-icon:nth-child(3) {
  font-size: 30px;
  animation-delay: 1s;
  transform: rotate(10deg);
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

/* 工具包头部信息 */
.toolkit-header {
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

.toolkit-header::before {
  content: "🎁";
  position: absolute;
  top: 15px;
  right: 15px;
  font-size: 40px;
  opacity: 0.1;
  transform: rotate(15deg);
}

.toolkit-category {
  font-size: 14px;
  color: var(--accent-color);
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

.toolkit-title {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 20px;
  line-height: 1.3;
  color: var(--text-primary);
}

.toolkit-meta {
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

.toolkit-summary {
  font-size: 16px;
  line-height: 1.7;
  color: var(--text-secondary);
  background-color: var(--bg-secondary);
  padding: 18px;
  border-radius: 12px;
  border-left: 4px solid var(--accent-color);
  margin-bottom: 30px;
}

/* 价格和购买按钮 */
.toolkit-price-section {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
}

.price-info {
  display: flex;
  align-items: baseline;
  gap: 10px;
}

.current-price {
  font-size: 32px;
  font-weight: 700;
  color: var(--accent-color);
}

.original-price {
  font-size: 16px;
  color: var(--text-light);
  text-decoration: line-through;
}

/* 工具包详情内容 */
.toolkit-content {
  margin-bottom: 40px;
  font-size: 16px;
  line-height: 1.8;
  color: var(--text-primary);
  background-color: var(--bg-primary);
  padding: 30px;
  border-radius: 16px;
  box-shadow: var(--shadow-medium);
}

.toolkit-content h2 {
  font-size: 24px;
  font-weight: 600;
  margin: 35px 0 20px;
  color: var(--text-primary);
  padding-bottom: 8px;
  border-bottom: 2px solid var(--border-color);
}

.toolkit-content h2:first-child {
  margin-top: 0;
}

.toolkit-content p {
  margin-bottom: 25px;
  text-align: justify;
}

.toolkit-content ul, .toolkit-content ol {
  margin-left: 25px;
  margin-bottom: 25px;
  padding-left: 10px;
}

.toolkit-content li {
  margin-bottom: 12px;
  padding-left: 8px;
}

.toolkit-content ul li::marker {
  color: var(--accent-color);
  font-size: 18px;
}

.toolkit-content ol li::marker {
  color: var(--accent-color);
  font-weight: 600;
}

/* 工具包包含内容 */
.toolkit-includes {
  margin-bottom: 40px;
  padding: 25px;
  background-color: var(--bg-primary);
  border-radius: 16px;
  box-shadow: var(--shadow-medium);
}

.section-title {
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 20px;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-icon {
  font-size: 24px;
  color: var(--accent-color);
}

.includes-list {
  list-style: none;
}

.include-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 15px;
  font-size: 15px;
  color: var(--text-secondary);
  padding: 12px;
  background-color: var(--bg-secondary);
  border-radius: 8px;
  transition: all 0.3s ease;
}

.include-item:hover {
  transform: translateX(5px);
  background-color: var(--bg-accent);
}

.include-item .icon {
  margin-top: 5px;
  color: var(--accent-color);
  font-size: 18px;
}

/* 用户评价 */
.toolkit-reviews {
  margin-bottom: 40px;
}

.reviews-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 25px;
}

.review-item {
  padding: 25px;
  background-color: var(--bg-primary);
  border-radius: 16px;
  box-shadow: var(--shadow-medium);
  transition: all 0.3s ease;
  border-left: 4px solid var(--accent-color);
}

.review-item:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-large);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  font-size: 14px;
}

.reviewer-name {
  font-weight: 600;
  color: var(--text-primary);
}

.review-rating {
  color: var(--accent-color);
  font-size: 16px;
}

.review-date {
  color: var(--text-light);
}

.review-content {
  font-size: 14px;
  line-height: 1.7;
  color: var(--text-secondary);
  background-color: var(--bg-secondary);
  padding: 15px;
  border-radius: 8px;
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
  color: var(--accent-color);
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
  transition: all 0.3s ease;
  box-shadow: var(--shadow-medium);
  border-left: 4px solid var(--accent-color);
}

.related-item:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-large);
}

.related-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.related-item-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
  color: var(--text-primary);
  line-height: 1.4;
}

.related-item-summary {
  font-size: 14px;
  line-height: 1.5;
  color: var(--text-secondary);
  margin-bottom: 15px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  background-color: var(--bg-secondary);
  padding: 10px;
  border-radius: 6px;
}

.related-item-price {
  font-size: 18px;
  font-weight: 600;
  color: var(--accent-color);
  background-color: var(--bg-secondary);
  padding: 6px 12px;
  border-radius: 12px;
  display: inline-block;
}

/* 响应式设计 */
@media (max-width: 992px) {
  .toolkit-title {
    font-size: 28px;
  }
  
  .toolkit-content {
    padding: 25px;
  }
  
  .toolkit-content h2 {
    font-size: 22px;
  }
  
  .reviews-list {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
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
  .toolkit-header {
    padding: 20px;
  }
  
  .toolkit-title {
    font-size: 24px;
  }
  
  .toolkit-meta {
    gap: 10px;
  }
  
  .toolkit-price-section {
    gap: 15px;
  }
  
  .current-price {
    font-size: 28px;
  }
  
  .toolkit-content {
    padding: 20px;
    font-size: 15px;
  }
  
  .toolkit-content h2 {
    font-size: 20px;
  }
  
  .toolkit-includes {
    padding: 20px;
  }
  
  .section-title {
    font-size: 20px;
  }
  
  .reviews-list {
    grid-template-columns: 1fr;
    gap: 18px;
  }
  
  .review-item {
    padding: 20px;
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
  .toolkit-title {
    font-size: 20px;
  }
  
  .toolkit-summary {
    font-size: 14px;
  }
  
  .toolkit-content {
    font-size: 14px;
  }
  
  .toolkit-content h2 {
    font-size: 18px;
  }
  
  .section-title {
    font-size: 18px;
  }
  
  .related-item-title {
    font-size: 15px;
  }
}
</style>