<template>
  <div class="payment-view">
    <!-- 支付页面头部 -->
    <div class="payment-header">
      <h1 class="page-title">订单支付</h1>
      <div class="payment-steps">
        <div class="step" :class="{ active: currentStep === 1, completed: currentStep > 1 }">
          <div class="step-number">1</div>
          <div class="step-name">订单确认</div>
        </div>
        <div class="step-arrow">→</div>
        <div class="step" :class="{ active: currentStep === 2, completed: currentStep > 2 }">
          <div class="step-number">2</div>
          <div class="step-name">支付方式</div>
        </div>
        <div class="step-arrow">→</div>
        <div class="step" :class="{ active: currentStep === 3, completed: currentStep > 3 }">
          <div class="step-number">3</div>
          <div class="step-name">支付结果</div>
        </div>
      </div>
    </div>

    <!-- 母婴主题装饰 -->
    <div class="theme-decoration">
      <div class="decoration-item">👶</div>
      <div class="decoration-item">🎀</div>
      <div class="decoration-item">💖</div>
      <div class="decoration-item">🍼</div>
      <div class="decoration-item">🤰</div>
    </div>

    <!-- 订单确认步骤 -->
    <div v-if="currentStep === 1" class="payment-step step-1">
      <div class="payment-card">
        <h2 class="card-title">订单信息</h2>
        <div class="order-info">
          <div class="order-item">
            <span class="label">商品名称：</span>
            <span class="value">{{ orderInfo.productName }}</span>
          </div>
          <div class="order-item">
            <span class="label">商品类型：</span>
            <span class="value">{{ orderInfo.productType === 'toolkit' ? '工具包' : '文章' }}</span>
          </div>
          <div class="order-item">
            <span class="label">商品价格：</span>
            <span class="value price">¥{{ orderInfo.price.toFixed(2) }}</span>
          </div>
          <div class="order-item">
            <span class="label">订单号：</span>
            <span class="value">{{ orderInfo.orderId }}</span>
          </div>
          <div class="order-item">
            <span class="label">创建时间：</span>
            <span class="value">{{ orderInfo.createTime }}</span>
          </div>
        </div>
        
        <h3 class="section-title">收货信息</h3>
        <div class="address-info">
          <div class="address-item">
            <span class="label">收货人：</span>
            <span class="value">{{ userInfo.name }}</span>
          </div>
          <div class="address-item">
            <span class="label">联系电话：</span>
            <span class="value">{{ userInfo.phone }}</span>
          </div>
          <div class="address-item">
            <span class="label">邮箱：</span>
            <span class="value">{{ userInfo.email }}</span>
          </div>
        </div>
        
        <div class="order-total">
          <span class="total-label">应付金额：</span>
          <span class="total-price">¥{{ orderInfo.price.toFixed(2) }}</span>
        </div>
        
        <div class="payment-actions">
          <button class="btn btn-primary" @click="nextStep">继续支付</button>
          <button class="btn btn-secondary" @click="cancelPayment">取消订单</button>
        </div>
      </div>
    </div>

    <!-- 支付方式选择步骤 -->
    <div v-if="currentStep === 2" class="payment-step step-2">
      <div class="payment-card">
        <h2 class="card-title">选择支付方式</h2>
        
        <div class="payment-methods">
          <div 
            v-for="method in paymentMethods" 
            :key="method.id" 
            class="payment-method" 
            :class="{ active: selectedPayment === method.id }"
            @click="selectedPayment = method.id"
          >
            <div class="method-icon">{{ method.icon }}</div>
            <div class="method-info">
              <div class="method-name">{{ method.name }}</div>
              <div class="method-desc">{{ method.desc }}</div>
            </div>
            <div class="method-radio">
              <div class="radio-circle" :class="{ checked: selectedPayment === method.id }"></div>
            </div>
          </div>
        </div>
        
        <div class="order-summary">
          <div class="summary-item">
            <span class="label">商品金额：</span>
            <span class="value">¥{{ orderInfo.price.toFixed(2) }}</span>
          </div>
          <div class="summary-item">
            <span class="label">优惠金额：</span>
            <span class="value discount">-¥{{ orderInfo.discount.toFixed(2) }}</span>
          </div>
          <div class="summary-item total">
            <span class="label">实付金额：</span>
            <span class="value">¥{{ (orderInfo.price - orderInfo.discount).toFixed(2) }}</span>
          </div>
        </div>
        
        <div class="payment-actions">
          <button class="btn btn-primary" @click="processPayment">立即支付</button>
          <button class="btn btn-secondary" @click="prevStep">返回上一步</button>
        </div>
      </div>
    </div>

    <!-- 支付结果步骤 -->
    <div v-if="currentStep === 3" class="payment-step step-3">
      <div class="payment-card result-card">
        <div class="result-icon" :class="paymentResult.status">
          {{ paymentResult.status === 'success' ? '✅' : '❌' }}
        </div>
        <h2 class="result-title">{{ paymentResult.title }}</h2>
        <p class="result-message">{{ paymentResult.message }}</p>
        
        <div v-if="paymentResult.status === 'success'" class="result-details">
          <div class="detail-item">
            <span class="label">支付方式：</span>
            <span class="value">{{ selectedPaymentName }}</span>
          </div>
          <div class="detail-item">
            <span class="label">支付金额：</span>
            <span class="value price">¥{{ (orderInfo.price - orderInfo.discount).toFixed(2) }}</span>
          </div>
          <div class="detail-item">
            <span class="label">支付时间：</span>
            <span class="value">{{ paymentResult.payTime }}</span>
          </div>
          <div class="detail-item download-section">
            <span class="label">下载工具包：</span>
            <a href="#" class="download-link" @click.prevent="downloadToolkit">
              📥 立即下载 {{ orderInfo.productName }}
            </a>
          </div>
        </div>
        
        <div class="payment-actions">
          <button v-if="paymentResult.status === 'success'" class="btn btn-primary" @click="goToUserCenter">查看订单</button>
          <button v-if="paymentResult.status === 'success'" class="btn btn-success" @click="downloadToolkit">立即下载</button>
          <button v-else class="btn btn-primary" @click="retryPayment">重新支付</button>
          <button class="btn btn-secondary" @click="goToHome">返回首页</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores'

