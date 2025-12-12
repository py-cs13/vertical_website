<template>
  <header class="header">
    <div class="container">
      <div class="header-content">
        <div class="logo">
      <router-link to="/">宝贝成长母婴平台</router-link>
    </div>
        
        <!-- 桌面端导航 -->
        <nav class="nav-desktop">
          <ul>
            <li><router-link to="/">首页</router-link></li>
            <li><router-link to="/?category=article">文章</router-link></li>
            <li><router-link to="/?category=toolkit">工具包</router-link></li>
            <li><router-link to="/about">关于我们</router-link></li>
          </ul>
        </nav>
        
        <div class="user-actions">
          <button class="search-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
          </button>
          
          <template v-if="userStore.isAuthenticated">
            <router-link to="/user" class="user-profile">
              <span class="user-name">{{ userStore.user?.username || '用户' }}</span>
            </router-link>
          </template>
          <template v-else>
            <router-link to="/login" class="login-btn">登录</router-link>
            <router-link to="/register" class="register-btn">注册</router-link>
          </template>
          
          <!-- 移动端菜单按钮 -->
          <button class="menu-btn" @click="showMobileMenu = !showMobileMenu">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path v-if="!showMobileMenu" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
      </div>
      
      <!-- 移动端导航菜单 -->
      <div class="nav-mobile" v-if="showMobileMenu">
        <ul>
            <li><router-link to="/" @click="showMobileMenu = false">首页</router-link></li>
            <li><router-link to="/?category=article" @click="showMobileMenu = false">文章</router-link></li>
            <li><router-link to="/?category=toolkit" @click="showMobileMenu = false">工具包</router-link></li>
            <li><router-link to="/about" @click="showMobileMenu = false">关于我们</router-link></li>
            <li><a href="#" @click.prevent="showMobileMenu = false; showAffiliateAlert">联盟合作</a></li>
            <li v-if="userStore.isAuthenticated">
              <router-link to="/user" @click="showMobileMenu = false" class="user-info">
                <span class="user-name">{{ userStore.user?.username || '用户' }}</span>
              </router-link>
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
import { ref } from 'vue'
import { useAuthStore } from '../stores'
import Swal from 'sweetalert2'

const userStore = useAuthStore()
const showMobileMenu = ref(false)

// 显示联盟推广弹窗
const showAffiliateAlert = () => {
  Swal.fire({
    title: '联盟推广',
    text: '感谢您对我们的支持！目前联盟推广功能正在开发中，敬请期待。',
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
  z-index: 1000;
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
  text-decoration: none;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 25px;
  transition: all 0.3s ease;
  background-color: var(--bg-secondary);
}

.user-profile:hover {
  background-color: var(--bg-accent);
  color: var(--primary-color);
  transform: translateY(-2px);
}

.user-name {
  color: var(--primary-color);
  font-weight: 700;
  font-size: 16px;
  padding: 4px 8px;
  background-color: var(--bg-accent);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.user-profile:hover .user-name {
  background-color: var(--primary-color);
  color: white;
  transform: scale(1.05);
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
}

</style>