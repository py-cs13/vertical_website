// 调试文章ID 59的内容格式
const axios = require('axios');

async function debugArticle() {
    try {
        const response = await axios.get('http://localhost:8000/api/content/59');
        const article = response.data;
        
        console.log('=== 文章详情 (ID: 59) ===');
        console.log('标题:', article.title);
        console.log('分类:', article.category);
        console.log('内容类型:', typeof article.content);
        console.log('内容长度:', article.content.length);
        console.log('\n=== 原始内容预览 (前200字符) ===');
        console.log(article.content.substring(0, 200) + '...');
        
        // 检查内容是否包含Markdown格式
        console.log('\n=== 格式检查 ===');
        console.log('包含标题 (#):', article.content.includes('#'));
        console.log('包含二级标题 (##):', article.content.includes('##'));
        console.log('包含粗体 (**):', article.content.includes('**'));
        console.log('包含列表 (-):', article.content.includes('- '));
        
        // 使用marked库测试转换
        const { marked } = await import('marked');
        const html = marked(article.content);
        console.log('\n=== HTML转换结果 (前300字符) ===');
        console.log(html.substring(0, 300) + '...');
        
    } catch (error) {
        console.error('错误:', error.message);
        if (error.response) {
            console.error('响应状态:', error.response.status);
            console.error('响应数据:', error.response.data);
        }
    }
}

debugArticle();