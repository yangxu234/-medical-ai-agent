import { defineStore } from 'pinia'
import { ref, triggerRef } from 'vue'
import { conversationApi, messageApi } from '@/api/conversation'
import type { Conversation } from '@/types/conversation'
import type { Message } from '@/types/message'

export const useConversationStore = defineStore('conversation', () => {
  const conversations = ref<Conversation[]>([])
  const currentId = ref<number | null>(null)
  const messages = ref<Message[]>([])
  const isLoading = ref(false)
  const streamingMsg = ref<Message | null>(null)

  async function loadConversations() {
    try {
      conversations.value = await conversationApi.list()
    } catch (error) {
      console.error('加载对话列表失败:', error)
    }
  }

  async function createConversation() {
    try {
      const conv = await conversationApi.create({ title: '新对话' })
      conversations.value.unshift(conv)
      currentId.value = conv.id
      messages.value = []
      return conv
    } catch (error) {
      console.error('创建对话失败:', error)
      return null
    }
  }

  async function selectConversation(id: number) {
    currentId.value = id
    try {
      messages.value = await messageApi.list(id)
    } catch (error) {
      console.error('加载消息失败:', error)
      messages.value = []
    }
  }

  async function sendMessage(content: string) {
    if (!currentId.value) {
      await createConversation()
    }

    // 乐观更新：立即显示用户消息
    const tempUserMsg: Message = {
      id: Date.now(),
      role: 'user',
      content,
      created_at: new Date().toISOString(),
    }
    messages.value.push(tempUserMsg)

    // 创建ref包裹的AI消息，确保响应式
    const aiMsg = ref<Message>({
      id: Date.now() + 1,
      role: 'assistant',
      content: '',
      created_at: new Date().toISOString(),
    })
    streamingMsg.value = aiMsg.value
    messages.value.push(aiMsg.value)

    isLoading.value = true

    try {
      await messageApi.sendStream(
        currentId.value!,
        { content },
        // onToken
        (token: string) => {
          if (token.startsWith('__CORRECT__')) {
            aiMsg.value.content = token.slice(11)
          } else {
            aiMsg.value.content += token
          }
          triggerRef(aiMsg)
        },
        // onDone
        () => {
          isLoading.value = false
          streamingMsg.value = null
          const conv = conversations.value.find(c => c.id === currentId.value)
          if (conv && conv.title === '新对话') {
            conv.title = content.slice(0, 20) + (content.length > 20 ? '...' : '')
          }
        },
        // onError
        (err: string) => {
          aiMsg.value.content = `抱歉，发送消息失败：${err}`
          triggerRef(aiMsg)
          isLoading.value = false
          streamingMsg.value = null
        },
      )
    } catch (error: any) {
      aiMsg.value.content = '抱歉，发送消息失败。请检查网络连接或重试。'
      triggerRef(aiMsg)
      isLoading.value = false
      streamingMsg.value = null
    }
  }

  async function deleteConversation(id: number) {
    try {
      await conversationApi.delete(id)
      conversations.value = conversations.value.filter(c => c.id !== id)
      if (currentId.value === id) {
        currentId.value = null
        messages.value = []
      }
    } catch (error) {
      console.error('删除对话失败:', error)
    }
  }

  return {
    conversations,
    currentId,
    messages,
    isLoading,
    streamingMsg,
    loadConversations,
    createConversation,
    selectConversation,
    sendMessage,
    deleteConversation,
  }
})
