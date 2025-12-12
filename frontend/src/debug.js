// 详细调试脚本：捕获所有与用户认证相关的操作

// 保存原始的XMLHttpRequest和fetch方法
const originalXHRSend = XMLHttpRequest.prototype.send;
const originalFetch = window.fetch;

// 重写XMLHttpRequest.send方法
XMLHttpRequest.prototype.send = function(body) {
  const xhr = this;
  const url = this.url || this._url;
  const method = this.method || this._method;
  
  console.log('=== XMLHttpRequest请求 ===');
  console.log('URL:', url);
  console.log('Method:', method);
  console.log('Request Body:', body);
  
  // 捕获响应
  const originalOnload = this.onload;
  this.onload = function() {
    console.log('=== XMLHttpRequest响应 ===');
    console.log('Status:', this.status);
    console.log('Response:', this.responseText);
    
    // 检查是否是用户信息更新请求
    if (url && url.includes('/api/users/me') && method === 'PUT') {
      console.log('=== 用户信息更新响应分析 ===');
      try {
        const response = JSON.parse(this.responseText);
        console.log('响应数据:', response);
        console.log('用户ID:', response.id);
        console.log('用户状态:', response.is_active);
        console.log('响应包含的字段:', Object.keys(response));
      } catch (e) {
        console.error('解析响应失败:', e);
      }
    }
    
    // 检查是否是401错误
    if (this.status === 401) {
      console.error('⚠️ 收到401未授权错误！');
      console.error('请求URL:', url);
      console.error('请求方法:', method);
    }
    
    // 调用原始的onload方法
    if (originalOnload) {
      originalOnload.apply(this, arguments);
    }
  };
  
  // 调用原始的send方法
  originalXHRSend.apply(this, arguments);
};

// 重写fetch方法
window.fetch = async function(resource, init = {}) {
  console.log('=== Fetch请求 ===');
  console.log('URL:', resource);
  console.log('Method:', init.method || 'GET');
  console.log('Request Headers:', init.headers);
  console.log('Request Body:', init.body);
  
  try {
    // 发送请求
    const response = await originalFetch.apply(this, arguments);
    
    console.log('=== Fetch响应 ===');
    console.log('Status:', response.status);
    console.log('Response Headers:', response.headers);
    
    // 检查是否是JSON响应
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      // 克隆响应以便读取内容
      const clonedResponse = response.clone();
      const responseData = await clonedResponse.json();
      console.log('Response Body:', responseData);
      
      // 检查是否是用户信息更新请求
      if (typeof resource === 'string' && resource.includes('/api/users/me') && init.method === 'PUT') {
        console.log('=== 用户信息更新响应分析 ===');
        console.log('用户ID:', responseData.id);
        console.log('用户状态:', responseData.is_active);
        console.log('响应包含的字段:', Object.keys(responseData));
      }
    }
    
    // 检查是否是401错误
    if (response.status === 401) {
      console.error('⚠️ 收到401未授权错误！');
      console.error('请求URL:', resource);
      console.error('请求方法:', init.method || 'GET');
    }
    
    return response;
  } catch (error) {
    console.error('=== Fetch请求失败 ===');
    console.error('Error:', error);
    throw error;
  }
};

// 监听localStorage的变化
const originalSetItem = localStorage.setItem;
localStorage.setItem = function(key, value) {
  console.log('=== localStorage.setItem ===');
  console.log('Key:', key);
  console.log('Value:', value);
  originalSetItem.apply(this, arguments);
};

const originalRemoveItem = localStorage.removeItem;
localStorage.removeItem = function(key) {
  console.log('=== localStorage.removeItem ===');
  console.log('Key:', key);
  originalRemoveItem.apply(this, arguments);
};

const originalClear = localStorage.clear;
localStorage.clear = function() {
  console.log('=== localStorage.clear ===');
  originalClear.apply(this, arguments);
};

// 监听Vuex/Pinia的状态变化
if (window.Pinia) {
  console.log('=== Pinia状态管理可用 ===');
  // 这里可以添加更多的Pinia状态监听逻辑
}

// 监听路由变化
if (window.__VUE_ROUTER__) {
  console.log('=== Vue Router可用 ===');
  window.__VUE_ROUTER__.afterEach((to, from) => {
    console.log('=== 路由变化 ===');
    console.log('从:', from.path);
    console.log('到:', to.path);
  });
}

// 监听页面刷新和关闭
window.addEventListener('beforeunload', () => {
  console.log('=== 页面即将刷新或关闭 ===');
  console.log('当前localStorage内容:');
  console.log('token:', localStorage.getItem('token'));
  console.log('user:', localStorage.getItem('user'));
});

// 检查当前认证状态
setTimeout(() => {
  console.log('=== 当前认证状态检查 ===');
  console.log('token:', localStorage.getItem('token'));
  console.log('user:', localStorage.getItem('user'));
  console.log('是否有token:', !!localStorage.getItem('token'));
}, 1000);

console.log('=== 详细调试脚本已加载 ===');
