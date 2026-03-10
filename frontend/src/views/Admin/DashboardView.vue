<template>
  <div class="dashboard-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>仪表盘</h1>
      <p>欢迎使用母婴垂直网站管理后台</p>
    </div>

    <!-- 统计卡片区域 -->
    <div class="stats-grid">
      <!-- 总用户数 -->
      <div class="stat-card">
        <div class="stat-icon user-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
        </div>
        <div class="stat-content">
          <h3>总用户数</h3>
          <p class="stat-value">{{ totalUsers }}</p>
          <p class="stat-change">+{{ userGrowth }}% 较上月</p>
        </div>
      </div>

      <!-- 总文章数 -->
      <div class="stat-card">
        <div class="stat-icon article-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
          </svg>
        </div>
        <div class="stat-content">
          <h3>总文章数</h3>
          <p class="stat-value">{{ totalArticles }}</p>
          <p class="stat-change">+{{ articleGrowth }}% 较上月</p>
        </div>
      </div>

      <!-- 总智能体数 -->
      <div class="stat-card">
        <div class="stat-icon toolkit-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
            <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
          </svg>
        </div>
        <div class="stat-content">
          <h3>总智能体数</h3>
          <p class="stat-value">{{ totalAgents }}</p>
          <p class="stat-change">+{{ agentGrowth }}% 较上月</p>
        </div>
      </div>

      <!-- 总订单数 -->
      <div class="stat-card">
        <div class="stat-icon order-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
          </svg>
        </div>
        <div class="stat-content">
          <h3>总订单数</h3>
          <p class="stat-value">{{ totalOrders }}</p>
          <p class="stat-change">+{{ orderGrowth }}% 较上月</p>
        </div>
      </div>

      <!-- 总浏览量 -->
      <div class="stat-card">
        <div class="stat-icon view-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
            <circle cx="12" cy="12" r="3"></circle>
          </svg>
        </div>
        <div class="stat-content">
          <h3>总浏览量</h3>
          <p class="stat-value">{{ totalViews }}</p>
          <p class="stat-change">累计浏览次数</p>
        </div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="charts-grid">
      <!-- 用户增长趋势 -->
      <div class="chart-card">
        <div class="chart-header">
          <h3>用户增长趋势</h3>
          <div class="chart-controls">
            <button class="chart-btn" :class="{ active: timeRange === 'week' }" @click="timeRange = 'week'">本周</button>
            <button class="chart-btn" :class="{ active: timeRange === 'month' }" @click="timeRange = 'month'">本月</button>
            <button class="chart-btn" :class="{ active: timeRange === 'year' }" @click="timeRange = 'year'">今年</button>
          </div>
        </div>
        <div class="chart-content">
          <div class="chart-placeholder">
            <p>用户增长趋势图表</p>
          </div>
        </div>
      </div>

      <!-- 推广统计 -->
      <div class="chart-card">
        <div class="chart-header">
          <h3>推广统计</h3>
        </div>
        <div class="chart-content">
          <div class="stats-grid-inner">
            <div class="stat-item">
              <h4>总点击量</h4>
              <p>{{ totalClicks }}</p>
            </div>
            <div class="stat-item">
              <h4>总佣金</h4>
              <p>¥{{ totalCommission.toFixed(2) }}</p>
            </div>
            <div class="stat-item">
              <h4>推广用户</h4>
              <p>{{ totalAffiliates }}</p>
            </div>
            <div class="stat-item">
              <h4>转化率</h4>
              <p>{{ conversionRate }}%</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 最近活动 -->
    <div class="activity-card">
      <div class="card-header">
        <h3>最近活动</h3>
        <a href="#" class="view-all">查看全部</a>
      </div>
      <div class="activity-list">
        <div class="activity-item" v-for="(activity, index) in recentActivities" :key="index">
          <div class="activity-icon" :class="activity.iconClass">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path :d="activity.iconPath"></path>
            </svg>
          </div>
          <div class="activity-content">
            <p class="activity-text">{{ activity.text }}</p>
            <p class="activity-time">{{ activity.time }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useContentStore, useAuthStore } from '../../stores/index.js'
