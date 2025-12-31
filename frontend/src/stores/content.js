import { defineStore } from 'pinia'
import { ref } from 'vue'
import apiClient from '../utils/api'
import { getArticles, getAdminArticles, createArticle, updateArticle, deleteArticle, batchDeleteArticles } from '../utils/api'

// 内容管理store
export const useContentStore = defineStore('content', {
  state: () => ({
    articles: [],
    todayFeature: null,
    loading: false,
    error: null,
    // 管理后台相关状态
    adminArticles: [],
    totalArticles: 0,
    currentPage: 1,
    pageSize: 10,
    filter: {
      search: '',
      category: '',
      status: ''
    }
  }),
  
  actions: {
    // 获取缓存数据
    getCachedData(key) {
      const cached = localStorage.getItem(key)
      if (cached) {
        try {
          const data = JSON.parse(cached)
          // 检查缓存是否过期（1小时）
          if (Date.now() - data.timestamp < 3600000) {
            return data.content
          }
        } catch (e) {
          console.error('Error parsing cached data:', e)
        }
      }
      return null
    },
    
    // 设置缓存数据
    setCachedData(key, content) {
      try {
        localStorage.setItem(key, JSON.stringify({
          content,
          timestamp: Date.now()
        }))
      } catch (e) {
        console.error('Error setting cached data:', e)
      }
    },
    
    // 清除缓存数据
    clearCachedData(key) {
      localStorage.removeItem(key)
    },
    
    // 获取今日推荐内容
    async fetchTodayFeature() {
      this.loading = true
      this.error = null
      try {
        // 今日推荐不缓存，每次都从API获取
        const response = await apiClient.get('/content/today-feature')
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
        // 清除旧缓存，确保获取最新点赞数
        this.clearCachedData('latest_articles')
        
        // 直接从API获取最新文章，不使用缓存
        const response = await apiClient.get('/articles')
        // 处理不同的数据格式
        let data = response.data
        if (response.data && response.data.data && Array.isArray(response.data.data)) {
          data = response.data.data
        } else if (response.data && Array.isArray(response.data)) {
          data = response.data
        }
        console.log('API返回的文章数量:', data.length)
        this.articles = data
        // 更新缓存
        this.setCachedData('latest_articles', this.articles)
      } catch (error) {
        this.error = error.message
        console.error('Failed to fetch latest articles from API:', error)
        
        // API请求失败时，尝试从缓存获取
        const cachedArticles = this.getCachedData('latest_articles')
        if (cachedArticles) {
          console.log('使用缓存的文章数据')
          this.articles = cachedArticles
        } else {
          // 如果缓存也没有数据，使用空数组
          console.log('没有可用的文章数据，使用空数组')
          this.articles = []
        }
      } finally {
        this.loading = false
      }
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
        const response = await getAdminArticles(params)
        this.adminArticles = response.data.data
        this.totalArticles = response.data.total
      } catch (error) {
        this.error = error.response?.data?.message || '获取文章列表失败'
        console.error('Failed to fetch admin articles:', error)
      } finally {
        this.loading = false
      }
    },
    
    // 管理后台 - 创建文章
    async createArticle(articleData) {
      this.loading = true
      this.error = null
      try {
        const response = await createArticle(articleData)
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
        const response = await updateArticle(id, articleData)
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
        const response = await deleteArticle(id)
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
        const response = await batchDeleteArticles(ids)
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
    },
    
    // 获取文章详情
    async fetchArticleDetail(id) {
      this.loading = true
      this.error = null
      try {
        // 从API获取文章详情（baseURL已包含/api）
        // 确保id是字符串类型
        const stringId = id.toString()
        const response = await apiClient.get(`/content/${stringId}`)
        const articleData = response.data
        
        // 更新缓存
        this.setCachedData(`article_${id}`, articleData)
        
        // 更新articles列表中对应的数据
        this.updateArticleInList(articleData)
        
        return articleData
      } catch (error) {
        this.error = error.message
        console.error(`Failed to fetch article detail (ID: ${id}):`, error)
        
        // 如果API请求失败，尝试从缓存获取
        const cachedArticle = this.getCachedData(`article_${id}`)
        if (cachedArticle) {
          // 如果缓存存在，同时更新articles列表中对应的数据
          this.updateArticleInList(cachedArticle)
          return cachedArticle
        }
        
        return null
      } finally {
        this.loading = false
      }
    },
    
    // 更新articles列表中对应的数据
    updateArticleInList(articleData) {
      const index = this.articles.findIndex(article => article.id === articleData.id)
      if (index !== -1) {
        // 更新列表中的文章数据
        this.articles[index] = { ...this.articles[index], ...articleData }
      }
    },
    
    // 刷新所有内容数据
    async refreshContent() {
      try {
        // 请求文章数据
        await this.fetchLatestArticles()
      } catch (error) {
        console.error('Failed to refresh content:', error)
      }
    }
  }
})
