<template>
  <header class="header">
    <div class="container">
      <div class="header-content">
        <div class="logo">
      <router-link to="/">母婴趣指南</router-link>
    </div>
        
        <!-- 桌面端导航 -->
        <nav class="nav-desktop">
          <ul>
            <li><router-link to="/">首页</router-link></li>
            <li><router-link to="/articles">文章</router-link></li>
            <li><router-link to="/agents">智能体</router-link></li>
            <li><router-link to="/products">精选好物</router-link></li>
            <li><router-link to="/about">关于我们</router-link></li>
          </ul>
        </nav>
        
        <div class="user-actions">
          <div class="search-container" :class="{ 'expanded': showSearch }">
            <button class="search-btn" @click="toggleSearch" v-if="!showSearch">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
            </button>
            <input type="text" v-model="searchQuery" placeholder="搜索文章、智能体..." class="search-input" v-show="showSearch" @keyup.enter="performSearch" ref="searchInput">
            <button class="search-submit-btn" @click="performSearch" v-show="showSearch">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
              <span>搜索</span>
            </button>
            <button class="search-close-btn" @click="toggleSearch" v-show="showSearch">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
          
          <template v-if="userStore.isAuthenticated">
            <div class="user-profile">
              <span class="user-name" :title="userStore.user?.username">{{ truncatedUsername }}</span>
            </div>
          </template>
          <template v-else>
            <router-link to="/login" class="login-btn">登录</router-link>
            <router-link to="/register" class="register-btn">注册</router-link>
          </template>
          
          <!-- 菜单按钮（移动端和桌面端） -->
          <div class="menu-wrapper">
            <button class="menu-btn" @click="toggleMenu">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path v-if="!showMobileMenu && !showDesktopMenu" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
            
            <!-- 桌面端下拉菜单 -->
            <div class="desktop-menu" v-if="showDesktopMenu">
              <ul>
                <li v-if="userStore.isAuthenticated">
                  <router-link to="/user" @click="showDesktopMenu = false">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="menu-icon">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                    </svg>
                    个人中心
                  </router-link>
                </li>
                <li v-if="userStore.isAuthenticated">
                  <a href="#" @click.prevent="showDesktopMenu = false; userStore.logout()">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="menu-icon">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
                    </svg>
                    退出登录
                  </a>
                </li>
                <li><router-link to="/about" @click="showDesktopMenu = false">
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="menu-icon">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  关于我们
                </router-link></li>
                <li><a href="#" @click.prevent="showDesktopMenu = false; showAffiliateAlert">
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="menu-icon">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                  </svg>
                  联盟合作
                </a></li>
                <li><a href="#" @click.prevent="showDesktopMenu = false; showContactAlert">
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="menu-icon">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                  </svg>
                  联系我们
                </a></li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 移动端导航菜单 -->
      <div class="nav-mobile" v-if="showMobileMenu">
        <ul>
            <li><router-link to="/" @click="showMobileMenu = false">首页</router-link></li>
            <li><router-link to="/articles" @click="showMobileMenu = false">文章</router-link></li>
            <li><router-link to="/agents" @click="showMobileMenu = false">智能体</router-link></li>
            <li><router-link to="/products" @click="showMobileMenu = false">精选好物</router-link></li>
            <li><router-link to="/about" @click="showMobileMenu = false">关于我们</router-link></li>
            <li><a href="#" @click.prevent="showMobileMenu = false; showAffiliateAlert">联盟合作</a></li>
            <li v-if="userStore.isAuthenticated">
              <router-link to="/user" @click="showMobileMenu = false" class="user-info">
                <span class="user-name" :title="userStore.user?.username">{{ truncatedUsername }}</span>
              </router-link>
            </li>
            <li v-if="userStore.isAuthenticated">
              <a href="#" @click.prevent="showMobileMenu = false; userStore.logout()">退出登录</a>
            </li>
            <li v-else>
              <router-link to="/login" @click="showMobileMenu = false">登录</router-link>
              <router-link to="/register" @click="showMobileMenu = false">注册</router-link>
            </li>
          </ul>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '../stores'
import Swal from 'sweetalert2'
import { useRouter } from 'vue-router'

