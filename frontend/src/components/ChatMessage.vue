<template>
  <div
    class="message"
    :class="[message.role === 'user' ? 'flex justify-end' : 'flex justify-start']"
  >
    <div
      :class="[
        'max-w-3xl rounded-lg px-4 py-3',
        message.role === 'user'
          ? 'bg-blue-600 text-white'
          : 'bg-gray-100 text-gray-800'
      ]"
    >
      <!-- 助手消息 -->
      <div v-if="message.role === 'assistant'" class="prose prose-sm max-w-none">
        <!-- 流式中：纯文本（快速） -->
        <div v-if="isStreaming" style="white-space: pre-wrap;">{{ message.content }}<span class="inline-block w-2 h-4 bg-gray-400 ml-0.5 animate-pulse"></span></div>
        <!-- 完成后：渲染Markdown -->
        <div v-else v-html="renderedMarkdown"></div>
      </div>
      <!-- 用户消息 -->
      <div v-else>
        {{ message.content }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { marked } from 'marked'
import type { Message } from '@/types/message'

const props = defineProps<{
  message: Message
  isStreaming?: boolean
}>()

marked.setOptions({ breaks: true, gfm: true })

const renderedMarkdown = computed(() => {
  return marked.parse(props.message.content) as string
})
</script>

<style scoped>
.prose :deep(strong) {
  font-weight: 600;
}
</style>
