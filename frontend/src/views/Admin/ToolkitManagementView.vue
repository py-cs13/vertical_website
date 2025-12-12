<template>
  <div class="toolkit-management-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>工具包管理</h1>
      <button class="add-btn" @click="handleAddToolkit">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        添加工具包
      </button>
    </div>

    <!-- 搜索和筛选 -->
    <div class="filter-section">
      <div class="search-box">
        <input 
          type="text" 
          placeholder="搜索工具包名称或描述" 
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

    <!-- 工具包列表 -->
    <div class="toolkits-grid">
      <div 
        v-for="toolkit in filteredToolkits" 
        :key="toolkit.id" 
        class="toolkit-card" 
        :class="{ selected: selectedToolkits.includes(toolkit.id) }"
      >
        <div class="toolkit-header">
          <input 
            type="checkbox" 
            :checked="selectedToolkits.includes(toolkit.id)" 
            @change="toggleSelect(toolkit.id)"
          >
          <span class="toolkit-status" :class="toolkit.status">
            {{ toolkit.status === 'active' ? '已上架' : '已下架' }}
          </span>
        </div>
        
        <div class="toolkit-image">
          <img :src="toolkit.image_url || '/placeholder-image.jpg'" alt="工具包图片">
        </div>
        
        <div class="toolkit-info">
          <h3 class="toolkit-name">{{ toolkit.name }}</h3>
          <p class="toolkit-description">{{ toolkit.description }}</p>
          <div class="toolkit-meta">
            <span class="category">{{ getCategoryName(toolkit.category_id) }}</span>
            <span class="price">¥{{ toolkit.price.toFixed(2) }}</span>
          </div>
          <div class="toolkit-stats">
            <span>销量: {{ toolkit.sales_count }}</span>
            <span>下载: {{ toolkit.download_count }}</span>
          </div>
        </div>
        
        <div class="toolkit-actions">
          <button class="view-btn" @click="handleViewToolkit(toolkit)">
            查看
          </button>
          <button class="edit-btn" @click="handleEditToolkit(toolkit)">
            编辑
          </button>
          <button class="delete-btn" @click="handleDeleteToolkit(toolkit.id)">
            删除
          </button>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-if="filteredToolkits.length === 0" class="empty-state">
        <p>暂无工具包数据</p>
      </div>
    </div>

    <!-- 批量操作 -->
    <div v-if="selectedToolkits.length > 0" class="batch-actions">
      <p>已选择 {{ selectedToolkits.length }} 项</p>
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
    <div v-if="filteredToolkits.length > 0" class="pagination">
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

    <!-- 添加/编辑工具包模态框 -->
    <div v-if="showToolkitModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editingToolkit ? '编辑工具包' : '添加工具包' }}</h3>
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
              <input type="text" v-model="toolkitForm.name" required>
            </div>

            <div class="form-group">
              <label>分类</label>
              <select v-model="toolkitForm.category_id" required>
                <option value="">请选择分类</option>
                <option v-for="category in categories" :key="category.id" :value="category.id">
                  {{ category.name }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label>价格 (元)</label>
              <input type="number" v-model.number="toolkitForm.price" min="0" step="0.01" required>
            </div>

            <div class="form-group">
              <label>状态</label>
              <select v-model="toolkitForm.status" required>
                <option value="active">已上架</option>
                <option value="inactive">已下架</option>
              </select>
            </div>

            <div class="form-group">
              <label>描述</label>
              <textarea v-model="toolkitForm.description" rows="5" required></textarea>
            </div>

            <div class="form-group">
              <label>工具包文件</label>
              <input type="file" @change="handleFileUpload">
              <div v-if="toolkitForm.file_name" class="file-info">
                当前文件: {{ toolkitForm.file_name }}
              </div>
            </div>

            <div class="form-group">
              <label>工具包图片</label>
              <input type="file" accept="image/*" @change="handleImageUpload">
              <div v-if="toolkitForm.image_url" class="image-preview">
                <img :src="toolkitForm.image_url" alt="工具包预览">
              </div>
            </div>

            <div class="form-actions">
              <button type="button" class="cancel-btn" @click="closeModal">
                取消
              </button>
              <button type="submit" class="submit-btn">
                {{ editingToolkit ? '更新工具包' : '保存工具包' }}
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

// 工具包列表（从store获取）
const toolkits = computed(() => contentStore.toolkits)

// 过滤后的工具包列表
const filteredToolkits = computed(() => {
  return toolkits.value.filter(toolkit => {
    const matchesSearch = !searchQuery.value || 
      toolkit.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      toolkit.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    const matchesCategory = !categoryFilter.value || toolkit.category_id === Number(categoryFilter.value)
    const matchesStatus = !statusFilter.value || toolkit.status === statusFilter.value
    
    return matchesSearch && matchesCategory && matchesStatus
  })
})

// 总页数
const totalPages = computed(() => {
  return Math.ceil(filteredToolkits.value.length / pageSize.value)
})

// 监听筛选条件变化
watch([searchQuery, categoryFilter, statusFilter], () => {
  currentPage.value = 1
  contentStore.setFilter({
    search: searchQuery.value,
    category: categoryFilter.value,
    status: statusFilter.value
  })
  fetchToolkits()
})

// 获取分类名称
const getCategoryName = (categoryId) => {
  const category = categories.value.find(c => c.id === categoryId)
  return category ? category.name : '未分类'
}

// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
  fetchToolkits()
}