import apiClient from '../../utils/api'

const contentStore = useContentStore()
const authStore = useAuthStore()

// 检查用户登录状态和管理员权限
const currentUser = computed(() => authStore.currentUser)
const isAdmin = computed(() => authStore.isAdmin)
const isAuthenticated = computed(() => authStore.isAuthenticated)

// 时间范围选择
const timeRange = ref('week')

// 统计数据
const totalUsers = ref(0)
const totalArticles = ref(0)
const totalAgents = ref(0)
const totalOrders = ref(0)
const totalViews = ref(0)

// 增长率
const userGrowth = ref(0)
const articleGrowth = ref(0)
const agentGrowth = ref(0)
const orderGrowth = ref(0)

// 推广统计数据
const totalClicks = ref(0)
const totalCommission = ref(0)
const totalAffiliates = ref(0)
const conversionRate = ref(0)

// 最近活动
const recentActivities = ref([])

// 获取统计数据
const fetchDashboardStats = async () => {
  try {
    console.log('开始获取统计数据...')
    console.log('当前用户:', currentUser.value)
    console.log('是否已登录:', isAuthenticated.value)
    console.log('是否为管理员:', isAdmin.value)

    // 检查用户是否登录和管理员权限
    if (!isAuthenticated.value) {
      console.error('用户未登录')
      return
    }

    if (!isAdmin.value) {
      console.error('用户没有管理员权限')
      return
    }

    // 获取用户总数
    try {
      const usersResponse = await apiClient.get('/admin/users', { params: { limit: 10000 } })
      console.log('用户API响应:', usersResponse.data)
      totalUsers.value = usersResponse.data.total || usersResponse.data.data?.length || 0
      console.log('用户总数:', totalUsers.value)
    } catch (error) {
      console.error('获取用户总数失败:', error.response?.data || error.message)
      if (error.response?.status === 401 || error.response?.status === 403) {
        console.error('用户未登录或没有管理员权限')
      }
    }

    // 获取文章总数
    try {
      const articlesResponse = await apiClient.get('/articles')
      console.log('文章API响应:', articlesResponse.data)
      totalArticles.value = Array.isArray(articlesResponse.data) ? articlesResponse.data.length : articlesResponse.data.data?.length || 0
      console.log('文章总数:', totalArticles.value)
    } catch (error) {
      console.error('获取文章总数失败:', error.response?.data || error.message)
    }

    // 获取智能体总数
    try {
      const agentsResponse = await apiClient.get('/agents')
      console.log('智能体API响应:', agentsResponse.data)
      totalAgents.value = Array.isArray(agentsResponse.data) ? agentsResponse.data.length : agentsResponse.data.data?.length || 0
      console.log('智能体总数:', totalAgents.value)
    } catch (error) {
      console.error('获取智能体总数失败:', error.response?.data || error.message)
    }

    // 获取订单总数
    try {
      const ordersResponse = await apiClient.get('/admin/orders', { params: { limit: 10000 } })
      console.log('订单API响应:', ordersResponse.data)
      totalOrders.value = ordersResponse.data.total || ordersResponse.data.data?.length || 0
      console.log('订单总数:', totalOrders.value)
    } catch (error) {
      console.error('获取订单总数失败:', error.response?.data || error.message)
      if (error.response?.status === 401 || error.response?.status === 403) {
        console.error('用户未登录或没有管理员权限')
      }
    }

    // 获取推广统计
    try {
      const affiliateResponse = await apiClient.get('/admin/affiliate/stats')
      console.log('推广统计API响应:', affiliateResponse.data)
      const stats = affiliateResponse.data
      totalClicks.value = stats.total_clicks || 0
      totalCommission.value = stats.total_commission || 0
      totalAffiliates.value = stats.total_affiliates || 0
      conversionRate.value = stats.conversion_rate || 0
      console.log('推广统计:', { totalClicks: totalClicks.value, totalCommission: totalCommission.value })
    } catch (error) {
      console.error('获取推广统计失败:', error.response?.data || error.message)
      if (error.response?.status === 401 || error.response?.status === 403) {
        console.error('用户未登录或没有管理员权限')
      }
    }

    // 获取内容统计（包括总浏览量）
    try {
      const contentResponse = await apiClient.get('/admin/content/stats')
      console.log('内容统计API响应:', contentResponse.data)
      const contentStats = contentResponse.data
      totalViews.value = contentStats.total_views || 0
      console.log('内容统计:', { totalViews: totalViews.value })
    } catch (error) {
      console.error('获取内容统计失败:', error.response?.data || error.message)
      if (error.response?.status === 401 || error.response?.status === 403) {
        console.error('用户未登录或没有管理员权限')
      }
    }

    console.log('统计数据加载完成:', {
      totalUsers: totalUsers.value,
      totalArticles: totalArticles.value,
      totalAgents: totalAgents.value,
      totalOrders: totalOrders.value
    })
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 页面加载时获取数据
onMounted(() => {
  fetchDashboardStats()
  console.log('仪表盘页面加载完成')
})
</script>

<style scoped>
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* 页面标题 */
.page-header {
  margin-bottom: 30px;
}

.page-header h1 {
  margin: 0 0 10px 0;
  font-size: 28px;
  color: #303133;
}

.page-header p {
  margin: 0;
  color: #606266;
  font-size: 14px;
}

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 20px;
}

.user-icon {
  background-color: #409eff;
}

.article-icon {
  background-color: #67c23a;
}

.toolkit-icon {
  background-color: #e6a23c;
}

.order-icon {
  background-color: #f56c6c;
}

.view-icon {
  background-color: #909399;
}

.stat-content h3 {
  margin: 0 0 5px 0;
  font-size: 14px;
  color: #909399;
  font-weight: 400;
}

.stat-value {
  margin: 0 0 5px 0;
  font-size: 24px;
  color: #303133;
  font-weight: 600;
}

.stat-change {
  margin: 0;
  font-size: 12px;
  color: #67c23a;
}

/* 图表区域 */
.charts-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  margin-bottom: 30px;
}

