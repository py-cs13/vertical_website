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

    <!-- 订单确认步骤 -->
    <div v-if="currentStep === 1" class="payment-step step-1">
      <div class="payment-card">
        <h2 class="card-title">确认订单信息</h2>
        
        <div class="order-info">
          <div class="info-item">
            <span class="label">产品类型：</span>
            <span class="value">{{ getProductTypeText() }}</span>
          </div>
          <div class="info-item">
            <span class="label">产品名称：</span>
            <span class="value">{{ orderInfo.title }}</span>
          </div>
          <div class="info-item">
            <span class="label">商品价格：</span>
            <span class="value price">¥{{ orderInfo.price.toFixed(2) }}</span>
          </div>
          <div v-if="orderInfo.discount > 0" class="info-item">
            <span class="label">优惠金额：</span>
            <span class="value discount">-¥{{ orderInfo.discount.toFixed(2) }}</span>
          </div>
          <div class="info-item order-total">
            <span class="label">实付金额：</span>
            <span class="value total-price">¥{{ (orderInfo.price - orderInfo.discount).toFixed(2) }}</span>
          </div>
        </div>

        <div class="payment-actions">
          <button class="btn btn-primary" @click="proceedToPayment">确认并支付</button>
          <button class="btn btn-secondary" @click="cancelOrder">取消订单</button>
        </div>
      </div>
    </div>

    <!-- 支付方式选择步骤 -->
    <div v-if="currentStep === 2" class="payment-step step-2">
      <div class="payment-card">
        <h2 class="card-title">选择支付方式</h2>
        
        <div class="order-summary">
          <div class="summary-item">
            <span>商品：{{ orderInfo.title }}</span>
            <span>¥{{ (orderInfo.price - orderInfo.discount).toFixed(2) }}</span>
          </div>
        </div>

        <div class="payment-methods">
          <div 
            v-for="method in paymentMethods" 
            :key="method.id"
            class="payment-method"
            :class="{ active: selectedPayment === method.id }"
            @click="selectPayment(method.id)"
          >
            <div class="method-info">
              <div class="method-icon">{{ method.icon }}</div>
              <div class="method-details">
                <div class="method-name">{{ method.name }}</div>
                <div class="method-desc">{{ method.description }}</div>
              </div>
            </div>
            <div class="method-radio">
              <input 
                type="radio" 
                :value="method.id" 
                v-model="selectedPayment"
                class="radio-input"
              >
            </div>
          </div>
        </div>

        <div class="payment-actions">
          <button class="btn btn-primary" @click="confirmPayment">确认支付</button>
          <button class="btn btn-secondary" @click="backToOrder">返回订单</button>
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
        </div>
        <button v-else class="btn btn-primary" @click="retryPayment">重新支付</button>
        <button class="btn btn-secondary" @click="goToHome">返回首页</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores'
import axios from 'axios'
import apiClient from '../utils/api.js'
import { createOrder, payOrder } from '../utils/api.js'
import Swal from 'sweetalert2'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

// 响应式数据
const currentStep = ref(1)
const selectedPayment = ref('alipay')
const orderInfo = ref({
  id: '',
  title: '',
  price: 0,
  discount: 0,
  productType: 'content'
})
const paymentResult = ref({
  status: 'pending',
  title: '',
  message: '',
  payTime: ''
})

// 支付方式选项
const paymentMethods = ref([
  {
    id: 'alipay',
    name: '支付宝',
    icon: '💙',
    description: '安全快捷，支持花呗分期'
  },
  {
    id: 'wechat',
    name: '微信支付',
    icon: '💚',
    description: '微信扫码支付，方便快捷'
  },
  {
    id: 'bank',
    name: '银行卡',
    icon: '💳',
    description: '储蓄卡/信用卡直接支付'
  }
])

// 计算属性
const selectedPaymentName = computed(() => {
  const method = paymentMethods.value.find(m => m.id === selectedPayment.value)
  return method ? method.name : ''
})

// 方法
const getProductTypeText = () => {
  const typeMap = {
    'content': '内容付费',
    'course': '在线课程',
    'service': '专业服务'
  }
  return typeMap[orderInfo.value.productType] || '内容付费'
}

const proceedToPayment = () => {
  currentStep.value = 2
}

const backToOrder = () => {
  currentStep.value = 1
}

const selectPayment = (methodId) => {
  selectedPayment.value = methodId
}

const confirmPayment = async () => {
  try {
    // 创建订单
    const orderData = {
      product_id: route.query.id || '1',
      product_type: orderInfo.value.productType,
      payment_method: selectedPayment.value,
      amount: orderInfo.value.price - orderInfo.value.discount
    }

    const order = await createOrder(orderData)
    orderInfo.value.id = order.id

    // 模拟支付过程
    await simulatePayment()
  } catch (error) {
    console.error('支付失败:', error)
    Swal.fire({
      icon: 'error',
      title: '支付失败',
      text: error.message || '支付过程中出现错误，请稍后重试',
      confirmButtonText: '确定'
    })
  }
}

