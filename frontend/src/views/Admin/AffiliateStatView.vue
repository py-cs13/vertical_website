<template>
  <div class="affiliate-stat-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>推广统计</h1>
      <div class="header-actions">
        <button class="export-btn" @click="handleExport">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="7 10 12 15 17 10"></polyline>
            <line x1="12" y1="15" x2="12" y2="3"></line>
          </svg>
          导出报表
        </button>
        <button class="refresh-btn" @click="refreshData">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="23 4 23 10 17 10"></polyline>
            <polyline points="1 20 1 14 7 14"></polyline>
            <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
          </svg>
          刷新数据
        </button>
      </div>
    </div>

    <!-- 筛选和统计时间 -->
    <div class="filter-section">
      <div class="date-filter">
        <button 
          class="date-btn" 
          :class="{ active: dateRange === '7d' }" 
          @click="setDateRange('7d')"
        >
          近7天
        </button>
        <button 
          class="date-btn" 
          :class="{ active: dateRange === '30d' }" 
          @click="setDateRange('30d')"
        >
          近30天
        </button>
        <button 
          class="date-btn" 
          :class="{ active: dateRange === '90d' }" 
          @click="setDateRange('90d')"
        >
          近90天
        </button>
        <button 
          class="date-btn" 
          :class="{ active: dateRange === 'custom' }" 
          @click="setDateRange('custom')"
        >
          自定义
        </button>
      </div>

      <div class="custom-date" v-if="dateRange === 'custom'">
        <input type="date" v-model="customStartDate" @change="updateCustomDateRange">
        <span>至</span>
        <input type="date" v-model="customEndDate" @change="updateCustomDateRange">
        <button class="apply-btn" @click="applyCustomDateRange">
          应用
        </button>
      </div>

      <div class="stat-type">
        <button 
          class="type-btn" 
          :class="{ active: statType === 'clicks' }" 
          @click="setStatType('clicks')"
        >
          点击量
        </button>
        <button 
          class="type-btn" 
          :class="{ active: statType === 'conversions' }" 
          @click="setStatType('conversions')"
        >
          转化率
        </button>
        <button 
          class="type-btn" 
          :class="{ active: statType === 'commissions' }" 
          @click="setStatType('commissions')"
        >
          佣金收入
        </button>
      </div>
    </div>

    <!-- 统计概览卡片 -->
    <div class="stat-overview">
      <div class="stat-card">
        <div class="stat-header">
          <h3>总点击量</h3>
          <span class="stat-change" :class="overallStats.clicksChange > 0 ? 'positive' : 'negative'">
            {{ overallStats.clicksChange > 0 ? '+' : '' }}{{ overallStats.clicksChange }}%
          </span>
        </div>
        <div class="stat-value">{{ formatNumber(overallStats.totalClicks) }}</div>
        <div class="stat-desc">相比上周同期</div>
      </div>

      <div class="stat-card">
        <div class="stat-header">
          <h3>总转化量</h3>
          <span class="stat-change" :class="overallStats.conversionsChange > 0 ? 'positive' : 'negative'">
            {{ overallStats.conversionsChange > 0 ? '+' : '' }}{{ overallStats.conversionsChange }}%
          </span>
        </div>
        <div class="stat-value">{{ formatNumber(overallStats.totalConversions) }}</div>
        <div class="stat-desc">相比上周同期</div>
      </div>

      <div class="stat-card">
        <div class="stat-header">
          <h3>平均转化率</h3>
          <span class="stat-change" :class="overallStats.conversionRateChange > 0 ? 'positive' : 'negative'">
            {{ overallStats.conversionRateChange > 0 ? '+' : '' }}{{ overallStats.conversionRateChange }}%
          </span>
        </div>
        <div class="stat-value">{{ overallStats.averageConversionRate }}%</div>
        <div class="stat-desc">相比上周同期</div>
      </div>

      <div class="stat-card">
        <div class="stat-header">
          <h3>总佣金金额</h3>
          <span class="stat-change" :class="overallStats.commissionsChange > 0 ? 'positive' : 'negative'">
            {{ overallStats.commissionsChange > 0 ? '+' : '' }}{{ overallStats.commissionsChange }}%
          </span>
        </div>
        <div class="stat-value">¥{{ formatNumber(overallStats.totalCommissions, 2) }}</div>
        <div class="stat-desc">相比上周同期</div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="chart-section">
      <div class="chart-card">
        <div class="chart-header">
          <h3>{{ chartTitle }}</h3>
        </div>
        <div class="chart-container">
          <PromotionChart 
            :chart-type="chartType"
            :title="chartTitle"
            :chart-data="formattedChartData"
          />
        </div>
      </div>
    </div>

    <!-- 推广用户排名 -->
    <div class="ranking-section">
      <div class="section-header">
        <h3>推广用户排名</h3>
        <select v-model="rankingSort" @change="updateRanking">
          <option value="clicks">按点击量</option>
          <option value="conversions">按转化量</option>
          <option value="commission_amount">按佣金金额</option>
        </select>
      </div>
      
      <div class="ranking-list">
        <div class="ranking-header">
          <div class="rank-col">排名</div>
          <div class="user-col">推广用户</div>
          <div class="clicks-col">点击量</div>
          <div class="conversions-col">转化量</div>
          <div class="rate-col">转化率</div>
          <div class="commission-col">佣金金额</div>
          <div class="action-col">操作</div>
        </div>
        
        <div 
          v-for="(affiliate, index) in sortedAffiliates" 
          :key="affiliate.id" 
          class="ranking-item"
          :class="{ top3: index < 3 }"
        >
          <div class="rank-col">
            <div class="rank-number" :class="{ 
              first: index === 0, 
              second: index === 1, 
              third: index === 2 
            }">
              {{ index + 1 }}
            </div>
          </div>
          <div class="user-col">
            <div class="user-info">
              <img class="user-avatar" :src="affiliate.user?.avatar_url || '/avatar-placeholder.png'" alt="用户头像">
              <div class="user-details">
                <div class="username">{{ affiliate.user?.username }}</div>
                <div class="email">{{ affiliate.user?.email }}</div>
              </div>
            </div>
          </div>
          <div class="clicks-col">{{ formatNumber(affiliate.clicks) }}</div>
          <div class="conversions-col">{{ formatNumber(affiliate.conversions) }}</div>
          <div class="rate-col">{{ affiliate.conversion_rate }}%</div>
          <div class="commission-col">¥{{ formatNumber(affiliate.commission_amount, 2) }}</div>
          <div class="action-col">
            <button class="detail-btn" @click="viewAffiliateDetail(affiliate)">
              详情
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 佣金结算统计 -->
    <div class="commission-section">
      <div class="section-header">
        <h3>佣金结算统计</h3>
        <button class="settle-btn" @click="handleSettlement">
          结算佣金
        </button>
      </div>
      
      <div class="commission-stats">
        <div class="commission-card">
          <div class="commission-title">待结算佣金</div>
          <div class="commission-value">¥{{ formatNumber(commissionStats.pending, 2) }}</div>
          <div class="commission-count">{{ commissionStats.pending_count }}笔订单</div>
        </div>
        
        <div class="commission-card">
          <div class="commission-title">已结算佣金</div>
          <div class="commission-value">¥{{ formatNumber(commissionStats.paid, 2) }}</div>
          <div class="commission-count">{{ commissionStats.paid_count }}笔订单</div>
        </div>
        
        <div class="commission-card">
          <div class="commission-title">已取消佣金</div>
          <div class="commission-value">¥{{ formatNumber(commissionStats.cancelled, 2) }}</div>
          <div class="commission-count">{{ commissionStats.cancelled_count }}笔订单</div>
        </div>
        
        <div class="commission-card">
          <div class="commission-title">本月预计收入</div>
          <div class="commission-value">¥{{ formatNumber(commissionStats.expected, 2) }}</div>
          <div class="commission-count">预估数据</div>
        </div>
      </div>
    </div>

    <!-- 推广渠道分析 -->
    <div class="channel-section">
      <div class="section-header">
        <h3>推广渠道分析</h3>
      </div>
      
      <div class="channel-stats">
        <div class="channel-chart">
          <!-- 这里可以集成饼图或环形图 -->
          <div class="chart-placeholder">
            <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="300" viewBox="0 0 400 300">
              <!-- 环形图 -->
              <g transform="translate(200, 150)">
                <!-- 微信 -->
                <path d="M0,0 v-100 A100,100 0 0,1 86.6,-50 L51.96,-30 A60,60 0 0,0 0,-60 z" fill="#409eff"></path>
                <!-- 微博 -->
                <path d="M86.6,-50 v0 A100,100 0 0,1 30,-95.39 L18,-57.24 A60,60 0 0,0 51.96,-30 z" fill="#67c23a"></path>
                <!-- 朋友圈 -->
                <path d="M30,-95.39 v0 A100,100 0 0,1 -50,-86.6 L-30,-51.96 A60,60 0 0,0 18,-57.24 z" fill="#e6a23c"></path>
                <!-- 其他 -->
                <path d="M-50,-86.6 v0 A100,100 0 0,1 -86.6,50 L-51.96,30 A60,60 0 0,0 -30,-51.96 z" fill="#f56c6c"></path>
                <!-- 中心圆 -->
                <circle cx="0" cy="0" r="60" fill="#fff"></circle>
                <!-- 中心文本 -->
                <text x="0" y="0" font-size="20" font-weight="bold" fill="#303133" text-anchor="middle" dominant-baseline="middle">56%</text>
                <text x="0" y="25" font-size="12" fill="#909399" text-anchor="middle">转化率</text>
              </g>
              
              <!-- 图例 -->
              <g transform="translate(150, 250)">
                <rect x="0" y="0" width="12" height="12" fill="#409eff" rx="2" ry="2"></rect>
                <text x="20" y="10" font-size="12" fill="#606266">微信 (45%)</text>
                
                <rect x="100" y="0" width="12" height="12" fill="#67c23a" rx="2" ry="2"></rect>
                <text x="120" y="10" font-size="12" fill="#606266">微博 (25%)</text>
                
                <rect x="200" y="0" width="12" height="12" fill="#e6a23c" rx="2" ry="2"></rect>
                <text x="220" y="10" font-size="12" fill="#606266">朋友圈 (20%)</text>
                
                <rect x="300" y="0" width="12" height="12" fill="#f56c6c" rx="2" ry="2"></rect>
                <text x="320" y="10" font-size="12" fill="#606266">其他 (10%)</text>
              </g>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- 推广链接详情模态框 -->
    <div v-if="showAffiliateDetail" class="modal-overlay" @click="closeAffiliateDetail">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>推广用户详情</h3>
          <button class="close-btn" @click="closeAffiliateDetail">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div v-if="currentAffiliate" class="affiliate-detail">
            <!-- 用户基本信息 -->
            <div class="detail-section">
              <h4>用户信息</h4>
              <div class="user-detail">
                <img class="user-avatar" :src="currentAffiliate.user?.avatar_url || '/avatar-placeholder.png'" alt="用户头像">
                <div class="user-info">
                  <div class="user-name">{{ currentAffiliate.user?.username }}</div>
                  <div class="user-nickname">{{ currentAffiliate.user?.nickname || '-' }}</div>
                  <div class="user-email">{{ currentAffiliate.user?.email }}</div>
                  <div class="user-registered">注册时间: {{ formatDate(currentAffiliate.user?.created_at) }}</div>
                </div>
              </div>
            </div>

            <!-- 推广数据 -->
            <div class="detail-section">
              <h4>推广数据</h4>
              <div class="stat-grid">
                <div class="stat-item">
                  <div class="stat-label">总点击量</div>
                  <div class="stat-value">{{ formatNumber(currentAffiliate.clicks) }}</div>
                </div>
                <div class="stat-item">
                  <div class="stat-label">总转化量</div>
                  <div class="stat-value">{{ formatNumber(currentAffiliate.conversions) }}</div>
                </div>
                <div class="stat-item">
                  <div class="stat-label">转化率</div>
                  <div class="stat-value">{{ currentAffiliate.conversion_rate }}%</div>
                </div>
                <div class="stat-item">
                  <div class="stat-label">总佣金金额</div>
                  <div class="stat-value">¥{{ formatNumber(currentAffiliate.commission_amount, 2) }}</div>
                </div>
                <div class="stat-item">
                  <div class="stat-label">推广链接</div>
                  <div class="stat-value link-value">
                    <code>{{ currentAffiliate.link }}</code>
                  </div>
                </div>
              </div>
            </div>

            <!-- 佣金结算记录 -->
            <div class="detail-section">
              <h4>佣金结算记录</h4>
              <div class="commission-table-container">
                <table class="commission-table">
                  <thead>
                    <tr>
                      <th>结算时间</th>
                      <th>结算金额</th>
                      <th>结算状态</th>
                      <th>结算方式</th>
                      <th>操作</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="record in currentAffiliate.commission_records" :key="record.id">
                      <td>{{ formatDate(record.settlement_date) }}</td>
                      <td>¥{{ formatNumber(record.amount, 2) }}</td>
                      <td>
                        <span class="status-tag" :class="record.status">
                          {{ getSettlementStatusText(record.status) }}
                        </span>
                      </td>
                      <td>{{ record.payment_method }}</td>
                      <td>
                        <button class="view-btn" @click="viewSettlementDetail(record)">
                          查看
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import Swal from 'sweetalert2'
import { useAffiliateStatStore } from '../../stores/index.js'
import PromotionChart from '@/components/PromotionChart.vue'

