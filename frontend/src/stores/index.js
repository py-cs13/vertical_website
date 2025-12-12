import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'
import * as api from '../utils/api'

// 导入其他store
import { useContentStore } from './content'
import { useAuthStore } from './auth'

// 导出所有store
export {
  useContentStore,
  useAuthStore
}

// 推广统计Store
export const useAffiliateStatStore = defineStore('affiliateStat', () => {
  // 状态
  const affiliateStats = ref({})
  const affiliateUsers = ref([])
  const commissionStats = ref({})
  const filterParams = ref({
    dateRange: '7d',
    startDate: '',
    endDate: '',
    statType: 'clicks'
  })
  const loading = ref(false)
  const error = ref(null)

  // 获取总体统计数据
  const fetchAffiliateStats = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await api.getAffiliateStats(filterParams.value)
      affiliateStats.value = response.data
    } catch (err) {
      console.error('获取推广统计数据失败:', err)
      error.value = err.response?.data?.message || '获取推广统计数据失败'
    } finally {
      loading.value = false
    }
  }

  // 获取推广用户列表
  const fetchAffiliateUsers = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await api.getAffiliateUsers()
      affiliateUsers.value = response.data
    } catch (err) {
      console.error('获取推广用户列表失败:', err)
      error.value = err.response?.data?.message || '获取推广用户列表失败'
    } finally {
      loading.value = false
    }
  }

  // 获取佣金统计数据
  const fetchCommissionStats = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await api.getCommissionStats(filterParams.value)
      commissionStats.value = response.data
    } catch (err) {
      console.error('获取佣金统计数据失败:', err)
      error.value = err.response?.data?.message || '获取佣金统计数据失败'
    } finally {
      loading.value = false
    }
  }

  // 更新筛选条件
  const updateFilterParams = (params) => {
    filterParams.value = { ...filterParams.value, ...params }
  }

  return {
    affiliateStats,
    affiliateUsers,
    commissionStats,
    filterParams,
    loading,
    error,
    fetchAffiliateStats,
    fetchAffiliateUsers,
    fetchCommissionStats,
    updateFilterParams
  }
})

// 订单管理Store
export const useOrderStore = defineStore('order', () => {
  // 状态
  const orders = ref([])
  const totalOrders = ref(0)
  const currentPage = ref(1)
  const pageSize = ref(10)
  const loading = ref(false)
  const error = ref(null)
  const filter = ref({
    search: '',
    status: '',
    dateRange: ''
  })

  // 获取订单列表（带分页和筛选）
  const fetchOrders = async (params = {}) => {
    loading.value = true
    error.value = null
    try {
      // 合并默认参数和传入参数
      const requestParams = {
        page: currentPage.value,
        page_size: pageSize.value,
        ...filter.value,
        ...params
      }
      
      const response = await api.getOrders(requestParams)
      orders.value = response.data.orders
      totalOrders.value = response.data.total
      return response.data
    } catch (err) {
      console.error('获取订单列表失败:', err)
      error.value = err.response?.data?.message || '获取订单列表失败'
      return null
    } finally {
      loading.value = false
    }
  }

  // 获取订单详情
  const fetchOrderDetail = async (id) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.getOrderDetail(id)
      return response.data
    } catch (err) {
      console.error(`获取订单详情 ${id} 失败:`, err)
      error.value = err.response?.data?.message || '获取订单详情失败'
      return null
    } finally {
      loading.value = false
    }
  }

  // 更新订单状态
  const updateOrderStatus = async (id, status) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.updateOrderStatus(id, status)
      // 重新获取订单列表以更新数据
      await fetchOrders()
      return response.data
    } catch (err) {
      console.error(`更新订单状态 ${id} 失败:`, err)
      error.value = err.response?.data?.message || '更新订单状态失败'
      return null
    } finally {
      loading.value = false
    }
  }

  // 删除订单
  const deleteOrder = async (id) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.deleteOrder(id)
      // 重新获取订单列表以更新数据
      await fetchOrders()
      return response.data
    } catch (err) {
      console.error(`删除订单 ${id} 失败:`, err)
      error.value = err.response?.data?.message || '删除订单失败'
      return null
    } finally {
      loading.value = false
    }
  }

  // 批量删除订单
  const batchDeleteOrders = async (ids) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.batchDeleteOrders(ids)
      // 重新获取订单列表以更新数据
      await fetchOrders()
      return response.data
    } catch (err) {
      console.error('批量删除订单失败:', err)
      error.value = err.response?.data?.message || '批量删除订单失败'
      return null
    } finally {
      loading.value = false
    }
  }

  // 设置筛选条件
  const setFilter = (newFilter) => {
    filter.value = { ...filter.value, ...newFilter }
    // 筛选条件变化时重置页码
    currentPage.value = 1
  }

  // 设置当前页码
  const setCurrentPage = (page) => {
    currentPage.value = page
  }

  // 设置每页显示数量
  const setPageSize = (size) => {
    pageSize.value = size
    // 每页数量变化时重置页码
    currentPage.value = 1
  }

  // 重置筛选条件
  const resetFilter = () => {
    filter.value = {
      search: '',
      status: '',
      dateRange: ''
    }
    currentPage.value = 1
  }

  return {
    orders,
    totalOrders,
    currentPage,
    pageSize,
    loading,
    error,
    filter,
    fetchOrders,
    fetchOrderDetail,
    updateOrderStatus,
    deleteOrder,
    batchDeleteOrders,
    setFilter,
    setCurrentPage,
    setPageSize,
    resetFilter
  }
})

