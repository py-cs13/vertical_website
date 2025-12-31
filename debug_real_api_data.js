// 模拟从API获取的真实数据结构
const mockApiResponse = [
  { id: 39, title: "如何选择适合宝宝的辅食", summary: "这是一篇关于宝宝辅食选择的文章摘要", category: "辅食营养", author: "管理员", created_at: "2024-11-08T12:00:00" },
  { id: 40, title: "新生儿护理的10个关键要点", summary: "这是一篇关于新生儿护理的文章摘要", category: "育儿知识", author: "管理员", created_at: "2024-11-08T12:00:00" },
  { id: 41, title: "孕期如何保持健康的饮食习惯", summary: "这是一篇关于孕期饮食的文章摘要", category: "孕期保健", author: "管理员", created_at: "2024-11-08T12:00:00" },
  { id: 42, title: "### 产后恢复的重要性", summary: "这是一篇关于###产后恢复的文章摘要***", category: "产后恢复", author: "管理员", created_at: "2024-11-08T12:00:00" },
  { id: 43, title: "*** 如何培养宝宝的阅读习惯 ***", summary: "这是一篇关于***宝宝阅读习惯的文章摘要", category: "早期教育", author: "管理员", created_at: "2024-11-08T12:00:00" },
  { id: 44, title: "选择安全的母婴用品指南", summary: "这是一篇关于母婴用品选择的文章摘要", category: "母婴用品", author: "管理员", created_at: "2024-11-08T12:00:00" },
  { id: 45, title: "### 亲子活动推荐 ***", summary: "这是一篇关于###亲子活动的文章摘要***", category: "亲子活动", author: "管理员", created_at: "2024-11-08T12:00:00" },
  { id: 46, title: "### 母婴育儿知识大全 ***", summary: "这是一篇关于###母婴育儿的文章摘要***", category: "母婴育儿", author: "管理员", created_at: "2024-11-08T12:00:00" },
  { id: 47, title: "宝宝睡眠问题解决方案", summary: "这是一篇关于宝宝睡眠的文章摘要", category: "育儿知识", author: "管理员", created_at: "2024-11-08T12:00:00" },
  { id: 48, title: "*** 孕期运动注意事项 ***", summary: "这是一篇关于***孕期运动的文章摘要", category: "孕期保健", author: "管理员", created_at: "2024-11-08T12:00:00" }
];

// 模拟displayedArticles计算属性的逻辑
function testDisplayedArticles(articles, displayedCount) {
  console.log(`=== 测试显示 ${displayedCount} 篇文章 ===`);
  
  // 过滤掉标题或摘要中包含不合法字符的文章
  const validArticles = articles.filter(article => {
    const hasInvalidChars = /[#*]{3,}/.test(article.title + article.summary);
    console.log(`文章 ${article.id}: ${article.title} - 有效: ${!hasInvalidChars}`);
    return !hasInvalidChars;
  });
  
  console.log(`有效文章数量: ${validArticles.length}`);
  const result = validArticles.slice(0, displayedCount);
  console.log(`初步过滤后显示: ${result.length} 篇`);
  
  // 如果有效文章不足displayedCount，从剩余文章中补充
  if (result.length < displayedCount) {
    const remainingArticles = articles.filter(article => {
      const hasInvalidChars = /[#*]{3,}/.test(article.title + article.summary);
      return hasInvalidChars;
    });
    
    console.log(`剩余文章数量: ${remainingArticles.length}`);
    const supplementCount = displayedCount - result.length;
    const supplementArticles = remainingArticles.slice(0, supplementCount);
    
    // 对补充的文章进行字符清理
    const cleanedSupplementArticles = supplementArticles.map(article => {
      const cleanedArticle = {
        ...article,
        title: article.title.replace(/[#*]{3,}/g, ''),
        summary: article.summary.replace(/[#*]{3,}/g, '')
      };
      console.log(`补充文章 ${article.id}: 清理前标题: "${article.title}", 清理后标题: "${cleanedArticle.title}"`);
      return cleanedArticle;
    });
    
    const finalResult = [...result, ...cleanedSupplementArticles];
    console.log(`最终显示: ${finalResult.length} 篇文章`);
    return finalResult;
  }
  
  console.log(`最终显示: ${result.length} 篇文章`);
  return result;
}

// 测试初始显示6篇文章
const initialDisplay = testDisplayedArticles(mockApiResponse, 6);
console.log('\n初始显示的文章ID:', initialDisplay.map(a => a.id));

// 测试加载更多（6+4=10篇）
console.log('\n');
const loadMoreDisplay = testDisplayedArticles(mockApiResponse, 10);
console.log('\n加载更多后显示的文章ID:', loadMoreDisplay.map(a => a.id));
