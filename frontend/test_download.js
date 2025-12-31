import axios from 'axios'

// 测试下载功能
async function testDownload() {
  try {
    // 首先获取智能体列表
    const agentsResponse = await axios.get('http://localhost:8000/api/agents')
    const agents = agentsResponse.data.data
    
    if (agents.length === 0) {
      console.log('没有可用的智能体')
      return
    }
    
    const firstAgent = agents[0]
    console.log(`测试下载第一个智能体: ${firstAgent.title}`)
    console.log(`智能体ID: ${firstAgent.id}`)
    console.log(`分类: ${firstAgent.category}`)
    
    // 测试下载API（注意：这里需要有效token才能成功）
    const token = 'your-valid-token-here' // 需要替换为真实token
    
    try {
      const downloadResponse = await axios.get(`http://localhost:8000/api/agents/${firstAgent.id}/download`, {
        headers: {
          'Authorization': `Bearer ${token}`
        },
        responseType: 'arraybuffer'
      })
      
      console.log('下载请求成功！')
      console.log(`响应状态码: ${downloadResponse.status}`)
      console.log(`响应类型: ${downloadResponse.headers['content-type']}`)
      console.log(`内容长度: ${downloadResponse.data.length} 字节`)
      console.log(`文件名: ${downloadResponse.headers['content-disposition']}`)
      
      if (downloadResponse.data.length > 0) {
        console.log('✓ 下载功能正常工作！')
      } else {
        console.log('✗ 下载的文件内容为空')
      }
      
    } catch (downloadError) {
      if (downloadError.response) {
        console.log(`下载请求失败，状态码: ${downloadError.response.status}`)
        console.log(`错误信息: ${downloadError.response.data.message || downloadError.response.data}`)
        
        if (downloadError.response.status === 401) {
          console.log('提示：下载需要有效的认证token，请登录后测试')
        }
      } else {
        console.log('下载请求失败:', downloadError.message)
      }
    }
    
  } catch (error) {
    console.error('获取工具包列表失败:', error.message)
  }
}

testDownload()
