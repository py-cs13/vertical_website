<template>
  <div class="agent-management-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>智能体管理</h1>
      <button class="add-btn" @click="handleAddAgent">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        添加智能体
      </button>
    </div>

    <!-- 搜索和筛选 -->
    <div class="filter-section">
      <div class="search-box">
        <input 
          type="text" 
          placeholder="搜索智能体名称或描述" 
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
        <select v-model="categoryFilter" @change="handleFilter">
          <option value="">所有分类</option>
          <option v-for="category in categories" :key="category.id" :value="category.id">
            {{ category.name }}
          </option>
        </select>

        <select v-model="statusFilter" @change="handleFilter">
          <option value="">所有状态</option>
          <option value="active">已上架</option>
          <option value="inactive">已下架</option>
        </select>

        <button class="filter-btn" @click="resetFilters">
          重置筛选
        </button>
      </div>
    </div>

    <!-- 智能体列表 -->
    <div class="agents-grid">
      <div 
        v-for="agent in filteredAgents" 
        :key="agent.id" 
        class="agent-card" 
        :class="{ selected: selectedAgents.includes(agent.id) }"
      >
        <div class="agent-header">
          <input 
            type="checkbox" 
            :checked="selectedAgents.includes(agent.id)" 
            @change="toggleSelect(agent.id)"
          >
          <span class="agent-status" :class="agent.status">
            {{ agent.status === 'active' ? '已上架' : '已下架' }}
          </span>
        </div>
        
        <div class="agent-image">
          <img :src="agent.image_url || '/placeholder-image.jpg'" alt="智能体图片">
        </div>
        
        <div class="agent-info">
          <h3 class="agent-name">{{ agent.name }}</h3>
          <p class="agent-description">{{ agent.description }}</p>
          <div class="agent-meta">
            <span class="category">{{ getCategoryName(agent.category_id) }}</span>
            <span class="price">¥{{ agent.price.toFixed(2) }}</span>
          </div>
          <div class="agent-stats">
            <span>销量: {{ agent.sales_count }}</span>
            <span>下载: {{ agent.download_count }}</span>
          </div>
        </div>
        
        <div class="agent-actions">
          <button class="view-btn" @click="handleViewAgent(agent)">
            查看
          </button>
          <button class="edit-btn" @click="handleEditAgent(agent)">
            编辑
          </button>
          <button class="delete-btn" @click="handleDeleteAgent(agent.id)">
            删除
          </button>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-if="filteredAgents.length === 0" class="empty-state">
        <p>暂无智能体数据</p>
      </div>
    </div>

    <!-- 批量操作 -->
    <div v-if="selectedAgents.length > 0" class="batch-actions">
      <p>已选择 {{ selectedAgents.length }} 项</p>
      <div class="batch-buttons">
        <button class="batch-active-btn" @click="handleBatchActive">
          批量上架
        </button>
        <button class="batch-inactive-btn" @click="handleBatchInactive">
          批量下架
        </button>
        <button class="batch-delete-btn" @click="handleBatchDelete">
          批量删除
        </button>
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="filteredAgents.length > 0" class="pagination">
      <button 
        class="page-btn" 
        :disabled="currentPage === 1" 
        @click="currentPage--"
      >
        上一页
      </button>
      <span class="page-info">
        第 {{ currentPage }} / {{ totalPages }} 页
      </span>
      <button 
        class="page-btn" 
        :disabled="currentPage === totalPages" 
        @click="currentPage++"
      >
        下一页
      </button>
    </div>

    <!-- 添加/编辑智能体模态框 -->
    <div v-if="showAgentModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editingAgent ? '编辑智能体' : '添加智能体' }}</h3>
          <button class="close-btn" @click="closeModal">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <div class="form-group">
              <label>名称</label>
              <input type="text" v-model="agentForm.name" required>
            </div>

            <div class="form-group">
              <label>分类</label>
              <select v-model="agentForm.category_id" required>
                <option value="">请选择分类</option>
                <option v-for="category in categories" :key="category.id" :value="category.id">
                  {{ category.name }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label>价格 (元)</label>
              <input type="number" v-model.number="agentForm.price" min="0" step="0.01" required>
            </div>

            <div class="form-group">
              <label>状态</label>
              <select v-model="agentForm.status" required>
                <option value="active">已上架</option>
                <option value="inactive">已下架</option>
              </select>
            </div>

            <div class="form-group">
              <label>描述</label>
              <textarea v-model="agentForm.description" rows="5" required></textarea>
            </div>

            <div class="form-group">
              <label>智能体文件</label>
              <input type="file" @change="handleFileUpload">
              <div v-if="agentForm.file_name" class="file-info">
                当前文件: {{ agentForm.file_name }}
              </div>
            </div>

            <div class="form-group">
              <label>智能体图片</label>
              <input type="file" accept="image/*" @change="handleImageUpload">
              <div v-if="agentForm.image_url" class="image-preview">
                <img :src="agentForm.image_url" alt="智能体预览">
              </div>
            </div>

            <div class="form-actions">
              <button type="button" class="cancel-btn" @click="closeModal">
                取消
              </button>
              <button type="submit" class="submit-btn">
                {{ editingAgent ? '更新智能体' : '保存智能体' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useContentStore } from '../../stores/index.js'
import Swal from 'sweetalert2'

const contentStore = useContentStore()

// 搜索和筛选
const searchQuery = ref('')
const categoryFilter = ref('')
const statusFilter = ref('')

// 分页
const currentPage = ref(1)
const pageSize = ref(12)

// 选择功能
const selectedToolkits = ref([])

// 模态框
const showToolkitModal = ref(false)
const editingToolkit = ref(false)

// 表单数据
const toolkitForm = ref({
  name: '',
  category_id: '',
  price: 0,
  status: 'active',
  description: '',
  image_url: '',
  file_name: '',
  file_path: ''
})

// 分类列表（从store获取）
const categories = computed(() => contentStore.categories)

// 智能体列表（从store获取）
const agents = computed(() => contentStore.agents)

// 过滤后的智能体列表
const filteredAgents = computed(() => {
  return agents.value.filter(agent => {
    const matchesSearch = !searchQuery.value || 
      agent.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      agent.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    const matchesCategory = !categoryFilter.value || agent.category_id === Number(categoryFilter.value)
    const matchesStatus = !statusFilter.value || agent.status === statusFilter.value
    
    return matchesSearch && matchesCategory && matchesStatus
  })
})

// 总页数
const totalPages = computed(() => {
  return Math.ceil(filteredAgents.value.length / pageSize.value)
})

// 监听筛选条件变化
watch([searchQuery, categoryFilter, statusFilter], () => {
  currentPage.value = 1
  contentStore.setFilter({
    search: searchQuery.value,
    category: categoryFilter.value,
    status: statusFilter.value
  })
  fetchAgents()
})

// 获取分类名称
const getCategoryName = (categoryId) => {
  const category = categories.value.find(c => c.id === categoryId)
  return category ? category.name : '未分类'
}

// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
  fetchAgents()
}

// 筛选处理
const handleFilter = () => {
  currentPage.value = 1
  fetchAgents()
}

// 重置筛选
const resetFilters = () => {
  searchQuery.value = ''
  categoryFilter.value = ''
  statusFilter.value = ''
  currentPage.value = 1
  contentStore.resetFilter()
  fetchAgents()
}

// 单个选择
const toggleSelect = (agentId) => {
  const index = selectedAgents.value.indexOf(agentId)
  if (index > -1) {
    selectedAgents.value.splice(index, 1)
  } else {
    selectedAgents.value.push(agentId)
  }
}

// 添加智能体
const handleAddAgent = () => {
  editingAgent.value = false
  agentForm.value = {
    name: '',
    category_id: '',
    price: 0,
    status: 'active',
    description: '',
    image_url: '',
    file_name: '',
    file_path: ''
  }
  showAgentModal.value = true
}

// 编辑智能体
const handleEditAgent = (agent) => {
  editingAgent.value = true
  agentForm.value = { ...agent }
  showAgentModal.value = true
}

// 查看智能体
const handleViewAgent = (agent) => {
  // 这里可以添加查看智能体详情的逻辑
  console.log('查看智能体:', agent)
}

// 删除智能体
const handleDeleteAgent = async (agentId) => {
  const result = await Swal.fire({
    title: '确定要删除这个智能体吗？',
    text: '删除后将无法恢复！',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#d33',
    cancelButtonColor: '#3085d6',
    confirmButtonText: '删除',
    cancelButtonText: '取消'
  })

  if (result.isConfirmed) {
    try {
      await contentStore.deleteAgent(agentId)
      Swal.fire('删除成功！', '智能体已被删除。', 'success')
    } catch (error) {
      Swal.fire('错误', '删除智能体失败', 'error')
    }
  }
}

// 批量上架
const handleBatchActive = async () => {
  const result = await Swal.fire({
    title: '确定要批量上架选中的智能体吗？',
    icon: 'question',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#6c757d',
    confirmButtonText: '上架',
    cancelButtonText: '取消'
  })

  if (result.isConfirmed) {
    try {
      await contentStore.batchUpdateAgents(selectedAgents.value, { status: 'active' })
      selectedAgents.value = []
      Swal.fire('操作成功！', '选中的智能体已批量上架。', 'success')
    } catch (error) {
      Swal.fire('错误', '批量上架失败', 'error')
    }
  }
}

// 批量下架
const handleBatchInactive = async () => {
  const result = await Swal.fire({
    title: '确定要批量下架选中的智能体吗？',
    icon: 'question',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#6c757d',
    confirmButtonText: '下架',
    cancelButtonText: '取消'
  })

  if (result.isConfirmed) {
    try {
      await contentStore.batchUpdateAgents(selectedAgents.value, { status: 'inactive' })
      selectedAgents.value = []
      Swal.fire('操作成功！', '选中的智能体已批量下架。', 'success')
    } catch (error) {
      Swal.fire('错误', '批量下架失败', 'error')
    }
  }
}

// 批量删除
const handleBatchDelete = async () => {
  const result = await Swal.fire({
    title: '确定要批量删除选中的智能体吗？',
    text: '删除后将无法恢复！',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#d33',
    cancelButtonColor: '#6c757d',
    confirmButtonText: '删除',
    cancelButtonText: '取消'
  })

  if (result.isConfirmed) {
    try {
      await contentStore.batchDeleteAgents(selectedAgents.value)
      selectedAgents.value = []
      Swal.fire('删除成功！', '选中的智能体已批量删除。', 'success')
    } catch (error) {
      Swal.fire('错误', '批量删除失败', 'error')
    }
  }
}

// 关闭模态框
const closeModal = () => {
  showAgentModal.value = false
  setTimeout(() => {
    agentForm.value = {
      name: '',
      category_id: '',
      price: 0,
      status: 'active',
      description: '',
      image_url: '',
      file_name: '',
      file_path: ''
    }
    editingAgent.value = false
  }, 300)
}

// 文件上传处理
const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    agentForm.value.file_name = file.name
    // 这里可以添加文件上传的API调用
    // 实际项目中应该上传文件到服务器并获取file_path
  }
}

