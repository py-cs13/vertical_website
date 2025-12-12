import axios from 'axios'
import Swal from 'sweetalert2'

// 创建axios实例
const apiClient = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器：添加认证token
apiClient.interceptors.request.use(
  (config) => {
    // 直接从localStorage获取token，避免在组件外部使用useAuthStore
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器：统一处理错误
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // 处理403错误（权限不足）
    if (error.response && error.response.status === 403) {
      Swal.fire('权限不足', '您没有足够的权限执行此操作', 'error')
    }
    return Promise.reject(error)
  }
)

// ========================= 内容管理API =========================

// 获取文章列表
export const getArticles = async (params = {}) => {
  try {
    const response = await apiClient.get('/admin/articles', { params })
    return response.data
  } catch (error) {
    console.error('获取文章列表失败:', error)
    throw error
  }
}

// 获取文章详情
export const getArticleDetail = async (id) => {
  try {
    const response = await apiClient.get(`/admin/articles/${id}`)
    return response.data
  } catch (error) {
    console.error(`获取文章详情失败 (ID: ${id}):`, error)
    throw error
  }
}

// 创建文章
export const createArticle = async (articleData) => {
  try {
    const response = await apiClient.post('/admin/articles', articleData)
    return response.data
  } catch (error) {
    console.error('创建文章失败:', error)
    throw error
  }
}

// 更新文章
export const updateArticle = async (id, articleData) => {
  try {
    const response = await apiClient.put(`/admin/articles/${id}`, articleData)
    return response.data
  } catch (error) {
    console.error(`更新文章失败 (ID: ${id}):`, error)
    throw error
  }
}

// 删除文章
export const deleteArticle = async (id) => {
  try {
    const response = await apiClient.delete(`/admin/articles/${id}`)
    return response.data
  } catch (error) {
    console.error(`删除文章失败 (ID: ${id}):`, error)
    throw error
  }
}

// 批量删除文章
export const batchDeleteArticles = async (ids) => {
  try {
    const response = await apiClient.delete('/admin/articles', { data: { ids } })
    return response.data
  } catch (error) {
    console.error('批量删除文章失败:', error)
    throw error
  }
}

// ========================= 工具包管理API =========================

// 获取工具包列表
export const getToolkits = async (params = {}) => {
  try {
    const response = await apiClient.get('/admin/toolkits', { params })
    return response.data
  } catch (error) {
    console.error('获取工具包列表失败:', error)
    throw error
  }
}

// 获取工具包详情
export const getToolkitDetail = async (id) => {
  try {
    const response = await apiClient.get(`/admin/toolkits/${id}`)
    return response.data
  } catch (error) {
    console.error(`获取工具包详情失败 (ID: ${id}):`, error)
    throw error
  }
}

// 创建工具包
export const createToolkit = async (toolkitData) => {
  try {
    const response = await apiClient.post('/admin/toolkits', toolkitData)
    return response.data
  } catch (error) {
    console.error('创建工具包失败:', error)
    throw error
  }
}

// 更新工具包
export const updateToolkit = async (id, toolkitData) => {
  try {
    const response = await apiClient.put(`/admin/toolkits/${id}`, toolkitData)
    return response.data
  } catch (error) {
    console.error(`更新工具包失败 (ID: ${id}):`, error)
    throw error
  }
}

// 删除工具包
export const deleteToolkit = async (id) => {
  try {
    const response = await apiClient.delete(`/admin/toolkits/${id}`)
    return response.data
  } catch (error) {
    console.error(`删除工具包失败 (ID: ${id}):`, error)
    throw error
  }
}

// 批量删除工具包
export const batchDeleteToolkits = async (ids) => {
  try {
    const response = await apiClient.delete('/admin/toolkits', { data: { ids } })
    return response.data
  } catch (error) {
    console.error('批量删除工具包失败:', error)
    throw error
  }
}

// ========================= 用户管理API =========================

// 获取用户列表
export const getUsers = async (params = {}) => {
  try {
    const response = await apiClient.get('/admin/users', { params })
    return response.data
  } catch (error) {
    console.error('获取用户列表失败:', error)
    throw error
  }
}

