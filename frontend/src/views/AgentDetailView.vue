<template>
  <div class="toolkit-detail-view">
    <div class="not-available-container">
      <div class="not-available-icon">🔧</div>
      <h2 class="not-available-title">工具包功能还未开放</h2>
      <p class="not-available-description">
        工具包功能正在紧张开发中，敬请期待！
      </p>
      <router-link to="/" class="back-home-btn">返回首页</router-link>
    </div>
  </div>
</template>

<script setup>
// 工具包功能暂未开放
</script>

<style scoped>
.toolkit-detail-view {
  min-height: 80vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.not-available-container {
  text-align: center;
  max-width: 500px;
  background-color: white;
  border-radius: 16px;
  padding: 60px 40px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.not-available-icon {
  font-size: 64px;
  margin-bottom: 20px;
  opacity: 0.8;
}

.not-available-title {
  font-size: 28px;
  color: #333;
  margin-bottom: 15px;
}

.not-available-description {
  font-size: 16px;
  color: #666;
  margin-bottom: 30px;
  line-height: 1.6;
}

.back-home-btn {
  display: inline-block;
  padding: 12px 30px;
  background-color: var(--primary-color);
  color: white;
  border-radius: 25px;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-medium);
}

.back-home-btn:hover {
  background-color: #FF4785;
  transform: translateY(-2px);
  box-shadow: var(--shadow-large);
}
</style>