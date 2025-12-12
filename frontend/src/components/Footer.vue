<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-section">
          <h3 class="footer-title">关于我们</h3>
          <p class="footer-text">
            宝贝成长母婴平台专注于为0-6岁宝宝的父母提供专业的育儿知识、实用的育儿工具和优质的育儿课程，陪伴宝宝健康快乐成长。
          </p>
        </div>
        
        <div class="footer-section">
          <h3 class="footer-title">快速链接</h3>
          <ul class="footer-links">
            <li><router-link to="/">首页</router-link></li>
            <li><router-link to="/about">关于我们</router-link></li>
            <li><a href="#">联系我们</a></li>
            <li><a href="#">隐私政策</a></li>
            <li><a href="#">服务条款</a></li>
          </ul>
        </div>
        
        <div class="footer-section">
          <h3 class="footer-title">联系方式</h3>
          <div class="contact-info">
            <p><i class="icon">📧</i> contact@example.com</p>
            <p><i class="icon">📞</i> 400-123-4567</p>
            <p><i class="icon">📍</i> 北京市朝阳区科技园区</p>
          </div>
        </div>
        
        <div class="footer-section">
          <h3 class="footer-title">关注我们</h3>
          <div class="social-links">
            <a href="#" class="social-link">
              <span class="icon">微信</span>
            </a>
            <a href="#" class="social-link">
              <span class="icon">微博</span>
            </a>
            <a href="#" class="social-link">
              <span class="icon">知乎</span>
            </a>
            <a href="#" class="social-link">
              <span class="icon">小红书</span>
            </a>
          </div>
        </div>
      </div>
      
      <div class="footer-bottom">
        <p>&copy; {{ new Date().getFullYear() }} 宝贝成长母婴平台. 保留所有权利.</p>
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
  gap: 40px;
  margin-bottom: 30px;
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
  background-color: var(--bg-primary);
  padding: 15px;
  border-radius: 10px;
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-light);
}

.footer-links {
  list-style: none;
}

.footer-links li {
  margin-bottom: 12px;
  position: relative;
  padding-left: 22px;
}

.footer-links li::before {
  content: "🌟";
  position: absolute;
  left: 0;
  top: 4px;
  font-size: 12px;
  color: var(--accent-color);
}

.footer-links a {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 14px;
  transition: all 0.3s ease;
  padding: 6px 8px;
  border-radius: 6px;
  display: inline-block;
}

.footer-links a:hover {
  color: var(--primary-color);
  background-color: var(--bg-accent);
  transform: translateX(5px);
}

.contact-info p {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 15px;
  font-size: 14px;
  color: var(--text-secondary);
  background-color: var(--bg-primary);
  padding: 10px 15px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.contact-info p:hover {
  box-shadow: var(--shadow-light);
  transform: translateY(-2px);
}

.icon {
  font-size: 18px;
  color: var(--primary-color);
  flex-shrink: 0;
}

.social-links {
  display: flex;
  gap: 18px;
  flex-wrap: wrap;
}

.social-link {
  display: inline-block;
  width: 45px;
  height: 45px;
  background-color: var(--bg-primary);
  color: var(--text-secondary);
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  text-decoration: none;
  font-size: 15px;
  transition: all 0.3s ease;
  border: 2px solid var(--border-color);
  box-shadow: var(--shadow-light);
}

.social-link:hover {
  background-color: var(--primary-color);
  color: white;
  transform: translateY(-4px) scale(1.1);
  border-color: var(--primary-color);
  box-shadow: var(--shadow-medium);
}

.footer-bottom {
  text-align: center;
  padding-top: 25px;
  border-top: 2px solid var(--border-color);
  color: var(--text-light);
  font-size: 14px;
  background-color: var(--bg-primary);
  margin: 0 -20px -20px;
  padding-left: 20px;
  padding-right: 20px;
  border-radius: 0 0 15px 15px;
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
  
  .footer-section .footer-title {
    font-size: 17px;
  }
  
  .footer-section .footer-title::before {
    font-size: 16px;
  }
  
  .social-links {
    justify-content: center;
    gap: 15px;
  }
  
  .social-link {
    width: 40px;
    height: 40px;
    font-size: 14px;
  }
  
  .contact-info p {
    padding: 8px 12px;
    gap: 10px;
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