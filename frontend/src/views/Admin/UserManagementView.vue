<template>
  <div class="user-management-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>用户管理</h1>
      <div class="header-actions">
        <button class="export-btn" @click="handleExport">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="7 10 12 15 17 10"></polyline>
            <line x1="12" y1="15" x2="12" y2="3"></line>
          </svg>
          导出用户
        </button>
        <button class="add-btn" @click="openUserModal()">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          添加用户
        </button>
      </div>
    </div>

    <!-- 搜索和筛选 -->
    <div class="filter-section">
      <div class="search-box">
        <input 
          type="text" 
          placeholder="搜索用户名、邮箱或昵称" 
          v-model="searchQuery"
        >
        <button class="search-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </button>
      </div>

      <div class="filter-controls">
        <select v-model="roleFilter">
          <option value="">所有角色</option>
          <option value="user">普通用户</option>
          <option value="admin">管理员</option>
        </select>

        <select v-model="statusFilter">
          <option value="">所有状态</option>
          <option value="active">活跃</option>
          <option value="inactive">禁用</option>
        </select>

        <select v-model="sortBy">
          <option value="created_at">注册时间</option>
          <option value="username">用户名</option>
          <option value="email">邮箱</option>
        </select>

        <button class="filter-btn" @click="resetFilters">
          重置筛选
        </button>
      </div>
    </div>

    <!-- 用户列表 -->
    <div class="table-container">
      <table class="user-table">
        <thead>
          <tr>
            <th>
              <input type="checkbox" v-model="selectAll">
            </th>
            <th>ID</th>
            <th>头像</th>
            <th>用户名</th>
            <th>昵称</th>
            <th>邮箱</th>
            <th>角色</th>
            <th>状态</th>
            <th>注册时间</th>
            <th>最后登录</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in filteredUsers" :key="user.id" :class="{ selected: selectedUsers.includes(user.id) }">
            <td>
              <input type="checkbox" :checked="selectedUsers.includes(user.id)" @change="(e) => { if (e.target.checked) selectedUsers.push(user.id); else selectedUsers.splice(selectedUsers.indexOf(user.id), 1); }">
            </td>
            <td>{{ user.id }}</td>
            <td>
              <img class="user-avatar" :src="user.avatar_url || '/avatar-placeholder.png'" alt="用户头像">
            </td>
            <td>{{ user.username }}</td>
            <td>{{ user.nickname || '-' }}</td>
            <td>{{ user.email }}</td>
            <td>
              <span class="role-tag" :class="user.is_admin ? 'admin' : 'user'">
                {{ user.is_admin ? '管理员' : '普通用户' }}
              </span>
            </td>
            <td>
              <span class="status-tag" :class="user.is_active ? 'active' : 'inactive'">
                {{ user.is_active ? '活跃' : '禁用' }}
              </span>
            </td>
            <td>{{ formatDate(user.created_at) }}</td>
            <td>{{ formatDate(user.last_login) }}</td>
            <td class="action-buttons">
              <button class="view-btn" @click="openUserModal(user, true)">
                查看
              </button>
              <button class="edit-btn" @click="openUserModal(user)">
                编辑
              </button>
              <button 
                class="status-btn" 
                :class="user.is_active ? 'disable' : 'enable'"
                @click="handleToggleStatus(user)"
              >
                {{ user.is_active ? '禁用' : '启用' }}
              </button>
              <button class="delete-btn" @click="handleDeleteUser(user.id)">
                删除
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- 空状态 -->
      <div v-if="filteredUsers.length === 0" class="empty-state">
        <p>暂无用户数据</p>
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="filteredUsers.length > 0" class="pagination">
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
    <div v-if="selectedUsers.length > 0" class="batch-actions">
      <p>已选择 {{ selectedUsers.length }} 项</p>
      <div class="batch-buttons">
        <button class="batch-enable-btn" @click="handleBatchEnable">
          批量启用
        </button>
        <button class="batch-disable-btn" @click="handleBatchDisable">
          批量禁用
        </button>
        <button class="batch-delete-btn" @click="handleBatchDelete">
          批量删除
        </button>
        <button class="batch-export-btn" @click="handleBatchExport">
          批量导出
        </button>
      </div>
    </div>

    <!-- 添加/编辑用户模态框 -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ modalTitle }}</h3>
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
              <label>用户名</label>
              <input type="text" v-model="userForm.username" :disabled="isViewMode" required>
            </div>

            <div class="form-group">
              <label>昵称</label>
              <input type="text" v-model="userForm.nickname" :disabled="isViewMode">
            </div>

            <div class="form-group">
              <label>邮箱</label>
              <input type="email" v-model="userForm.email" :disabled="isViewMode" required>
            </div>

            <div class="form-group" v-if="!isViewMode && !editingUser">
              <label>密码</label>
              <input type="password" v-model="userForm.password" required>
            </div>

            <div class="form-group" v-if="!isViewMode && !editingUser">
              <label>确认密码</label>
              <input type="password" v-model="userForm.confirm_password" required>
            </div>

            <div class="form-group" v-if="!isViewMode">
              <label>角色</label>
              <select v-model="userForm.is_admin" required>
                <option :value="false">普通用户</option>
                <option :value="true">管理员</option>
              </select>
            </div>

            <div class="form-group" v-if="!isViewMode">
              <label>状态</label>
              <select v-model="userForm.is_active" required>
                <option :value="true">活跃</option>
                <option :value="false">禁用</option>
              </select>
            </div>

            <div class="form-group" v-if="!isViewMode">
              <label>头像</label>
              <input type="file" accept="image/*" @change="handleAvatarUpload">
              <div v-if="userForm.avatar_url" class="avatar-preview">
                <img :src="userForm.avatar_url" alt="头像预览">
              </div>
            </div>

            <div class="form-actions">
              <button type="button" class="cancel-btn" @click="closeModal">
                取消
              </button>
              <button type="submit" class="submit-btn" v-if="!isViewMode">
                {{ editingUser ? '更新用户' : '添加用户' }}
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
import { useAuthStore } from '../../stores'
import Swal from 'sweetalert2'

