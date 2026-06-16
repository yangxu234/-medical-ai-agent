<template>
  <div class="chat-input-container">
    <div class="flex gap-2">
      <textarea
        :value="modelValue"
        @input="onInput"
        @keydown.enter.exact.prevent="handleSend"
        :placeholder="disabled ? 'AI正在思考中...' : '请描述您的症状或健康问题...'"
        :disabled="disabled"
        rows="1"
        class="flex-1 border border-gray-300 rounded-lg px-4 py-3 resize-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
      ></textarea>
      <button
        @click="handleSend"
        :disabled="disabled || !modelValue?.trim()"
        class="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        发送
      </button>
    </div>
    <p class="text-xs text-gray-500 mt-2">
      按 Enter 发送，Shift + Enter 换行
    </p>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  modelValue: string
  disabled?: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
  'send': []
}>()

const onInput = (e: Event) => {
  const target = e.target as HTMLTextAreaElement
  emit('update:modelValue', target.value)
}

const handleSend = () => {
  if (!props.disabled && props.modelValue?.trim()) {
    emit('send')
  }
}
</script>