// 获取store实例
const statStore = useAffiliateStatStore()

// 日期范围
const dateRange = ref('7d')
const customStartDate = ref('')
const customEndDate = ref('')

// 统计类型
const statType = ref('clicks')

// 排名排序
const rankingSort = ref('clicks')

// 图表类型：bar（柱状图）或 line（折线图）
const chartType = ref('bar')

// 模态框
const showAffiliateDetail = ref(false)
const currentAffiliate = ref(null)

// 从store获取数据
const overallStats = computed(() => statStore.affiliateStats)
const affiliates = computed(() => statStore.affiliateUsers)
const commissionStats = computed(() => statStore.commissionStats)
const loading = computed(() => statStore.loading)

// 监听日期范围变化
watch(dateRange, (newRange) => {
  statStore.setDateRange(newRange)
  if (newRange !== 'custom') {
    updateStats()
  }
})

// 监听统计类型变化
watch(statType, (newType) => {
  statStore.setStatType(newType)
  updateStats()
})

// 排序后的推广用户
const sortedAffiliates = computed(() => {
  const sorted = [...affiliates.value]
  sorted.sort((a, b) => {
    if (rankingSort.value === 'clicks' || rankingSort.value === 'conversions') {
      return b[rankingSort.value] - a[rankingSort.value]
    } else if (rankingSort.value === 'commission_amount') {
      return b.commission_amount - a.commission_amount
    } else {
      return 0
    }
  })
  return sorted
})

