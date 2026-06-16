import api from './client'
import type { ModelConfig, ModelConfigResponse, TestConnectionResult } from '@/types/model'

export const modelConfigApi = {
  async getProviders(): Promise<Record<string, any>> {
    const response = await api.get('/settings/providers')
    return response.data
  },

  async getMyConfig(): Promise<ModelConfigResponse> {
    const response = await api.get('/settings/model')
    return response.data
  },

  async save(config: ModelConfig): Promise<void> {
    await api.post('/settings/model', config)
  },

  async testConnection(config: {
    provider: string
    model_name: string
    api_key: string
    base_url?: string
  }): Promise<TestConnectionResult> {
    const response = await api.post('/settings/test-connection', config)
    return response.data
  },

  async reset(): Promise<void> {
    await api.delete('/settings/model')
  },
}
