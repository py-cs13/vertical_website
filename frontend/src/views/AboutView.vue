<template>
  <div class="about-view">
    <h1 class="page-title">关于我们</h1>
    
    <!-- 网站介绍 -->
    <section class="about-section">
      <h2 class="section-title">网站介绍</h2>
      <div class="section-content">
        <p>垂直生活健康内容平台是一家专注于提供高质量生活健康知识的平台，我们致力于为用户提供专业、实用、可靠的健康生活内容。</p>
        <p>我们的团队由一群热爱健康生活的专业人士组成，包括医生、营养师、健身教练等，他们将自己的专业知识转化为通俗易懂的文章和工具包，帮助用户更好地管理自己的健康。</p>
      </div>
    </section>
    
    <!-- 我们的使命 -->
    <section class="about-section">
      <h2 class="section-title">我们的使命</h2>
      <div class="section-content">
        <p>我们的使命是让每个人都能轻松获取专业的健康生活知识，通过科学的方法提升生活质量。</p>
        <ul class="mission-list">
          <li>提供高质量的健康生活内容</li>
          <li>传播科学的健康生活理念</li>
          <li>帮助用户养成健康的生活习惯</li>
          <li>建立一个健康生活的交流社区</li>
        </ul>
      </div>
    </section>
    
    <!-- 团队介绍 -->
    <section class="about-section">
      <h2 class="section-title">团队介绍</h2>
      <div class="team-list">
        <div class="team-member" v-for="member in teamMembers" :key="member.id">
          <div class="member-avatar">
            <img :src="member.avatar" :alt="member.name" />
          </div>
          <div class="member-info">
            <h3 class="member-name">{{ member.name }}</h3>
            <p class="member-title">{{ member.title }}</p>
            <p class="member-bio">{{ member.bio }}</p>
          </div>
        </div>
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
            <p>contact@example.com</p>
          </div>
        </div>
        <div class="contact-item">
          <i class="icon">📞</i>
          <div class="contact-details">
            <h3>电话</h3>
            <p>400-123-4567</p>
          </div>
        </div>
        <div class="contact-item">
          <i class="icon">📍</i>
          <div class="contact-details">
            <h3>地址</h3>
            <p>北京市朝阳区科技园区</p>
          </div>
        </div>
      </div>
    </section>
    
    <!-- 合作方式 -->
    <section class="about-section">
      <h2 class="section-title">合作方式</h2>
      <div class="section-content">
        <p>我们欢迎各种形式的合作，包括内容合作、广告合作、品牌合作等。如果您有合作意向，请联系我们，我们将尽快回复您。</p>
        <div class="cooperation-types">
          <div class="cooperation-type">
            <h3>内容合作</h3>
            <p>如果您是健康领域的专业人士，欢迎与我们合作创作内容。</p>
          </div>
          <div class="cooperation-type">
            <h3>广告合作</h3>
            <p>我们提供多种广告形式，包括横幅广告、植入广告等。</p>
          </div>
          <div class="cooperation-type">
            <h3>品牌合作</h3>
            <p>我们欢迎与健康相关的品牌进行合作。</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 团队成员
const teamMembers = ref([
  {
    id: 1,
    name: '张三',
    title: '创始人兼CEO',
    avatar: 'https://via.placeholder.com/150',
    bio: '医学博士，从事健康管理工作10年，致力于传播科学的健康生活理念。'
  },
  {
    id: 2,
    name: '李四',
    title: '内容总监',
    avatar: 'https://via.placeholder.com/150',
    bio: '营养学硕士，曾在多家健康媒体担任编辑，擅长将专业知识转化为通俗易懂的内容。'
  },
  {
    id: 3,
    name: '王五',
    title: '技术总监',
    avatar: 'https://via.placeholder.com/150',
    bio: '资深全栈工程师，拥有丰富的Web开发经验，负责平台的技术架构和开发工作。'
  }
])
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

/* 团队列表 */
.team-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 30px;
}

.team-member {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.member-avatar {
  margin-bottom: 20px;
}

.member-avatar img {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
}

.member-name {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #333;
}

.member-title {
  font-size: 15px;
  color: #1E88E5;
  margin-bottom: 10px;
}

.member-bio {
  font-size: 14px;
  line-height: 1.6;
  color: #666;
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
  
  .team-list {
    grid-template-columns: 1fr;
    gap: 20px;
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