// 测试修复后的工具包下载功能
const axios = require('axios');
const fs = require('fs');

async function testToolkitDownload() {
  try {
    const BASE_URL = 'http://localhost:8000';
    
    // 1. 注册新用户
    const testUser = {
      username: 'testuser_' + Math.random().toString(36).substring(2, 8),
      email: 'test_' + Math.random().toString(36).substring(2, 8) + '@example.com',
      password: 'Password123!'
    };
    
    const registerResponse = await axios.post(`${BASE_URL}/api/auth/register`, testUser);
    console.log('注册成功！');
    
    // 2. 用户登录
    const loginResponse = await axios.post(`${BASE_URL}/api/auth/login`, {
      email: testUser.email,
      password: testUser.password
    });
    
    const token = loginResponse.data.access_token;
    console.log('登录成功，获取到token:', token);
    
    // 3. 获取工具包列表
    const toolkitsResponse = await axios.get(`${BASE_URL}/api/toolkits`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    console.log('工具包列表获取成功，数量:', toolkitsResponse.data.length);
    
    if (toolkitsResponse.data.length === 0) {
      console.error('没有可用的工具包');
      return;
    }
    
    // 4. 选择第一个工具包进行下载
    const toolkitId = toolkitsResponse.data[0].id;
    const toolkitTitle = toolkitsResponse.data[0].title;
    console.log('准备下载工具包ID:', toolkitId);
    console.log('工具包标题:', toolkitTitle);
    
    // 5. 购买工具包
    console.log('正在购买工具包...');
    const orderResponse = await axios.post(`${BASE_URL}/api/orders`, {
      product_type: 'toolkit',
      product_id: toolkitId,
      amount: 0.01, // 测试用的小额支付
      items: [{
        product_name: toolkitTitle,
        product_price: 0.01,
        quantity: 1,
        total_amount: 0.01
      }]
    }, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    console.log('购买成功！订单ID:', orderResponse.data.id);
    const orderId = orderResponse.data.id;
    
    // 6. 完成支付（测试模式下自动完成）
    console.log('正在完成支付...');
    const paymentResponse = await axios.post(`${BASE_URL}/api/orders/${orderId}/pay`, {
      order_id: orderId,
      payment_method: 'alipay',
      return_url: 'http://localhost:5173/payment-success'
    }, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    console.log('支付成功:', paymentResponse.data);
    console.log('支付URL:', paymentResponse.data.payment_url);
    
    // 7. 下载工具包
    console.log('正在下载工具包...');
    const downloadResponse = await axios.get(`${BASE_URL}/api/toolkits/${toolkitId}/download`, {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      responseType: 'blob'
    });
    
    console.log('工具包下载成功，响应状态:', downloadResponse.status);
    console.log('文件大小:', downloadResponse.data.length, 'bytes');
    
    // 6. 保存文件
    const fileName = `test_toolkit_${toolkitId}.pdf`;
    fs.writeFileSync(fileName, Buffer.from(await downloadResponse.data.arrayBuffer()));
    console.log('文件保存成功:', fileName);
    
    console.log('\n✅ 工具包下载测试成功完成！');
    
  } catch (error) {
    console.error('测试失败:', error.message);
    if (error.response) {
      console.error('响应状态:', error.response.status);
      console.error('响应数据:', error.response.data);
    }
  }
}

testToolkitDownload();