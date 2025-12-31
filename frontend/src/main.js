import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import './style.css'
import App from './App.vue'

// 移除全局axios配置，避免影响apiClient实例

// 生产环境不加载调试脚本

// 创建Pinia实例
const pinia = createPinia()

// 创建Vue应用实例
const app = createApp(App)

// 注册插件
app.use(pinia)
app.use(router)

// 挂载应用前加载用户信息
import { useAuthStore } from './stores/auth.js'
const userStore = useAuthStore()
userStore.loadUserFromStorage()

// 挂载应用
app.mount('#app')
