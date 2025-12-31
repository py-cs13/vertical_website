<template>
  <div class="test-container">
    <h2>测试v-html指令</h2>
    <div v-html="testContent"></div>
    <button @click="updateContent">更新内容</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const testContent = ref('<h3>测试HTML内容</h3><p>这是一个段落</p><ul><li>列表项1</li><li>列表项2</li></ul>')

const updateContent = () => {
  testContent.value = '<h4>更新后的内容</h4><p>这是更新后的段落</p><ol><li>有序列表项1</li><li>有序列表项2</li></ol>'
}
</script>

<style scoped>
.test-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
</style>