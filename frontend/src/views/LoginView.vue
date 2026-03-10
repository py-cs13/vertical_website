<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-header">
        <h1>登录</h1>
        <p>欢迎回到母婴健康垂直站</p>
      </div>
      
      <div class="auth-form">
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="email">邮箱</label>
            <input 
              type="email" 
              id="email" 
              v-model="email" 
              placeholder="请输入您的邮箱" 
              required
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label for="password">密码</label>
            <input 
              type="password" 
              id="password" 
              v-model="password" 
              placeholder="请输入您的密码" 
              required
              class="form-input"
            />
          </div>
          
          <div class="form-actions">
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? '登录中...' : '登录' }}
            </button>
          </div>
          
          <div class="form-footer">
            <p>还没有账号？<a href="#" @click.prevent="$router.push('/register')">立即注册</a></p>
            <p><a href="#" @click.prevent="forgotPassword">忘记密码？</a></p>
          </div>
        </form>
        
        <!-- 错误提示 -->
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores'

const router = useRouter()
const userStore = useAuthStore()

// 表单数据
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

// 组件挂载时重置表单数据、错误信息，并滚动到页面顶部
onMounted(() => {
  email.value = ''
  password.value = ''
  error.value = ''
  
  // 滚动到页面顶部 - 添加小延迟确保组件完全挂载
  setTimeout(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }, 50)
})

// 处理登录
  const handleLogin = async () => {
    loading.value = true
    error.value = ''
    
    try {
      const result = await userStore.login(email.value, password.value)
      if (result && result.access_token) {
        // 登录成功，跳转到首页
        router.push('/')
      } else {
        error.value = userStore.error || '邮箱或密码错误，请重试'
      }
    } catch (err) {
      error.value = userStore.error || '登录失败，请检查网络连接或稍后重试'
      console.error('登录错误:', err)
    } finally {
      loading.value = false
    }
  }

// 忘记密码
const forgotPassword = () => {
  // 这里可以实现忘记密码逻辑
  alert('忘记密码功能将在后续版本中实现')
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #FFF5F8 0%, #F0F8FF 100%);
  padding: 20px;
}

.auth-container {
  background-color: white;
  border-radius: 12px;
  padding: 40px;
  box-shadow: var(--shadow-medium);
  max-width: 400px;
  width: 100%;
}

.auth-header {
  text-align: center;
  margin-bottom: 30px;
}

.auth-header h1 {
  font-size: 28px;
  font-weight: 700;
  color: var(--primary-color);
  margin-bottom: 10px;
}

.auth-header p {
  font-size: 14px;
  color: var(--text-secondary);
}

.auth-form {
  width: 100%;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.form-input {
  width: 100%;
  padding: 12px;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  font-size: 15px;
  transition: all 0.3s ease;
  background-color: var(--bg-secondary);
}

.form-input:focus {
  outline: none;
  border-color: var(--primary-color);
  background-color: white;
  box-shadow: 0 0 0 3px rgba(255, 105, 180, 0.1);
}

.form-actions {
  margin-top: 30px;
}

.btn {
  width: 100%;
  padding: 14px;
  border: none;
  border-radius: 25px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
}

.btn-primary:hover {
  background-color: #FF4785;
  transform: translateY(-2px);
  box-shadow: var(--shadow-medium);
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.form-footer {
  margin-top: 20px;
  text-align: center;
  font-size: 14px;
}

.form-footer p {
  margin-bottom: 10px;
  color: var(--text-secondary);
}

.form-footer a {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 500;
}

.form-footer a:hover {
  text-decoration: underline;
}

.error-message {
  margin-top: 20px;
  padding: 12px;
  background-color: #FFF0F0;
  border: 1px solid #FFB3B3;
  border-radius: 8px;
  color: #FF6B6B;
  font-size: 14px;
  text-align: center;
}

/* 响应式设计 */
@media (max-width: 576px) {
  .auth-container {
    padding: 30px 20px;
  }
  
  .auth-header h1 {
    font-size: 24px;
  }
  
  .btn {
    padding: 12px;
    font-size: 15px;
  }
}
</style>