// 图表标题
const chartTitle = computed(() => {
  if (selectedStatType.value === 'clicks') {
    return '推广点击量趋势'
  } else if (selectedStatType.value === 'conversions') {
    return '推广转化率趋势'
  } else {
    return '推广佣金收入趋势'
  }
})

// 格式化图表数据
const formattedChartData = computed(() => {
  if (!statStore.affiliateStats || !statStore.affiliateStats.date_series) {
    return {
      labels: [],
      datasets: []
    }
  }
  
  const { date_series, clicks, conversions, commissions } = statStore.affiliateStats
  
  // 准备数据集
  const datasets = []
  
  // 根据统计类型添加对应的数据
  if (selectedStatType.value === 'clicks') {
    datasets.push({
      label: '点击量',
      data: clicks,
      backgroundColor: '#409eff',
      borderColor: '#409eff',
      borderWidth: 1
    })
    
    // 添加转化量作为折线
    datasets.push({
      label: '转化量',
      data: conversions,
      backgroundColor: 'rgba(103, 194, 58, 0.1)',
      borderColor: '#67c23a',
      borderWidth: 2,
      type: 'line',
      fill: false,
      tension: 0.4
    })
  } else if (selectedStatType.value === 'conversions') {
    datasets.push({
      label: '转化量',
      data: conversions,
      backgroundColor: '#67c23a',
      borderColor: '#67c23a',
      borderWidth: 1
    })
  } else if (selectedStatType.value === 'commission') {
    datasets.push({
      label: '佣金金额',
      data: commissions,
      backgroundColor: '#e6a23c',
      borderColor: '#e6a23c',
      borderWidth: 1
    })
  }
  
  return {
    labels: date_series,
    datasets: datasets
  }
})

