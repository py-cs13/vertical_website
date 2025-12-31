// 测试下载功能修复的脚本
import axios from 'axios';

// 创建axios实例
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 从localStorage获取token
const token = localStorage.getItem('token');
if (token) {
  apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

// 测试下载功能
async function testDownload() {
  try {
    console.log('开始测试下载功能...');
    
    // 1. 测试获取token
    console.log('当前token:', token ? token.substring(0, 20) + '...' : '无');
    
    // 2. 测试API调用
    const productId = '1'; // 替换为实际的产品ID
    console.log(`测试下载产品ID: ${productId}`);
    
    const response = await apiClient.get(`/toolkits/${productId}/download`, {
      responseType: 'blob'
    });
    
    console.log('下载请求成功!');
    console.log('响应状态:', response.status);
    console.log('响应头:', response.headers);
    console.log('内容类型:', response.headers['content-type']);
    console.log('内容长度:', response.headers['content-length']);
    
    // 3. 测试文件处理
    const blob = response.data;
    console.log('Blob对象:', blob);
    console.log('Blob大小:', blob.size);
    
    console.log('✅ 下载功能测试成功!');
    
  } catch (error) {
    console.error('❌ 下载功能测试失败:', error.response ? error.response.status : error.message);
    if (error.response) {
      console.error('错误详情:', error.response.data);
      console.error('错误头:', error.response.headers);
    }
  }
}

// 运行测试
testDownload();