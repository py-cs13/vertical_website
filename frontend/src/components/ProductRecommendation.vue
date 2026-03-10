<template>
  <div class="product-recommendation">
    <div class="recommendation-header">
      <span class="header-icon">🛍️</span>
      <h3 class="header-title">精选推荐</h3>
    </div>
    
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>
    
    <div v-else-if="products.length === 0" class="empty-state">
      <div class="empty-icon">📦</div>
      <p>暂无推荐商品</p>
    </div>
    
    <div v-else class="products-container" :class="`layout-${layout}`">
      <div 
        v-for="product in products" 
        :key="product.id" 
        class="product-card"
      >
        <a 
          :href="product.link_url" 
          target="_blank" 
          rel="noopener noreferrer"
          class="product-link"
          @click="handleProductClick(product.id)"
        >
          <div class="product-image">
            <img :src="product.image_url" :alt="product.name">
          </div>
          
          <div class="product-info">
            <h4 class="product-name">{{ product.name }}</h4>
            <p v-if="product.description" class="product-description">
              {{ product.description }}
            </p>
            <div class="product-footer">
              <span class="product-price">¥{{ product.price }}</span>
              <span class="product-action">立即购买 →</span>
            </div>
          </div>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import apiClient from '../utils/api'

const props = defineProps({
  category: {
    type: String,
    default: null
  },
  articleId: {
    type: Number,
    default: null
  },
  mode: {
    type: String,
    default: 'category',
    validator: (value) => ['category', 'ai', 'history'].includes(value)
  },
  limit: {
    type: Number,
    default: 2
  },
  layout: {
    type: String,
    default: 'list',
    validator: (value) => ['list', 'grid'].includes(value)
  }
})

const products = ref([])
const loading = ref(true)

const loadProducts = async () => {
  try {
    loading.value = true
    
    if (props.mode === 'ai' && props.articleId) {
      const response = await apiClient.get('/products/recommend-by-content', {
        params: {
          article_id: props.articleId,
          limit: props.limit
        }
      })
      products.value = response.data
    } else if (props.mode === 'history') {
      const response = await apiClient.get('/products/recommend-by-history', {
        params: {
          limit: props.limit
        }
      })
      products.value = response.data
    } else {
      const response = await apiClient.get('/products/recommend', {
        params: {
          category: props.category || '育儿用品',
          limit: props.limit
        }
      })
      products.value = response.data
    }
  } catch (error) {
    console.error('加载推荐商品失败:', error)
    products.value = []
  } finally {
    loading.value = false
  }
}

const handleProductClick = async (productId) => {
  try {
    await apiClient.post(`/products/${productId}/click`)
  } catch (error) {
    console.error('记录商品点击失败:', error)
  }
}

onMounted(() => {
  loadProducts()
})

watch(() => props.articleId, () => {
  if (props.mode === 'ai' && props.articleId) {
    loadProducts()
  }
})

watch(() => props.category, (newCategory) => {
  if (newCategory) {
    loadProducts()
  }
})
</script>

<style scoped>
.product-recommendation {
  background-color: var(--bg-secondary);
  border-radius: 10px;
  padding: 15px;
  box-shadow: var(--shadow-light);
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.product-recommendation:hover {
  box-shadow: var(--shadow-medium);
  transform: translateY(-2px);
}

.recommendation-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 2px solid var(--bg-accent);
}

.header-icon {
  font-size: 18px;
}

.header-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--primary-color);
  margin: 0;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 30px 15px;
  gap: 10px;
}

.loading-spinner {
  width: 30px;
  height: 30px;
  border: 3px solid var(--bg-accent);
  border-top: 3px solid var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-container p {
  font-size: 13px;
  color: var(--text-secondary);
  margin: 0;
}

.empty-state {
  text-align: center;
  padding: 30px 15px;
  color: var(--text-secondary);
}

.empty-icon {
  font-size: 36px;
  margin-bottom: 10px;
  opacity: 0.5;
}

.empty-state p {
  font-size: 13px;
  margin: 0;
}

.products-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.products-container.layout-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
}

.product-card {
  border-radius: 10px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.product-card:hover {
  transform: translateY(-2px);
}

.product-link {
  display: block;
  text-decoration: none;
  color: inherit;
  background-color: white;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.product-link:hover {
  border-color: var(--primary-color);
  box-shadow: var(--shadow-light);
}

.product-image {
  width: 100%;
  height: 140px;
  overflow: hidden;
  background-color: #fafafa;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.product-link:hover .product-image img {
  transform: scale(1.05);
}

.product-info {
  padding: 12px;
}

.product-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 6px 0;
  line-height: 1.4;
}

.product-description {
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.5;
  margin: 0 0 10px 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 10px;
  border-top: 1px solid var(--border-color);
}

.product-price {
  font-size: 16px;
  font-weight: 700;
  color: var(--accent-color);
}

.product-action {
  font-size: 12px;
  font-weight: 500;
  color: var(--primary-color);
  transition: color 0.3s ease;
}

.product-link:hover .product-action {
  color: var(--accent-color);
}

/* 响应式设计 */
@media (max-width: 992px) {
  .product-image {
    height: 120px;
  }
  
  .product-name {
    font-size: 13px;
  }
  
  .product-description {
    font-size: 11px;
  }
  
  .product-price {
    font-size: 15px;
  }
}

@media (max-width: 768px) {
  .product-image {
    height: 160px;
  }
  
  .product-name {
    font-size: 14px;
  }
  
  .product-description {
    font-size: 12px;
  }
  
  .product-price {
    font-size: 16px;
  }
}
</style>