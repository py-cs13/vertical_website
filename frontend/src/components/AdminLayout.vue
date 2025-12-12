<template>
  <div class="admin-layout">
    <!-- 顶部导航 -->
    <header class="admin-header">
      <div class="header-left">
        <button class="menu-toggle" @click="toggleSidebar">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="3" y1="12" x2="21" y2="12"></line>
            <line x1="3" y1="6" x2="21" y2="6"></line>
            <line x1="3" y1="18" x2="21" y2="18"></line>
          </svg>
        </button>
        <h1 class="admin-title">母婴垂直网站管理后台</h1>
      </div>
      <div class="header-right">
        <div class="user-info">
          <span class="username">{{ currentUser?.username }}</span>
          <button class="logout-btn" @click="logout">退出</button>
        </div>
      </div>
    </header>

    <div class="admin-container">
      <!-- 侧边栏 -->
      <aside class="admin-sidebar" :class="{ 'sidebar-open': isSidebarOpen }">
        <AdminSidebar />
      </aside>

      <!-- 主内容区域 -->
      <main class="admin-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/index.js'
import AdminSidebar from './AdminSidebar.vue'

const router = useRouter()
const authStore = useAuthStore()
const isSidebarOpen = ref(true)

// 获取当前用户信息
const currentUser = computed(() => authStore.currentUser)

// 切换侧边栏显示状态
const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}

// 退出登录
const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f5f7fa;
  color: #333;
}

/* 顶部导航 */
.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 60px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.menu-toggle {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #666;
  padding: 5px;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.menu-toggle:hover {
  background-color: #f0f0f0;
}

.admin-title {
  font-size: 20px;
  font-weight: 600;
  color: #409eff;
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.username {
  font-size: 14px;
  font-weight: 500;
}

.logout-btn {
  padding: 6px 15px;
  background-color: #ff4d4f;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background-color: #ff7875;
}

/* 主容器 */
.admin-container {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* 侧边栏 */
.admin-sidebar {
  width: 200px;
  background-color: #304156;
  color: #fff;
  transition: all 0.3s ease;
  overflow-y: auto;
}

.admin-sidebar.sidebar-open {
  transform: translateX(0);
}

/* 主内容区域 */
.admin-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .admin-sidebar {
    position: fixed;
    left: 0;
    top: 60px;
    bottom: 0;
    transform: translateX(-100%);
    z-index: 99;
  }
}
</style>