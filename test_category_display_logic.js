// 测试分类标签显示逻辑
class TestCategoryDisplay {
  constructor() {
    // 模拟Vue的ref和computed
    this.isExpanded = false;
    this.categories = [
      { id: 1, name: '母婴育儿' },
      { id: 2, name: '育儿知识' },
      { id: 3, name: '营养辅食' },
      { id: 4, name: '产后恢复' },
      { id: 5, name: '亲子互动' },
      { id: 6, name: '成长发育' },
      { id: 7, name: '早期教育' },
      { id: 8, name: '健康养生' }
    ];
    this.activeCategory = 'all';
    this.currentPage = 1;
  }

  // 模拟computed属性
  get displayedCategories() {
    console.log('计算displayedCategories，isExpanded:', this.isExpanded);
    console.log('categories长度:', this.categories.length);
    if (this.isExpanded) {
      console.log('返回所有分类:', this.categories);
      return this.categories;
    }
    const slicedCategories = this.categories.slice(0, 4);
    console.log('返回前4个分类:', slicedCategories);
    return slicedCategories;
  }

  // 模拟toggleAllCategories方法
  toggleAllCategories() {
    console.log('\n=== 点击"全部"按钮 ===');
    console.log('切换前isExpanded:', this.isExpanded);
    this.isExpanded = !this.isExpanded;
    console.log('切换后isExpanded:', this.isExpanded);
    this.activeCategory = 'all';
    this.currentPage = 1;
    console.log('当前activeCategory:', this.activeCategory);
    console.log('当前currentPage:', this.currentPage);
    console.log('当前显示的分类数量:', this.displayedCategories.length);
    console.log('显示的分类:', this.displayedCategories.map(cat => cat.name));
  }

  // 模拟setActiveCategory方法
  setActiveCategory(categoryId) {
    console.log('\n=== 点击分类标签:', categoryId);
    this.activeCategory = categoryId;
    this.currentPage = 1;
    console.log('当前activeCategory:', this.activeCategory);
    console.log('当前isExpanded:', this.isExpanded);
    console.log('当前显示的分类数量:', this.displayedCategories.length);
  }

  // 测试初始状态
  testInitialState() {
    console.log('\n=== 测试初始状态 ===');
    console.log('初始isExpanded:', this.isExpanded);
    console.log('初始activeCategory:', this.activeCategory);
    console.log('初始显示的分类数量:', this.displayedCategories.length);
    console.log('初始显示的分类:', this.displayedCategories.map(cat => cat.name));
  }

  // 运行完整测试
  runTests() {
    console.log('开始测试分类标签显示逻辑');
    console.log('============================');
    
    // 测试初始状态
    this.testInitialState();
    
    // 测试点击"全部"按钮展开
    this.toggleAllCategories();
    
    // 测试点击其他分类
    this.setActiveCategory(3); // 点击"营养辅食"
    
    // 测试再次点击"全部"按钮收起
    this.toggleAllCategories();
    
    // 测试再次点击"全部"按钮展开
    this.toggleAllCategories();
    
    console.log('\n============================');
    console.log('测试完成');
  }
}

// 创建测试实例并运行测试
const test = new TestCategoryDisplay();
test.runTests();