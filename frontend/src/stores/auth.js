import { defineStore } from 'pinia'
import axios from 'axios'
import apiClient from '../utils/api.js'

// Auth Store
export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null,
    loading: false,
    error: null
  }),
  
  getters: {
    currentUser: (state) => state.user,
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.user?.is_admin
  },
  
  actions: {
    // 保存用户信息到localStorage
    saveUserToStorage() {
      // 分别保存user和token，即使其中一个不存在
      if (this.user) {
        localStorage.setItem('user', JSON.stringify(this.user))
      }
      if (this.token) {
        localStorage.setItem('token', this.token)
      }
    },
    
    // 从localStorage加载用户信息
    loadUserFromStorage() {
      const savedUser = localStorage.getItem('user')
      const savedToken = localStorage.getItem('token')
      
      if (savedUser && savedToken) {
        try {
          this.user = JSON.parse(savedUser)
          this.token = savedToken
        } catch (e) {
          console.error('Error parsing user data from localStorage:', e)
          this.logout()
        }
      }
    },
    
    // 登录
    async login(email, password) {
      this.loading = true
      this.error = null
      try {
        // 使用apiClient确保错误处理一致
        const response = await apiClient.post('/auth/login', { email, password })
        this.token = response.data.access_token
        
        // 登录成功后获取用户信息
        try {
          const userResponse = await apiClient.get('/users/me')
          this.user = userResponse.data
        } catch (userError) {
          console.error('Failed to fetch user info after login:', userError)
          // 如果获取用户信息失败，至少保证token被存储
        }
        
        this.saveUserToStorage()
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || '登录失败'
        console.error('Login failed:', error)
        return null
      } finally {
        this.loading = false
      }
    },
    
    // 注册
    async register(userData) {
      this.loading = true
      this.error = null
      try {
        // 使用apiClient确保错误处理一致
        const response = await apiClient.post('/auth/register', userData)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || '注册失败'
        console.error('Registration failed:', error)
        return null
      } finally {
        this.loading = false
      }
    },
    
    // 登出
    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('user')
      localStorage.removeItem('token')
    },
    
    // 更新用户信息
    async updateUser(userData) {
      this.loading = true
      this.error = null
      try {
        // 使用apiClient确保错误处理一致
        const response = await apiClient.put('/users/me', userData)
        this.user = response.data
        this.saveUserToStorage()
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || '更新用户信息失败'
        console.error('Failed to update user:', error)
        return null
      } finally {
        this.loading = false
      }
    },
    
    // 确保认证信息存在（用于路由切换时调用）
    ensureAuth() {
      this.loadUserFromStorage()
    }
  }
})