// 获取用户详情
export const getUserDetail = async (id) => {
  try {
    const response = await apiClient.get(`/admin/users/${id}`)
    return response.data
  } catch (error) {
    console.error(`获取用户详情失败 (ID: ${id}):`, error)
    throw error
  }
}

// 更新用户状态
export const updateUserStatus = async (id, status) => {
  try {
    const response = await apiClient.patch(`/admin/users/${id}/status`, { is_active: status })
    return response.data
  } catch (error) {
    console.error(`更新用户状态失败 (ID: ${id}):`, error)
    throw error
  }
}

// 更新用户角色
export const updateUserRole = async (id, isAdmin) => {
  try {
    const response = await apiClient.patch(`/admin/users/${id}/role`, { is_admin: isAdmin })
    return response.data
  } catch (error) {
    console.error(`更新用户角色失败 (ID: ${id}):`, error)
    throw error
  }
}

// 删除用户
export const deleteUser = async (id) => {
  try {
    const response = await apiClient.delete(`/admin/users/${id}`)
    return response.data
  } catch (error) {
    console.error(`删除用户失败 (ID: ${id}):`, error)
    throw error
  }
}

// 批量删除用户
export const batchDeleteUsers = async (ids) => {
  try {
    const response = await apiClient.delete('/admin/users', { data: { ids } })
    return response.data
  } catch (error) {
    console.error('批量删除用户失败:', error)
    throw error
  }
}

// ========================= 订单管理API =========================

// 获取订单列表
export const getOrders = async (params = {}) => {
  try {
    const response = await apiClient.get('/admin/orders', { params })
    return response.data
  } catch (error) {
    console.error('获取订单列表失败:', error)
    throw error
  }
}

// 获取订单详情
export const getOrderDetail = async (id) => {
  try {
    const response = await apiClient.get(`/admin/orders/${id}`)
    return response.data
  } catch (error) {
    console.error(`获取订单详情失败 (ID: ${id}):`, error)
    throw error
  }
}

// 更新订单状态
export const updateOrderStatus = async (id, status) => {
  try {
    const response = await apiClient.patch(`/admin/orders/${id}/status`, { status })
    return response.data
  } catch (error) {
    console.error(`更新订单状态失败 (ID: ${id}):`, error)
    throw error
  }
}

// ========================= 推广统计API =========================

// 获取推广统计数据
export const getAffiliateStats = async (params = {}) => {
  try {
    const response = await apiClient.get('/admin/affiliate/stats', { params })
    return response.data
  } catch (error) {
    console.error('获取推广统计数据失败:', error)
    throw error
  }
}

// 获取推广用户排名
export const getAffiliateRanking = async (params = {}) => {
  try {
    const response = await apiClient.get('/admin/affiliate/ranking', { params })
    return response.data
  } catch (error) {
    console.error('获取推广用户排名失败:', error)
    throw error
  }
}

// 结算佣金
export const settleCommissions = async () => {
  try {
    const response = await apiClient.post('/admin/affiliate/settle')
    return response.data
  } catch (error) {
    console.error('结算佣金失败:', error)
    throw error
  }
}

// 获取推广用户详情
export const getAffiliateDetail = async (id) => {
  try {
    const response = await apiClient.get(`/admin/affiliate/${id}`)
    return response.data
  } catch (error) {
    console.error(`获取推广用户详情失败 (ID: ${id}):`, error)
    throw error
  }
}

// 获取推广用户列表
export const getAffiliateUsers = async (params = {}) => {
  try {
    const response = await apiClient.get('/admin/affiliate/users', { params })
    return response.data
  } catch (error) {
    console.error('获取推广用户列表失败:', error)
    throw error
  }
}

// 获取佣金统计数据
export const getCommissionStats = async (params = {}) => {
  try {
    const response = await apiClient.get('/admin/affiliate/commissions/stats', { params })
    return response.data
  } catch (error) {
    console.error('获取佣金统计数据失败:', error)
    throw error
  }
}

// 导出推广统计数据
export const exportAffiliateStats = async (params = {}) => {
  try {
    const response = await apiClient.get('/admin/affiliate/export', { 
      params,
      responseType: 'blob'
    })
    return response.data
  } catch (error) {
    console.error('导出推广统计数据失败:', error)
    throw error
  }
}

export default apiClient
