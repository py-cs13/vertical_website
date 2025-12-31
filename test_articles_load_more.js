// 测试文章加载更多功能的脚本
const axios = require('axios');

// 模拟Vue组件的状态管理
class MockArticlesView {
  constructor() {
    this.articles = [];
    this.allArticles = [];
    this.loading = false;
    this.loadStep = 4;
  }

  // 模拟获取所有文章
  async fetchAllArticles() {
    try {
      this.loading = true;
      console.log('开始请求所有文章数据...');
      const response = await axios.get('http://localhost:8000/api/articles');
      console.log('API响应状态:', response.status);
      console.log('API响应数据类型:', typeof response.data);
      console.log('API响应数据长度:', Array.isArray(response.data) ? response.data.length : '不是数组');
      
      // 处理API响应
      const apiArticles = Array.isArray(response.data) ? response.data : (response.data.data || []);
      console.log('处理后的文章总数:', apiArticles.length);
      
      // 赋值数据
      this.allArticles = apiArticles;
      this.articles = this.allArticles.slice(0, 6);
      console.log('初始显示文章数:', this.articles.length);
      
      return true;
    } catch (error) {
      console.error('获取文章失败:', error);
      console.error('错误详情:', error.response || error.message);
      this.allArticles = [];
      this.articles = [];
      return false;
    } finally {
      this.loading = false;
    }
  }

  // 模拟加载更多
  async handleLoadMore() {
    console.log('=== 加载更多按钮被点击了！ ===');
    console.log('当前显示:', this.articles.length, '篇文章');
    console.log('总共有:', this.allArticles.length, '篇文章');
    console.log('是否有更多文章:', this.articles.length < this.allArticles.length);
    console.log('按钮是否被禁用:', this.loading || this.articles.length >= this.allArticles.length);
    
    // 防止重复点击
    if (this.loading || this.articles.length >= this.allArticles.length) {
      console.log('按钮被禁用或没有更多文章，不执行加载操作');
      return false;
    }
    
    try {
      this.loading = true;
      
      // 模拟网络延迟
      await new Promise(resolve => setTimeout(resolve, 300));
      
      const currentLength = this.articles.length;
      const newLength = currentLength + this.loadStep;
      console.log('准备加载从', currentLength, '到', newLength, '的文章');
      
      const moreArticles = this.allArticles.slice(currentLength, newLength);
      console.log('获取到的新文章:', moreArticles.length, '篇');
      
      // 添加新文章
      this.articles = [...this.articles, ...moreArticles];
      console.log('加载成功！现在显示:', this.articles.length, '篇文章');
      
      return true;
    } catch (error) {
      console.error('加载更多时发生错误:', error);
      return false;
    } finally {
      this.loading = false;
    }
  }
}

// 测试执行逻辑
async function runTest() {
  console.log('=== 开始测试文章加载更多功能 ===\n');
  
  const mockView = new MockArticlesView();
  
  // 测试1: 获取所有文章
  console.log('测试1: 获取所有文章');
  const fetchSuccess = await mockView.fetchAllArticles();
  if (!fetchSuccess) {
    console.log('获取文章失败，测试结束');
    return;
  }
  console.log('✓ 获取文章成功\n');
  
  // 测试2: 加载更多一次
  console.log('测试2: 第一次加载更多');
  const loadMoreSuccess1 = await mockView.handleLoadMore();
  if (!loadMoreSuccess1) {
    console.log('第一次加载更多失败');
  } else {
    console.log('✓ 第一次加载更多成功\n');
  }
  
  // 测试3: 加载更多第二次
  console.log('测试3: 第二次加载更多');
  const loadMoreSuccess2 = await mockView.handleLoadMore();
  if (!loadMoreSuccess2) {
    console.log('第二次加载更多失败');
  } else {
    console.log('✓ 第二次加载更多成功\n');
  }
  
  // 测试4: 测试禁用状态
  console.log('测试4: 检查是否还有更多文章');
  console.log('当前显示:', mockView.articles.length, '篇文章');
  console.log('总共有:', mockView.allArticles.length, '篇文章');
  console.log('是否可以继续加载:', mockView.articles.length < mockView.allArticles.length);
  
  console.log('\n=== 测试结束 ===');
  console.log('最终显示文章数:', mockView.articles.length);
  console.log('总文章数:', mockView.allArticles.length);
}

// 运行测试
runTest().catch(error => {
  console.error('测试过程中发生错误:', error);
});
