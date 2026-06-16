import api from './client'
import { useAuthStore } from '@/stores/auth'
import type { Conversation } from '@/types/conversation'
import type { Message } from '@/types/message'

export const conversationApi = {
  async list(): Promise<Conversation[]> {
    const response = await api.get('/conversations')
    return response.data
  },

  async create(data: { title?: string }): Promise<Conversation> {
    const response = await api.post('/conversations', data)
    return response.data
  },

  async get(id: number): Promise<Conversation> {
    const response = await api.get(`/conversations/${id}`)
    return response.data
  },

  async delete(id: number): Promise<void> {
    await api.delete(`/conversations/${id}`)
  },
}

export const messageApi = {
  async list(conversationId: number): Promise<Message[]> {
    const response = await api.get(`/conversations/${conversationId}/messages`)
    return response.data
  },

  async send(conversationId: number, data: { content: string }): Promise<Message> {
    const response = await api.post(`/conversations/${conversationId}/messages`, data)
    return response.data
  },

  async sendStream(
    conversationId: number,
    data: { content: string },
    onToken: (token: string) => void,
    onDone: () => void,
    onError: (err: string) => void,
  ) {
    const authStore = useAuthStore()
    const response = await fetch(`/api/conversations/${conversationId}/messages/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authStore.token}`,
      },
      body: JSON.stringify(data),
    })

    if (!response.ok) {
      onError(`HTTP ${response.status}`)
      return
    }

    const reader = response.body!.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop() || ''

      for (const line of lines) {
        if (!line.startsWith('data: ')) continue
        try {
          const payload = JSON.parse(line.slice(6))
          if (payload.type === 'content') {
            onToken(payload.text)
          } else if (payload.type === 'correct') {
            onToken('__CORRECT__' + payload.text)
          } else if (payload.type === 'done') {
            onDone()
            return
          }
        } catch {
          // ignore parse errors
        }
      }
    }
    onDone()
  },
}
