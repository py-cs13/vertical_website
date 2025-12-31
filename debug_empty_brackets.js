// 调试脚本来查看文章内容的实际格式
const fs = require('fs');
const path = require('path');

// 模拟从数据库获取的内容格式
const testContent = `宝成长。值得注意的是，每个孩子发展节奏不同，游戏设计应兼顾年龄特点与个体差异。坚持创造游戏环境，您将见证宝宝在认知、情感、运动等领域的全面进步。

(
)
`;

console.log('原始内容:');
console.log(testContent);
console.log('\n内容的字符编码:');
for (let i = 0; i < testContent.length; i++) {
  const char = testContent[i];
  const code = char.charCodeAt(0);
  console.log(`字符 ${i}: '${char}' (${code})`);
}

// 测试当前的正则表达式
const regex = /\s*\(\s*\)\s*/g;
const result = testContent.replace(regex, '');
console.log('\n使用当前正则表达式替换后的结果:');
console.log(result);

// 测试更强大的正则表达式（明确匹配换行符）
const regex2 = /\s*\((\s|\n)*\)\s*/g;
const result2 = testContent.replace(regex2, '');
console.log('\n使用更强大的正则表达式替换后的结果:');
console.log(result2);

// 测试最强大的正则表达式（使用dotAll模式匹配所有字符）
const regex3 = /\s*\((.|\n)*?\)\s*/g;
const result3 = testContent.replace(regex3, '');
console.log('\n使用dotAll模式正则表达式替换后的结果:');
console.log(result3);
