<template>
  <div class="form-group">
    <label v-if="label" :for="id" class="form-label">{{ label }}</label>
    <textarea
      :id="id"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :readonly="readonly"
      :required="required"
      :maxlength="maxlength"
      :minlength="minlength"
      :rows="rows"
      :cols="cols"
      :name="name"
      @input="handleInput"
      @blur="$emit('blur')"
      @focus="$emit('focus')"
      class="form-textarea"
    ></textarea>
    <div v-if="error" class="form-error">{{ error }}</div>
    <div v-if="showCount" class="form-count">{{ modelValue.length }}/{{ maxlength }}</div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

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
  // 绑定的值
  modelValue: {
    type: String,
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
  // 行数
  rows: {
    type: Number,
    default: 4
  },
  // 列数
  cols: {
    type: Number,
    default: 50
  },
  // 错误信息
  error: {
    type: String,
    default: ''
  },
  // 是否显示字数统计
  showCount: {
    type: Boolean,
    default: false
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

.form-textarea {
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
  resize: vertical;
  min-height: 120px;
}

.form-textarea:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(255, 71, 133, 0.1);
}

.form-textarea:disabled,
.form-textarea[readonly] {
  background-color: var(--bg-primary);
  opacity: 0.7;
  cursor: not-allowed;
  resize: none;
}

.form-error {
  margin-top: 6px;
  color: var(--error-color, #F44336);
  font-size: 13px;
}

.form-count {
  margin-top: 6px;
  color: var(--text-secondary);
  font-size: 13px;
  text-align: right;
}
</style>