<template>
  <div class="order-management-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>订单管理</h1>
      <div class="header-actions">
        <button class="export-btn" @click="handleExport">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="7 10 12 15 17 10"></polyline>
            <line x1="12" y1="15" x2="12" y2="3"></line>
          </svg>
          导出订单
        </button>
        <button class="search-btn" @click="openAdvancedSearch">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          高级搜索
        </button>
      </div>
    </div>

    <!-- 搜索和筛选 -->
    <div class="filter-section">
      <div class="search-box">
        <input 
          type="text" 
          placeholder="搜索订单号、用户、产品名称" 
          v-model="searchQuery"
          @input="handleSearch"
        >
        <button class="search-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </button>
      </div>

      <div class="filter-controls">
        <select v-model="statusFilter" @change="handleFilter">
          <option value="">所有状态</option>
          <option value="pending">待支付</option>
          <option value="paid">已支付</option>
          <option value="cancelled">已取消</option>
          <option value="refunded">已退款</option>
        </select>

        <select v-model="sortBy" @change="handleSort">
          <option value="created_at">创建时间</option>
          <option value="total_amount">订单金额</option>
          <option value="status">订单状态</option>
        </select>

        <div class="date-range">
          <input type="date" v-model="dateRange.start" @change="handleFilter">
          <span>至</span>
          <input type="date" v-model="dateRange.end" @change="handleFilter">
        </div>

        <button class="filter-btn" @click="resetFilters">
          重置筛选
        </button>
      </div>
    </div>

    <!-- 订单列表 -->
    <div class="table-container">
      <table class="order-table">
        <thead>
          <tr>
            <th>
              <input type="checkbox" @change="toggleSelectAll">
            </th>
            <th>订单号</th>
            <th>用户</th>
            <th>产品</th>
            <th>金额</th>
            <th>支付方式</th>
            <th>状态</th>
            <th>创建时间</th>
            <th>完成时间</th>
            <th>来源</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in filteredOrders" :key="order.id" :class="{ selected: selectedOrders.includes(order.id) }">
            <td>
              <input type="checkbox" :checked="selectedOrders.includes(order.id)" @change="toggleSelect(order.id)">
            </td>
            <td>
              <a class="order-id" @click="viewOrderDetail(order)">
                {{ order.order_number }}
              </a>
            </td>
            <td>
              <div class="user-info">
                <img class="user-avatar" :src="order.user?.avatar_url || '/avatar-placeholder.png'" alt="用户头像">
                <div class="user-details">
                  <div>{{ order.user?.username }}</div>
                  <div class="user-email">{{ order.user?.email }}</div>
                </div>
              </div>
            </td>
            <td>
              <div class="product-list">
                <div v-for="item in order.items" :key="item.id" class="product-item">
                  <div class="product-name">{{ item.name }}</div>
                  <div class="product-quantity">x{{ item.quantity }}</div>
                </div>
              </div>
            </td>
            <td class="amount">¥{{ order.total_amount.toFixed(2) }}</td>
            <td>{{ order.payment_method }}</td>
            <td>
              <span class="status-tag" :class="order.status">
                {{ getStatusText(order.status) }}
              </span>
            </td>
            <td>{{ formatDate(order.created_at) }}</td>
            <td>{{ formatDate(order.completed_at) }}</td>
            <td>
              <span class="source-tag" v-if="order.affiliate_source">
                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="2" y1="12" x2="22" y2="12"></line>
                  <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
                </svg>
                推广
              </span>
              <span v-else>
                直接
              </span>
            </td>
            <td class="action-buttons">
              <button class="view-btn" @click="viewOrderDetail(order)">
                查看
              </button>
              <button 
                v-if="order.status === 'pending'" 
                class="cancel-btn"
                @click="cancelOrder(order)"
              >
                取消
              </button>
              <button 
                v-if="order.status === 'paid'" 
                class="refund-btn"
                @click="refundOrder(order)"
              >
                退款
              </button>
              <button class="print-btn" @click="printOrder(order)">
                打印
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- 空状态 -->
      <div v-if="filteredOrders.length === 0" class="empty-state">
        <p>暂无订单数据</p>
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="filteredOrders.length > 0" class="pagination">
      <button 
        class="page-btn" 
        :disabled="currentPage === 1" 
        @click="currentPage--"
      >
        上一页
      </button>
      <span class="page-info">
          共 {{ totalItems }} 条记录，第 {{ currentPage }} / {{ totalPages }} 页
        </span>
      <button 
        class="page-btn" 
        :disabled="currentPage === totalPages" 
        @click="currentPage++"
      >
        下一页
      </button>
    </div>

    <!-- 批量操作 -->
    <div v-if="selectedOrders.length > 0" class="batch-actions">
      <p>已选择 {{ selectedOrders.length }} 项</p>
      <div class="batch-buttons">
        <button class="batch-export-btn" @click="handleBatchExport">
          批量导出
        </button>
        <button class="batch-print-btn" @click="handleBatchPrint">
          批量打印
        </button>
      </div>
    </div>

    <!-- 订单详情模态框 -->
    <div v-if="showOrderDetail" class="modal-overlay" @click="closeOrderDetail">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>订单详情</h3>
          <button class="close-btn" @click="closeOrderDetail">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div v-if="currentOrder" class="order-detail">
            <!-- 订单基本信息 -->
            <div class="detail-section">
              <h4>基本信息</h4>
              <div class="info-grid">
                <div class="info-item">
                  <span class="info-label">订单号:</span>
                  <span class="info-value">{{ currentOrder.order_number }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">订单状态:</span>
                  <span class="info-value">
                    <span class="status-tag" :class="currentOrder.status">
                      {{ getStatusText(currentOrder.status) }}
                    </span>
                  </span>
                </div>
                <div class="info-item">
                  <span class="info-label">创建时间:</span>
                  <span class="info-value">{{ formatDate(currentOrder.created_at) }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">完成时间:</span>
                  <span class="info-value">{{ formatDate(currentOrder.completed_at) }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">支付方式:</span>
                  <span class="info-value">{{ currentOrder.payment_method }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">支付流水号:</span>
                  <span class="info-value">{{ currentOrder.payment_transaction_id || '-' }}</span>
                </div>
              </div>
            </div>

            <!-- 用户信息 -->
            <div class="detail-section">
              <h4>用户信息</h4>
              <div class="user-detail">
                <img class="user-avatar" :src="currentOrder.user?.avatar_url || '/avatar-placeholder.png'" alt="用户头像">
                <div class="user-info">
                  <div class="user-name">{{ currentOrder.user?.username }}</div>
                  <div class="user-nickname">{{ currentOrder.user?.nickname || '-' }}</div>
                  <div class="user-email">{{ currentOrder.user?.email }}</div>
                  <div class="user-registered">注册时间: {{ formatDate(currentOrder.user?.created_at) }}</div>
                </div>
              </div>
            </div>

            <!-- 产品信息 -->
            <div class="detail-section">
              <h4>产品信息</h4>
              <table class="product-table">
                <thead>
                  <tr>
                    <th>产品名称</th>
                    <th>数量</th>
                    <th>单价</th>
                    <th>小计</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in currentOrder.items" :key="item.id">
                    <td>{{ item.name }}</td>
                    <td>{{ item.quantity }}</td>
                    <td>¥{{ item.price.toFixed(2) }}</td>
                    <td>¥{{ (item.price * item.quantity).toFixed(2) }}</td>
                  </tr>
                </tbody>
                <tfoot>
                  <tr>
                    <td colspan="3">小计</td>
                    <td>¥{{ currentOrder.subtotal.toFixed(2) }}</td>
                  </tr>
                  <tr>
                    <td colspan="3">运费</td>
                    <td>¥{{ currentOrder.shipping_fee.toFixed(2) }}</td>
                  </tr>
                  <tr>
                    <td colspan="3">优惠</td>
                    <td>-¥{{ currentOrder.discount.toFixed(2) }}</td>
                  </tr>
                  <tr>
                    <td colspan="3">总计</td>
                    <td class="total-amount">¥{{ currentOrder.total_amount.toFixed(2) }}</td>
                  </tr>
                </tfoot>
              </table>
            </div>

            <!-- 推广信息 -->
            <div class="detail-section" v-if="currentOrder.affiliate_source">
              <h4>推广信息</h4>
              <div class="info-grid">
                <div class="info-item">
                  <span class="info-label">推广来源:</span>
                  <span class="info-value">{{ currentOrder.affiliate_source }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">推广用户:</span>
                  <span class="info-value">{{ currentOrder.affiliate_user?.username || '-' }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">佣金比例:</span>
                  <span class="info-value">{{ currentOrder.commission_rate || 10 }}%</span>
                </div>
                <div class="info-item">
                  <span class="info-label">佣金金额:</span>
                  <span class="info-value">¥{{ currentOrder.commission_amount.toFixed(2) }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">佣金状态:</span>
                  <span class="info-value">{{ getCommissionStatusText(currentOrder.commission_status) }}</span>
                </div>
              </div>
            </div>

            <!-- 操作记录 -->
            <div class="detail-section">
              <h4>操作记录</h4>
              <div class="log-list">
                <div v-for="log in currentOrder.logs" :key="log.id" class="log-item">
                  <div class="log-time">{{ formatDate(log.created_at) }}</div>
                  <div class="log-content">{{ log.content }}</div>
                </div>
              </div>
            </div>

            <!-- 操作按钮 -->
            <div class="order-actions">
              <button 
                v-if="currentOrder.status === 'pending'" 
                class="cancel-btn"
                @click="cancelOrder(currentOrder)"
              >
                取消订单
              </button>
              <button 
                v-if="currentOrder.status === 'paid'" 
                class="refund-btn"
                @click="refundOrder(currentOrder)"
              >
                退款
              </button>
              <button class="print-btn" @click="printOrder(currentOrder)">
                打印订单
              </button>
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
import { useOrderStore } from '../../stores/index.js'

// 搜索和筛选
const searchQuery = ref('')
const statusFilter = ref('')
const sortBy = ref('created_at')
const sortOrder = ref('desc')
const dateRange = ref({
  start: '',
  end: ''
})

// 初始化store
const orderStore = useOrderStore()

// 分页
const currentPage = ref(1)
const pageSize = ref(10)
const totalItems = ref(0)

// 选择功能
const selectedOrders = ref([])
const selectAll = ref(false)

// 模态框
const showOrderDetail = ref(false)
const currentOrder = ref(null)

// 过滤后的订单列表
const filteredOrders = computed(() => {
  return orderStore.adminOrders
})

// 总页数
const totalPages = computed(() => {
  return Math.max(1, Math.ceil(totalItems.value / pageSize.value))
})

// 日期格式化
const formatDate = (dateString) => {
  if (!dateString) return '-'  
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// 状态监听
watch(
  [searchQuery, statusFilter, sortBy, sortOrder, dateRange, currentPage, pageSize],
  () => {
    fetchOrders()
  },
  { deep: true }
)

// 获取订单列表
const fetchOrders = async () => {
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchQuery.value,
      status: statusFilter.value,
      sort_field: sortBy.value,
      sort_direction: sortOrder.value,
      start_date: dateRange.value.start,
      end_date: dateRange.value.end
    }
    
    // 移除空值
    Object.keys(params).forEach(key => {
      if (!params[key] && params[key] !== 0) delete params[key]
    })
    
    const response = await orderStore.fetchAdminOrders(params)
    totalItems.value = response.total
  } catch (error) {
    console.error('获取订单列表失败:', error)
    Swal.fire('错误', '获取订单列表失败', 'error')
  }
}

// 格式化日期函数已在上方定义

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    'pending': '待支付',
    'paid': '已支付',
    'cancelled': '已取消',
    'refunded': '已退款'
  }
  return statusMap[status] || status
}

// 获取佣金状态文本
const getCommissionStatusText = (status) => {
  const statusMap = {
    'pending': '待结算',
    'paid': '已结算',
    'cancelled': '已取消'
  }
  return statusMap[status] || status
}

// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
  fetchOrders()
}

// 筛选处理
const handleFilter = () => {
  currentPage.value = 1
  fetchOrders()
}

// 排序处理
const handleSort = () => {
  // 切换排序顺序
  sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
}

// 重置筛选
const resetFilters = () => {
  searchQuery.value = ''
  statusFilter.value = ''
  dateRange.value = {
    start: '',
    end: ''
  }
  sortBy.value = 'created_at'
  sortOrder.value = 'desc'
  currentPage.value = 1
  fetchOrders()
}

// 全选/取消全选
const toggleSelectAll = () => {
  selectAll.value = !selectAll.value
  if (selectAll.value) {
    selectedOrders.value = filteredOrders.value.map(order => order.id)
  } else {
    selectedOrders.value = []
  }
}

// 单个选择
const toggleSelect = (orderId) => {
  const index = selectedOrders.value.indexOf(orderId)
  if (index > -1) {
    selectedOrders.value.splice(index, 1)
    selectAll.value = false
  } else {
    selectedOrders.value.push(orderId)
    if (selectedOrders.value.length === filteredOrders.value.length) {
      selectAll.value = true
    }
  }
}

// 查看订单详情
const viewOrderDetail = async (order) => {
  try {
    const orderDetail = await orderStore.fetchOrderDetail(order.id)
    currentOrder.value = orderDetail
    showOrderDetail.value = true
  } catch (error) {
    console.error('获取订单详情失败:', error)
    Swal.fire('错误', '获取订单详情失败', 'error')
  }
}

// 关闭订单详情
const closeOrderDetail = () => {
  showOrderDetail.value = false
  setTimeout(() => {
    currentOrder.value = null
  }, 300)
}

// 取消订单
const cancelOrder = async (order) => {
  const result = await Swal.fire({
    title: '确定要取消这个订单吗？',
    text: `取消订单 "${order.order_number}" 后将无法恢复！`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#d33',
    cancelButtonColor: '#3085d6',
    confirmButtonText: '取消订单',
    cancelButtonText: '取消'
  })

  if (result.isConfirmed) {
    try {
      await orderStore.cancelOrder(order.id)
      Swal.fire('操作成功！', '订单已取消。', 'success')
      fetchOrders()
    } catch (error) {
      console.error('取消订单失败:', error)
      Swal.fire('错误', '取消订单失败', 'error')
    }
  }
}

// 退款订单
const refundOrder = async (order) => {
  const result = await Swal.fire({
    title: '确定要给这个订单退款吗？',
    text: `退款后订单 "${order.order_number}" 将无法恢复！`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#d33',
    cancelButtonColor: '#3085d6',
    confirmButtonText: '确认退款',
    cancelButtonText: '取消'
  })

  if (result.isConfirmed) {
    try {
      await orderStore.refundOrder(order.id)
      Swal.fire('操作成功！', '退款已处理。', 'success')
      fetchOrders()
    } catch (error) {
      console.error('退款订单失败:', error)
      Swal.fire('错误', '退款订单失败', 'error')
    }
  }
}

// 打印订单
const printOrder = (order) => {
  // 这里可以添加打印订单的逻辑
  Swal.fire('提示', '打印功能开发中...', 'info')
}

// 导出订单
const handleExport = async () => {
  try {
    await orderStore.exportOrders()
    Swal.fire('成功', '订单导出成功', 'success')
  } catch (error) {
    console.error('导出订单失败:', error)
    Swal.fire('错误', '导出订单失败', 'error')
  }
}

// 批量导出
const handleBatchExport = async () => {
  if (selectedOrders.value.length === 0) {
    Swal.fire('提示', '请选择要导出的订单', 'warning')
    return
  }
  
  try {
    await orderStore.batchExportOrders(selectedOrders.value)
    Swal.fire('成功', '批量导出订单成功', 'success')
  } catch (error) {
    console.error('批量导出订单失败:', error)
    Swal.fire('错误', '批量导出订单失败', 'error')
  }
}

// 批量打印
const handleBatchPrint = () => {
  if (selectedOrders.value.length === 0) return
  // 这里可以添加批量打印订单的逻辑
  Swal.fire('提示', '批量打印功能开发中...', 'info')
}

// 高级搜索
const openAdvancedSearch = () => {
  Swal.fire('提示', '高级搜索功能开发中...', 'info')
}

// 页面加载时获取数据
onMounted(async () => {
  fetchOrders()
})
</script>

<style scoped>
.order-management-container {
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
.search-btn {
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

.search-btn {
  background-color: #409eff;
  color: #fff;
}

.search-btn:hover {
  background-color: #66b1ff;
}

/* 筛选区域 */
.filter-section {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  align-items: center;
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.search-box {
  display: flex;
  flex: 1;
  min-width: 250px;
}

.search-box input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px 0 0 4px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s ease;
}

.search-box input:focus {
  border-color: #409eff;
}

.search-box .search-btn {
  border-radius: 0 4px 4px 0;
}

.filter-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
}

.filter-controls select,
.filter-controls input[type="date"] {
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s ease;
}

.filter-controls select:focus,
.filter-controls input[type="date"]:focus {
  border-color: #409eff;
}

.date-range {
  display: flex;
  align-items: center;
  gap: 8px;
}

.date-range span {
  color: #606266;
  font-size: 14px;
}

.filter-btn {
  padding: 8px 16px;
  background-color: #909399;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.filter-btn:hover {
  background-color: #a6a9ad;
}

/* 表格容器 */
.table-container {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin-bottom: 20px;
}

.order-table {
  width: 100%;
  border-collapse: collapse;
}

.order-table th,
.order-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #ebeef5;
}

.order-table th {
  background-color: #f5f7fa;
  font-weight: 600;
  color: #303133;
  font-size: 14px;
  white-space: nowrap;
}

.order-table td {
  color: #606266;
  font-size: 14px;
}

.order-table tr:hover {
  background-color: #f5f7fa;
}

.order-table tr.selected {
  background-color: #ecf5ff;
}

/* 订单号 */
.order-id {
  color: #409eff;
  cursor: pointer;
  text-decoration: underline;
  transition: color 0.3s ease;
}

.order-id:hover {
  color: #66b1ff;
}

/* 用户信息 */
.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.user-email {
  font-size: 12px;
  color: #909399;
}

/* 产品列表 */
.product-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.product-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
}

.product-name {
  color: #303133;
}

.product-quantity {
  color: #909399;
}

/* 金额 */
.amount {
  font-weight: 600;
  color: #e6a23c;
}

/* 状态标签 */
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
  background-color: #909399;
  color: #fff;
}

.status-tag.refunded {
  background-color: #f56c6c;
  color: #fff;
}

/* 来源标签 */
.source-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 8px;
  background-color: #ecf5ff;
  color: #409eff;
  border-radius: 4px;
  font-size: 12px;
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.view-btn,
.cancel-btn,
.refund-btn,
.print-btn {
  padding: 4px 10px;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-btn {
  background-color: #409eff;
  color: #fff;
}

.view-btn:hover {
  background-color: #66b1ff;
}

.cancel-btn {
  background-color: #f56c6c;
  color: #fff;
}

.cancel-btn:hover {
  background-color: #f78989;
}

.refund-btn {
  background-color: #e6a23c;
  color: #fff;
}

.refund-btn:hover {
  background-color: #ebb563;
}

.print-btn {
  background-color: #909399;
  color: #fff;
}

.print-btn:hover {
  background-color: #a6a9ad;
}

/* 空状态 */
.empty-state {
  padding: 60px 20px;
  text-align: center;
  color: #909399;
}

/* 分页 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.page-btn {
  padding: 6px 12px;
  background-color: #f5f7fa;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  color: #606266;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.page-btn:hover:not(:disabled) {
  background-color: #ecf5ff;
  border-color: #c6e2ff;
  color: #409eff;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: #606266;
  font-size: 14px;
}

/* 批量操作 */
.batch-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 20px;
}

.batch-actions p {
  margin: 0;
  color: #606266;
  font-size: 14px;
}

.batch-buttons {
  display: flex;
  gap: 10px;
}

.batch-export-btn,
.batch-print-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.batch-export-btn {
  background-color: #67c23a;
  color: #fff;
}

.batch-export-btn:hover {
  background-color: #85ce61;
}

.batch-print-btn {
  background-color: #409eff;
  color: #fff;
}

.batch-print-btn:hover {
  background-color: #66b1ff;
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
  max-width: 800px;
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

/* 订单详情 */
.order-detail {
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

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 12px;
}

.info-item {
  display: flex;
  gap: 8px;
}

.info-label {
  color: #909399;
  font-size: 14px;
  min-width: 80px;
}

.info-value {
  color: #303133;
  font-size: 14px;
  flex: 1;
}

/* 用户详情 */
.user-detail {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-detail .user-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
}

.user-detail .user-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.user-name {
  font-size: 16px;
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

/* 产品表格 */
.product-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #fff;
  border-radius: 6px;
  overflow: hidden;
}

.product-table th,
.product-table td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid #ebeef5;
  font-size: 14px;
}

.product-table th {
  background-color: #f5f7fa;
  font-weight: 600;
  color: #303133;
}

.product-table td {
  color: #606266;
}

.product-table tfoot td {
  font-weight: 600;
}

.product-table tfoot .total-amount {
  color: #e6a23c;
  font-size: 16px;
}

/* 操作记录 */
.log-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.log-item {
  display: flex;
  gap: 12px;
  font-size: 14px;
}

.log-time {
  color: #909399;
  min-width: 180px;
}

.log-content {
  color: #606266;
  flex: 1;
}

/* 订单操作按钮 */
.order-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 10px;
}

.order-actions button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.order-actions .cancel-btn {
  background-color: #f56c6c;
  color: #fff;
}

.order-actions .cancel-btn:hover {
  background-color: #f78989;
}

.order-actions .refund-btn {
  background-color: #e6a23c;
  color: #fff;
}

.order-actions .refund-btn:hover {
  background-color: #ebb563;
}

.order-actions .print-btn {
  background-color: #409eff;
  color: #fff;
}

.order-actions .print-btn:hover {
  background-color: #66b1ff;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .order-table {
    overflow-x: auto;
    display: block;
  }
  
  .action-buttons {
    flex-direction: column;
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
  
  .search-box {
    min-width: auto;
  }
  
  .filter-controls {
    justify-content: center;
  }
  
  .header-actions {
    flex-direction: column;
    gap: 8px;
  }
  
  .batch-actions {
    flex-direction: column;
    gap: 10px;
  }
  
  .user-detail {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .order-actions {
    flex-direction: column;
  }
}
</style>