// 调试脚本：检查文章数据获取
import axios from 'axios';

async function debugArticles() {
  try {
    console.log('开始调试文章数据获取...');
    
    // 模拟前端API调用
    const response = await axios.get('http://localhost:8000/api/articles');
    
    console.log('API响应状态:', response.status);
    console.log('API返回文章总数:', response.data.length);
    console.log('前10篇文章:', response.data.slice(0, 10).map(a => ({id: a.id, title: a.title})));
    
    // 检查是否有数据问题
    const invalidArticles = response.data.filter(a => !a.id || !a.title);
    console.log('无效文章数量:', invalidArticles.length);
    if (invalidArticles.length > 0) {
      console.log('无效文章:', invalidArticles);
    }
    
    // 模拟前端的显示逻辑
    const displayedCount = 6;
    const displayedArticles = response.data.slice(0, displayedCount);
    console.log('按照前端逻辑应显示的文章数量:', displayedArticles.length);
    console.log('应显示的文章:', displayedArticles.map(a => ({id: a.id, title: a.title})));
    
  } catch (error) {
    console.error('调试出错:', error.message);
  }
}

debugArticles();