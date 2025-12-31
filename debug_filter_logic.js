// 测试文章过滤和补充逻辑
const testArticles = [
  { id: 1, title: "正常文章1", summary: "这是一篇正常的文章摘要" },
  { id: 2, title: "正常文章2", summary: "这是一篇正常的文章摘要" },
  { id: 3, title: "正常文章3", summary: "这是一篇正常的文章摘要" },
  { id: 4, title: "正常文章4", summary: "这是一篇正常的文章摘要" },
  { id: 5, title: "### 带Markdown的文章1", summary: "这是一篇带###的文章摘要" },
  { id: 6, title: "带***的文章2", summary: "这是一篇带***的文章摘要" },
  { id: 7, title: "正常文章5", summary: "这是一篇正常的文章摘要" },
  { id: 8, title: "正常文章6", summary: "这是一篇正常的文章摘要" },
  { id: 9, title: "### 带Markdown的文章3", summary: "这是一篇带###的文章摘要" },
  { id: 10, title: "带***的文章4", summary: "这是一篇带***的文章摘要" }
];

const displayedCount = 6;
const loadStep = 4;

// 模拟displayedArticles计算属性的逻辑
function getDisplayedArticles(articles, count) {
  // 过滤掉标题或摘要中包含不合法字符的文章
  const validArticles = articles.filter(article => {
    // 检查标题和摘要是否包含不合法的Markdown字符
    const hasInvalidChars = /[#*]{3,}/.test(article.title + article.summary);
    return !hasInvalidChars;
  });
  
  const result = validArticles.slice(0, count);
  console.log('有效文章:', validArticles);
  console.log('初步结果:', result);
  
  // 如果有效文章不足count，从剩余文章中补充
  if (result.length < count) {
    const remainingArticles = articles.filter(article => {
      const hasInvalidChars = /[#*]{3,}/.test(article.title + article.summary);
      return hasInvalidChars;
    });
    
    console.log('剩余文章:', remainingArticles);
    const supplementCount = count - result.length;
    const supplementArticles = remainingArticles.slice(0, supplementCount);
    
    // 对补充的文章进行字符清理
    const cleanedSupplementArticles = supplementArticles.map(article => {
      return {
        ...article,
        title: article.title.replace(/[#*]{3,}/g, ''),
        summary: article.summary.replace(/[#*]{3,}/g, '')
      };
    });
    
    console.log('补充文章:', cleanedSupplementArticles);
    return [...result, ...cleanedSupplementArticles];
  }
  
  return result;
}

console.log('=== 测试初始显示6篇文章 ===');
let displayed = getDisplayedArticles(testArticles, 6);
console.log('最终显示:', displayed);
console.log('显示数量:', displayed.length);

console.log('\n=== 测试加载更多（6+4=10篇）===');
displayed = getDisplayedArticles(testArticles, 10);
console.log('最终显示:', displayed);
console.log('显示数量:', displayed.length);
