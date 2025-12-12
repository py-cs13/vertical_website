<template>
  <button 
    class="btn"
    :class="[
      `btn-${variant}`,
      `btn-${size}`,
      { 'btn-block': block },
      { 'btn-disabled': disabled },
      { 'btn-loading': loading }
    ]"
    :disabled="disabled || loading"
    @click="$emit('click', $event)"
  >
    <div v-if="loading" class="btn-loading-spinner"></div>
    <slot></slot>
  </button>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

// 定义组件属性
const props = defineProps({
  // 按钮变体：primary, secondary, success, danger, warning, info
  variant: {
    type: String,
    default: 'primary'
  },
  // 按钮尺寸：small, medium, large
  size: {
    type: String,
    default: 'medium'
  },
  // 是否禁用
  disabled: {
    type: Boolean,
    default: false
  },
  // 是否显示加载状态
  loading: {
    type: Boolean,
    default: false
  },
  // 是否块级显示
  block: {
    type: Boolean,
    default: false
  }
})

// 定义事件
const emit = defineEmits(['click'])
</script>

<style scoped>
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-weight: 600;
  text-align: center;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: inherit;
  outline: none;
  position: relative;
  overflow: hidden;
}

/* 按钮变体 */
.btn-primary {
  background-color: var(--primary-color);
  color: white;
  box-shadow: var(--shadow-medium);
}

.btn-primary:hover:not(:disabled):not(.btn-loading) {
  background-color: #FF4785;
  transform: translateY(-2px);
  box-shadow: var(--shadow-large);
}

.btn-secondary {
  background-color: var(--bg-secondary);
  color: var(--text-primary);
  border: 2px solid var(--border-color);
}

.btn-secondary:hover:not(:disabled):not(.btn-loading) {
  background-color: var(--bg-primary);
  border-color: var(--primary-color);
}

.btn-success {
  background-color: #4CAF50;
  color: white;
  box-shadow: var(--shadow-medium);
}

.btn-success:hover:not(:disabled):not(.btn-loading) {
  background-color: #45a049;
  transform: translateY(-2px);
  box-shadow: var(--shadow-large);
}

.btn-danger {
  background-color: #F44336;
  color: white;
  box-shadow: var(--shadow-medium);
}

.btn-danger:hover:not(:disabled):not(.btn-loading) {
  background-color: #da190b;
  transform: translateY(-2px);
  box-shadow: var(--shadow-large);
}

.btn-warning {
  background-color: #FF9800;
  color: white;
  box-shadow: var(--shadow-medium);
}

.btn-warning:hover:not(:disabled):not(.btn-loading) {
  background-color: #fb8c00;
  transform: translateY(-2px);
  box-shadow: var(--shadow-large);
}

.btn-info {
  background-color: #2196F3;
  color: white;
  box-shadow: var(--shadow-medium);
}

.btn-info:hover:not(:disabled):not(.btn-loading) {
  background-color: #1976D2;
  transform: translateY(-2px);
  box-shadow: var(--shadow-large);
}

/* 按钮尺寸 */
.btn-small {
  padding: 8px 16px;
  font-size: 14px;
  min-width: 80px;
  max-width: 100%;
  word-wrap: break-word;
  white-space: normal;
  line-height: 1.4;
}

.btn-medium {
  padding: 10px 20px;
  font-size: 16px;
  min-width: 100px;
  max-width: 100%;
  word-wrap: break-word;
  white-space: normal;
  line-height: 1.4;
}

.btn-large {
  padding: 12px 24px;
  font-size: 18px;
  min-width: 120px;
  max-width: 100%;
  word-wrap: break-word;
  white-space: normal;
  line-height: 1.4;
}

/* 块级按钮 */
.btn-block {
  width: 100%;
  display: flex;
}

/* 禁用状态 */
.btn-disabled,
.btn[disabled] {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: none !important;
}

/* 加载状态 */
.btn-loading {
  cursor: wait;
}

.btn-loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s linear infinite;
}

/* 深色按钮的加载动画 */
.btn-secondary .btn-loading-spinner {
  border-color: rgba(0, 0, 0, 0.1);
  border-top-color: var(--text-primary);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>