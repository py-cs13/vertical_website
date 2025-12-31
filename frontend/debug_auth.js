// 调试认证状态的脚本
console.log('=== 认证状态调试 ===');

// 检查localStorage
const user = localStorage.getItem('user');
const token = localStorage.getItem('token');

console.log('1. localStorage状态:');
console.log('   user:', user ? '存在' : '不存在');
console.log('   token:', token ? '存在' : '不存在');

if (user) {
  try {
    const userObj = JSON.parse(user);
    console.log('   用户ID:', userObj.id);
    console.log('   用户名:', userObj.nickname);
  } catch (e) {
    console.error('   user不是有效的JSON:', e);
  }
}

if (token) {
  console.log('   token长度:', token.length);
  console.log('   token前30位:', token.substring(0, 30) + '...');
}

// 检查当前URL
console.log('\n2. 当前URL:');
console.log('   ', window.location.href);

// 检查apiClient配置
console.log('\n3. apiClient配置:');
if (typeof apiClient !== 'undefined') {
  console.log('   baseURL:', apiClient.defaults.baseURL);
  console.log('   timeout:', apiClient.defaults.timeout);
  console.log('   headers:', apiClient.defaults.headers);
}

// 测试API调用
async function testApi() {
  console.log('\n4. 测试API调用:');
  
  try {
    const response = await fetch('/api/users/me', {
      method: 'GET',
      headers: {
        'Authorization': token ? `Bearer ${token}` : '',
        'Content-Type': 'application/json'
      }
    });
    
    console.log('   状态:', response.status);
    console.log('   状态文本:', response.statusText);
    
    if (response.status === 200) {
      const data = await response.json();
      console.log('   响应数据:', data);
      console.log('   ✅ 认证成功');
    } else {
      const error = await response.text();
      console.log('   错误:', error);
      console.log('   ❌ 认证失败');
    }
  } catch (error) {
    console.error('   请求异常:', error);
  }
}

// 执行测试
testApi();