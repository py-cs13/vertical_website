const axios = require('axios');

// 模拟新的显示逻辑
async function testNewDisplayLogic() {
  try {
    // 1. 获取所有文章
    const response = await axios.get('http://localhost:8000/api/articles');
    const articles = response.data;
    
    console.log('总文章数量:', articles.length);
    
    // 2. 测试初始显示6篇的情况
    const displayedCount = 6;
    
    // 1. 先获取所有文章（不考虑是否有特殊字符）
    const allArticles = articles.slice(0, displayedCount);
    
    // 2. 对每篇文章进行字符清理
    const cleanedArticles = allArticles.map(article => {
      // 清理标题和摘要中的所有#和*字符
      const cleanedTitle = article.title.replace(/[#*]/g, '').trim();
      const cleanedSummary = article.summary.replace(/[#*]/g, '').trim();
      
      if (cleanedTitle !== article.title || cleanedSummary !== article.summary) {
        console.log(`文章 ${article.id}: 清理前 - "${article.title}", 清理后 - "${cleanedTitle}"`);
      }
      
      return {
        ...article,
        title: cleanedTitle,
        summary: cleanedSummary
      };
    });
    
    console.log('\n清理后显示文章数量:', cleanedArticles.length);
    console.log('\n显示的文章列表:');
    cleanedArticles.forEach((article, index) => {
      console.log(`${index + 1}. ID: ${article.id} - ${article.title}`);
    });
    
    return cleanedArticles;
  } catch (error) {
    console.error('测试失败:', error.message);
  }
}

testNewDisplayLogic();