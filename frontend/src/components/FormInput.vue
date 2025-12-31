<template>
  <div class="form-group">
    <label v-if="label" :for="id" class="form-label">{{ label }}</label>
    <input
      :id="id"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :readonly="readonly"
      :required="required"
      :maxlength="maxlength"
      :minlength="minlength"
      :pattern="pattern"
      :name="name"
      @input="handleInput"
      @blur="$emit('blur')"
      @focus="$emit('focus')"
      class="form-input"
    >
    <div v-if="error" class="form-error">{{ error }}</div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, computed } from 'vue'

// 定义组件属性
const props = defineProps({
  // 表单控件的id
  id: {
    type: String,
    default: ''
  },
  // 表单控件的name
  name: {
    type: String,
    default: ''
  },
  // 输入框类型
  type: {
    type: String,
    default: 'text'
  },
  // 绑定的值
  modelValue: {
    type: [String, Number, Date, null],
    default: ''
  },
  // 标签文本
  label: {
    type: String,
    default: ''
  },
  // 占位符文本
  placeholder: {
    type: String,
    default: ''
  },
  // 是否禁用
  disabled: {
    type: Boolean,
    default: false
  },
  // 是否只读
  readonly: {
    type: Boolean,
    default: false
  },
  // 是否必填
  required: {
    type: Boolean,
    default: false
  },
  // 最大长度
  maxlength: {
    type: [Number, String],
    default: null
  },
  // 最小长度
  minlength: {
    type: [Number, String],
    default: null
  },
  // 验证正则表达式
  pattern: {
    type: String,
    default: ''
  },
  // 错误信息
  error: {
    type: String,
    default: ''
  }
})

// 定义事件
const emit = defineEmits(['update:modelValue', 'blur', 'focus'])

// 处理输入事件
const handleInput = (event) => {
  emit('update:modelValue', event.target.value)
}
</script>

<style scoped>
.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: var(--text-primary);
  font-size: 14px;
}

.form-input {
  width: 100%;
  padding: 12px;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  font-size: 16px;
  background-color: var(--bg-secondary);
  color: var(--text-primary);
  transition: all 0.3s ease;
  font-family: inherit;
  outline: none;
}

.form-input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(255, 71, 133, 0.1);
}

.form-input:disabled,
.form-input[readonly] {
  background-color: var(--bg-primary);
  opacity: 0.7;
  cursor: not-allowed;
}

.form-error {
  margin-top: 6px;
  color: var(--error-color, #F44336);
  font-size: 13px;
}
</style>