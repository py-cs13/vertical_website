const axios = require('axios')

async function testDisplayedArticles() {
  console.log('测试前端displayedArticles计算属性逻辑...')
  
  try {
    const response = await axios.get('http://localhost:8000/api/articles')
    const articles = response.data.data || response.data || []
    
    console.log(`\nAPI返回的文章总数: ${articles.length}`)
    
    // 模拟前端的displayedArticles计算属性逻辑
    const displayedCount = 6
    
    // 过滤掉标题或摘要中包含不合法字符的文章
    const validArticles = articles.filter(article => {
      // 检查标题和摘要是否包含不合法的Markdown字符
      const hasInvalidChars = /[#*]{3,}/.test(article.title + article.summary)
      return !hasInvalidChars
    })
    
    console.log(`\n有效文章数量: ${validArticles.length}`)
    
    let result = validArticles.slice(0, displayedCount)
    
    // 如果有效文章不足displayedCount，从剩余文章中补充
    if (result.length < displayedCount) {
      const remainingArticles = articles.filter(article => {
        const hasInvalidChars = /[#*]{3,}/.test(article.title + article.summary)
        return hasInvalidChars
      })
      
      const supplementCount = displayedCount - result.length
      const supplementArticles = remainingArticles.slice(0, supplementCount)
      
      // 对补充的文章进行字符清理
      const cleanedSupplementArticles = supplementArticles.map(article => {
        return {
          ...article,
          title: article.title.replace(/[#*]{3,}/g, ''),
          summary: article.summary.replace(/[#*]{3,}/g, '')
        }
      })
      
      result = [...result, ...cleanedSupplementArticles]
    }
    
    console.log(`\n经过处理后，应该显示的文章数量: ${result.length}`)
    console.log('\n显示的文章列表:')
    result.forEach((article, index) => {
      console.log(`${index + 1}. ${article.title} (ID: ${article.id}, 分类: ${article.category})`)
    })
    
    if (result.length >= displayedCount) {
      console.log(`\n✅ 测试通过: 成功显示了${displayedCount}篇文章`)
    } else {
      console.log(`\n❌ 测试失败: 只显示了${result.length}篇文章，目标是显示${displayedCount}篇`)
    }
    
  } catch (error) {
    console.error('请求失败:', error)
  }
}

testDisplayedArticles()