// 测试文章页面显示逻辑
const simulateArticlesViewDisplay = () => {
  // 模拟场景1：数据库中有10篇文章
  console.log('=== 场景1：数据库中有10篇文章 ===')
  const mockArticles1 = Array.from({ length: 10 }, (_, i) => ({
    id: i + 1,
    title: `文章标题${i + 1}`,
    summary: `文章摘要${i + 1}`,
    category: '育儿知识',
    created_at: '2024-06-03'
  }))
  
  // 模拟场景2：数据库中有4篇文章
  console.log('\n=== 场景2：数据库中有4篇文章 ===')
  const mockArticles2 = Array.from({ length: 4 }, (_, i) => ({
    id: i + 1,
    title: `文章标题${i + 1}`,
    summary: `文章摘要${i + 1}`,
    category: '育儿知识',
    created_at: '2024-06-03'
  }))
  
  // 模拟场景3：数据库中有8篇文章，其中3篇包含不合法字符
  console.log('\n=== 场景3：数据库中有8篇文章，其中3篇包含不合法字符 ===')
  const mockArticles3 = Array.from({ length: 8 }, (_, i) => {
    const baseTitle = `文章标题${i + 1}`
    const baseSummary = `文章摘要${i + 1}`
    
    // 第3、5、7篇文章包含不合法字符
    if ([2, 4, 6].includes(i)) {
      return {
        id: i + 1,
        title: `${baseTitle}###`,
        summary: `${baseSummary}***`,
        category: '育儿知识',
        created_at: '2024-06-03'
      }
    }
    
    return {
      id: i + 1,
      title: baseTitle,
      summary: baseSummary,
      category: '育儿知识',
      created_at: '2024-06-03'
    }
  })
  
  // 模拟文章页面的显示逻辑
  const testDisplayLogic = (articles, scenarioName) => {
    const displayedCount = 6 // 默认显示6篇文章
    
    // 过滤掉标题或摘要中包含不合法字符的文章
    const validArticles = articles.filter(article => {
      const hasInvalidChars = /[#*]{3,}/.test(article.title + article.summary)
      return !hasInvalidChars
    })
    
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
    
    console.log(`${scenarioName}:`)
    console.log(`- 数据库中文章总数: ${articles.length}`)
    console.log(`- 有效文章数（无特殊字符）: ${validArticles.length}`)
    console.log(`- 实际显示文章数: ${result.length}`)
    console.log(`- 显示的文章ID:`, result.map(a => a.id))
    console.log(`- 显示标题是否包含特殊字符: ${result.some(a => /[#*]{3,}/.test(a.title))}`)
    console.log(`- 是否符合要求: ${result.length <= 6 && result.length === Math.min(articles.length, 6) ? '✅ 是' : '❌ 否'}`)
  }
  
  // 运行测试
  testDisplayLogic(mockArticles1, '10篇文章')
  testDisplayLogic(mockArticles2, '4篇文章')
  testDisplayLogic(mockArticles3, '8篇文章（含特殊字符）')
}

simulateArticlesViewDisplay()
