#!/usr/bin/env node
// 简化版工具包下载测试脚本

const axios = require('axios');

async function testSimpleDownload() {
  console.log('🚀 开始简化版工具包下载测试...');
  
  try {
    const BASE_URL = 'http://localhost:8000';
    
    // 直接测试下载API（不涉及用户认证和购买）
    // 注意：这可能会返回403或404错误，因为需要认证和购买
    const toolkitId = '1'; // 假设工具包ID为1
    
    console.log(`📥 尝试下载工具包ID: ${toolkitId}`);
    console.log(`🔗 请求URL: ${BASE_URL}/api/toolkits/${toolkitId}/download`);
    
    const response = await axios.get(`${BASE_URL}/api/toolkits/${toolkitId}/download`, {
      responseType: 'blob',
      validateStatus: false // 不抛出状态码错误，以便查看响应
    });
    
    console.log('📊 响应状态码:', response.status);
    console.log('📁 响应数据类型:', response.data.type);
    console.log('📏 响应数据大小:', response.data.size, 'bytes');
    
    if (response.status === 200) {
      console.log('✅ 下载成功！');
    } else if (response.status === 403) {
      console.log('⚠️  下载失败：需要用户认证和购买权限');
      console.log('💡 这是正常的，因为没有提供认证信息和购买凭证');
    } else if (response.status === 404) {
      console.log('❌ 下载失败：工具包不存在或路径错误');
    } else {
      console.log('⚠️  下载失败：未知错误');
    }
    
    console.log('🎉 测试完成！');
    
  } catch (error) {
    console.error('❌ 测试失败:', error.message);
    if (error.code === 'ECONNREFUSED') {
      console.error('💡 提示：请确保后端服务器正在运行（http://localhost:8000）');
    }
  }
}

testSimpleDownload();