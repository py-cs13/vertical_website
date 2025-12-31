const axios = require('axios');

async function testAPI() {
  try {
    console.log('正在调用API获取文章数据...');
    const response = await axios.get('http://localhost:8000/api/articles');
    console.log('API响应状态:', response.status);
    console.log('API响应数据结构:', JSON.stringify(Object.keys(response.data), null, 2));
    
    // 检查响应数据
    const articles = response.data.data || response.data || [];
    console.log('文章总数:', articles.length);
    
    if (articles.length > 0) {
      console.log('前3篇文章标题:');
      articles.slice(0, 3).forEach((article, index) => {
        console.log(`${index + 1}. ${article.title}`);
      });
    }
    
  } catch (error) {
    console.error('API调用错误:', error.message);
    if (error.response) {
      console.error('错误状态:', error.response.status);
      console.error('错误数据:', error.response.data);
    }
  }
}

testAPI();