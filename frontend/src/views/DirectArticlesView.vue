<template>
  <div style="max-width: 1200px; margin: 0 auto; padding: 20px;">
    
    <!-- API状态信息 -->
    <div style="background-color: #f0f0f0; padding: 10px; margin-bottom: 20px; border-radius: 5px;">
      <p>API状态: {{ apiStatus }}</p>
      <p>获取到的文章总数: {{ allArticles.length }}</p>
      <p>当前显示的文章数: {{ displayedArticles.length }}</p>
      <p>加载步长: {{ loadStep }}</p>
    </div>
    
    <!-- 文章列表 -->
    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin-bottom: 20px;">
      <div 
        v-for="(article, index) in displayedArticles" 
        :key="article.id || index" 
        style="border: 1px solid #ddd; padding: 15px; border-radius: 5px;"
      >
        <h3 style="margin-top: 0;">{{ article.title }}</h3>
        <p>{{ article.summary }}</p>
        <button @click="navigateToArticle(article.id)" style="background-color: #FF6B8B; color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer;">
          阅读全文
        </button>
      </div>
    </div>
    
    <!-- 加载更多按钮 -->
    <div style="text-align: center;">
      <button 
        @click="loadMore"
        :disabled="loading || displayedArticles.length >= allArticles.length"
        style="background-color: #FF6B8B; color: white; border: none; padding: 10px 20px; border-radius: 25px; font-size: 16px; cursor: pointer;"
      >
        {{ loading ? '加载中...' : '加载更多' }} ({{ displayedArticles.length }} / {{ allArticles.length }})
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const allArticles = ref([])  // 存储所有文章
const displayedArticles = ref([])  // 存储当前显示的文章
const loading = ref(false)  // 加载状态
const loadStep = 6  // 每次加载6篇文章
const apiStatus = ref('未开始')  // API调用状态

// 导航到文章详情页
const navigateToArticle = (id) => {
  if (id) {
    router.push(`/article/${id}`)
  }
}

// 加载更多文章
const loadMore = () => {
  if (loading.value || displayedArticles.value.length >= allArticles.value.length) {
    return
  }
  
  // 加载更多按钮被点击
  
  loading.value = true
  
  // 模拟网络延迟
  setTimeout(() => {
    const currentLength = displayedArticles.value.length
    const newLength = currentLength + loadStep
    const newArticles = allArticles.value.slice(currentLength, newLength)
    
    displayedArticles.value = [...displayedArticles.value, ...newArticles]
    
    // 加载后显示完成
    loading.value = false
  }, 300)
}

// 从API获取所有文章
const fetchArticlesFromAPI = async () => {
  apiStatus.value = '加载中...'
  loading.value = true
  
  try {
    // 开始从API获取文章...
    const response = await axios.get('http://localhost:8000/api/articles')
    
    // 直接使用response.data，因为API返回的是文章数组
    if (Array.isArray(response.data)) {
      allArticles.value = response.data
      
      // 初始显示前6篇文章
      displayedArticles.value = allArticles.value.slice(0, loadStep)
      
      apiStatus.value = '加载成功'
    } else {
      // 处理可能的不同响应格式
      allArticles.value = response.data.data || []
      displayedArticles.value = allArticles.value.slice(0, loadStep)
      apiStatus.value = '加载成功 (格式转换)'
    }
    
  } catch (error) {
    // API调用失败
    apiStatus.value = '加载失败: ' + error.message
    allArticles.value = []
    displayedArticles.value = []
  } finally {
    loading.value = false
  }
}

// 页面加载时获取文章
onMounted(() => {
  fetchArticlesFromAPI()
})
</script>