<template>
  <div class="consultation-container h-screen flex">
    <!-- 侧边栏 -->
    <aside class="w-64 bg-gray-900 text-white flex flex-col">
      <!-- 新建对话按钮 -->
      <div class="p-4 border-b border-gray-700">
        <button
          @click="createNewConversation"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg transition-colors"
        >
          + 新对话
        </button>
      </div>

      <!-- 对话列表 -->
      <div class="flex-1 overflow-y-auto p-2">
        <div
          v-for="conv in conversations"
          :key="conv.id"
          @click="selectConversation(conv.id)"
          class="p-3 rounded-lg cursor-pointer mb-1 transition-colors"
          :class="[
            conv.id === currentId
              ? 'bg-blue-600'
              : 'hover:bg-gray-800'
          ]"
        >
          <div class="flex justify-between items-center">
            <span class="truncate text-sm">{{ conv.title }}</span>
            <button
              @click.stop="deleteConversation(conv.id)"
              class="text-gray-400 hover:text-red-400 text-xs"
            >
              删除
            </button>
          </div>
        </div>

        <div v-if="conversations.length === 0" class="text-gray-500 text-sm text-center py-4">
          暂无对话记录
        </div>
      </div>

      <!-- 返回首页 -->
      <div class="p-4 border-t border-gray-700">
        <router-link to="/" class="text-gray-400 hover:text-white text-sm">
          ← 返回首页
        </router-link>
        <br>
        <router-link to="/settings" class="text-gray-400 hover:text-white text-sm">
          ⚙️ 模型配置
        </router-link>
        <div v-if="isAuthenticated" class="mt-3 flex items-center justify-between">
          <span class="text-gray-400 text-xs truncate">{{ user?.name }}</span>
          <button
            @click="handleLogout"
            class="text-gray-400 hover:text-red-400 text-xs"
          >
            退出
          </button>
        </div>
      </div>
    </aside>

    <!-- 主对话区域 -->
    <main class="flex-1 flex flex-col bg-white">
      <!-- 消息列表 -->
      <div ref="messagesRef" class="flex-1 overflow-y-auto p-4 space-y-4">
        <!-- 空状态 -->
        <div v-if="messages.length === 0" class="flex items-center justify-center h-full">
          <div class="text-center text-gray-500">
            <div class="text-6xl mb-4">🩺</div>
            <p class="text-lg mb-2">您好！我是医疗健康咨询助手</p>
            <p>请描述您的症状或健康问题，我会为您提供专业建议</p>
          </div>
        </div>

        <!-- 消息列表 -->
        <ChatMessage
          v-for="msg in messages"
          :key="msg.id"
          :message="msg"
          :is-streaming="isLoading && msg.role === 'assistant' && msg.id === messages[messages.length - 1]?.id"
        />

        <!-- 加载动画 -->
        <div v-if="isLoading" class="flex justify-start">
          <div class="bg-gray-100 rounded-lg px-4 py-3">
            <div class="flex items-center gap-2">
              <div class="animate-pulse text-gray-500">思考中</div>
              <div class="flex gap-1">
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="border-t p-4">
        <ChatInput
          v-model="inputText"
          @send="handleSend"
          :disabled="isLoading"
        />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import { useConversationStore } from '@/stores/conversation'
import { useAuthStore } from '@/stores/auth'
import ChatMessage from '@/components/ChatMessage.vue'
import ChatInput from '@/components/ChatInput.vue'

const router = useRouter()
const store = useConversationStore()
const authStore = useAuthStore()
const { conversations, currentId, messages, isLoading } = storeToRefs(store)
const { isAuthenticated, user } = storeToRefs(authStore)

const inputText = ref('')
const messagesRef = ref<HTMLElement>()

// 页面加载时获取对话列表
onMounted(async () => {
  await store.loadConversations()
})

// 监听消息变化，自动滚动到底部
watch(messages, async () => {
  await nextTick()
  if (messagesRef.value) {
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight
  }
}, { deep: true })

const createNewConversation = async () => {
  await store.createConversation()
}

const selectConversation = async (id: number) => {
  await store.selectConversation(id)
}

const deleteConversation = async (id: number) => {
  if (confirm('确定删除该对话吗？')) {
    await store.deleteConversation(id)
  }
}

const handleSend = async () => {
  if (!inputText.value.trim() || isLoading.value) return
  
  const content = inputText.value
  inputText.value = ''
  
  await store.sendMessage(content)
}

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}
</script>
