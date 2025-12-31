// 测试Markdown格式修复函数
const originalContent = "# 宝宝衣物挑选指南：二胎妈妈的纯干货分享 作为一位经历过无数踩坑的二胎妈妈，今天把最实用的宝宝衣物挑选经验分享给大家，记得先收藏再慢慢看哦💗 ## ✅ 材质选择是首要 一定要选**A类纯棉材质** ！透气柔软对宝宝皮肤最友好，记得看标签上的安全类别标识哦✨ ## 📏 尺码挑选有技巧 - 新生儿建议买大1-2码，宝宝长得快，大一点更舒适 - 3个月前的宝宝准备59码最实用，性价比超高😉 ## 👗 款式选择要注意 - 首选开衫式和尚服，穿脱方便不碰头 - 避免过多装饰物，防止刮伤宝宝娇嫩皮肤 ## 🔍 细节检查不能忘 - 标签要在外侧或无标签，避免刺激皮肤 - 缝线要平整无骨缝制，减少摩擦 - 纽扣按扣要牢固无松动，防止宝宝误食 ## 🧼 清洗保养要仔细 - 新衣服一定要先洗后穿，使用婴儿专用洗衣液 - 单独手洗最安全，避免交叉感染 - 阳光下自然晾晒杀菌，完全干透再收纳，避免潮湿发霉 ## ❌ 这些雷区要避开 - 不要买深色衣物，易褪色且可能含有更多染料 - 不要选带绳带的设计，存在安全隐患 - 不要用成人洗衣产品，成分太刺激 记住这几个要点，宝宝衣物挑选不再头疼！带娃路上我们又进步一点点啦💪 分享给需要的宝妈们，让我们一起科学育儿，做个不焦虑的快乐妈妈💕";

// 修复函数
function fixMarkdownFormat(content) {
  if (!content) return '';
  
  let processedContent = content;
  
  // 1. 在一级标题后添加换行符
  processedContent = processedContent.replace(/(#\s.+?)(?=##|$)/s, (match) => {
    return match.replace(/(?<!\n)$/, '\n\n');
  });
  
  // 2. 在二级标题前添加换行符
  processedContent = processedContent.replace(/([^\n])(##\s)/g, '$1\n\n$2');
  
  // 3. 在二级标题后添加换行符
  processedContent = processedContent.replace(/(##\s.+?)(?=##|-|$)/gs, (match) => {
    return match.replace(/(?<!\n)$/, '\n\n');
  });
  
  // 4. 在所有列表项前添加换行符
  processedContent = processedContent.replace(/([^\n])(-\s)/g, '$1\n$2');
  
  // 5. 在粗体文本和普通文本之间添加适当的空格
  processedContent = processedContent.replace(/(\*\*[^\*]+\*\*)([^\s\n])/g, '$1 $2');
  
  // 6. 确保每个列表项之间有适当的间隔
  processedContent = processedContent.replace(/(-\s[^-\n]+)(?=-\s)/g, '$1\n');
  
  // 7. 清理多余的空行
  processedContent = processedContent.replace(/^\n+/, ''); // 移除开头的空行
  processedContent = processedContent.replace(/\n{3,}/g, '\n\n'); // 将3个或更多的空行替换为2个
  
  return processedContent;
}

// 测试修复效果
const fixedContent = fixMarkdownFormat(originalContent);

console.log("=== 原始内容 ===");
console.log(originalContent);
console.log("\n=== 修复后的内容 ===");
console.log(fixedContent);