// 佣金管理Store
export const useCommissionStore = defineStore('commission', () => {
  // 状态
  const commissions = ref([])
  const totalCommissions = ref(0)
  const currentPage = ref(1)
  const pageSize = ref(10)
  const loading = ref(false)
  const error = ref(null)
  const filter = ref({
    search: '',
    status: '',
    dateRange: ''
  })

  // 获取佣金列表（带分页和筛选）
  const fetchCommissions = async (params = {}) => {
    loading.value = true
    error.value = null
    try {
      // 合并默认参数和传入参数
      const requestParams = {
        page: currentPage.value,
        page_size: pageSize.value,
        ...filter.value,
        ...params
      }
      
      const response = await api.getCommissions(requestParams)
      commissions.value = response.data.commissions
      totalCommissions.value = response.data.total
      return response.data
    } catch (err) {
      console.error('获取佣金列表失败:', err)
      error.value = err.response?.data?.message || '获取佣金列表失败'
      return null
    } finally {
      loading.value = false
    }
  }

  // 获取佣金详情
  const fetchCommissionDetail = async (id) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.getCommissionDetail(id)
      return response.data
    } catch (err) {
      console.error(`获取佣金详情 ${id} 失败:`, err)
      error.value = err.response?.data?.message || '获取佣金详情失败'
      return null
    } finally {
      loading.value = false
    }
  }

  // 更新佣金状态
  const updateCommissionStatus = async (id, status) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.updateCommissionStatus(id, status)
      // 重新获取佣金列表以更新数据
      await fetchCommissions()
      return response.data
    } catch (err) {
      console.error(`更新佣金状态 ${id} 失败:`, err)
      error.value = err.response?.data?.message || '更新佣金状态失败'
      return null
    } finally {
      loading.value = false
    }
  }

  // 设置筛选条件
  const setFilter = (newFilter) => {
    filter.value = { ...filter.value, ...newFilter }
    // 筛选条件变化时重置页码
    currentPage.value = 1
  }

  // 设置当前页码
  const setCurrentPage = (page) => {
    currentPage.value = page
  }

  // 设置每页显示数量
  const setPageSize = (size) => {
    pageSize.value = size
    // 每页数量变化时重置页码
    currentPage.value = 1
  }

  // 重置筛选条件
  const resetFilter = () => {
    filter.value = {
      search: '',
      status: '',
      dateRange: ''
    }
    currentPage.value = 1
  }

  return {
    commissions,
    totalCommissions,
    currentPage,
    pageSize,
    loading,
    error,
    filter,
    fetchCommissions,
    fetchCommissionDetail,
    updateCommissionStatus,
    setFilter,
    setCurrentPage,
    setPageSize,
    resetFilter
  }
})
