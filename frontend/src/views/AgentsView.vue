<template>
  <div class="agents-view">
    <div class="overlay"></div>
    <div class="not-available-container">
      <div class="not-available-icon">🤖</div>
      <h2 class="not-available-title">暂时还未使用</h2>
      <p class="not-available-description">
        智能体功能正在紧张开发中，敬请期待！
      </p>
      <router-link to="/" class="back-home-btn">返回首页</router-link>
    </div>
  </div>
</template>

<script setup>
// 智能体功能暂未开放
</script>

<style scoped>
.agents-view {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  background-color: #f5f5f5;
  position: relative;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.25);
  z-index: 1;
}

.not-available-container {
  text-align: center;
  max-width: 500px;
  background-color: white;
  border-radius: 16px;
  padding: 60px 40px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  position: relative;
  z-index: 2;
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