// 用户Store
const userStore = useAuthStore()

// 搜索筛选
const searchQuery = ref('')
const roleFilter = ref('')
const statusFilter = ref('')
const sortBy = ref('created_at')
const sortOrder = ref('desc')

// 分页
const currentPage = ref(1)
const pageSize = ref(10)

// 选择功能
const selectAll = ref(false)
const selectedUsers = ref([])

// 模态框
const showModal = ref(false)
const modalTitle = ref('')
const isViewMode = ref(false)
const editingUser = ref(null)

// 用户表单数据
const userForm = ref({
  id: '',
  username: '',
  nickname: '',
  email: '',
  is_admin: false,
  is_active: true,
  avatar_url: '',
  password: '',
  confirm_password: ''
})

// 监听全选
watch(selectAll, (newValue) => {
  if (newValue) {
    // 全选
    selectedUsers.value = filteredUsers.value.map(user => user.id)
  } else {
    // 取消全选
    selectedUsers.value = []
  }
})

// 监听选中用户变化
watch(selectedUsers, (newValue) => {
  if (newValue.length === filteredUsers.value.length && filteredUsers.value.length > 0) {
    selectAll.value = true
  } else {
    selectAll.value = false
  }
}, { deep: true })

// 监听筛选条件变化
watch([searchQuery, roleFilter, statusFilter], () => {
  currentPage.value = 1
  fetchUsers()
}, { deep: true })

// 监听分页变化
watch(currentPage, () => {
  fetchUsers()
})

// 监听每页数量变化
watch(pageSize, () => {
  currentPage.value = 1
  fetchUsers()
})

// 监听排序变化
watch([sortBy, sortOrder], () => {
  currentPage.value = 1
  fetchUsers()
})

// 过滤后的用户列表
const filteredUsers = computed(() => {
  return userStore.adminUsers
})

// 总页数
const totalPages = computed(() => {
  return Math.ceil(userStore.totalUsers / pageSize.value)
})

// 获取用户列表
const fetchUsers = async () => {
  try {
    // 准备筛选参数
    const params = {
      search: searchQuery.value,
      role: roleFilter.value,
      status: statusFilter.value,
      sort_by: sortBy.value,
      sort_order: sortOrder.value,
      page: currentPage.value,
      page_size: pageSize.value
    }
    
    // 调用store的API
    await userStore.fetchAdminUsers(params)
  } catch (error) {
    console.error('获取用户列表失败:', error)
    Swal.fire('获取失败', '加载用户列表时发生错误', 'error')
  }
}

// 切换排序
const toggleSort = (field) => {
  if (sortBy.value === field) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortBy.value = field
    sortOrder.value = 'asc'
  }
}

