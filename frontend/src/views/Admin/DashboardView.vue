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

      <!-- 总工具包数 -->
      <div class="stat-card">
        <div class="stat-icon toolkit-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
            <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
          </svg>
        </div>
        <div class="stat-content">
          <h3>总工具包数</h3>
          <p class="stat-value">{{ totalToolkits }}</p>
          <p class="stat-change">+{{ toolkitGrowth }}% 较上月</p>
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
import { ref, onMounted } from 'vue'
import { useContentStore, useAuthStore } from '../../stores/index.js'

const contentStore = useContentStore()
const authStore = useAuthStore()

// 时间范围选择
const timeRange = ref('week')

// 统计数据（模拟）
const totalUsers = ref(1280)
const totalArticles = ref(542)
const totalToolkits = ref(85)
const totalOrders = ref(1235)

// 增长率（模拟）
const userGrowth = ref(12.5)
const articleGrowth = ref(8.3)
const toolkitGrowth = ref(25.7)
const orderGrowth = ref(18.9)

// 推广统计数据（模拟）
const totalClicks = ref(5678)
const totalCommission = ref(23456.78)
const totalAffiliates = ref(342)
const conversionRate = ref(4.2)

// 最近活动（模拟）
const recentActivities = ref([
  {
    iconClass: 'user-activity',
    iconPath: 'M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2',
    text: '用户 "张三" 注册成功',
    time: '刚刚'
  },
  {
    iconClass: 'order-activity',
    iconPath: 'M18 8h1a4 4 0 0 1 0 8h-1',
    text: '用户 "李四" 购买了 "新生儿护理工具包"',
    time: '15分钟前'
  },
  {
    iconClass: 'article-activity',
    iconPath: 'M4 19.5A2.5 2.5 0 0 1 6.5 17H20',
    text: '文章 "如何科学安排孕期饮食" 被发布',
    time: '1小时前'
  },
  {
    iconClass: 'affiliate-activity',
    iconPath: 'M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71',
    text: '推广链接 "ref=abc123" 产生了1笔订单',
    time: '2小时前'
  },
  {
    iconClass: 'user-activity',
    iconPath: 'M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2',
    text: '用户 "王五" 升级为VIP',
    time: '3小时前'
  }
])

// 页面加载时获取数据
onMounted(() => {
  // 这里可以添加获取实际数据的API调用
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