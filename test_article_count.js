const axios = require('axios');

async function testArticleCount() {
  try {
    console.log('正在调用文章API...');
    const response = await axios.get('http://localhost:8000/api/articles');
    
    console.log('API响应状态:', response.status);
    console.log('返回的文章数量:', response.data.length);
    console.log('文章列表:', response.data.map(a => ({id: a.id, title: a.title, category: a.category, is_published: a.is_published})));
    
  } catch (error) {
    console.error('调用API失败:', error.message);
    if (error.response) {
      console.error('错误状态:', error.response.status);
      console.error('错误数据:', error.response.data);
    }
  }
}

testArticleCount();