// 图片上传处理
const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      agentForm.value.image_url = e.target.result
    }
    reader.readAsDataURL(file)
    // 实际项目中应该上传图片到服务器并获取image_url
  }
}

// 提交表单
const handleSubmit = async () => {
  try {
    if (editingAgent.value) {
      // 更新智能体
      await contentStore.updateAgent(agentForm.value)
      Swal.fire('更新成功！', '智能体已更新。', 'success')
    } else {
      // 添加新智能体
      await contentStore.createAgent(agentForm.value)
      Swal.fire('添加成功！', '智能体已添加。', 'success')
    }
    closeModal()
  } catch (error) {
    Swal.fire('错误', editingAgent.value ? '更新智能体失败' : '添加智能体失败', 'error')
  }
}

// 获取智能体数据
const fetchAgents = async () => {
  try {
    await contentStore.fetchAgents()
    await contentStore.fetchCategories()
  } catch (error) {
    console.error('获取智能体列表失败:', error)
    Swal.fire('错误', '获取智能体列表失败', 'error')
  }
}

// 页面加载时获取数据
onMounted(async () => {
  await fetchAgents()
})
</script>

<style scoped>
.agents-management-container {
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

.add-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background-color: #409eff;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-btn:hover {
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

.search-btn {
  padding: 0 15px;
  background-color: #409eff;
  color: #fff;
  border: none;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s ease;
}

.search-btn:hover {
  background-color: #66b1ff;
}

.filter-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
}

