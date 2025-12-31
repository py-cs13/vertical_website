// 测试分类标签显示功能
const axios = require('axios');

// 模拟前端分类数据
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

// 模拟分类显示逻辑
class MockCategoryDisplay {
  constructor() {
    this.isExpanded = false;
    this.activeCategory = 'all';
    this.categories = categories;
  }

  // 显示的分类（根据isExpanded决定显示全部还是前4个）
  getDisplayedCategories() {
    if (this.isExpanded) {
      return this.categories;
    }
    return this.categories.slice(0, 4);
  }

  // 切换展开/收起所有分类
  toggleAllCategories() {
    this.isExpanded = !this.isExpanded;
    this.activeCategory = 'all';
  }

  // 设置当前分类
  setActiveCategory(categoryId) {
    this.activeCategory = categoryId;
  }

  // 测试分类标签显示功能
  testDisplay() {
    console.log('\n========== 分类标签显示测试 ==========');
    
    // 初始状态（收起）
    console.log('1. 初始状态（收起）:');
    console.log(`   展开状态: ${this.isExpanded}`);
    console.log(`   当前分类: ${this.activeCategory}`);
    console.log(`   显示的分类: ${this.getDisplayedCategories().map(c => c.name).join(', ')}`);
    console.log(`   显示数量: ${this.getDisplayedCategories().length}`);
    
    // 点击"全部"按钮（展开）
    this.toggleAllCategories();
    console.log('\n2. 点击"全部"按钮（展开）:');
    console.log(`   展开状态: ${this.isExpanded}`);
    console.log(`   当前分类: ${this.activeCategory}`);
    console.log(`   显示的分类: ${this.getDisplayedCategories().map(c => c.name).join(', ')}`);
    console.log(`   显示数量: ${this.getDisplayedCategories().length}`);
    
    // 点击"母婴育儿"分类
    this.setActiveCategory(1);
    console.log('\n3. 点击"母婴育儿"分类:');
    console.log(`   展开状态: ${this.isExpanded}`);
    console.log(`   当前分类: ${this.activeCategory}`);
    console.log(`   显示的分类: ${this.getDisplayedCategories().map(c => c.name).join(', ')}`);
    console.log(`   显示数量: ${this.getDisplayedCategories().length}`);
    
    // 再次点击"全部"按钮（收起）
    this.toggleAllCategories();
    console.log('\n4. 再次点击"全部"按钮（收起）:');
    console.log(`   展开状态: ${this.isExpanded}`);
    console.log(`   当前分类: ${this.activeCategory}`);
    console.log(`   显示的分类: ${this.getDisplayedCategories().map(c => c.name).join(', ')}`);
    console.log(`   显示数量: ${this.getDisplayedCategories().length}`);
    
    // 验证分类数据完整性
    console.log('\n5. 分类数据完整性验证:');
    console.log(`   总分类数: ${this.categories.length}`);
    console.log(`   分类列表: ${this.categories.map(c => c.name).join(', ')}`);
    
    // 检查是否有重复分类
    const categoryNames = this.categories.map(c => c.name);
    const uniqueCategories = [...new Set(categoryNames)];
    console.log(`   唯一分类数: ${uniqueCategories.length}`);
    console.log(`   重复分类: ${categoryNames.length - uniqueCategories.length > 0 ? '存在' : '无'}`);
    
    console.log('\n========== 测试完成 ==========');
  }
}

// 运行测试
function runTest() {
  const mockDisplay = new MockCategoryDisplay();
  mockDisplay.testDisplay();
}

runTest();
