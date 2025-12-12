<template>
  <div 
    v-if="visible" 
    class="toast" 
    :class="[`toast-${type}`, { 'toast-fade-in': visible, 'toast-fade-out': !visible }]"
  >
    <div class="toast-content">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

// 定义组件属性
const props = defineProps({
  // 提示类型：success, error, warning, info
  type: {
    type: String,
    default: 'success'
  },
  // 显示时长（毫秒）
  duration: {
    type: Number,
    default: 3000
  },
  // 是否自动关闭
  autoClose: {
    type: Boolean,
    default: true
  }
})

// 定义事件
const emit = defineEmits(['close'])

// 显示状态
const visible = ref(true)

// 监听visible变化，当变为false时触发close事件
watch(visible, (newVal) => {
  if (!newVal) {
    emit('close')
  }
})

// 组件挂载后，设置自动关闭定时器
onMounted(() => {
  if (props.autoClose) {
    setTimeout(() => {
      visible.value = false
    }, props.duration)
  }
})
</script>

<style scoped>
.toast {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 16px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  opacity: 0;
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.toast-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 提示类型样式 */
.toast-success {
  background-color: #4CAF50;
  color: white;
}

.toast-error {
  background-color: #F44336;
  color: white;
}

.toast-warning {
  background-color: #FF9800;
  color: white;
}

.toast-info {
  background-color: #2196F3;
  color: white;
}

/* 动画效果 */
.toast-fade-in {
  opacity: 1;
  transform: translate(-50%, -50%) scale(1);
}

.toast-fade-out {
  opacity: 0;
  transform: translate(-50%, -50%) scale(0.9);
}
</style>