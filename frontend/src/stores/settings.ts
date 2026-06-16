import { defineStore } from 'pinia'
import { ref } from 'vue'
import { modelConfigApi } from '@/api/settings'
import type { ModelConfigResponse, TestConnectionResult } from '@/types/model'

export const useSettingsStore = defineStore('settings', () => {
  const providers = ref<Record<string, any>>({})
  const currentConfig = ref<ModelConfigResponse>({
    provider: 'deepseek-v4-pro',
    model_name: 'deepseek-chat',
    base_url: null,
    temperature: 0.7,
    max_tokens: 2000,
    is_configured: false,
  })

  async function loadProviders() {
    try {
      providers.value = await modelConfigApi.getProviders()
    } catch (error) {
      console.error('加载提供商失败:', error)
    }
  }

  async function loadCurrentConfig() {
    try {
      currentConfig.value = await modelConfigApi.getMyConfig()
    } catch (error) {
      console.error('加载配置失败:', error)
    }
  }

  async function saveConfig(config: {
    provider: string
    model_name: string
    api_key: string
    base_url?: string
    temperature: number
    max_tokens: number
  }) {
    await modelConfigApi.save(config)
    await loadCurrentConfig()
  }

  async function testConnection(config: {
    provider: string
    model_name: string
    api_key: string
    base_url?: string
  }): Promise<TestConnectionResult> {
    return await modelConfigApi.testConnection(config)
  }

  async function resetConfig() {
    await modelConfigApi.reset()
    await loadCurrentConfig()
  }

  return {
    providers,
    currentConfig,
    loadProviders,
    loadCurrentConfig,
    saveConfig,
    testConnection,
    resetConfig,
  }
})
