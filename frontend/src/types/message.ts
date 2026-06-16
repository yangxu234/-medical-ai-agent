export interface Message {
  id: number
  role: 'user' | 'assistant'
  content: string
  metadata_json?: Record<string, any>
  created_at?: string
}
