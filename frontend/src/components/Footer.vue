<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-content">
        <!-- 按高度从高到低排列：关于我们 > 快速链接 > 关注我们 > 联系方式 -->
        <div class="footer-section">
          <h3 class="footer-title">关于我们</h3>
          <p class="footer-text">
            母婴趣指南专注于为0-6岁宝宝的父母提供专业的育儿知识、实用的育儿工具和优质的育儿课程，陪伴宝宝健康快乐成长。
          </p>
        </div>
        
        <div class="footer-section">
          <h3 class="footer-title">快速链接</h3>
          <ul class="footer-links">
            <li><router-link to="/">首页</router-link></li>
            <li><router-link to="/about">关于我们</router-link></li>
            <li><router-link to="/articles">文章中心</router-link></li>
            <li><router-link to="/agents">智能体工具</router-link></li>
          </ul>
        </div>
        
        <div class="footer-section">
          <h3 class="footer-title">关注我们</h3>
          <ul class="social-links">
            <li><span class="social-text">微信</span></li>
            <li><span class="social-text">微博</span></li>
            <li><span class="social-text">知乎</span></li>
            <li><span class="social-text">小红书</span></li>
          </ul>
        </div>
        
        <div class="footer-section">
          <h3 class="footer-title">联系方式</h3>
          <div class="contact-info">
            <p><i class="icon">📧</i> cl06221227@gmail.com</p>
            <p><i class="icon">📞</i> 19041331887</p>
            <p><i class="icon">📍</i> 河北省邯郸市</p>
          </div>
        </div>
      </div>
      
      <div class="footer-bottom">
        <p>&copy; {{ new Date().getFullYear() }} 母婴趣指南. 保留所有权利.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
// Footer组件不需要复杂的逻辑
</script>

<style scoped>
.footer {
  background: linear-gradient(180deg, #FFF5F8 0%, #F8F9FA 100%);
  color: var(--text-primary);
  padding: 40px 0 20px;
  margin-top: 60px;
  border-top: 3px solid var(--primary-color);
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.05);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  margin-bottom: 30px;
  align-items: start;
}

.footer-section {
  background-color: var(--bg-primary);
  padding: 20px;
  border-radius: 10px;
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-light);
}

.footer-section .footer-title {
  font-size: 19px;
  font-weight: 600;
  margin-bottom: 20px;
  color: var(--primary-color);
  display: flex;
  align-items: center;
  gap: 10px;
}

.footer-section .footer-title::before {
  content: "🎀";
  font-size: 18px;
}

.footer-text {
  font-size: 14px;
  line-height: 1.8;
  color: var(--text-secondary);
  margin: 0;
}

.footer-links {
  list-style: none;
  margin: 0;
  padding: 0;
}

.footer-links li {
  margin-bottom: 12px;
  position: relative;
  padding-left: 22px;
}

.footer-links li::before {
  content: "🌟";
  position: absolute;
  left: 8px;
  top: 10px;
  font-size: 12px;
  color: var(--accent-color);
}

.footer-links a {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 14px;
  transition: all 0.3s ease;
  padding: 8px 12px;
  border-radius: 8px;
  display: block;
}

.footer-links a:hover {
  color: var(--primary-color);
  background-color: var(--bg-accent);
  transform: translateX(5px);
}

.contact-info {
  margin: 0;
  padding: 0;
}

.contact-info p {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 15px;
  font-size: 14px;
  color: var(--text-secondary);
}

.contact-info p:last-child {
  margin-bottom: 0;
}

.contact-info p:hover {
  transform: translateY(-2px);
}

.icon {
  font-size: 18px;
  color: var(--primary-color);
  flex-shrink: 0;
}

.social-links {
  list-style: none;
  margin: 0;
  padding: 0;
}

.social-links li {
  margin-bottom: 12px;
  position: relative;
  padding-left: 22px;
}

.social-links li:last-child {
  margin-bottom: 0;
}

.social-links li::before {
  content: "🌟";
  position: absolute;
  left: 8px;
  top: 10px;
  font-size: 12px;
  color: var(--accent-color);
}

.social-text {
  color: var(--text-secondary);
  font-size: 14px;
  padding: 8px 12px;
  border-radius: 8px;
  display: block;
}

.footer-bottom {
  text-align: center;
  padding-top: 25px;
  border-top: 2px solid var(--border-color);
  color: var(--text-light);
  font-size: 14px;
}

.footer-bottom p {
  margin: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .footer {
    padding: 30px 0 15px;
    margin-top: 40px;
  }
  
  .footer-content {
    grid-template-columns: 1fr;
    gap: 30px;
  }
  
  .footer-section {
    padding: 15px;
  }
  
  .footer-section .footer-title {
    font-size: 17px;
  }
  
  .footer-section .footer-title::before {
    font-size: 16px;
  }
  
  .social-link {
    font-size: 13px;
    padding: 6px 10px;
  }
}

@media (max-width: 480px) {
  .footer-content {
    gap: 25px;
  }
  
  .footer-text {
    font-size: 13px;
    padding: 12px;
  }
  
  .footer-links a {
    font-size: 13px;
  }
}
</style>