.filter-controls select {
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s ease;
  min-width: 120px;
}

.filter-controls select:focus {
  border-color: #409eff;
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

/* 智能体网格 */
.agents-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

/* 智能体卡片 */
.agent-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.3s ease;
}

.agent-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.agent-card.selected {
  border: 2px solid #409eff;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.agent-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  background-color: #f5f7fa;
}

.agent-status {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.agent-status.active {
  background-color: #ecf5ff;
  color: #409eff;
}

.agent-status.inactive {
  background-color: #fdf6ec;
  color: #e6a23c;
}

.agent-image {
  height: 200px;
  overflow: hidden;
  background-color: #f5f7fa;
}

.agent-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.agent-card:hover .agent-image img {
  transform: scale(1.05);
}

.agent-info {
  padding: 15px;
}

.agent-name {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #303133;
  font-weight: 600;
}

.agent-description {
  margin: 0 0 15px 0;
  font-size: 14px;
  color: #606266;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.agent-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.agent-stats {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #909399;
}

.agent-actions {
  display: flex;
  padding: 10px 15px 15px;
  gap: 8px;
}

.view-btn,
.edit-btn,
.delete-btn {
  flex: 1;
  padding: 6px;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-btn {
  background-color: #909399;
  color: #fff;
}

.view-btn:hover {
  background-color: #a6a9ad;
}

.edit-btn {
  background-color: #67c23a;
  color: #fff;
}

.edit-btn:hover {
  background-color: #85ce61;
}

.delete-btn {
  background-color: #f56c6c;
  color: #fff;
}

.delete-btn:hover {
  background-color: #f78989;
}

/* 空状态 */
.empty-state {
  grid-column: 1 / -1;
  padding: 60px 20px;
  text-align: center;
  color: #909399;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
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

.batch-active-btn,
.batch-inactive-btn,
.batch-delete-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.batch-active-btn {
  background-color: #409eff;
  color: #fff;
}

.batch-active-btn:hover {
  background-color: #66b1ff;
}

.batch-inactive-btn {
  background-color: #e6a23c;
  color: #fff;
}

.batch-inactive-btn:hover {
  background-color: #ebb563;
}

.batch-delete-btn {
  background-color: #f56c6c;
  color: #fff;
}

.batch-delete-btn:hover {
  background-color: #f78989;
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
  max-width: 600px;
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

/* 表单样式 */
.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  color: #303133;
  font-weight: 500;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  color: #606266;
  outline: none;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: #409eff;
}

.form-group textarea {
  resize: vertical;
}

/* 文件信息 */
.file-info {
  margin-top: 10px;
  padding: 8px;
  background-color: #f5f7fa;
  border-radius: 4px;
  font-size: 14px;
  color: #606266;
}

/* 图片预览 */
.image-preview {
  margin-top: 10px;
  max-width: 200px;
  max-height: 150px;
  overflow: hidden;
  border-radius: 4px;
  border: 1px solid #dcdfe6;
}

.image-preview img {
  width: 100%;
  height: auto;
  display: block;
}

/* 表单操作按钮 */
.form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 30px;
}

.cancel-btn,
.submit-btn {
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn {
  background-color: #fff;
  color: #606266;
  border: 1px solid #dcdfe6;
}

.cancel-btn:hover {
  background-color: #f5f7fa;
}

.submit-btn {
  background-color: #409eff;
  color: #fff;
  border: none;
}

.submit-btn:hover {
  background-color: #66b1ff;
}

/* 响应式设计 */
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
  
  .agents-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  }
  
  .batch-actions {
    flex-direction: column;
    gap: 10px;
  }
}

@media (max-width: 480px) {
  .agents-grid {
    grid-template-columns: 1fr;
  }
}
</style>