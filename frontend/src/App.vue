<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter, onBeforeRouteUpdate } from 'vue-router'
import Header from './components/Header.vue'
import Sidebar from './components/Sidebar.vue'
import Footer from './components/Footer.vue'
import { useContentStore, useAuthStore } from './stores'

const route = useRoute()
const router = useRouter()
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
  // contentStore.fetchLatestToolkits() - 已删除工具包功能
  
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
  checkSidebarVisibility() // 路由变化时更新侧边栏可见性
})

// 显示逻辑：在所有页面都显示侧边栏，除了特定页面
const checkSidebarVisibility = () => {
  // 可以在这里添加例外页面，例如：route.path === '/admin' 等
  showSidebar.value = true // 所有页面都显示侧边栏
}

// 检测移动设备
const checkMobileDevice = () => {
  isMobile.value = window.innerWidth < 768
  // 在移动设备上默认不显示侧边栏
  if (isMobile.value && route.path !== '/') {
    showSidebar.value = false
  }
}

// 处理分类筛选
const handleCategoryFilter = (categoryName) => {
  // 跳转到文章列表页面，并携带分类参数
  router.push({
    path: '/articles',
    query: { category: categoryName }
  })
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
          <Sidebar v-if="showSidebar" @filter-category="handleCategoryFilter" />
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
  width: 100%;
}

/* 确保在大屏幕上内容区域和侧边栏的整体布局更加平衡 */
@media (min-width: 1200px) {
  /* 在大屏幕上，为内容区域和侧边栏添加统一的外边距 */
  .content-view {
    flex: 1;
    min-width: 0;
  }
  
  /* 确保侧边栏不会挤压主内容 */
  .sidebar {
    flex-shrink: 0;
  }
  
  /* 调整整体容器，确保左右留白对称 */
  .container {
    max-width: calc(1200px + 40px); /* 包含左右各20px的边距 */
    padding: 0;
  }
}

.content-view {
  flex: 1;
  background-color: var(--bg-primary);
  border-radius: 16px;
  padding: 30px;
  box-shadow: var(--shadow-medium);
  transition: all 0.3s ease;
  box-sizing: border-box;
  /* 移除可能影响侧边栏点击的溢出设置 */
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
