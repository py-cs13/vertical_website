<template>
  <div 
    class="card"
    :class="[
      `card-${variant}`,
      `card-${size}`,
      { 'card-shadow': shadow },
      { 'card-hover': hoverable }
    ]"
  >
    <!-- Card Header -->
    <div v-if="$slots.header" class="card-header">
      <slot name="header"></slot>
    </div>
    
    <!-- Card Image -->
    <img 
      v-if="image" 
      :src="image" 
      :alt="imageAlt" 
      class="card-image"
    >
    
    <!-- Card Body -->
    <div class="card-body">
      <slot></slot>
    </div>
    
    <!-- Card Footer -->
    <div v-if="$slots.footer" class="card-footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

// 定义组件属性
const props = defineProps({
  // 卡片变体：default, outline, filled
  variant: {
    type: String,
    default: 'default'
  },
  // 卡片尺寸：small, medium, large
  size: {
    type: String,
    default: 'medium'
  },
  // 是否显示阴影
  shadow: {
    type: Boolean,
    default: true
  },
  // 是否有悬停效果
  hoverable: {
    type: Boolean,
    default: false
  },
  // 卡片图片URL
  image: {
    type: String,
    default: ''
  },
  // 卡片图片alt属性
  imageAlt: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.card {
  background-color: var(--bg-primary);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
}

/* 卡片变体 */
.card-default {
  background-color: var(--bg-primary);
  border: 1px solid var(--border-color);
}

.card-outline {
  background-color: transparent;
  border: 2px solid var(--border-color);
}

.card-filled {
  background-color: var(--bg-secondary);
  border: 1px solid var(--border-color);
}

/* 卡片尺寸 */
.card-small {
  padding: 12px;
}

.card-medium {
  padding: 16px;
}

.card-large {
  padding: 24px;
}

/* 卡片阴影 */
.card-shadow {
  box-shadow: var(--shadow-medium);
}

/* 悬停效果 */
.card-hover {
  cursor: pointer;
}

.card-hover:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-large);
}

/* 卡片头部 */
.card-header {
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 12px;
}

/* 卡片图片 */
.card-image {
  width: 100%;
  height: auto;
  object-fit: cover;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 12px;
}

/* 卡片主体 */
.card-body {
  /* 内容由插槽提供 */
}

/* 卡片底部 */
.card-footer {
  padding-top: 12px;
  border-top: 1px solid var(--border-color);
  margin-top: 12px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>