// 测试Markdown修复效果
const axios = require('axios');

async function testMarkdownFix() {
    try {
        // 获取文章内容
        const response = await axios.get('http://localhost:8000/api/content/59');
        const article = response.data;
        
        console.log('=== 原始文章内容 ===');
        console.log(article.content);
        
        // 应用修复函数
        const fixMarkdown = (content) => {
            if (!content) return '';
            
            let processedContent = content;
            
            // 1. 在一级标题后添加换行符
            processedContent = processedContent.replace(/(#\s[^#\n]+)/g, '$1\n\n');
            
            // 2. 在二级标题前添加换行符
            processedContent = processedContent.replace(/([^\n])(##\s)/g, '$1\n\n$2');
            
            // 3. 在列表项前添加换行符
            processedContent = processedContent.replace(/([^\n])(-\s)/g, '$1\n$2');
            
            // 4. 在粗体文本和普通文本之间添加适当的空格
            processedContent = processedContent.replace(/(\*\*[^\*]+\*\*)([^\s\n])/g, '$1 $2');
            
            // 5. 确保每个列表项之间有适当的间隔
            processedContent = processedContent.replace(/(-\s[^-\n]+)(?=-\s)/g, '$1\n');
            
            return processedContent;
        };
        
        const fixedContent = fixMarkdown(article.content);
        
        console.log('\n=== 修复后的内容 ===');
        console.log(fixedContent);
        
        // 测试marked转换
        const { marked } = await import('marked');
        const html = marked(fixedContent);
        
        console.log('\n=== HTML转换结果 ===');
        console.log(html);
        
        // 检查是否正确生成了段落和标题
        console.log('\n=== 转换质量检查 ===');
        console.log('包含h1标签:', html.includes('<h1>'));
        console.log('包含h2标签:', html.includes('<h2>'));
        console.log('包含p标签:', html.includes('<p>'));
        console.log('包含ul标签:', html.includes('<ul>'));
        console.log('包含li标签:', html.includes('<li>'));
        
    } catch (error) {
        console.error('错误:', error.message);
    }
}

testMarkdownFix();