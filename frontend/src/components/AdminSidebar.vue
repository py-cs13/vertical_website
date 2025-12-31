<template>
  <div class="admin-sidebar-wrapper">
    <!-- Logo -->
    <div class="sidebar-logo">
      <h2>管理后台</h2>
    </div>

    <!-- 导航菜单 -->
    <nav class="sidebar-nav">
      <ul class="nav-list">
        <!-- 仪表盘 -->
        <li class="nav-item">
          <router-link 
            to="/admin/dashboard" 
            class="nav-link" 
            active-class="active"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="3" width="7" height="7"></rect>
              <rect x="14" y="3" width="7" height="7"></rect>
              <rect x="14" y="14" width="7" height="7"></rect>
              <rect x="3" y="14" width="7" height="7"></rect>
            </svg>
            <span>仪表盘</span>
          </router-link>
        </li>

        <!-- 内容管理 -->
        <li class="nav-item">
          <a 
            href="#" 
            class="nav-link" 
            @click.prevent="toggleSubmenu('content')"
            :class="{ 'active': activeSubmenu === 'content' }"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
            </svg>
            <span>内容管理</span>
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" :class="{ 'rotate': openSubmenus.includes('content') }">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </a>
          <ul class="submenu" v-if="openSubmenus.includes('content')">
            <li>
              <router-link to="/admin/contents/articles" active-class="active">文章管理</router-link>
            </li>
            <li>
              <router-link to="/admin/contents/agents" active-class="active">智能体管理</router-link>
            </li>
          </ul>
        </li>

        <!-- 用户管理 -->
        <li class="nav-item">
          <router-link 
            to="/admin/users" 
            class="nav-link" 
            active-class="active"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
            <span>用户管理</span>
          </router-link>
        </li>

        <!-- 订单管理 -->
        <li class="nav-item">
          <router-link 
            to="/admin/orders" 
            class="nav-link" 
            active-class="active"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
            </svg>
            <span>订单管理</span>
          </router-link>
        </li>

        <!-- 推广统计 -->
        <li class="nav-item">
          <router-link 
            to="/admin/affiliate" 
            class="nav-link" 
            active-class="active"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="20" x2="18" y2="10"></line>
              <line x1="12" y1="20" x2="12" y2="4"></line>
              <line x1="6" y1="20" x2="6" y2="14"></line>
            </svg>
            <span>推广统计</span>
          </router-link>
        </li>
      </ul>
    </nav>

    <!-- 版本信息 -->
    <div class="sidebar-footer">
      <p>版本 1.0.0</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 管理侧边栏子菜单的展开状态
const openSubmenus = ref([])
const activeSubmenu = ref('')

// 切换子菜单显示状态
const toggleSubmenu = (submenuName) => {
  const index = openSubmenus.value.indexOf(submenuName)
  if (index > -1) {
    openSubmenus.value.splice(index, 1)
    if (activeSubmenu.value === submenuName) {
      activeSubmenu.value = ''
    }
  } else {
    openSubmenus.value.push(submenuName)
    activeSubmenu.value = submenuName
  }
}
</script>

<style scoped>
.admin-sidebar-wrapper {
  height: 100%;
  display: flex;
  flex-direction: column;
}

/* Logo */
.sidebar-logo {
  padding: 20px;
  border-bottom: 1px solid #435e7e;
  text-align: center;
}

.sidebar-logo h2 {
  margin: 0;
  font-size: 18px;
  color: #fff;
  font-weight: 600;
}

/* 导航菜单 */
.sidebar-nav {
  flex: 1;
  padding: 20px 0;
}

.nav-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-item {
  margin-bottom: 5px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  color: rgba(255, 255, 255, 0.85);
  text-decoration: none;
  font-size: 14px;
  transition: all 0.3s ease;
  border-left: 3px solid transparent;
}

.nav-link:hover {
  background-color: #263445;
  color: #fff;
  border-left-color: #409eff;
}

.nav-link.active {
  background-color: #263445;
  color: #fff;
  border-left-color: #409eff;
}

/* 子菜单 */
.submenu {
  list-style: none;
  margin: 0;
  padding: 5px 0;
  background-color: #1f2d3d;
}

.submenu li {
  margin: 0;
}

.submenu a {
  display: block;
  padding: 10px 20px 10px 50px;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-size: 13px;
  transition: all 0.3s ease;
}

.submenu a:hover {
  background-color: #263445;
  color: #fff;
}

.submenu a.active {
  background-color: #263445;
  color: #409eff;
}

/* 图标旋转动画 */
.rotate {
  transform: rotate(180deg);
  transition: transform 0.3s ease;
}

/* 底部信息 */
.sidebar-footer {
  padding: 15px 20px;
  border-top: 1px solid #435e7e;
  text-align: center;
}

.sidebar-footer p {
  margin: 0;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
}
</style>