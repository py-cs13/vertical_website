<template>
  <div class="about-view">
    <h1 class="page-title">关于我们</h1>
    
    <!-- 网站介绍 -->
    <section class="about-section">
      <h2 class="section-title">网站介绍</h2>
      <div class="section-content">
        <p>母婴趣指南是一家专注于0-6岁宝宝成长的垂直内容平台，我们致力于为新手父母提供专业、实用、温暖的育儿知识与服务。</p>
        <p>我们的团队由儿科医生、早教专家、资深营养师和经验丰富的育儿顾问组成，以科学专业为基础，用温暖贴心的方式，将前沿育儿理念转化为通俗易懂的文章和实用工具包，陪伴每一位父母度过美好的育儿时光。</p>
      </div>
    </section>
    
    <!-- 我们的使命 -->
    <section class="about-section">
      <h2 class="section-title">我们的使命</h2>
      <div class="section-content">
        <p>我们的使命是陪伴每一位父母，用科学的育儿知识和温暖的人类关怀，让每个孩子都能在爱与智慧中健康成长。</p>
        <ul class="mission-list">
          <li>提供专业、易懂的0-6岁育儿知识</li>
          <li>传播科学、先进的育儿理念</li>
          <li>开发实用、便捷的育儿工具</li>
          <li>构建温暖、互助的育儿社区</li>
        </ul>
      </div>
    </section>
    

    
    <!-- 联系我们 -->
    <section class="about-section">
      <h2 class="section-title">联系我们</h2>
      <div class="contact-info">
        <div class="contact-item">
          <i class="icon">📧</i>
          <div class="contact-details">
            <h3>邮箱</h3>
            <p>cl06221227@gmail.com</p>
          </div>
        </div>
        <div class="contact-item">
          <i class="icon">📞</i>
          <div class="contact-details">
            <h3>电话</h3>
            <p>19041331887</p>
          </div>
        </div>
        <div class="contact-item">
          <i class="icon">📍</i>
          <div class="contact-details">
            <h3>地址</h3>
            <p>河北省邯郸市</p>
          </div>
        </div>
      </div>
    </section>
    
    <!-- 合作方式 -->
    <section class="about-section">
      <h2 class="section-title">合作方式</h2>
      <div class="section-content">
        <p>我们欢迎与母婴领域相关的各种形式合作，共同为父母们提供更好的育儿资源和服务。如果您有合作意向，请联系我们，我们将尽快回复您。</p>
        <div class="cooperation-types">
          <div class="cooperation-type">
            <h3>内容合作</h3>
            <p>如果您是早教专家、资深育儿顾问或有丰富育儿经验的作者，欢迎与我们合作创作专业的母婴内容。</p>
          </div>
          <div class="cooperation-type">
            <h3>品牌合作</h3>
            <p>我们欢迎与母婴产品、早教机构等相关品牌进行深度合作。</p>
          </div>
          <div class="cooperation-type">
            <h3>资源合作</h3>
            <p>如果您有优质的育儿资源或服务，欢迎与我们开展资源互换与合作。</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'


</script>

<style scoped>
.about-view {
  max-width: 100%;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 30px;
  color: #333;
}

/* 通用章节样式 */
.about-section {
  margin-bottom: 50px;
  padding: 30px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 20px;
  color: #333;
  padding-bottom: 10px;
  border-bottom: 2px solid #1E88E5;
}

.section-content {
  font-size: 16px;
  line-height: 1.8;
  color: #666;
}

.section-content p {
  margin-bottom: 20px;
}

/* 使命列表 */
.mission-list {
  margin-left: 20px;
}

.mission-list li {
  margin-bottom: 10px;
  position: relative;
  padding-left: 20px;
}

.mission-list li:before {
  content: '✓';
  position: absolute;
  left: 0;
  color: #1E88E5;
  font-weight: bold;
}

/* 联系信息 */
.contact-info {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 20px;
  min-width: 300px;
}

.contact-item .icon {
  font-size: 32px;
  color: #1E88E5;
}

.contact-details h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 5px;
  color: #333;
}

.contact-details p {
  font-size: 16px;
  color: #666;
  margin-bottom: 0;
}

/* 合作方式 */
.cooperation-types {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 30px;
}

.cooperation-type {
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.cooperation-type h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 10px;
  color: #333;
}

.cooperation-type p {
  font-size: 14px;
  line-height: 1.6;
  color: #666;
  margin-bottom: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-title {
    font-size: 24px;
  }
  
  .about-section {
    padding: 20px;
    margin-bottom: 30px;
  }
  
  .section-title {
    font-size: 20px;
  }
  
  .section-content {
    font-size: 15px;
  }
  
  .contact-info {
    flex-direction: column;
    gap: 20px;
  }
  
  .contact-item {
    min-width: auto;
  }
  
  .cooperation-types {
    grid-template-columns: 1fr;
    gap: 15px;
  }
}
</style>