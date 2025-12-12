<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, onBeforeRouteUpdate } from 'vue-router'
import Header from './components/Header.vue'
import Sidebar from './components/Sidebar.vue'
import Footer from './components/Footer.vue'
import { useContentStore, useAuthStore } from './stores'

const route = useRoute()
const contentStore = useContentStore()
const userStore = useAuthStore()
const showSidebar = ref(true)
const isMobile = ref(false)

// 监听路由变化，在首页显示侧边栏，详情页隐藏侧边栏
onMounted(() => {
  // 初始化认证信息
  userStore.loadUserFromStorage()
  checkSidebarVisibility()
  checkMobileDevice()
  // 加载内容列表
  contentStore.fetchLatestArticles()
  contentStore.fetchLatestToolkits()
  
  // 检测URL中的推广参数
  checkReferral()
  
  // 监听窗口大小变化
  window.addEventListener('resize', checkMobileDevice)
})

// 检测并处理URL中的推广参数
const checkReferral = () => {
  const urlParams = new URLSearchParams(window.location.search)
  const referralCode = urlParams.get('ref')
  if (referralCode) {
    // 将推广码发送到后端进行记录
    fetch('/api/affiliate/track', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ referral_code: referralCode })
    }).catch(error => {
      console.error('Failed to track referral:', error)
    })
  }
}

// 每次路由切换前确保认证信息存在
onBeforeRouteUpdate(() => {
  userStore.ensureAuth()
})

const checkSidebarVisibility = () => {
  showSidebar.value = route.path === '/'
}

// 检测移动设备
const checkMobileDevice = () => {
  isMobile.value = window.innerWidth < 768
  // 在移动设备上默认不显示侧边栏
  if (isMobile.value && route.path !== '/') {
    showSidebar.value = false
  }
}
</script>

<template>
  <div class="app-container">
    <!-- 头部导航 -->
    <Header />
    
    <!-- 主要内容区域 -->
    <main class="main-content">
      <div class="container">
        <div class="content-wrapper">
          <!-- 路由视图 -->
          <section class="content-view">
            <router-view v-slot="{ Component }">
              <transition name="fade" mode="out-in">
                <component :is="Component" />
              </transition>
            </router-view>
          </section>
          
          <!-- 侧边栏 -->
          <Sidebar v-if="showSidebar" />
        </div>
      </div>
    </main>
    
    <!-- 页脚 -->
    <Footer />
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #fdfbfb 0%, #f8f0f3 100%);
  background-attachment: fixed;
}

.main-content {
  flex: 1;
  padding: 30px 0;
  position: relative;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.content-wrapper {
  display: flex;
  gap: 30px;
  align-items: flex-start;
  position: relative;
}

.content-view {
  flex: 1;
  background-color: var(--bg-primary);
  border-radius: 16px;
  padding: 30px;
  box-shadow: var(--shadow-medium);
  transition: all 0.3s ease;
}

.content-view:hover {
  box-shadow: var(--shadow-large);
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.4s cubic-bezier(0.33, 1, 0.68, 1);
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .container {
    max-width: 100%;
  }
  
  .main-content {
    padding: 25px 0;
  }
}

@media (max-width: 992px) {
  .main-content {
    padding: 20px 0;
  }
  
  .content-wrapper {
    gap: 20px;
  }
  
  .content-view {
    padding: 25px;
  }
  
  /* 在平板设备上优化侧边栏 */
  .content-wrapper:has(.sidebar) {
    gap: 15px;
  }
}

@media (max-width: 768px) {
  .main-content {
    padding: 15px 0;
  }
  
  .container {
    padding: 0 15px;
  }
  
  .content-wrapper {
    flex-direction: column;
    gap: 20px;
  }
  
  .content-view {
    padding: 20px;
    border-radius: 12px;
  }
  
  /* 在移动设备上优化内容显示 */
  .content-view {
    min-height: calc(100vh - 200px);
  }
  
  /* 为移动设备添加更好的触摸反馈 */
  .content-view * {
    touch-action: manipulation;
  }
}

@media (max-width: 480px) {
  .main-content {
    padding: 10px 0;
  }
  
  .container {
    padding: 0 12px;
  }
  
  .content-view {
    padding: 16px;
    border-radius: 10px;
  }
}
</style>
