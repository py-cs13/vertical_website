<template>
  <div class="product-card">
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
          <span class="product-category">{{ product.category }}</span>
        </div>
      </div>
    </a>
  </div>
</template>

<script setup>
import apiClient from '../utils/api'

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
})

const handleProductClick = async (productId) => {
  try {
    await apiClient.post(`/products/${productId}/click`)
  } catch (error) {
    console.error('记录商品点击失败:', error)
  }
}
</script>

<style scoped>
.product-card {
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.product-card:hover {
  transform: translateY(-5px);
}

.product-link {
  display: block;
  text-decoration: none;
  color: inherit;
  background-color: white;
  border-radius: 12px;
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
  height: 200px;
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
  padding: 16px;
}

.product-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 8px 0;
  line-height: 1.4;
}

.product-description {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
  margin: 0 0 12px 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid var(--border-color);
}

.product-price {
  font-size: 18px;
  font-weight: 700;
  color: var(--accent-color);
}

.product-category {
  font-size: 12px;
  color: var(--text-secondary);
  background-color: var(--bg-accent);
  padding: 4px 12px;
  border-radius: 12px;
}

@media (max-width: 992px) {
  .product-image {
    height: 180px;
  }
  
  .product-name {
    font-size: 15px;
  }
  
  .product-description {
    font-size: 12px;
  }
  
  .product-price {
    font-size: 16px;
  }
}

@media (max-width: 768px) {
  .product-image {
    height: 200px;
  }
  
  .product-name {
    font-size: 16px;
  }
  
  .product-description {
    font-size: 13px;
  }
  
  .product-price {
    font-size: 18px;
  }
}
</style>
