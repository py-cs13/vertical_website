// 测试前端获取智能体数据的脚本
import axios from 'axios';

async function testFrontendAgentAPI() {
  try {
    console.log('测试前端获取智能体数据...');
    
    // 测试获取所有智能体
    const allAgentsResponse = await axios.get('http://localhost:8000/api/agents');
    console.log('\n✅ 获取所有智能体成功!');
    console.log(`共获取到 ${allAgentsResponse.data.length} 个智能体`);
    
    // 测试获取最新智能体
    const latestAgentsResponse = await axios.get('http://localhost:8000/api/agents/latest');
    console.log('\n✅ 获取最新智能体成功!');
    console.log(`共获取到 ${latestAgentsResponse.data.length} 个最新智能体`);
    
    // 显示智能体信息
    console.log('\n=== 智能体信息 ===');
    latestAgentsResponse.data.forEach((agent, index) => {
      console.log(`${index + 1}. ${agent.title}`);
      console.log(`   分类: ${agent.category}`);
      console.log(`   价格: ¥${agent.price}`);
      console.log(`   内容长度: ${agent.content.length} 字符`);
      console.log(`   发布时间: ${agent.published_at}`);
      console.log('---');
    });
    
    console.log('\n🎉 测试完成! 前端可以正常获取智能体数据。');
    
  } catch (error) {
    console.error('❌ 测试失败:', error.message);
    if (error.response) {
      console.error('   状态码:', error.response.status);
      console.error('   错误内容:', error.response.data);
    }
  }
}

testFrontendAgentAPI();
