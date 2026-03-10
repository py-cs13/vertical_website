<template>
  <div class="products-view">
    <div v-if="showProductRecommendations" class="container">
      <div class="page-header">
        <h1 class="page-title">精选好物</h1>
        <p class="page-subtitle">为您推荐优质的母婴用品</p>
      </div>
      
      <div class="filter-section">
        <div class="category-filter">
          <button 
            v-for="cat in categories" 
            :key="cat"
            :class="{ active: activeCategory === cat }"
            @click="filterByCategory(cat)"
            class="filter-btn"
          >
            {{ cat }}
          </button>
        </div>
        
        <div class="sort-options">
          <select v-model="sortBy" @change="loadProducts" class="sort-select">
            <option value="created_at">最新上架</option>
            <option value="price_asc">价格从低到高</option>
            <option value="price_desc">价格从高到低</option>
            <option value="click_count">最受欢迎</option>
          </select>
        </div>
      </div>
      
      <div v-if="loading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>
      
      <div v-else-if="products.length === 0" class="empty-state">
        <div class="empty-icon">📦</div>
        <p>暂无商品</p>
      </div>
      
      <div v-else class="products-grid">
        <ProductCard 
          v-for="product in products" 
          :key="product.id"
          :product="product"
        />
      </div>
      
      <div v-if="hasMore" class="load-more-container">
        <button 
          @click="loadMore"
          :disabled="loadingMore"
          class="load-more-btn"
        >
          {{ loadingMore ? '加载中...' : '加载更多' }}
        </button>
      </div>
    </div>
    
    <!-- 当商品推荐被隐藏时显示提示信息 -->
    <div v-else class="container">
      <div class="disabled-state">
        <div class="disabled-icon">🔒</div>
        <h2>精选好物功能暂未开放</h2>
        <p>我们正在优化商品推荐功能，敬请期待！</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import apiClient from '../utils/api'
import ProductCard from '../components/ProductCard.vue'

// 是否显示商品推荐（根据环境变量控制）
const showProductRecommendations = computed(() => {
  return import.meta.env.VITE_SHOW_PRODUCT_RECOMMENDATIONS === 'true'
})

const categories = ref([
  '全部',
  '孕期指南',
  '新生照顾',
  '幼儿发展',
  '亲子互动',
  '早期教育',
  '营养健康',
  '产后恢复',
  '育儿用品'
])

const activeCategory = ref('全部')
const sortBy = ref('created_at')
const products = ref([])
const loading = ref(true)
const loadingMore = ref(false)
const currentPage = ref(1)
const pageSize = ref(12)
const hasMore = ref(false)

const loadProducts = async () => {
  try {
    loading.value = true
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      sort_by: sortBy.value
    }
    
    if (activeCategory.value !== '全部') {
      params.category = activeCategory.value
    }
    
    const response = await apiClient.get('/products', { params })
    products.value = response.data.products
    hasMore.value = response.data.total > currentPage.value * pageSize.value
  } catch (error) {
    console.error('加载商品失败:', error)
    products.value = []
  } finally {
    loading.value = false
  }
}

const loadMore = async () => {
  if (loadingMore.value) return
  loadingMore.value = true
  
  try {
    currentPage.value += 1
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      sort_by: sortBy.value
    }
    
    if (activeCategory.value !== '全部') {
      params.category = activeCategory.value
    }
    
    const response = await apiClient.get('/products', { params })
    products.value = [...products.value, ...response.data.products]
    hasMore.value = response.data.total > currentPage.value * pageSize.value
  } catch (error) {
    console.error('加载更多商品失败:', error)
  } finally {
    loadingMore.value = false
  }
}

const filterByCategory = (category) => {
  activeCategory.value = category
  currentPage.value = 1
  products.value = []
  loadProducts()
}

onMounted(() => {
  loadProducts()
})
</script>

<style scoped>
.products-view {
  min-height: 100vh;
  padding: 40px 0;
  background-color: var(--bg-primary);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 10px 0;
}

.page-subtitle {
  font-size: 16px;
  color: var(--text-secondary);
  margin: 0;
}

.filter-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding: 20px;
  background-color: var(--bg-secondary);
  border-radius: 12px;
  border: 1px solid var(--border-color);
}

.category-filter {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 10px 20px;
  border: 2px solid var(--border-color);
  background-color: var(--bg-primary);
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  color: var(--text-secondary);
}

.filter-btn:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
  background-color: rgba(255, 255, 255, 0.95);
}

.filter-btn.active {
  background-color: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.sort-options {
  display: flex;
  align-items: center;
}

.sort-select {
  padding: 10px 16px;
  border: 2px solid var(--border-color);
  background-color: var(--bg-primary);
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  color: var(--text-secondary);
  transition: all 0.3s ease;
}

.sort-select:hover {
  border-color: var(--primary-color);
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  gap: 10px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--bg-accent);
  border-top: 4px solid var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-container p {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: var(--text-secondary);
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 20px;
  opacity: 0.5;
}

.empty-state p {
  font-size: 16px;
  margin: 0;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.load-more-container {
  text-align: center;
  margin-top: 30px;
}

.load-more-btn {
  padding: 12px 32px;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.load-more-btn:hover:not(:disabled) {
  background-color: var(--accent-color);
  transform: translateY(-2px);
  box-shadow: var(--shadow-medium);
}

.load-more-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 992px) {
  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 16px;
  }
  
  .filter-section {
    flex-direction: column;
    gap: 16px;
  }
  
  .category-filter {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 12px;
  }
  
  .page-title {
    font-size: 24px;
  }
  
  .page-subtitle {
    font-size: 14px;
  }
  
  .filter-btn {
    padding: 8px 16px;
    font-size: 13px;
  }
}

/* 商品推荐被隐藏时的样式 */
.disabled-state {
  text-align: center;
  padding: 80px 20px;
  background-color: var(--bg-secondary);
  border-radius: 12px;
  border: 2px dashed var(--border-color);
  margin-top: 40px;
}

.disabled-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.disabled-state h2 {
  font-size: 24px;
  color: var(--text-primary);
  margin-bottom: 10px;
}

.disabled-state p {
  font-size: 16px;
  color: var(--text-secondary);
  line-height: 1.6;
}
</style>
