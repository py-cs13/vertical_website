// 简单的登录测试脚本
const axios = require('axios');

// 测试登录API
async function testLogin() {
    try {
        // 首先确保使用正确的API路径（带/api前缀）
        const loginResponse = await axios.post('http://localhost:8000/api/auth/login', {
            email: 'test@example.com',
            password: 'test123'
        });
        
        console.log('登录成功:', loginResponse.data);
        
        // 使用返回的token获取用户信息
        const token = loginResponse.data.access_token;
        
        const userResponse = await axios.get('http://localhost:8000/api/users/me', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        console.log('获取用户信息成功:', userResponse.data);
        
        // 测试/auth/me路径
        const authMeResponse = await axios.get('http://localhost:8000/api/auth/me', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        console.log('获取用户信息(/auth/me)成功:', authMeResponse.data);
        
        console.log('所有测试通过！登录功能正常工作。');
        return true;
    } catch (error) {
        console.error('测试失败:', error.response?.data || error.message);
        return false;
    }
}

// 运行测试
testLogin();