const userStore = useAuthStore()
const showMobileMenu = ref(false)
const showDesktopMenu = ref(false)
const showSearch = ref(false)
const searchQuery = ref('')
const router = useRouter()

// 计算属性：截断用户名显示（最多5个字符）
const truncatedUsername = computed(() => {
  const username = userStore.user?.username || '用户'
  if (username.length <= 5) {
    return username
  }
  return username.substring(0, 5) + '...'
})

// 切换菜单（根据屏幕尺寸判断显示哪个菜单）
const toggleMenu = () => {
  // 检查屏幕宽度，判断是移动端还是桌面端
  if (window.innerWidth <= 768) {
    showMobileMenu.value = !showMobileMenu.value
    showDesktopMenu.value = false
  } else {
    showDesktopMenu.value = !showDesktopMenu.value
    showMobileMenu.value = false
  }
}

// 切换搜索框显示/隐藏
const searchInput = ref(null)
const toggleSearch = () => {
  showSearch.value = !showSearch.value
  // 如果显示搜索框，自动聚焦
  if (showSearch.value) {
    setTimeout(() => {
      if (searchInput.value) {
        searchInput.value.focus()
      }
    }, 300)
  } else {
    searchQuery.value = ''
  }
}

// 执行搜索
const performSearch = () => {
  if (searchQuery.value.trim()) {
    // 跳转到文章列表页并带上搜索参数
    router.push({ path: '/articles', query: { search: searchQuery.value.trim() } })
    showSearch.value = false
  }
}

// 显示联盟推广弹窗
const showAffiliateAlert = () => {
  Swal.fire({
    title: '联盟推广',
    text: '感谢您对我们的支持！目前联盟推广功能正在开发中，敬请期待。',
    icon: 'info',
    confirmButtonText: '确定'
  })
}

// 显示联系我们弹窗
const showContactAlert = () => {
  Swal.fire({
    title: '联系我们',
    html: '<p>邮箱：cl06221227@gmail.com</p><p>微信：muyingquzhinan</p>',
    icon: 'info',
    confirmButtonText: '确定'
  })
}
</script>

<style scoped>
.header {
  background-color: var(--bg-primary);
  box-shadow: var(--shadow-light);
  position: sticky;
  top: 0;
  z-index: 12000; /* 高于分类标签的z-index */
  border-bottom: 2px solid var(--primary-color);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 75px;
}

.logo {
  font-size: 26px;
  font-weight: 700;
}

.logo a {
  color: var(--primary-color);
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo a::before {
  content: "👶";
  font-size: 28px;
}

/* 桌面端导航 */
.nav-desktop ul {
  display: flex;
  list-style: none;
  gap: 35px;
}

.nav-desktop a {
  color: var(--text-primary);
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  padding: 8px 12px;
  border-radius: 20px;
  font-size: 16px;
}

.nav-desktop a:hover {
  color: var(--primary-color);
  background-color: var(--bg-accent);
  transform: translateY(-1px);
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

/* 菜单按钮容器 */
.menu-wrapper {
  position: relative;
}

/* 桌面端下拉菜单 */
.desktop-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 10px;
  background-color: var(--bg-primary);
  box-shadow: var(--shadow-medium);
  border-radius: 12px;
  border: 1px solid var(--border-color);
  min-width: 180px;
  z-index: 13000;
}

.desktop-menu ul {
  list-style: none;
  padding: 8px 0;
}

.desktop-menu a {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  color: var(--text-primary);
  text-decoration: none;
  transition: all 0.3s ease;
  font-size: 15px;
}

.desktop-menu a:hover {
  background-color: var(--bg-accent);
  color: var(--primary-color);
}

.menu-icon {
  flex-shrink: 0;
}

.search-btn, .menu-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: var(--text-secondary);
  padding: 10px;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.search-container {
  position: relative;
  display: flex;
  align-items: center;
  background-color: var(--bg-secondary);
  border-radius: 25px;
  transition: all 0.3s ease-in-out;
  overflow: hidden;
  height: 40px;
  width: 40px;
  min-width: 40px;
  max-width: 280px;
}

.search-container.expanded {
  width: 280px;
  padding: 0 15px;
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-light);
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  padding: 0;
  font-size: 15px;
  color: var(--text-primary);
  opacity: 0;
  width: 0;
  transition: opacity 0.3s ease-in-out 0.1s, width 0.3s ease-in-out 0.1s;
  position: relative;
  z-index: 2;
}