// 格式化数字
const formatNumber = (num, decimals = 0) => {
  if (num === null || num === undefined) return '-'
  return num.toLocaleString('zh-CN', { 
    minimumFractionDigits: decimals, 
    maximumFractionDigits: decimals 
  })
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

// 设置日期范围
const setDateRange = (range) => {
  dateRange.value = range
  if (range !== 'custom') {
    // 根据范围设置开始和结束日期
    const endDate = new Date()
    const startDate = new Date()
    
    if (range === '7d') {
      startDate.setDate(endDate.getDate() - 7)
    } else if (range === '30d') {
      startDate.setDate(endDate.getDate() - 30)
    } else if (range === '90d') {
      startDate.setDate(endDate.getDate() - 90)
    }
    
    customStartDate.value = startDate.toISOString().split('T')[0]
    customEndDate.value = endDate.toISOString().split('T')[0]
    
    // 更新数据
    updateStats()
  }
}

// 更新自定义日期范围
const updateCustomDateRange = () => {
  // 可以在这里添加日期验证逻辑
}

// 应用自定义日期范围
const applyCustomDateRange = () => {
  if (!customStartDate.value || !customEndDate.value) {
    Swal.fire('提示', '请选择完整的日期范围', 'warning')
    return
  }
  
  // 更新store的筛选参数
  statStore.setFilterParams({
    startDate: customStartDate.value,
    endDate: customEndDate.value
  })
  
  updateStats()
}

// 设置统计类型
const setStatType = (type) => {
  statType.value = type
  updateStats()
}

// 更新排名
const updateRanking = () => {
  // 排名会通过计算属性自动更新
}

// 刷新数据
const refreshData = async () => {
  try {
    await updateStats()
    Swal.fire('刷新成功', '数据已更新', 'success')
  } catch (error) {
    console.error('刷新数据失败:', error)
    Swal.fire('错误', '刷新数据失败', 'error')
  }
}

// 导出报表
const handleExport = async () => {
  try {
    const data = await statStore.exportAffiliateStats()
    // 创建下载链接
    const url = window.URL.createObjectURL(new Blob([data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `推广统计报表_${new Date().toISOString().split('T')[0]}.xlsx`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    Swal.fire('导出成功', '报表已下载', 'success')
  } catch (error) {
    console.error('导出报表失败:', error)
    Swal.fire('错误', '导出报表失败', 'error')
  }
}

// 结算佣金
const handleSettlement = async () => {
  const result = await Swal.fire({
    title: '确定要结算所有待结算佣金吗？',
    text: '结算后将生成结算记录并发送到用户账户',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#6c757d',
    confirmButtonText: '确认结算',
    cancelButtonText: '取消'
  })

  if (result.isConfirmed) {
    try {
      await statStore.settleCommissions()
      await updateStats() // 刷新数据
      Swal.fire('结算成功', '所有待结算佣金已处理', 'success')
    } catch (error) {
      console.error('结算佣金失败:', error)
      Swal.fire('错误', '结算佣金失败', 'error')
    }
  }
}

// 查看推广用户详情
const viewAffiliateDetail = (affiliate) => {
  currentAffiliate.value = affiliate
  showAffiliateDetail.value = true
}

// 关闭推广用户详情
const closeAffiliateDetail = () => {
  showAffiliateDetail.value = false
  setTimeout(() => {
    currentAffiliate.value = null
  }, 300)
}

// 查看结算详情
const viewSettlementDetail = (record) => {
  // 这里可以添加查看结算详情的逻辑
  console.log('查看结算详情:', record)
}

// 获取结算状态文本
const getSettlementStatusText = (status) => {
  const statusMap = {
    'pending': '待结算',
    'paid': '已支付',
    'cancelled': '已取消'
  }
  return statusMap[status] || status
}

// 更新统计数据
const updateStats = async () => {
  try {
    await statStore.refreshAllData()
  } catch (error) {
    console.error('更新统计数据失败:', error)
    Swal.fire('错误', '获取统计数据失败', 'error')
  }
}

// 更新图表
const updateChart = () => {
  // 这里可以添加根据统计类型更新图表的逻辑
  console.log('更新图表:', statType.value)
}

// 页面加载时初始化数据
onMounted(async () => {
  // 设置默认日期范围
  setDateRange('7d')
  
  // 获取初始数据
  await updateStats()
})
</script>

<style scoped>
.affiliate-stat-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* 页面标题 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.page-header h1 {
  margin: 0;
  font-size: 24px;
  color: #303133;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.export-btn,
.refresh-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.export-btn {
  background-color: #67c23a;
  color: #fff;
}

.export-btn:hover {
  background-color: #85ce61;
}

.refresh-btn {
  background-color: #409eff;
  color: #fff;
}

.refresh-btn:hover {
  background-color: #66b1ff;
}

/* 筛选区域 */
.filter-section {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  align-items: center;
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.date-filter {
  display: flex;
  gap: 8px;
}

.date-btn {
  padding: 6px 12px;
  background-color: #fff;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.date-btn.active {
  background-color: #409eff;
  color: #fff;
  border-color: #409eff;
}

.date-btn:hover:not(.active) {
  background-color: #ecf5ff;
  border-color: #c6e2ff;
  color: #409eff;
}

.custom-date {
  display: flex;
  align-items: center;
  gap: 8px;
}

.custom-date input {
  padding: 6px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
}

.custom-date span {
  color: #606266;
}

.apply-btn {
  padding: 6px 12px;
  background-color: #409eff;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.apply-btn:hover {
  background-color: #66b1ff;
}

.stat-type {
  display: flex;
  gap: 8px;
  margin-left: auto;
}

.type-btn {
  padding: 6px 12px;
  background-color: #fff;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.type-btn.active {
  background-color: #67c23a;
  color: #fff;
  border-color: #67c23a;
}

.type-btn:hover:not(.active) {
  background-color: #f0f9eb;
  border-color: #d9f7be;
  color: #67c23a;
}

/* 统计概览卡片 */
.stat-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.stat-header h3 {
  margin: 0;
  font-size: 16px;
  color: #909399;
}

.stat-change {
  font-size: 12px;
  font-weight: 600;
}

.stat-change.positive {
  color: #67c23a;
}

.stat-change.negative {
  color: #f56c6c;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 5px;
}

.stat-desc {
  font-size: 12px;
  color: #909399;
}

/* 图表区域 */
.chart-section {
  margin-bottom: 30px;
}

.chart-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.chart-header {
  margin-bottom: 20px;
}

.chart-header h3 {
  margin: 0;
  font-size: 18px;
  color: #303133;
}

.chart-container {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-placeholder {
  width: 100%;
  height: 100%;
}

/* 推广用户排名 */
.ranking-section {
  margin-bottom: 30px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.section-header h3 {
  margin: 0;
  font-size: 18px;
  color: #303133;
}

.section-header select {
  padding: 6px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
}

.ranking-list {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.ranking-header {
  display: grid;
  grid-template-columns: 60px 1fr 120px 120px 100px 150px 80px;
  padding: 12px 15px;
  background-color: #f5f7fa;
  font-weight: 600;
  color: #303133;
  font-size: 14px;
}

.ranking-item {
  display: grid;
  grid-template-columns: 60px 1fr 120px 120px 100px 150px 80px;
  padding: 15px;
  border-bottom: 1px solid #ebeef5;
  transition: background-color 0.3s ease;
}

.ranking-item:hover {
  background-color: #f5f7fa;
}

.ranking-item.top3 {
  background-color: #f0f9eb;
}

.rank-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  font-weight: bold;
  color: #909399;
}

.rank-number.first {
  background-color: #e6a23c;
  color: #fff;
}

.rank-number.second {
  background-color: #909399;
  color: #fff;
}

.rank-number.third {
  background-color: #f56c6c;
  color: #fff;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.username {
  color: #303133;
  font-weight: 500;
}

.email {
  color: #909399;
  font-size: 12px;
}

.detail-btn {
  padding: 4px 10px;
  background-color: #409eff;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.detail-btn:hover {
  background-color: #66b1ff;
}

/* 佣金结算统计 */
.commission-section {
  margin-bottom: 30px;
}

.commission-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}

.commission-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  text-align: center;
}

.commission-title {
  color: #909399;
  font-size: 14px;
  margin-bottom: 10px;
}

.commission-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 5px;
}

.commission-count {
  color: #909399;
  font-size: 12px;
}

.settle-btn {
  padding: 8px 16px;
  background-color: #409eff;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.settle-btn:hover {
  background-color: #66b1ff;
}

/* 推广渠道分析 */
.channel-section {
  margin-bottom: 30px;
}

.channel-stats {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.channel-chart {
  height: 350px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 模态框 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background-color: #fff;
  border-radius: 8px;
  width: 100%;
  max-width: 700px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #ebeef5;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  color: #303133;
}

.close-btn {
  background: none;
  border: none;
  font-size: 18px;
  color: #909399;
  cursor: pointer;
  transition: color 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 4px;
}

.close-btn:hover {
  color: #606266;
  background-color: #f5f7fa;
}

.modal-body {
  padding: 20px;
}

/* 推广用户详情 */
.affiliate-detail {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-section {
  background-color: #f5f7fa;
  border-radius: 8px;
  padding: 15px;
}

.detail-section h4 {
  margin: 0 0 15px 0;
  font-size: 16px;
  color: #303133;
}

.user-detail {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-detail .user-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
}

.user-detail .user-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.user-name {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.user-nickname {
  font-size: 14px;
  color: #909399;
}

.user-email {
  font-size: 14px;
  color: #409eff;
}

.user-registered {
  font-size: 12px;
  color: #909399;
}

.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.stat-item {
  background-color: #fff;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
}

.stat-label {
  color: #909399;
  font-size: 14px;
  margin-bottom: 8px;
}

.stat-value {
  color: #303133;
  font-size: 20px;
  font-weight: bold;
}

.link-value {
  word-break: break-all;
}

.commission-table-container {
  overflow-x: auto;
}

.commission-table {
  width: 100%;
  border-collapse: collapse;
}

.commission-table th,
.commission-table td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid #ebeef5;
  font-size: 14px;
}

.commission-table th {
  background-color: #ecf5ff;
  font-weight: 600;
  color: #303133;
}

.commission-table td {
  color: #606266;
}

.status-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.status-tag.pending {
  background-color: #e6a23c;
  color: #fff;
}

.status-tag.paid {
  background-color: #67c23a;
  color: #fff;
}

.status-tag.cancelled {
  background-color: #f56c6c;
  color: #fff;
}

.view-btn {
  padding: 4px 10px;
  background-color: #409eff;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.view-btn:hover {
  background-color: #66b1ff;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .ranking-header,
  .ranking-item {
    grid-template-columns: 60px 1fr 100px 100px 80px 120px 80px;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .filter-section {
    flex-direction: column;
    align-items: stretch;
  }
  
  .stat-type {
    margin-left: 0;
    justify-content: center;
  }
  
  .stat-overview {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .commission-stats {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .ranking-header,
  .ranking-item {
    grid-template-columns: 60px 1fr;
    gap: 10px;
  }
  
  .clicks-col,
  .conversions-col,
  .rate-col,
  .commission-col,
  .action-col {
    display: none;
  }
  
  .user-detail {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>