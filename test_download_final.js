// 测试下载功能的简单脚本
// 这个脚本将模拟完整的用户注册、登录、购买和下载流程

import axios from 'axios';
import fs from 'fs';

// 生成随机字符串用于创建测试用户
const randomString = () => Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);

// 配置API客户端
const BASE_URL = 'http://localhost:8000'; // 后端API端口
const apiClient = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

async function testDownloadFlow() {
  try {
    console.log('=== 开始测试下载功能 ===');
    
    // 1. 生成随机测试用户
    const username = `test_${randomString()}`;
    const email = `${username}@example.com`;
    const password = 'Password123!';
    
    console.log(`\n1. 生成测试用户: ${email}`);
    
    // 2. 注册用户
    console.log('2. 注册用户...');
    const registerResponse = await apiClient.post('/api/register', {
      username,
      email,
      password
    });
    console.log('   ✅ 用户注册成功');
    
    // 3. 用户登录
    console.log('3. 用户登录...');
    const loginResponse = await apiClient.post('/api/login', {
      email,
      password
    });
    const token = loginResponse.data.token;
    console.log('   ✅ 用户登录成功，获取token:', token.substring(0, 20) + '...');
    
    // 4. 添加认证token到请求头
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    
    // 5. 获取工具包列表
    console.log('4. 获取工具包列表...');
    const toolkitsResponse = await apiClient.get('/api/toolkits');
    const toolkits = toolkitsResponse.data;
    console.log(`   ✅ 成功获取 ${toolkits.length} 个工具包`);
    
    if (toolkits.length === 0) {
      console.log('   ❌ 没有可用的工具包，测试结束');
      return;
    }
    
    // 选择第一个工具包进行测试
    const targetToolkit = toolkits[0];
    console.log(`   选择测试工具包: ${targetToolkit.name} (ID: ${targetToolkit.id})`);
    
    // 6. 购买工具包
    console.log('5. 购买工具包...');
    const orderResponse = await apiClient.post('/api/orders', {
      product_type: 'toolkit',
      product_id: targetToolkit.id,
      total_amount: targetToolkit.price,
      items: [{
        product_type: 'toolkit',
        product_id: targetToolkit.id,
        quantity: 1,
        price: targetToolkit.price
      }]
    });
    const orderId = orderResponse.data.id;
    console.log(`   ✅ 成功创建订单，订单ID: ${orderId}`);
    
    // 7. 支付订单
    console.log('6. 支付订单...');
    const payResponse = await apiClient.post(`/api/orders/${orderId}/pay`, {
      payment_method: 'test'
    });
    console.log('   ✅ 订单支付成功');
    
    // 8. 测试下载功能
    console.log('7. 测试下载工具包...');
    const downloadResponse = await apiClient.get(`/api/toolkits/${targetToolkit.id}/download`, {
      responseType: 'arraybuffer' // 使用arraybuffer类型获取二进制数据
    });
    
    // 验证响应状态
    console.log(`   ✅ 下载请求成功，状态码: ${downloadResponse.status}`);
    console.log(`   响应头 Content-Type: ${downloadResponse.headers['content-type']}`);
    
    // 获取文件名
    const contentDisposition = downloadResponse.headers['content-disposition'];
    let fileName = `${targetToolkit.name}.pdf`;
    if (contentDisposition) {
      const matches = contentDisposition.match(/filename\*=UTF-8''([^;]+)/);
      if (matches && matches[1]) {
        fileName = decodeURIComponent(matches[1]);
      }
    }
    
    // 保存文件
    console.log(`   保存文件: ${fileName}`);
    fs.writeFileSync(fileName, Buffer.from(downloadResponse.data));
    console.log('   ✅ 文件保存成功');
    
    console.log('\n=== 测试完成 ===');
    console.log('🎉 下载功能测试成功！');
    
  } catch (error) {
    console.error('\n❌ 测试失败:', error.message);
    if (error.response) {
      console.error('   状态码:', error.response.status);
      console.error('   响应数据:', error.response.data);
    }
  }
}

// 执行测试
testDownloadFlow();