const route = useRoute()
const router = useRouter()
const userStore = useAuthStore()

// 支付步骤
const currentStep = ref(1)

// 支付方式
const paymentMethods = ref([
  { id: 1, name: '微信支付', icon: '💬', desc: '推荐使用微信支付，安全快捷' },
  { id: 2, name: '支付宝', icon: '🐜', desc: '支持扫码支付和账号支付' },
  { id: 3, name: '银行卡', icon: '💳', desc: '支持国内外主流银行卡' }
])

// 选中的支付方式
const selectedPayment = ref(1)

// 模拟订单信息
const orderInfo = ref({
  orderId: '',
  productId: '',
  productName: '',
  productType: '',
  price: 0,
  discount: 0,
  createTime: ''
})

// 模拟用户信息
const userInfo = ref({
  name: '宝宝妈妈',
  phone: '138****8888',
  email: 'mama@example.com'
})

// 支付结果
const paymentResult = ref({
  status: '', // success or failed
  title: '',
  message: '',
  payTime: ''
})

// 计算属性：选中的支付方式名称
const selectedPaymentName = computed(() => {
  const method = paymentMethods.value.find(m => m.id === selectedPayment.value)
  return method ? method.name : ''
})

// 生成订单号
const generateOrderId = () => {
  const timestamp = Date.now()
  const random = Math.floor(Math.random() * 10000)
  return `ORDER${timestamp}${random.toString().padStart(4, '0')}`
}

// 初始化订单信息
onMounted(() => {
  // 从查询参数获取商品信息
  const { product_type, product_id, product_name, price } = route.query
  
  if (product_id) {
    orderInfo.value = {
      orderId: generateOrderId(),
      productId: product_id,
      productName: product_name || `商品 #${product_id}`,
      productType: product_type || 'toolkit',
      price: parseFloat(price) || 99.0,
      discount: Math.min(parseFloat(price) * 0.1, 10), // 10%优惠，最高10元
      createTime: new Date().toLocaleString('zh-CN')
    }
  } else {
    // 默认订单信息
    orderInfo.value = {
      orderId: generateOrderId(),
      productId: '1',
      productName: '家庭健康管理工具包',
      productType: 'toolkit',
      price: 99.00,
      discount: 9.90,
      createTime: new Date().toLocaleString('zh-CN')
    }
  }
})

// 下一步
const nextStep = () => {
  if (currentStep.value < 3) {
    currentStep.value++
  }
}

// 上一步
const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

