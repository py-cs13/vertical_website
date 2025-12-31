// 测试前端文章显示逻辑
const axios = require('axios');

// 模拟前端的分类数据
const categories = [
  { id: 1, name: '母婴育儿' },
  { id: 2, name: '育儿知识' },
  { id: 3, name: '营养辅食' },
  { id: 4, name: '产后恢复' },
  { id: 5, name: '亲子互动' },
  { id: 6, name: '成长发育' },
  { id: 7, name: '早期教育' },
  { id: 8, name: '健康养生' }
];

// 模拟前端组件逻辑
class MockArticlesView {
  constructor() {
    this.articles = [];
    this.activeCategory = 'all';
    this.currentPage = 1;
    this.itemsPerPage = 6;
    this.loadStep = 4;
  }

  // 从API获取文章数据
  async fetchArticles() {
    try {
      console.log('\n===== 开始获取文章数据 =====');
      const response = await axios.get('http://localhost:8000/api/articles');
      console.log(`API响应状态: ${response.status}`);
      
      // 处理API响应数据
      if (Array.isArray(response.data)) {
        this.articles = response.data;
      } else if (Array.isArray(response.data.data)) {
        this.articles = response.data.data;
      } else {
        console.error('API返回数据格式异常:', response.data);
        this.articles = [];
      }
      
      console.log(`获取到的文章总数: ${this.articles.length}`);
      console.log('\n前3篇文章预览:');
      this.articles.slice(0, 3).forEach((article, index) => {
        console.log(`${index + 1}. ID: ${article.id}, 标题: ${article.title}, 分类: ${article.category}`);
      });
      
      return true;
    } catch (error) {
      console.error('\n获取文章失败:', error.message);
      if (error.response) {
        console.error(`错误状态: ${error.response.status}`);
        console.error('错误数据:', error.response.data);
      }
      this.articles = [];
      return false;
    }
  }

  // 模拟过滤文章
  filterArticles(category) {
    this.activeCategory = category;
    console.log(`\n===== 切换到分类: ${category === 'all' ? '全部' : categories.find(c => c.id === category)?.name || category} =====`);
    
    let filtered = [];
    if (category === 'all') {
      filtered = this.articles;
    } else {
      const selectedCategory = categories.find(cat => cat.id === category);
      if (selectedCategory) {
        if (selectedCategory.name === '母婴育儿') {
          filtered = this.articles.filter(article => 
            article.category === '母婴育儿'
          );
        } else {
          filtered = this.articles.filter(article => 
            article.category === selectedCategory.name || 
            article.category === '母婴育儿'
          );
        }
      }
    }
    
    console.log(`过滤后文章数量: ${filtered.length}`);
    
    // 统计各分类文章数量
    this.countCategoryArticles(filtered);
    
    return filtered;
  }

  // 统计各分类文章数量
  countCategoryArticles(articles) {
    const categoryCounts = {};
    
    articles.forEach(article => {
      if (article.category) {
        categoryCounts[article.category] = (categoryCounts[article.category] || 0) + 1;
      }
    });
    
    console.log('\n各分类文章数量统计:');
    Object.entries(categoryCounts)
      .sort(([,a], [,b]) => b - a)
      .forEach(([category, count]) => {
        console.log(`${category}: ${count}篇`);
      });
  }

  // 测试分页显示逻辑
  testPagination(filteredArticles) {
    console.log('\n===== 测试分页显示逻辑 =====');
    
    const initialDisplay = filteredArticles.slice(0, this.currentPage * this.itemsPerPage);
    console.log(`初始显示文章数量: ${initialDisplay.length}篇`);
    
    // 测试加载更多
    this.currentPage += 1;
    const afterLoadMore = filteredArticles.slice(0, this.currentPage * this.itemsPerPage);
    console.log(`加载更多后显示: ${afterLoadMore.length}篇`);
    
    const hasMore = afterLoadMore.length < filteredArticles.length;
    console.log(`是否有更多文章: ${hasMore ? '是' : '否'}`);
  }

  // 检查文章数据完整性
  checkArticleIntegrity() {
    console.log('\n===== 检查文章数据完整性 =====');
    
    const invalidArticles = this.articles.filter(article => {
      return !article.id || !article.title || !article.category || !article.summary || !article.created_at;
    });
    
    console.log(`无效文章数量: ${invalidArticles.length}`);
    if (invalidArticles.length > 0) {
      console.log('无效文章详情:');
      invalidArticles.slice(0, 3).forEach(article => {
        console.log(`- ID: ${article.id}, 标题: ${article.title || '无'}`);
      });
    }
  }
}

// 运行测试
async function runTest() {
  console.log('\n========== 前端文章显示逻辑测试 ==========');
  
  const mockView = new MockArticlesView();
  
  // 获取文章数据
  const success = await mockView.fetchArticles();
  if (!success) {
    console.log('测试终止');
    return;
  }
  
  // 检查数据完整性
  mockView.checkArticleIntegrity();
  
  // 测试全部分类
  const allArticles = mockView.filterArticles('all');
  mockView.testPagination(allArticles);
  
  // 测试特定分类 - 母婴育儿
  const babyCareArticles = mockView.filterArticles(1);
  mockView.testPagination(babyCareArticles);
  
  // 测试特定分类 - 育儿知识
  const knowledgeArticles = mockView.filterArticles(2);
  mockView.testPagination(knowledgeArticles);
  
  console.log('\n========== 测试完成 ==========');
}

runTest().catch(error => {
  console.error('测试执行出错:', error);
});