// 重置筛选条件
const resetFilters = () => {
  searchQuery.value = ''
  roleFilter.value = ''
  statusFilter.value = ''
  sortBy.value = 'created_at'
  sortOrder.value = 'desc'
  currentPage.value = 1
  fetchUsers()
}

// 导出用户列表
const handleExport = () => {
  Swal.fire('提示', '导出功能开发中...', 'info')
}

// 批量导出
const handleBatchExport = () => {
  if (selectedUsers.value.length === 0) return
  Swal.fire('提示', '批量导出功能开发中...', 'info')
}

// 打开用户模态框
const openUserModal = (user = null, isView = false) => {
  isViewMode.value = isView
  if (user) {
    // 编辑或查看用户
    editingUser.value = user
    modalTitle.value = isView ? '查看用户' : '编辑用户'
    userForm.value = {
      ...user
    }
  } else {
    // 添加新用户
    editingUser.value = null
    modalTitle.value = '添加用户'
    userForm.value = {
      id: '',
      username: '',
      nickname: '',
      email: '',
      is_admin: false,
      is_active: true,
      avatar_url: '',
      password: '',
      confirm_password: ''
    }
  }
  showModal.value = true
}

// 关闭模态框
const closeModal = () => {
  showModal.value = false
  editingUser.value = null
  isViewMode.value = false
}

// 处理头像上传
const handleAvatarUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    // 这里可以添加文件上传的API调用
    // 暂时只显示文件名
    userForm.value.avatar_url = file.name
  }
}

// 提交表单
const handleSubmit = async () => {
  try {
    // 验证密码
    if (!isViewMode.value && !editingUser.value && userForm.value.password !== userForm.value.confirm_password) {
      Swal.fire('错误', '两次输入的密码不一致', 'error')
      return
    }

    if (editingUser.value) {
      // 更新用户
      await userStore.updateUserRole(editingUser.value.id, userForm.value.is_admin ? 'admin' : 'user')
      Swal.fire('更新成功', '用户信息已更新', 'success')
    } else {
      // 添加新用户
      Swal.fire('提示', '添加用户功能开发中...', 'info')
    }
    closeModal()
  } catch (error) {
    console.error('保存用户失败:', error)
    Swal.fire('保存失败', '处理用户信息时发生错误', 'error')
  }
}

// 切换用户状态
const handleToggleStatus = async (user) => {
  try {
    const newStatus = !user.is_active
    const actionText = newStatus ? '启用' : '禁用'
    
    const result = await Swal.fire({
      title: `确定要${actionText}用户 "${user.username}" 吗？`,
      icon: 'question',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#6c757d',
      confirmButtonText: actionText,
      cancelButtonText: '取消'
    })

    if (result.isConfirmed) {
      await userStore.updateUserStatus(user.id, newStatus)
      Swal.fire('操作成功', `用户已${actionText}`, 'success')
    }
  } catch (error) {
    console.error('切换用户状态失败:', error)
    Swal.fire('操作失败', '处理用户状态时发生错误', 'error')
  }
}

// 删除用户
const handleDeleteUser = async (userId) => {
  try {
    const user = userStore.adminUsers.find(u => u.id === userId)
    if (!user) return
    
    const result = await Swal.fire({
      title: '确定要删除这个用户吗？',
      text: `删除用户 "${user.username}" 后将无法恢复！`,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#3085d6',
      confirmButtonText: '删除',
      cancelButtonText: '取消'
    })

    if (result.isConfirmed) {
      await userStore.deleteUser(userId)
      Swal.fire('删除成功', '用户已被删除', 'success')
    }
  } catch (error) {
    console.error('删除用户失败:', error)
    Swal.fire('删除失败', '处理删除用户时发生错误', 'error')
  }
}

// 批量启用
const handleBatchEnable = async () => {
  try {
    if (selectedUsers.value.length === 0) return
    
    const result = await Swal.fire({
      title: '确定要批量启用选中的用户吗？',
      icon: 'question',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#6c757d',
      confirmButtonText: '启用',
      cancelButtonText: '取消'
    })

    if (result.isConfirmed) {
      for (const userId of selectedUsers.value) {
        await userStore.updateUserStatus(userId, true)
      }
      selectedUsers.value = []
      selectAll.value = false
      Swal.fire('操作成功', '选中的用户已批量启用', 'success')
    }
  } catch (error) {
    console.error('批量启用用户失败:', error)
    Swal.fire('操作失败', '处理批量启用时发生错误', 'error')
  }
}