.chart-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-header h3 {
  margin: 0;
  font-size: 16px;
  color: #303133;
}

.chart-controls {
  display: flex;
  gap: 10px;
}

.chart-btn {
  padding: 5px 15px;
  background-color: #f5f7fa;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  color: #606266;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.chart-btn:hover {
  background-color: #ecf5ff;
  border-color: #c6e2ff;
  color: #409eff;
}

.chart-btn.active {
  background-color: #409eff;
  border-color: #409eff;
  color: #fff;
}

.chart-content {
  height: 250px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-placeholder {
  width: 100%;
  height: 100%;
  background-color: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  color: #909399;
}

/* 内部统计网格 */
.stats-grid-inner {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  height: 100%;
}

.stat-item {
  background-color: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
  text-align: center;
}

.stat-item h4 {
  margin: 0 0 10px 0;
  font-size: 12px;
  color: #909399;
  font-weight: 400;
}

.stat-item p {
  margin: 0;
  font-size: 20px;
  color: #303133;
  font-weight: 600;
}

/* 活动卡片 */
.activity-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-header h3 {
  margin: 0;
  font-size: 16px;
  color: #303133;
}

.view-all {
  font-size: 14px;
  color: #409eff;
  text-decoration: none;
}

.view-all:hover {
  text-decoration: underline;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.activity-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 14px;
  flex-shrink: 0;
  margin-top: 2px;
}

.user-activity {
  background-color: #409eff;
}

.order-activity {
  background-color: #67c23a;
}

.article-activity {
  background-color: #e6a23c;
}

.affiliate-activity {
  background-color: #f56c6c;
}

.activity-content {
  flex: 1;
}

.activity-text {
  margin: 0 0 5px 0;
  font-size: 14px;
  color: #303133;
  line-height: 1.4;
}

.activity-time {
  margin: 0;
  font-size: 12px;
  color: #909399;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr 1fr;
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid-inner {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>