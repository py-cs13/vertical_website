import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/index.js'
import Swal from 'sweetalert2'

// 路由配置
const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomeView.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/RegisterView.vue')
  },
  {
    path: '/article/:id',
    name: 'article-detail',
    component: () => import('../views/ArticleDetailView.vue')
  },
  {
    path: '/agent/:id',
    name: 'agent-detail',
    component: () => import('../views/AgentDetailView.vue')
  },
  {    path: '/user',    name: 'user-center',    component: () => import('../views/UserCenterView.vue'),    meta: { requiresAuth: true }  },  {    path: '/payment',    name: 'payment',    component: () => import('../views/PaymentView.vue'),    meta: { requiresAuth: true }  },  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue')
  },
  {
    path: '/articles',
    name: 'articles',
    component: () => import('../views/ArticlesView.vue')
  },
  {
    path: '/simple-articles',
    name: 'SimpleArticles',
    component: () => import('../views/SimpleArticlesView.vue')
  },
  {
    path: '/direct-articles',
    name: 'DirectArticles',
    component: () => import('../views/DirectArticlesView.vue')
  },
  {
    path: '/agents',
    name: 'agents',
    component: () => import('../views/AgentsView.vue')
  },
  {
    path: '/affiliate',
    name: 'affiliate',
    component: () => import('../views/AffiliateView.vue'),
    meta: { requiresAuth: true }
  },
  // 管理后台路由
  {
    path: '/admin',
    name: 'admin-dashboard',
    component: () => import('../views/Admin/DashboardView.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/articles',
    name: 'admin-articles',
    component: () => import('../views/Admin/ArticleManagementView.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/agents',
    name: 'admin-agents',
    component: () => import('../views/Admin/AgentManagementView.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/users',
    name: 'admin-users',
    component: () => import('../views/Admin/UserManagementView.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/orders',
    name: 'admin-orders',
    component: () => import('../views/Admin/OrderManagementView.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/affiliate-stats',
    name: 'admin-affiliate-stats',
    component: () => import('../views/Admin/AffiliateStatView.vue'),
    meta: { requiresAdmin: true }
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 路由守卫：在每次路由切换时重置错误信息并检查权限
router.beforeEach((to, from, next) => {
  // 重置错误信息
  const userStore = useAuthStore()
  userStore.error = ''
  
  // 确保用户信息已从localStorage加载
  userStore.loadUserFromStorage()
  
  // 如果用户已登录，访问登录或注册页面时跳转到首页
  if ((to.path === '/login' || to.path === '/register') && userStore.isAuthenticated) {
    next({ name: 'home' })
    return
  }
  
  // 检查是否需要认证
  if (to.meta.requiresAuth) {
    // 检查用户是否已登录
    if (!userStore.token) {
      Swal.fire('提示', '请先登录', 'info').then(() => {
        next({ name: 'login' })
      })
      return
    }
  }
  
  // 检查是否需要管理员权限
  if (to.meta.requiresAdmin) {
    // 检查用户是否已登录
    if (!userStore.token) {
      Swal.fire('提示', '请先登录', 'info').then(() => {
        next({ name: 'login' })
      })
      return
    }
    
    // 检查用户是否为管理员
    if (!userStore.isAdmin) {
      Swal.fire('权限不足', '您没有管理员权限', 'error').then(() => {
        next({ name: 'home' })
      })
      return
    }
  }
  
  next()
})

export default router