const simulatePayment = async () => {
  currentStep.value = 3
  
  // 模拟支付延迟
  setTimeout(() => {
    const isSuccess = Math.random() > 0.1 // 90% 成功率
    
    if (isSuccess) {
      paymentResult.value = {
        status: 'success',
        title: '支付成功！',
        message: '恭喜您，支付已完成。您现在可以享受会员特权了。',
        payTime: new Date().toLocaleString('zh-CN')
      }
      
      Swal.fire({
        icon: 'success',
        title: '支付成功',
        text: '恭喜您，支付已完成！',
        confirmButtonText: '确定'
      })
    } else {
      paymentResult.value = {
        status: 'failed',
        title: '支付失败',
        message: '支付过程中出现错误，请稍后重试。',
        payTime: ''
      }
      
      Swal.fire({
        icon: 'error',
        title: '支付失败',
        text: '支付过程中出现错误，请稍后重试',
        confirmButtonText: '确定'
      })
    }
  }, 2000)
}

const retryPayment = () => {
  currentStep.value = 2
}

const cancelOrder = () => {
  Swal.fire({
    title: '确认取消订单？',
    text: '取消后将无法享受相关服务',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: '确认取消',
    cancelButtonText: '继续支付'
  }).then((result) => {
    if (result.isConfirmed) {
      goToHome()
    }
  })
}

const goToHome = () => {
  router.push('/')
}

// 生命周期
onMounted(() => {
  // 从路由参数获取订单信息
  const productId = route.query.id || '1'
  const productType = route.query.type || 'content'
  
  // 模拟订单数据
  orderInfo.value = {
    id: productId,
    title: '母婴护理专业知识',
    price: 99.00,
    discount: 0,
    productType: productType
  }
})
</script>

<style scoped>
.payment-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px 0;
}

.payment-header {
  max-width: 1200px;
  margin: 0 auto 40px;
  padding: 0 20px;
  text-align: center;
}

.page-title {
  color: white;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 30px;
  text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.payment-steps {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  background: rgba(255,255,255,0.1);
  backdrop-filter: blur(10px);
  padding: 20px 40px;
  border-radius: 50px;
  border: 1px solid rgba(255,255,255,0.2);
}

.step {
  display: flex;
  align-items: center;
  gap: 10px;
  color: rgba(255,255,255,0.6);
  transition: all 0.3s ease;
}

.step.active {
  color: white;
  font-weight: 600;
}

.step.completed {
  color: #4ade80;
}

.step-number {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: rgba(255,255,255,0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  transition: all 0.3s ease;
}

.step.active .step-number {
  background: #4ade80;
  color: white;
}

.step.completed .step-number {
  background: #4ade80;
  color: white;
}

.step-arrow {
  color: rgba(255,255,255,0.6);
  font-size: 1.2rem;
}

.payment-step {
  max-width: 600px;
  margin: 0 auto;
  padding: 0 20px;
}

.payment-card {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.card-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 30px;
  text-align: center;
}

.order-info {
  margin-bottom: 30px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #f3f4f6;
}

.info-item:last-child {
  border-bottom: none;
}

.label {
  color: #6b7280;
  font-weight: 500;
}

.value {
  color: #1f2937;
  font-weight: 600;
}

.value.price {
  color: #ef4444;
  font-size: 1.1rem;
}

.value.discount {
  color: #10b981;
}

.order-total {
  border-top: 2px solid #e5e7eb;
  margin-top: 10px;
  padding-top: 20px;
  font-size: 1.2rem;
}

.total-price {
  color: #ef4444;
  font-size: 1.5rem;
  font-weight: 700;
}

.order-summary {
  background: #f9fafb;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 30px;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.payment-methods {
  margin-bottom: 30px;
}

.payment-method {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  margin-bottom: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.payment-method:hover {
  border-color: #3b82f6;
  background: #f8fafc;
}

.payment-method.active {
  border-color: #3b82f6;
  background: #eff6ff;
}

.method-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.method-icon {
  font-size: 2rem;
}

.method-name {
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 5px;
}

.method-desc {
  color: #6b7280;
  font-size: 0.9rem;
}

.radio-input {
  width: 20px;
  height: 20px;
  accent-color: #3b82f6;
}

.result-card {
  text-align: center;
}

.result-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.result-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 15px;
}

.result-message {
  color: #6b7280;
  font-size: 1.1rem;
  margin-bottom: 30px;
}

.result-details {
  background: #f9fafb;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 30px;
  text-align: left;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #e5e7eb;
}

.detail-item:last-child {
  border-bottom: none;
}

.payment-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
}

.btn {
  padding: 12px 30px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 120px;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #2563eb, #1e40af);
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(59, 130, 246, 0.3);
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}

.btn-secondary:hover {
  background: #e5e7eb;
  transform: translateY(-1px);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .payment-steps {
    flex-direction: column;
    gap: 15px;
    padding: 15px 20px;
  }
  
  .step-arrow {
    transform: rotate(90deg);
  }
  
  .payment-card {
    padding: 20px;
    margin: 0 10px;
  }
  
  .payment-actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
  }
  
  .info-item {
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