<template>
  <div class="simple-articles-view">
    
    <!-- 文章列表 -->
    <div class="articles-list">
      <div 
        v-for="article in displayedArticles" 
        :key="article.id" 
        class="article-item"
      >
        <h3>{{ article.title }}</h3>
        <p>{{ article.summary }}</p>
        <button @click="navigateToArticle(article.id)">阅读全文</button>
      </div>
    </div>
    
    <!-- 生产环境不显示调试信息 -->
    
    <!-- 加载更多按钮 -->
    <button 
      @click="displayedCount += 4" 
      class="load-more-btn"
      :disabled="displayedArticles.length >= articles.length"
    >
      加载更多
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const articles = ref([])
const displayedCount = ref(6)

// 计算当前显示的文章
const displayedArticles = computed(() => {
  return articles.value.slice(0, displayedCount.value)
})

// 获取所有文章
const fetchArticles = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/articles')
    articles.value = response.data.data || response.data || []
    // 文章获取完成
  } catch (error) {
    // 文章获取失败
    articles.value = []
  }
}

// 导航到文章详情
const navigateToArticle = (id) => {
  router.push(`/article/${id}`)
}

// 页面挂载时获取文章
onMounted(() => {
  fetchArticles()
})
</script>

<style scoped>
.simple-articles-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.articles-list {
  margin-bottom: 20px;
}

.article-item {
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.load-more-btn {
  display: block;
  margin: 20px auto;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
}

.load-more-btn:hover {
  background-color: #45a049;
}

.load-more-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>