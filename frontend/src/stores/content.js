import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'
import * as api from '../utils/api'

// 内容管理store
export const useContentStore = defineStore('content', {
  state: () => ({
    articles: [],
    toolkits: [],
    todayFeature: null,
    loading: false,
    error: null,
    // 管理后台相关状态
    adminArticles: [],
    adminToolkits: [],
    totalArticles: 0,
    totalToolkits: 0,
    currentPage: 1,
    pageSize: 10,
    filter: {
      search: '',
      category: '',
      status: ''
    }
  }),
  
  actions: {
    // 获取今日推荐内容
    async fetchTodayFeature() {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get('/api/content/today-feature')
        this.todayFeature = response.data
      } catch (error) {
        this.error = error.message
        console.error('Failed to fetch today feature:', error)
      } finally {
        this.loading = false
      }
    },
    
    // 获取最新文章
    async fetchLatestArticles() {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get('/api/articles/latest')
        this.articles = response.data
      } catch (error) {
        this.error = error.message
        console.error('Failed to fetch latest articles:', error)
      } finally {
        this.loading = false
      }
    },
    
    // 获取工具包列表
    async fetchToolkits() {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get('/api/toolkits/latest')
        this.toolkits = response.data
      } catch (error) {
        this.error = error.message
        console.error('Failed to fetch toolkits:', error)
      } finally {
        this.loading = false
      }
    },
    
    // 获取最新工具包
    async fetchLatestToolkits() {
      // 调用现有的fetchToolkits方法，因为它已经获取了工具包列表
      await this.fetchToolkits()
    },
    
    // 管理后台 - 获取文章列表
    async fetchAdminArticles() {
      this.loading = true
      this.error = null
      try {
        const params = {
          page: this.currentPage,
          page_size: this.pageSize,
          ...this.filter
        }
        const response = await api.getAdminArticles(params)
        this.adminArticles = response.data.data
        this.totalArticles = response.data.total
      } catch (error) {
        this.error = error.response?.data?.message || '获取文章列表失败'
        console.error('Failed to fetch admin articles:', error)
      } finally {
        this.loading = false
      }
    },
    
    // 管理后台 - 获取工具包列表
    async fetchAdminToolkits() {
      this.loading = true
      this.error = null
      try {
        const params = {
          page: this.currentPage,
          page_size: this.pageSize,
          ...this.filter
        }
        const response = await api.getAdminToolkits(params)
        this.adminToolkits = response.data.data
        this.totalToolkits = response.data.total
      } catch (error) {
        this.error = error.response?.data?.message || '获取工具包列表失败'
        console.error('Failed to fetch admin toolkits:', error)
      } finally {
        this.loading = false
      }
    },
    
    // 管理后台 - 创建文章
    async createArticle(articleData) {
      this.loading = true
      this.error = null
      try {
        const response = await api.createArticle(articleData)
        // 重新获取文章列表以更新数据
        await this.fetchAdminArticles()
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || '创建文章失败'
        console.error('Failed to create article:', error)
        return null
      } finally {
        this.loading = false
      }
    },
    
    // 管理后台 - 更新文章
    async updateArticle(id, articleData) {
      this.loading = true
      this.error = null
      try {
        const response = await api.updateArticle(id, articleData)
        // 重新获取文章列表以更新数据
        await this.fetchAdminArticles()
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || '更新文章失败'
        console.error(`Failed to update article ${id}:`, error)
        return null
      } finally {
        this.loading = false
      }
    },
    
    // 管理后台 - 删除文章
    async deleteArticle(id) {
      this.loading = true
      this.error = null
      try {
        const response = await api.deleteArticle(id)
        // 重新获取文章列表以更新数据
        await this.fetchAdminArticles()
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || '删除文章失败'
        console.error(`Failed to delete article ${id}:`, error)
        return null
      } finally {
        this.loading = false
      }
    },
    
    // 管理后台 - 批量删除文章
    async batchDeleteArticles(ids) {
      this.loading = true
      this.error = null
      try {
        const response = await api.batchDeleteArticles(ids)
        // 重新获取文章列表以更新数据
        await this.fetchAdminArticles()
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || '批量删除文章失败'
        console.error('Failed to batch delete articles:', error)
        return null
      } finally {
        this.loading = false
      }
    },
    
    // 管理后台 - 创建工具包
    async createToolkit(toolkitData) {
      this.loading = true
      this.error = null
      try {
        const response = await api.createToolkit(toolkitData)
        // 重新获取工具包列表以更新数据
        await this.fetchAdminToolkits()
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || '创建工具包失败'
        console.error('Failed to create toolkit:', error)
        return null
      } finally {
        this.loading = false
      }
    },
    
    // 管理后台 - 更新工具包
    async updateToolkit(id, toolkitData) {
      this.loading = true
      this.error = null
      try {
        const response = await api.updateToolkit(id, toolkitData)
        // 重新获取工具包列表以更新数据
        await this.fetchAdminToolkits()
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || '更新工具包失败'
        console.error(`Failed to update toolkit ${id}:`, error)
        return null
      } finally {
        this.loading = false
      }
    },
    
    // 管理后台 - 删除工具包
    async deleteToolkit(id) {
      this.loading = true
      this.error = null
      try {
        const response = await api.deleteToolkit(id)
        // 重新获取工具包列表以更新数据
        await this.fetchAdminToolkits()
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || '删除工具包失败'
        console.error(`Failed to delete toolkit ${id}:`, error)
        return null
      } finally {
        this.loading = false
      }
    },
    
    // 管理后台 - 批量删除工具包
    async batchDeleteToolkits(ids) {
      this.loading = true
      this.error = null
      try {
        const response = await api.batchDeleteToolkits(ids)
        // 重新获取工具包列表以更新数据
        await this.fetchAdminToolkits()
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || '批量删除工具包失败'
        console.error('Failed to batch delete toolkits:', error)
        return null
      } finally {
        this.loading = false
      }
    },
    
    // 管理后台 - 设置筛选条件
    setFilter(filter) {
      this.filter = { ...this.filter, ...filter }
      // 筛选条件变化时重置页码
      this.currentPage = 1
    },
    
    // 管理后台 - 设置当前页码
    setCurrentPage(page) {
      this.currentPage = page
    },
    
    // 管理后台 - 设置每页显示数量
    setPageSize(size) {
      this.pageSize = size
      // 每页数量变化时重置页码
      this.currentPage = 1
    },
    
    // 管理后台 - 重置筛选条件
    resetFilter() {
      this.filter = {
        search: '',
        category: '',
        status: ''
      }
      this.currentPage = 1
    }
  }
})