// 筛选处理
const handleFilter = () => {
  currentPage.value = 1
  fetchToolkits()
}

// 重置筛选
const resetFilters = () => {
  searchQuery.value = ''
  categoryFilter.value = ''
  statusFilter.value = ''
  currentPage.value = 1
  contentStore.resetFilter()
  fetchToolkits()
}

// 单个选择
const toggleSelect = (toolkitId) => {
  const index = selectedToolkits.value.indexOf(toolkitId)
  if (index > -1) {
    selectedToolkits.value.splice(index, 1)
  } else {
    selectedToolkits.value.push(toolkitId)
  }
}

// 添加工具包
const handleAddToolkit = () => {
  editingToolkit.value = false
  toolkitForm.value = {
    name: '',
    category_id: '',
    price: 0,
    status: 'active',
    description: '',
    image_url: '',
    file_name: '',
    file_path: ''
  }
  showToolkitModal.value = true
}

// 编辑工具包
const handleEditToolkit = (toolkit) => {
  editingToolkit.value = true
  toolkitForm.value = { ...toolkit }
  showToolkitModal.value = true
}

// 查看工具包
const handleViewToolkit = (toolkit) => {
  // 这里可以添加查看工具包详情的逻辑
  console.log('查看工具包:', toolkit)
}

// 删除工具包
const handleDeleteToolkit = async (toolkitId) => {
  const result = await Swal.fire({
    title: '确定要删除这个工具包吗？',
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
      await contentStore.deleteToolkit(toolkitId)
      Swal.fire('删除成功！', '工具包已被删除。', 'success')
    } catch (error) {
      Swal.fire('错误', '删除工具包失败', 'error')
    }
  }
}

// 批量上架
const handleBatchActive = async () => {
  const result = await Swal.fire({
    title: '确定要批量上架选中的工具包吗？',
    icon: 'question',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#6c757d',
    confirmButtonText: '上架',
    cancelButtonText: '取消'
  })

  if (result.isConfirmed) {
    try {
      await contentStore.batchUpdateToolkits(selectedToolkits.value, { status: 'active' })
      selectedToolkits.value = []
      Swal.fire('操作成功！', '选中的工具包已批量上架。', 'success')
    } catch (error) {
      Swal.fire('错误', '批量上架失败', 'error')
    }
  }
}

