const axios = require('axios')

async function checkFirstSixArticles() {
  console.log('检查API返回的前6篇文章的数据完整性...')
  
  try {
    const response = await axios.get('http://localhost:8000/api/articles')
    const articles = response.data.data || response.data || []
    
    console.log(`\nAPI返回的文章总数: ${articles.length}`)
    
    // 检查前6篇文章
    const firstSix = articles.slice(0, 6)
    console.log(`\n前6篇文章详细信息:`)
    
    firstSix.forEach((article, index) => {
      console.log(`\n${index + 1}. 文章ID: ${article.id}`)
      console.log(`   标题: ${article.title}`)
      console.log(`   分类: ${article.category}`)
      console.log(`   摘要: ${article.summary}`)
      console.log(`   作者: ${article.author}`)
      console.log(`   创建时间: ${article.created_at}`)
      console.log(`   发布状态: ${article.is_published}`)
      
      // 检查必要字段是否存在
      const hasId = article.id !== undefined && article.id !== null
      const hasTitle = article.title !== undefined && article.title !== ''
      const hasCategory = article.category !== undefined && article.category !== ''
      const hasSummary = article.summary !== undefined && article.summary !== ''
      const hasCreatedAt = article.created_at !== undefined && article.created_at !== null
      
      console.log(`   必要字段完整性: ID=${hasId}, 标题=${hasTitle}, 分类=${hasCategory}, 摘要=${hasSummary}, 创建时间=${hasCreatedAt}`)
      
      // 检查是否有不合法字符
      const titleHasInvalidChars = /[\x00-\x1F\x7F]/.test(article.title)
      const summaryHasInvalidChars = /[\x00-\x1F\x7F]/.test(article.summary)
      
      if (titleHasInvalidChars) {
        console.log(`   警告: 标题包含不合法字符`)
      }
      if (summaryHasInvalidChars) {
        console.log(`   警告: 摘要包含不合法字符`)
      }
    })
    
    // 检查第6篇文章是否有特殊问题
    if (firstSix.length >= 6) {
      console.log(`\n=== 第6篇文章基本信息 ===`)
      const sixthArticle = firstSix[5]
      console.log('第6篇文章ID:', sixthArticle.id)
      console.log('第6篇文章标题:', sixthArticle.title)
      console.log('第6篇文章分类:', sixthArticle.category)
      console.log('第6篇文章摘要长度:', sixthArticle.summary ? sixthArticle.summary.length : '无')
      console.log('第6篇文章创建时间:', sixthArticle.created_at)
      console.log('第6篇文章发布状态:', sixthArticle.is_published)
      
      // 检查可能导致渲染问题的字段
      if (sixthArticle.title && sixthArticle.title.length > 100) {
        console.log('警告: 第6篇文章标题过长，可能导致渲染问题')
      }
      if (sixthArticle.summary && sixthArticle.summary.length > 500) {
        console.log('警告: 第6篇文章摘要过长，可能导致渲染问题')
      }
    } else {
      console.log(`\n警告: API返回的文章数量不足6篇，实际只有${firstSix.length}篇`)
    }
    
  } catch (error) {
    console.error('请求失败:', error)
  }
}

checkFirstSixArticles()