// 处理支付
const processPayment = () => {
  // 模拟支付过程
  setTimeout(() => {
    // 随机模拟支付成功或失败（90%成功率）
    const success = Math.random() > 0.1
    
    paymentResult.value = {
      status: success ? 'success' : 'failed',
      title: success ? '支付成功' : '支付失败',
      message: success ? '您的订单已支付成功，感谢您的购买！' : '支付失败，请检查支付信息后重试。',
      payTime: success ? new Date().toLocaleString('zh-CN') : ''
    }
    
    currentStep.value = 3
  }, 1500)
}

// 重试支付
const retryPayment = () => {
  currentStep.value = 2
  paymentResult.value = {
    status: '',
    title: '',
    message: '',
    payTime: ''
  }
}

// 取消支付
const cancelPayment = () => {
  if (confirm('确定要取消订单吗？')) {
    router.push('/')
  }
}

// 返回首页
const goToHome = () => {
  router.push('/')
}

// 前往用户中心
const goToUserCenter = () => {
  router.push('/user')
}

// 下载工具包
const downloadToolkit = async () => {
  try {
    // 调用后端API获取下载链接
    const response = await axios.get(`/api/download/${orderInfo.value.productId}`, {
      responseType: 'blob' // 重要：指定响应类型为二进制数据
    })
    
    // 创建下载链接
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `${orderInfo.value.productName}.zip`) // 设置下载文件名
    document.body.appendChild(link)
    link.click()
    
    // 清理
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
    console.log('下载工具包成功:', orderInfo.value.productName)
  } catch (error) {
    console.error('下载工具包失败:', error)
    alert('下载失败，请稍后重试')
  }
}
</script>

<style scoped>
.payment-view {
  max-width: 100%;
  position: relative;
  overflow: hidden;
}

/* 母婴主题装饰 */
.theme-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: -1;
  opacity: 0.05;
}

.decoration-item {
  position: absolute;
  font-size: 80px;
  animation: float 15s infinite ease-in-out;
}

.decoration-item:nth-child(1) { top: 10%; left: 5%; animation-delay: 0s; }
.decoration-item:nth-child(2) { top: 20%; right: 10%; animation-delay: 3s; }
.decoration-item:nth-child(3) { bottom: 20%; left: 15%; animation-delay: 6s; }
.decoration-item:nth-child(4) { bottom: 10%; right: 5%; animation-delay: 9s; }
.decoration-item:nth-child(5) { top: 50%; left: 50%; transform: translate(-50%, -50%); animation-delay: 12s; }

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  25% { transform: translateY(-20px) rotate(5deg); }
  50% { transform: translateY(10px) rotate(0deg); }
  75% { transform: translateY(-10px) rotate(-5deg); }
}

/* 支付页面头部 */
.payment-header {
  margin-bottom: 40px;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 30px;
  color: var(--text-primary);
  text-align: center;
}

.payment-steps {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 30px;
  margin-bottom: 40px;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--bg-secondary);
  color: var(--text-secondary);
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: 600;
  transition: all 0.3s ease;
}

.step.active .step-number {
  background-color: var(--primary-color);
  color: white;
}

.step.completed .step-number {
  background-color: var(--success-color);
  color: white;
}

.step-name {
  font-size: 14px;
  color: var(--text-secondary);
}

.step.active .step-name {
  color: var(--primary-color);
  font-weight: 500;
}

.step.completed .step-name {
  color: var(--success-color);
  font-weight: 500;
}

.step-arrow {
  color: var(--border-color);
  font-size: 20px;
}

/* 支付卡片 */
.payment-card {
  background-color: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: var(--shadow-medium);
  max-width: 600px;
  margin: 0 auto;
}

.card-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 25px;
  color: var(--text-primary);
  border-bottom: 2px solid var(--primary-color);
  padding-bottom: 15px;
}

/* 订单信息 */
.order-info {
  margin-bottom: 30px;
}

.order-item {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid var(--border-color);
}

.order-item:last-child {
  border-bottom: none;
}

.label {
  color: var(--text-secondary);
  font-size: 15px;
}

.value {
  color: var(--text-primary);
  font-size: 15px;
  font-weight: 500;
}

.value.price {
  color: var(--primary-color);
  font-size: 18px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 20px;
  color: var(--text-primary);
  margin-top: 30px;
}

