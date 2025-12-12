<template>
  <div class="article-management-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>文章管理</h1>
      <button class="add-btn" @click="handleAddArticle">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        添加文章
      </button>
    </div>

    <!-- 搜索和筛选 -->
    <div class="filter-section">
      <div class="search-box">
        <input 
          type="text" 
          placeholder="搜索文章标题或内容" 
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
          <option value="published">已发布</option>
          <option value="draft">草稿</option>
        </select>

        <button class="filter-btn" @click="resetFilters">
          重置筛选
        </button>
      </div>
    </div>

    <!-- 文章列表 -->
    <div class="table-container">
      <table class="article-table">
        <thead>
          <tr>
            <th>
              <input type="checkbox" @change="toggleSelectAll">
            </th>
            <th>ID</th>
            <th>标题</th>
            <th>分类</th>
            <th>作者</th>
            <th>发布状态</th>
            <th>发布时间</th>
            <th>阅读量</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="article in filteredArticles" :key="article.id" :class="{ selected: selectedArticles.includes(article.id) }">
            <td>
              <input type="checkbox" :checked="selectedArticles.includes(article.id)" @change="toggleSelect(article.id)">
            </td>
            <td>{{ article.id }}</td>
            <td class="title-cell">
              <a href="#" @click="handleViewArticle(article)">{{ article.title }}</a>
            </td>
            <td>{{ getCategoryName(article.category_id) }}</td>
            <td>{{ article.author }}</td>
            <td>
              <span class="status-tag" :class="article.status">
                {{ article.status === 'published' ? '已发布' : '草稿' }}
              </span>
            </td>
            <td>{{ formatDate(article.published_at) }}</td>
            <td>{{ article.views }}</td>
            <td class="action-buttons">
              <button class="view-btn" @click="handleViewArticle(article)">
                查看
              </button>
              <button class="edit-btn" @click="handleEditArticle(article)">
                编辑
              </button>
              <button class="delete-btn" @click="handleDeleteArticle(article.id)">
                删除
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- 空状态 -->
      <div v-if="filteredArticles.length === 0" class="empty-state">
        <p>暂无文章数据</p>
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="filteredArticles.length > 0" class="pagination">
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

    <!-- 批量操作 -->
    <div v-if="selectedArticles.length > 0" class="batch-actions">
      <p>已选择 {{ selectedArticles.length }} 项</p>
      <div class="batch-buttons">
        <button class="batch-publish-btn" @click="handleBatchPublish">
          批量发布
        </button>
        <button class="batch-draft-btn" @click="handleBatchDraft">
          批量设为草稿
        </button>
        <button class="batch-delete-btn" @click="handleBatchDelete">
          批量删除
        </button>
      </div>
    </div>

    <!-- 添加/编辑文章模态框 -->
    <div v-if="showArticleModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editingArticle ? '编辑文章' : '添加文章' }}</h3>
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
              <label>标题</label>
              <input type="text" v-model="articleForm.title" required>
            </div>

            <div class="form-group">
              <label>分类</label>
              <select v-model="articleForm.category_id" required>
                <option value="">请选择分类</option>
                <option v-for="category in categories" :key="category.id" :value="category.id">
                  {{ category.name }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label>作者</label>
              <input type="text" v-model="articleForm.author" required>
            </div>

            <div class="form-group">
              <label>发布状态</label>
              <select v-model="articleForm.status" required>
                <option value="draft">草稿</option>
                <option value="published">已发布</option>
              </select>
            </div>

            <div class="form-group">
              <label>内容</label>
              <textarea v-model="articleForm.content" rows="10" required></textarea>
            </div>

            <div class="form-group">
              <label>封面图片</label>
              <input type="file" accept="image/*" @change="handleImageUpload">
              <div v-if="articleForm.cover_image" class="image-preview">
                <img :src="articleForm.cover_image" alt="封面预览">
              </div>
            </div>

            <div class="form-actions">
              <button type="button" class="cancel-btn" @click="closeModal">
                取消
              </button>
              <button type="submit" class="submit-btn">
                {{ editingArticle ? '更新文章' : '保存文章' }}
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
import { useRouter } from 'vue-router'
import Swal from 'sweetalert2'

const contentStore = useContentStore()
const router = useRouter()

// 搜索和筛选
const searchQuery = ref('')
const categoryFilter = ref('')
const statusFilter = ref('')

// 选择功能
const selectedArticles = ref([])
const selectAll = ref(false)

// 模态框
const showArticleModal = ref(false)
const editingArticle = ref(false)

// 表单数据
const articleForm = ref({
  title: '',
  category_id: '',
  author: '',
  status: 'draft',
  content: '',
  cover_image: ''
})

// 分类列表
const categories = ref([])

// 计算过滤后的文章
const filteredArticles = computed(() => {
  return contentStore.adminArticles
})

// 总页数
const totalPages = computed(() => {
  return Math.ceil(contentStore.totalArticles / contentStore.pageSize)
})

// 获取分类名称
const getCategoryName = (categoryId) => {
  const category = categories.value.find(c => c.id === categoryId)
  return category ? category.name : '未分类'
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

// 监听筛选条件变化，更新store
watch([searchQuery, categoryFilter, statusFilter], () => {
  contentStore.setFilter({
    search: searchQuery.value,
    category: categoryFilter.value,
    status: statusFilter.value
  })
  fetchArticles()
})

// 监听当前页码变化
watch(() => contentStore.currentPage, (newPage) => {
  fetchArticles()
})

// 搜索处理
const handleSearch = () => {
  contentStore.setCurrentPage(1)
}

// 筛选处理
const handleFilter = () => {
  contentStore.setCurrentPage(1)
}

// 重置筛选
const resetFilters = () => {
  searchQuery.value = ''
  categoryFilter.value = ''
  statusFilter.value = ''
  contentStore.setCurrentPage(1)
  contentStore.setFilter({ search: '', category: '', status: '' })
  fetchArticles()
}

// 全选/取消全选
const toggleSelectAll = () => {
  selectAll.value = !selectAll.value
  if (selectAll.value) {
    selectedArticles.value = filteredArticles.value.map(article => article.id)
  } else {
    selectedArticles.value = []
  }
}

// 单个选择
const toggleSelect = (articleId) => {
  const index = selectedArticles.value.indexOf(articleId)
  if (index > -1) {
    selectedArticles.value.splice(index, 1)
    selectAll.value = false
  } else {
    selectedArticles.value.push(articleId)
    if (selectedArticles.value.length === filteredArticles.value.length) {
      selectAll.value = true
    }
  }
}

// 获取文章列表和分类
const fetchArticles = async () => {
  try {
    await contentStore.fetchAdminArticles()
    // 获取分类列表
    if (contentStore.categories.length === 0) {
      await contentStore.fetchCategories()
      categories.value = contentStore.categories
    }
  } catch (error) {
    console.error('获取文章列表失败:', error)
    Swal.fire('错误', '获取文章列表失败', 'error')
  }
}

// 添加文章
const handleAddArticle = () => {
  editingArticle.value = false
  articleForm.value = {
    title: '',
    category_id: '',
    author: '',
    status: 'draft',
    content: '',
    cover_image: ''
  }
  showArticleModal.value = true
}

// 编辑文章
const handleEditArticle = (article) => {
  editingArticle.value = true
  articleForm.value = { ...article }
  showArticleModal.value = true
}

// 查看文章
const handleViewArticle = (article) => {
  // 这里可以添加查看文章详情的逻辑
  console.log('查看文章:', article)
}

// 删除文章
const handleDeleteArticle = async (articleId) => {
  const result = await Swal.fire({
    title: '确定要删除这篇文章吗？',
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
      await contentStore.deleteArticle(articleId)
      await fetchArticles()
      Swal.fire('删除成功！', '文章已被删除。', 'success')
    } catch (error) {
      Swal.fire('错误', contentStore.error || '删除文章失败', 'error')
    }
  }
}

// 批量发布
const handleBatchPublish = async () => {
  const result = await Swal.fire({
    title: '确定要批量发布选中的文章吗？',
    icon: 'question',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#6c757d',
    confirmButtonText: '发布',
    cancelButtonText: '取消'
  })

  if (result.isConfirmed) {
    try {
      await contentStore.batchPublishArticles(selectedArticles.value)
      await fetchArticles()
      selectedArticles.value = []
      selectAll.value = false
      Swal.fire('发布成功！', '选中的文章已批量发布。', 'success')
    } catch (error) {
      Swal.fire('错误', contentStore.error || '批量发布文章失败', 'error')
    }
  }
}

// 批量设为草稿
const handleBatchDraft = async () => {
  const result = await Swal.fire({
    title: '确定要批量将选中的文章设为草稿吗？',
    icon: 'question',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#6c757d',
    confirmButtonText: '设为草稿',
    cancelButtonText: '取消'
  })

  if (result.isConfirmed) {
    try {
      await contentStore.batchDraftArticles(selectedArticles.value)
      await fetchArticles()
      selectedArticles.value = []
      selectAll.value = false
      Swal.fire('操作成功！', '选中的文章已批量设为草稿。', 'success')
    } catch (error) {
      Swal.fire('错误', contentStore.error || '批量设为草稿失败', 'error')
    }
  }
}

// 批量删除
const handleBatchDelete = async () => {
  const result = await Swal.fire({
    title: '确定要批量删除选中的文章吗？',
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
      await contentStore.batchDeleteArticles(selectedArticles.value)
      await fetchArticles()
      selectedArticles.value = []
      selectAll.value = false
      Swal.fire('删除成功！', '选中的文章已批量删除。', 'success')
    } catch (error) {
      Swal.fire('错误', contentStore.error || '批量删除文章失败', 'error')
    }
  }
}

// 关闭模态框
const closeModal = () => {
  showArticleModal.value = false
  setTimeout(() => {
    articleForm.value = {
      title: '',
      category_id: '',
      author: '',
      status: 'draft',
      content: '',
      cover_image: ''
    }
    editingArticle.value = false
  }, 300)
}

// 图片上传处理
const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      articleForm.value.cover_image = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

// 提交表单
const handleSubmit = async () => {
  try {
    if (editingArticle.value) {
      // 更新文章
      await contentStore.updateArticle(articleForm.value.id, articleForm.value)
      await fetchArticles()
      Swal.fire('更新成功！', '文章已更新。', 'success')
    } else {
      // 添加新文章
      await contentStore.createArticle(articleForm.value)
      await fetchArticles()
      Swal.fire('添加成功！', '文章已添加。', 'success')
    }
    closeModal()
  } catch (error) {
    Swal.fire('错误', contentStore.error || '保存文章失败', 'error')
  }
}

// 页面加载时获取数据
onMounted(async () => {
  await fetchArticles()
})
</script>

<style scoped>
.article-management-container {
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

/* 表格容器 */
.table-container {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin-bottom: 20px;
}

.article-table {
  width: 100%;
  border-collapse: collapse;
}

.article-table th,
.article-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #ebeef5;
}

.article-table th {
  background-color: #f5f7fa;
  font-weight: 600;
  color: #303133;
  font-size: 14px;
}

.article-table td {
  color: #606266;
  font-size: 14px;
}

.article-table tr:hover {
  background-color: #f5f7fa;
}

.article-table tr.selected {
  background-color: #ecf5ff;
}

.title-cell a {
  color: #409eff;
  text-decoration: none;
  transition: color 0.3s ease;
}

.title-cell a:hover {
  color: #66b1ff;
  text-decoration: underline;
}

/* 状态标签 */
.status-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.status-tag.published {
  background-color: #ecf5ff;
  color: #409eff;
}

.status-tag.draft {
  background-color: #fdf6ec;
  color: #e6a23c;
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  gap: 8px;
}

.view-btn,
.edit-btn,
.delete-btn {
  padding: 4px 12px;
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

.batch-publish-btn,
.batch-draft-btn,
.batch-delete-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.batch-publish-btn {
  background-color: #409eff;
  color: #fff;
}

.batch-publish-btn:hover {
  background-color: #66b1ff;
}

.batch-draft-btn {
  background-color: #e6a23c;
  color: #fff;
}

.batch-draft-btn:hover {
  background-color: #ebb563;
}

.batch-delete-btn {
  background-color: #f56c6c;
  color: #fff;
}

.batch-delete-btn:hover {
  background-color: #f78989;
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
  
  .article-table {
    overflow-x: auto;
    display: block;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .batch-actions {
    flex-direction: column;
    gap: 10px;
  }
}
</style>