// 批量禁用
const handleBatchDisable = async () => {
  try {
    if (selectedUsers.value.length === 0) return
    
    const result = await Swal.fire({
      title: '确定要批量禁用选中的用户吗？',
      icon: 'question',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#6c757d',
      confirmButtonText: '禁用',
      cancelButtonText: '取消'
    })

    if (result.isConfirmed) {
      for (const userId of selectedUsers.value) {
        await userStore.updateUserStatus(userId, false)
      }
      selectedUsers.value = []
      selectAll.value = false
      Swal.fire('操作成功', '选中的用户已批量禁用', 'success')
    }
  } catch (error) {
    console.error('批量禁用用户失败:', error)
    Swal.fire('操作失败', '处理批量禁用时发生错误', 'error')
  }
}

// 批量删除
const handleBatchDelete = async () => {
  try {
    if (selectedUsers.value.length === 0) return
    
    const result = await Swal.fire({
      title: '确定要批量删除选中的用户吗？',
      text: '删除后将无法恢复！',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#3085d6',
      confirmButtonText: '删除',
      cancelButtonText: '取消'
    })

    if (result.isConfirmed) {
      await userStore.batchDeleteUsers(selectedUsers.value)
      selectedUsers.value = []
      selectAll.value = false
      Swal.fire('删除成功', '选中的用户已批量删除', 'success')
    }
  } catch (error) {
    console.error('批量删除用户失败:', error)
    Swal.fire('删除失败', '处理批量删除时发生错误', 'error')
  }
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 页面加载时获取数据
onMounted(async () => {
  await fetchUsers()
})
</script>

<style scoped>
.user-management-container {
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
.add-btn {
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

.add-btn {
  background-color: #409eff;
  color: #fff;
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

.user-table {
  width: 100%;
  border-collapse: collapse;
}

.user-table th,
.user-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #ebeef5;
}

.user-table th {
  background-color: #f5f7fa;
  font-weight: 600;
  color: #303133;
  font-size: 14px;
  white-space: nowrap;
}

.user-table td {
  color: #606266;
  font-size: 14px;
}

.user-table tr:hover {
  background-color: #f5f7fa;
}

.user-table tr.selected {
  background-color: #ecf5ff;
}

/* 用户头像 */
.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
}

/* 角色标签 */
.role-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.role-tag.admin {
  background-color: #f56c6c;
  color: #fff;
}

.role-tag.user {
  background-color: #67c23a;
  color: #fff;
}

/* 状态标签 */
.status-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.status-tag.active {
  background-color: #67c23a;
  color: #fff;
}

.status-tag.inactive {
  background-color: #909399;
  color: #fff;
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.view-btn,
.edit-btn,
.status-btn,
.delete-btn {
  padding: 4px 10px;
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
  background-color: #409eff;
  color: #fff;
}

.edit-btn:hover {
  background-color: #66b1ff;
}

.status-btn.enable {
  background-color: #67c23a;
  color: #fff;
}

.status-btn.enable:hover {
  background-color: #85ce61;
}

.status-btn.disable {
  background-color: #e6a23c;
  color: #fff;
}

.status-btn.disable:hover {
  background-color: #ebb563;
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

.batch-enable-btn,
.batch-disable-btn,
.batch-delete-btn,
.batch-export-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.batch-enable-btn {
  background-color: #67c23a;
  color: #fff;
}

.batch-enable-btn:hover {
  background-color: #85ce61;
}

.batch-disable-btn {
  background-color: #e6a23c;
  color: #fff;
}

.batch-disable-btn:hover {
  background-color: #ebb563;
}

.batch-delete-btn {
  background-color: #f56c6c;
  color: #fff;
}

.batch-delete-btn:hover {
  background-color: #f78989;
}

.batch-export-btn {
  background-color: #909399;
  color: #fff;
}

.batch-export-btn:hover {
  background-color: #a6a9ad;
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
  max-width: 500px;
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

/* 头像预览 */
.avatar-preview {
  margin-top: 10px;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  overflow: hidden;
  border: 1px solid #dcdfe6;
}

.avatar-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
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
@media (max-width: 1024px) {
  .user-table {
    overflow-x: auto;
    display: block;
  }
  
  .action-buttons {
    flex-direction: column;
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
}
</style>