.search-container.expanded .search-input {
  opacity: 1;
  width: 160px;
}

.search-input::placeholder {
  color: var(--text-secondary);
}

/* 搜索提交按钮 - 使用固定定位避免布局跳动 */
.search-submit-btn {
  background-color: transparent;
  border: none;
  border-radius: 20px;
  padding: 6px 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  cursor: pointer;
  color: var(--text-secondary);
  opacity: 0;
  visibility: hidden;
  transform: scale(0.9);
  transition: all 0.3s ease-in-out 0.2s;
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  position: relative;
  z-index: 2;
}

.search-container.expanded .search-submit-btn {
  opacity: 1;
  visibility: visible;
  transform: scale(1);
}

/* 关闭按钮 - 使用固定定位避免布局跳动 */
.search-close-btn {
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
  color: var(--text-secondary);
  padding: 8px;
  border-radius: 50%;
  opacity: 0;
  visibility: hidden;
  transform: scale(0.9);
  transition: all 0.3s ease-in-out 0.2s;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 2;
}

.search-container.expanded .search-close-btn {
  opacity: 1;
  visibility: visible;
  transform: scale(1);
}

.search-close-btn:hover {
  background-color: var(--bg-accent);
  color: var(--primary-color);
}

.search-submit-btn:hover {
  background-color: var(--bg-accent);
  color: var(--primary-color);
  transform: scale(1.05);
}

.search-btn:hover, .menu-btn:hover {
  background-color: var(--bg-accent);
  color: var(--primary-color);
  transform: translateY(-2px);
}

.login-btn, .register-btn {
  padding: 10px 20px;
  border-radius: 25px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 15px;
}

.login-btn {
  background-color: transparent;
  border: 2px solid var(--primary-color);
  color: var(--primary-color);
}

.login-btn:hover {
  background-color: var(--bg-accent);
  transform: translateY(-2px);
}

.register-btn {
  background-color: var(--primary-color);
  border: none;
  color: white;
  box-shadow: var(--shadow-light);
}

.register-btn:hover {
  background-color: #FF4785;
  transform: translateY(-2px);
  box-shadow: var(--shadow-medium);
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--text-primary);
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 25px;
  background-color: var(--bg-secondary);
}

.user-name {
  color: var(--primary-color);
  font-weight: 700;
  font-size: 16px;
  padding: 4px 8px;
  background-color: var(--bg-accent);
  border-radius: 12px;
  /* 新增：用户名长度限制 */
  max-width: 85px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  cursor: default;
}

/* 移动端导航 */
.nav-mobile {
  display: none;
  padding: 20px 0;
  border-top: 1px solid var(--border-color);
  background-color: var(--bg-primary);
}

.nav-mobile ul {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.nav-mobile a {
  color: var(--text-primary);
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  padding: 12px 16px;
  border-radius: 25px;
  display: block;
}

.nav-mobile a:hover {
  color: var(--primary-color);
  background-color: var(--bg-accent);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .nav-desktop {
    display: none;
  }
  
  .nav-mobile {
    display: block;
  }
  
  .logo {
    font-size: 22px;
  }
  
  .logo a::before {
    font-size: 24px;
  }
  
  .user-actions {
    gap: 8px;
  }
  
  .login-btn, .register-btn {
    padding: 8px 16px;
    font-size: 14px;
  }
  
  .search-btn, .menu-btn {
    padding: 8px;
    font-size: 18px;
  }
  
  .search-container.expanded {
    width: 250px;
  }
  
  .search-container.expanded .search-input {
    width: 170px;
  }
  
  /* 移动端用户名长度限制 */
  .user-name {
    max-width: 70px;
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .logo {
    font-size: 20px;
  }
  
  .logo a::before {
    font-size: 22px;
  }
  
  .user-actions {
    gap: 5px;
  }
  
  .login-btn, .register-btn {
    padding: 6px 12px;
    font-size: 13px;
  }
  
  .search-container.expanded {
    width: 220px;
  }
  
  .search-container.expanded .search-input {
    width: 140px;
    font-size: 14px;
  }
}

</style>