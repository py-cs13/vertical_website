// 测试下载功能修复脚本
const axios = require('axios');

// 测试API调用
async function testDownloadApi() {
  try {
    // 模拟用户登录后获取的token
    const token = localStorage.getItem('token');
    
    if (!token) {
      console.log('⚠️  未找到登录token，请先登录后再测试');
      return;
    }
    
    // 创建axios实例
    const apiClient = axios.create({
      baseURL: 'http://localhost:5174/api',
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      }
    });
    
    // 添加认证token
    apiClient.interceptors.request.use(
      config => {
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      error => {
        return Promise.reject(error);
      }
    );
    
    // 测试下载API
    const productId = '107'; // 使用示例智能体ID
    console.log(`\n🔧 测试下载智能体API，产品ID: ${productId}`);
    console.log('📝 请求路径:', `/api/agents/${productId}/download`);
    console.log('🔑 已添加认证token:', !!token);
    
    // 发送请求
    const response = await apiClient.get(`/agents/${productId}/download`, {
      responseType: 'blob'
    });
    
    console.log('✅ 下载API调用成功');
    console.log('📋 响应状态码:', response.status);
    console.log('📁 响应数据类型:', response.data.type);
    console.log('📎 Content-Disposition:', response.headers['content-disposition']);
    
    // 检查响应数据
    if (response.data) {
      console.log('✅ 成功获取下载文件数据');
      console.log('📊 文件大小:', (response.data.size / 1024).toFixed(2), 'KB');
    }
    
    // 测试API路径是否正确
    try {
      console.log('\n🔧 测试另一个API端点以验证认证状态');
      const userResponse = await apiClient.get('/users/me');
      console.log('✅ 用户信息API调用成功，认证状态正常');
      console.log('👤 用户名:', userResponse.data.nickname);
    } catch (userError) {
      console.log('⚠️ 用户信息API调用失败:', userError.response?.status || '未知错误');
    }
    
  } catch (error) {
    console.log('❌ 下载API调用失败:', error.response?.status || '未知错误');
    if (error.response) {
      console.log('📝 错误详情:', error.response.data);
      console.log('📋 错误响应头:', error.response.headers);
    }
    console.log('💡 可能的问题:', error.message);
  }
}

// 运行测试
console.log('🚀 开始测试下载功能修复');
console.log('📅 测试时间:', new Date().toLocaleString());
console.log('🌐 测试环境:', window.location.href);

// 检查localStorage状态
console.log('\n📦 localStorage状态:');
console.log('👤 用户信息:', !!localStorage.getItem('user'));
console.log('🔑 Token存在:', !!localStorage.getItem('token'));

// 运行API测试
testDownloadApi().then(() => {
  console.log('\n✅ 测试完成');
});