<template>
  <div class="home-view">
    <!-- 母婴主题装饰 -->
    <div class="theme-decoration">
      <div class="decoration-icon">👶</div>
      <div class="decoration-icon">🍼</div>
      <div class="decoration-icon">🎀</div>
    </div>
      <!-- 页面副标题 -->
      <p class="page-subtitle main-subtitle">专业的母婴知识分享，陪伴宝贝健康成长每一天</p>
      
      <!-- 内容分类标签 -->
      <div class="category-tabs-wrapper">
        <div class="category-tabs-simple">
          <!-- 全部按钮 -->
          <button 
            class="tab-btn-simple" 
            :class="{ active: activeCategory === 0 }"
            @click="filterContent(0)"
          >
            <span class="tab-icon">{{ getCategoryIcon('全部') }}</span>
            全部
          </button>
          <!-- 其他分类标签容器 -->
          <div class="category-tabs-container">
            <button 
              v-for="category in categories.filter(c => c.id !== 0 && (isExpanded || c.id <= 4))" 
              :key="category.id" 
              class="tab-btn-simple" 
              :class="{ active: activeCategory === category.id }"
              @click="filterContent(category.id)"
            >
              <span class="tab-icon">{{ getCategoryIcon(category.name) }}</span>
              {{ category.name }}
            </button>
          </div>
        </div>
      </div>
    
    <!-- 加载状态：骨架屏 -->
    <div v-if="loading && !hasCachedContent" class="skeleton-container">
      <!-- 文章骨架屏 -->
      <div class="content-section">
        <div class="section-header skeleton">
          <div class="section-title skeleton-text"></div>
          <div class="view-all-link skeleton-text"></div>
        </div>
        <div class="content-list">
          <div v-for="i in 4" :key="'skeleton-article-' + i" class="content-card skeleton-card">
            <div class="card-header skeleton">