// 批量下架
const handleBatchInactive = async () => {
  const result = await Swal.fire({
    title: '确定要批量下架选中的工具包吗？',
    icon: 'question',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#6c757d',
    confirmButtonText: '下架',
    cancelButtonText: '取消'
  })

  if (result.isConfirmed) {
    try {
      await contentStore.batchUpdateToolkits(selectedToolkits.value, { status: 'inactive' })
      selectedToolkits.value = []
      Swal.fire('操作成功！', '选中的工具包已批量下架。', 'success')
    } catch (error) {
      Swal.fire('错误', '批量下架失败', 'error')
    }
  }
}

// 批量删除
const handleBatchDelete = async () => {
  const result = await Swal.fire({
    title: '确定要批量删除选中的工具包吗？',
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
      await contentStore.batchDeleteToolkits(selectedToolkits.value)
      selectedToolkits.value = []
      Swal.fire('删除成功！', '选中的工具包已批量删除。', 'success')
    } catch (error) {
      Swal.fire('错误', '批量删除失败', 'error')
    }
  }
}

// 关闭模态框
const closeModal = () => {
  showToolkitModal.value = false
  setTimeout(() => {
    toolkitForm.value = {
      name: '',
      category_id: '',
      price: 0,
      status: 'active',
      description: '',
      image_url: '',
      file_name: '',
      file_path: ''
    }
    editingToolkit.value = false
  }, 300)
}

// 文件上传处理
const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    toolkitForm.value.file_name = file.name
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
      toolkitForm.value.image_url = e.target.result
    }
    reader.readAsDataURL(file)
    // 实际项目中应该上传图片到服务器并获取image_url
  }
}

// 提交表单
const handleSubmit = async () => {
  try {
    if (editingToolkit.value) {
      // 更新工具包
      await contentStore.updateToolkit(toolkitForm.value)
      Swal.fire('更新成功！', '工具包已更新。', 'success')
    } else {
      // 添加新工具包
      await contentStore.createToolkit(toolkitForm.value)
      Swal.fire('添加成功！', '工具包已添加。', 'success')
    }
    closeModal()
  } catch (error) {
    Swal.fire('错误', editingToolkit.value ? '更新工具包失败' : '添加工具包失败', 'error')
  }
}

// 获取工具包数据
const fetchToolkits = async () => {
  try {
    await contentStore.fetchToolkits()
    await contentStore.fetchCategories()
  } catch (error) {
    console.error('获取工具包列表失败:', error)
    Swal.fire('错误', '获取工具包列表失败', 'error')
  }
}

// 页面加载时获取数据
onMounted(async () => {
  await fetchToolkits()
})
</script>

<style scoped>
.toolkits-management-container {
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

/* 工具包网格 */
.toolkits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

/* 工具包卡片 */
.toolkit-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.3s ease;
}

.toolkit-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.toolkit-card.selected {
  border: 2px solid #409eff;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.toolkit-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  background-color: #f5f7fa;
}

.toolkit-status {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.toolkit-status.active {
  background-color: #ecf5ff;
  color: #409eff;
}

.toolkit-status.inactive {
  background-color: #fdf6ec;
  color: #e6a23c;
}

.toolkit-image {
  height: 200px;
  overflow: hidden;
  background-color: #f5f7fa;
}

.toolkit-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.toolkit-card:hover .toolkit-image img {
  transform: scale(1.05);
}

.toolkit-info {
  padding: 15px;
}

.toolkit-name {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #303133;
  font-weight: 600;
}

.toolkit-description {
  margin: 0 0 15px 0;
  font-size: 14px;
  color: #606266;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.toolkit-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.category {
  font-size: 12px;
  color: #909399;
  background-color: #f5f7fa;
  padding: 2px 8px;
  border-radius: 4px;
}

.price {
  font-size: 16px;
  color: #f56c6c;
  font-weight: 600;
}

.toolkit-stats {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #909399;
}

.toolkit-actions {
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
  
  .toolkits-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  }
  
  .batch-actions {
    flex-direction: column;
    gap: 10px;
  }
}

@media (max-width: 480px) {
  .toolkits-grid {
    grid-template-columns: 1fr;
  }
}
</style>