// 测试修复后的分类过滤逻辑
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

// 模拟修复后的前端组件逻辑
class MockArticlesView {
  constructor() {
    this.articles = [];
  }

  // 从API获取文章数据
  async fetchArticles() {
    try {
      const response = await axios.get('http://localhost:8000/api/articles');
      this.articles = Array.isArray(response.data) ? response.data : (Array.isArray(response.data.data) ? response.data.data : []);
      console.log(`\n获取到的文章总数: ${this.articles.length}`);
      return true;
    } catch (error) {
      console.error('获取文章失败:', error.message);
      this.articles = [];
      return false;
    }
  }

  // 修复后的过滤逻辑 - 只显示当前选中分类的文章
  filterArticles(category) {
    console.log(`\n===== 测试分类: ${category === 'all' ? '全部' : categories.find(c => c.id === category)?.name} =====`);
    
    let filtered = [];
    if (category === 'all') {
      filtered = this.articles;
    } else {
      const selectedCategory = categories.find(cat => cat.id === category);
      if (selectedCategory) {
        // 修复后的逻辑：只显示当前选中分类的文章
        filtered = this.articles.filter(article => {
          return article && typeof article.category === 'string' && 
                 article.category === selectedCategory.name;
        });
      }
    }
    
    console.log(`过滤后文章数量: ${filtered.length}`);
    
    if (filtered.length > 0) {
      console.log('文章预览:');
      filtered.slice(0, 2).forEach(article => {
        console.log(`- ${article.title} (分类: ${article.category})`);
      });
    }
    
    return filtered;
  }
}

// 运行测试
async function runTest() {
  console.log('\n========== 修复后分类过滤逻辑测试 ==========');
  
  const mockView = new MockArticlesView();
  
  // 获取文章数据
  const success = await mockView.fetchArticles();
  if (!success) return;
  
  // 测试所有分类
  mockView.filterArticles('all');
  
  // 测试每个分类
  categories.forEach(category => {
    mockView.filterArticles(category.id);
  });
  
  console.log('\n========== 测试完成 ==========');
}

runTest();
