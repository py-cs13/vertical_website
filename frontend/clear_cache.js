// 清除前端缓存脚本
// 这个脚本会清除所有与内容相关的本地存储缓存

// 清除特定的缓存项
const cacheKeys = [
  'latest_articles',
  // 清除所有以article_开头的缓存项
  ...Object.keys(localStorage).filter(key => key.startsWith('article_'))
];

cacheKeys.forEach(key => {
  localStorage.removeItem(key);
  console.log(`已清除缓存: ${key}`);
});

console.log('所有内容缓存已清除！请刷新页面查看最新内容。');