/* 收货信息 */
.address-info {
  background-color: var(--bg-secondary);
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.address-item {
  display: flex;
  margin-bottom: 10px;
}

.address-item:last-child {
  margin-bottom: 0;
}

.address-item .label {
  width: 80px;
  flex-shrink: 0;
}

/* 订单总计 */
.order-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background-color: var(--bg-accent);
  border-radius: 8px;
  margin-top: 20px;
}

.order-total .label {
  font-size: 18px;
  font-weight: 600;
}

.order-total .value {
  font-size: 24px;
  color: var(--primary-color);
}

/* 支付方式 */
.payment-methods {
  margin-bottom: 30px;
}

.payment-method {
  display: flex;
  align-items: center;
  padding: 20px;
  border: 2px solid var(--border-color);
  border-radius: 12px;
  margin-bottom: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.payment-method:hover {
  border-color: var(--primary-color);
  background-color: var(--bg-accent);
}

.payment-method.active {
  border-color: var(--primary-color);
  background-color: var(--bg-accent);
}

.method-icon {
  font-size: 32px;
  margin-right: 20px;
}

.method-info {
  flex: 1;
}

.method-name {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 5px;
  color: var(--text-primary);
}

.method-desc {
  font-size: 14px;
  color: var(--text-secondary);
}

.method-radio {
  margin-left: 20px;
}

.radio-circle {
  width: 20px;
  height: 20px;
  border: 2px solid var(--border-color);
  border-radius: 50%;
  position: relative;
  transition: all 0.3s ease;
}

.radio-circle.checked {
  border-color: var(--primary-color);
  background-color: var(--primary-color);
}

.radio-circle.checked::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: white;
}

/* 订单摘要 */
.order-summary {
  background-color: var(--bg-secondary);
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
}

.summary-item.total {
  font-weight: 600;
  font-size: 18px;
  border-top: 2px solid var(--border-color);
  margin-top: 10px;
  padding-top: 15px;
}

.discount {
  color: var(--success-color);
}

/* 支付结果 */
.result-card {
  text-align: center;
}

.result-icon {
  font-size: 80px;
  margin-bottom: 25px;
  animation: bounceIn 0.6s ease;
}

.result-icon.success {
  color: var(--success-color);
}

.result-icon.failed {
  color: #FF6B6B;
}

@keyframes bounceIn {
  0% { transform: scale(0.3); opacity: 0; }
  50% { transform: scale(1.05); opacity: 1; }
  70% { transform: scale(0.9); }
  100% { transform: scale(1); }
}

.result-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 15px;
}

.result-icon.success + .result-title {
  color: var(--success-color);
}

.result-icon.failed + .result-title {
  color: #FF6B6B;
}

.result-message {
  font-size: 16px;
  color: var(--text-secondary);
  margin-bottom: 30px;
  line-height: 1.6;
}

.result-details {
  background-color: var(--bg-secondary);
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
  display: inline-block;
  text-align: left;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  min-width: 300px;
}

.download-section {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid var(--border-color);
}

.download-link {
  color: var(--success-color);
  text-decoration: none;
  font-weight: 600;
  cursor: pointer;
  transition: color 0.3s ease;
}

.download-link:hover {
  color: #2ecc71;
  text-decoration: underline;
}

.btn-success {
  background-color: var(--success-color);
  color: white;
}

.btn-success:hover {
  background-color: #2ecc71;
  transform: translateY(-2px);
  box-shadow: var(--shadow-medium);
}

/* 按钮样式 */
.payment-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-top: 30px;
}

.btn {
  padding: 12px 30px;
  border-radius: 25px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
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

.btn-secondary {
  background-color: var(--bg-secondary);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.btn-secondary:hover {
  background-color: var(--border-color);
  transform: translateY(-2px);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .payment-card {
    padding: 20px;
    margin: 0 15px;
  }
  
  .payment-steps {
    flex-wrap: wrap;
    gap: 20px;
  }
  
  .step-name {
    font-size: 12px;
  }
  
  .payment-method {
    padding: 15px;
  }
  
  .method-icon {
    font-size: 24px;
    margin-right: 15px;
  }
  
  .method-name {
    font-size: 14px;
  }
  
  .method-desc {
    font-size: 12px;
  }
  
  .order-item, .summary-item, .detail-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
  
  .order-total {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .payment-actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
  }
  
  .address-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
  
  .detail-item {
    min-width: auto;
  }
}
</style>