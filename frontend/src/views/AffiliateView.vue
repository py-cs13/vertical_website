<template>
  <div class="affiliate-container">
    <div class="affiliate-header">
      <h1>联盟推广系统</h1>
      <p>通过分享你的专属推广链接，获取丰厚佣金奖励</p>
    </div>
    
    <!-- 推广链接生成与管理 -->
    <div class="affiliate-section">
      <h2>我的推广链接</h2>
      <div class="affiliate-link-card" v-if="affiliateLink">
        <div class="link-info">
          <label>专属推广链接:</label>
          <div class="link-input-group">
            <input type="text" v-model="affiliateLink.link" readonly>
            <button @click="copyLink" class="btn btn-primary">复制链接</button>
          </div>
        </div>
        <div class="link-status">
          <span class="status-indicator" :class="{ 'active': affiliateLink.is_active }">
            {{ affiliateLink.is_active ? '已激活' : '已停用' }}
          </span>
        </div>
      </div>
      <div v-else>
        <button @click="generateAffiliateLink" class="btn btn-primary btn-large">生成推广链接</button>
        <p class="help-text">点击按钮生成你的专属推广链接</p>
      </div>
    </div>
    
    <!-- 推广统计 -->
    <div class="affiliate-section">
      <h2>推广统计</h2>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-number">{{ stats.click_count || 0 }}</div>
          <div class="stat-label">总点击次数</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ formatCurrency(stats.commission_total || 0) }}</div>
          <div class="stat-label">已结算佣金</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ formatCurrency(stats.pending_commission || 0) }}</div>
          <div class="stat-label">待结算佣金</div>
        </div>
      </div>
    </div>
    
    <!-- 佣金记录 -->
    <div class="affiliate-section">
      <h2>佣金记录</h2>
      <div class="commission-list" v-if="commissions.length > 0">
        <div class="commission-item" v-for="commission in commissions" :key="commission.id">
          <div class="commission-info">
            <div class="commission-order">订单 #{{ commission.order_id }}</div>
            <div class="commission-date">{{ formatDate(commission.created_at) }}</div>
          </div>
          <div class="commission-amount">{{ formatCurrency(commission.amount) }}</div>
          <div class="commission-status" :class="commission.status">
            {{ statusText[commission.status] }}
          </div>
        </div>
      </div>
      <div v-else class="no-data">
        <p>暂无佣金记录</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/index'
import Swal from 'sweetalert2'
import { formatDate } from '../utils/formatters'

const userStore = useAuthStore()
const router = useRouter()
const affiliateLink = ref(null)
const stats = ref({})
const commissions = ref([])

const statusText = {
  'pending': '待结算',
  'paid': '已结算',
  'cancelled': '已取消'
}

// 生成推广链接
const generateAffiliateLink = async () => {
  try {
    const response = await fetch('/api/affiliate/links', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${userStore.token}`
      }
    })
    
    if (!response.ok) throw new Error('生成推广链接失败')
    
    const data = await response.json()
    affiliateLink.value = data.data
    
    Swal.fire({
      icon: 'success',
      title: '推广链接生成成功',
      text: '你可以开始分享这个链接获取佣金了！'
    })
  } catch (error) {
    Swal.fire({
      icon: 'error',
      title: '错误',
      text: error.message || '生成推广链接时发生错误'
    })
  }
}

// 获取推广链接
const getAffiliateLink = async () => {
  try {
    const response = await fetch('/api/affiliate/links', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${userStore.token}`
      }
    })
    
    if (response.ok) {
      const data = await response.json()
      affiliateLink.value = data.data
    }
  } catch (error) {
    console.error('获取推广链接失败:', error)
  }
}

// 获取推广统计数据
const getAffiliateStats = async () => {
  try {
    const response = await fetch('/api/affiliate/stats', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${userStore.token}`
      }
    })
    
    if (response.ok) {
      const data = await response.json()
      stats.value = data.data
    }
  } catch (error) {
    console.error('获取推广统计数据失败:', error)
  }
}

// 获取佣金记录
const getAffiliateCommissions = async () => {
  try {
    const response = await fetch('/api/affiliate/commissions', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${userStore.token}`
      }
    })
    
    if (response.ok) {
      const data = await response.json()
      commissions.value = data.data
    }
  } catch (error) {
    console.error('获取佣金记录失败:', error)
  }
}

// 复制推广链接
const copyLink = () => {
  if (affiliateLink.value?.link) {
    navigator.clipboard.writeText(affiliateLink.value.link)
      .then(() => {
        Swal.fire({
          icon: 'success',
          title: '链接已复制',
          text: '推广链接已成功复制到剪贴板'
        })
      })
      .catch(() => {
        Swal.fire({
          icon: 'error',
          title: '复制失败',
          text: '无法复制链接，请手动复制'
        })
      })
  }
}



// 格式化货币
const formatCurrency = (amount) => {
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency: 'CNY'
  }).format(amount)
}

// 页面加载时获取推广数据
onMounted(async () => {
  await getAffiliateLink()
  await getAffiliateStats()
  await getAffiliateCommissions()
})
</script>

<style scoped>
.affiliate-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.affiliate-header {
  text-align: center;
  margin-bottom: 40px;
}

.affiliate-header h1 {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 10px;
}

.affiliate-header p {
  font-size: 1.1rem;
  color: #666;
}

.affiliate-section {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 20px;
  margin-bottom: 30px;
}

.affiliate-section h2 {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #f0f0f0;
}

.affiliate-link-card {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}

.link-info label {
  display: block;
  font-weight: bold;
  margin-bottom: 10px;
  color: #555;
}

.link-input-group {
  display: flex;
  gap: 10px;
  align-items: center;
}

.link-input-group input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.link-status {
  margin-top: 15px;
}

.status-indicator {
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: bold;
}

.status-indicator.active {
  background-color: #d4edda;
  color: #155724;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.stat-card {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.stat-number {
  font-size: 2.5rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.stat-label {
  font-size: 1rem;
  color: #666;
}

.commission-list {
  background-color: #f9f9f9;
  border-radius: 8px;
  overflow: hidden;
}

.commission-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #e9e9e9;
}

.commission-item:last-child {
  border-bottom: none;
}

.commission-info {
  flex: 1;
}

.commission-order {
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.commission-date {
  font-size: 0.9rem;
  color: #666;
}

.commission-amount {
  font-size: 1.2rem;
  font-weight: bold;
  color: #333;
  margin-right: 20px;
}

.commission-status {
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: bold;
}

.commission-status.pending {
  background-color: #fff3cd;
  color: #856404;
}

.commission-status.paid {
  background-color: #d4edda;
  color: #155724;
}

.commission-status.cancelled {
  background-color: #f8d7da;
  color: #721c24;
}

.no-data {
  text-align: center;
  padding: 40px;
  color: #666;
}

.help-text {
  color: #666;
  margin-top: 10px;
  font-size: 0.9rem;
}
</style>