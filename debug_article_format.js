const axios = require('axios');

async function debugArticleFormat() {
  try {
    const response = await axios.get('http://localhost:8000/api/articles');
    const articles = response.data;
    
    console.log('文章总数:', articles.length);
    
    // 检查每篇文章的必要字段
    console.log('\n=== 检查文章必要字段 ===');
    articles.forEach((article, index) => {
      const hasId = article.id !== undefined;
      const hasTitle = article.title !== undefined && article.title.trim() !== '';
      const hasCategory = article.category !== undefined;
      const hasSummary = article.summary !== undefined && article.summary.trim() !== '';
      const hasCreatedAt = article.created_at !== undefined;
      const hasAuthor = article.author !== undefined;
      
      console.log(`${index + 1}. 文章 ${article.id || '无ID'}:`);
      console.log(`   标题: ${hasTitle ? '✓' : '✗'} (${article.title ? article.title.length : 0}字符)`);
      console.log(`   分类: ${hasCategory ? '✓' : '✗'} (${article.category})`);
      console.log(`   摘要: ${hasSummary ? '✓' : '✗'} (${article.summary ? article.summary.length : 0}字符)`);
      console.log(`   创建时间: ${hasCreatedAt ? '✓' : '✗'}`);
      console.log(`   作者: ${hasAuthor ? '✓' : '✗'}`);
      
      // 检查是否有特殊字符或格式问题
      if (article.title && (article.title.includes('**') || article.title.includes('###'))) {
        console.log(`   ⚠️  标题包含特殊字符: ${article.title}`);
      }
      if (article.summary && article.summary.length > 200) {
        console.log(`   ⚠️  摘要过长: ${article.summary.length}字符`);
      }
    });
    
    // 检查前6篇文章（应该显示的）
    console.log('\n=== 前6篇文章详细信息 ===');
    const first6 = articles.slice(0, 6);
    first6.forEach((article, index) => {
      console.log(`\n${index + 1}. ${article.title}`);
      console.log(`   ID: ${article.id}`);
      console.log(`   分类: ${article.category}`);
      console.log(`   摘要: ${article.summary.substring(0, 50)}...`);
      console.log(`   创建时间: ${article.created_at}`);
      console.log(`   作者: ${article.author}`);
    });
    
  } catch (error) {
    console.error('调试出错:', error.message);
  }
}

debugArticleFormat();