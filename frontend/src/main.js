import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import './style.css'
import App from './App.vue'

import axios from 'axios'
axios.defaults.baseURL = 'http://localhost:8000/'

// 引入详细调试脚本
import './debug.js'

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
