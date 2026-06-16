<template>
  <div class="settings-container min-h-screen bg-gray-50">
    <!-- 导航栏 -->
    <nav class="bg-white shadow-sm p-4">
      <div class="max-w-4xl mx-auto flex justify-between items-center">
        <router-link to="/" class="text-gray-600 hover:text-blue-600">
          ← 返回首页
        </router-link>
        <h1 class="text-xl font-semibold">模型配置</h1>
        <div></div>
      </div>
    </nav>

    <main class="max-w-2xl mx-auto p-6">
      <!-- 说明 -->
      <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
        <p class="text-blue-800 text-sm">
          💡 配置您自己的API Key，选择适合的AI模型。您的Key将加密存储，仅用于调用模型服务。
        </p>
      </div>

      <!-- 配置表单 -->
      <form @submit.prevent="saveConfig" class="bg-white rounded-lg shadow-md p-6 space-y-6">
        <!-- 提供商选择 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            模型提供商
          </label>
          <select
            v-model="config.provider"
            @change="onProviderChange"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option v-for="(provider, key) in providers" :key="key" :value="key">
              {{ provider.name }} - {{ provider.description }}
            </option>
          </select>
        </div>

        <!-- 模型选择 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            选择模型
          </label>
          <select
            v-model="config.model_name"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option v-for="model in currentModels" :key="model.id" :value="model.id">
              {{ model.name }} - {{ model.description }}
            </option>
          </select>
        </div>

        <!-- API Key -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            API Key
          </label>
          <input
            v-model="config.api_key"
            type="password"
            placeholder="输入您的API Key"
            required
            class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
          <p class="text-xs text-gray-500 mt-1">您的Key将加密存储，仅用于调用模型</p>
        </div>

        <!-- 自定义端点 -->
        <div v-if="currentProvider?.requires_base_url">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            自定义端点
          </label>
          <input
            v-model="config.base_url"
            placeholder="https://api.example.com/v1"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        <!-- Temperature -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            创造性 (Temperature): {{ config.temperature }}
          </label>
          <input
            v-model.number="config.temperature"
            type="range"
            min="0"
            max="2"
            step="0.1"
            class="w-full"
          />
          <div class="flex justify-between text-xs text-gray-500">
            <span>精确 (0)</span>
            <span>创造 (2)</span>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="flex gap-4">
          <button
            type="button"
            @click="testConnection"
            :disabled="isTesting || !config.api_key"
            class="flex-1 bg-gray-100 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-200 transition-colors disabled:opacity-50"
          >
            {{ isTesting ? '测试中...' : '测试连接' }}
          </button>
          <button
            type="submit"
            :disabled="!isConnected"
            class="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
          >
            保存配置
          </button>
        </div>

        <!-- 测试结果 -->
        <div
          v-if="testResult"
          :class="[
            'p-3 rounded-lg text-sm',
            testResult.success ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'
          ]"
        >
          <span v-if="testResult.success">✅</span>
          <span v-else>❌</span>
          {{ testResult.message }}
          <span v-if="testResult.latency_ms">
            ({{ testResult.latency_ms }}ms)
          </span>
        </div>
      </form>

      <!-- 当前状态 -->
      <div class="mt-6 bg-white rounded-lg shadow-md p-6">
        <h3 class="font-semibold mb-2">当前配置状态</h3>
        <p v-if="currentConfig.is_configured" class="text-green-600">
          ✅ 已配置模型: {{ currentConfig.provider }} / {{ currentConfig.model_name }}
        </p>
        <p v-else class="text-orange-600">
          ⚠️ 使用默认配置 (DeepSeek)
        </p>
        <button
          v-if="currentConfig.is_configured"
          @click="resetConfig"
          class="mt-2 text-sm text-red-600 hover:text-red-700"
        >
          重置为默认配置
        </button>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useSettingsStore } from '@/stores/settings'

const settingsStore = useSettingsStore()
const { providers, currentConfig } = storeToRefs(settingsStore)

const config = ref({
  provider: 'deepseek',
  model_name: 'deepseek-chat',
  api_key: '',
  base_url: '',
  temperature: 0.7,
  max_tokens: 2000,
})

const isTesting = ref(false)
const isConnected = ref(false)
const testResult = ref<{ success: boolean; message: string; latency_ms?: number } | null>(null)

const currentProvider = computed(() => {
  return providers.value[config.value.provider]
})

const currentModels = computed(() => {
  return currentProvider.value?.models || []
})

const onProviderChange = () => {
  config.value.model_name = currentModels.value[0]?.id || ''
  config.value.base_url = ''
  isConnected.value = false
  testResult.value = null
}

const testConnection = async () => {
  isTesting.value = true
  testResult.value = null

  try {
    testResult.value = await settingsStore.testConnection({
      provider: config.value.provider,
      model_name: config.value.model_name,
      api_key: config.value.api_key,
      base_url: config.value.base_url || undefined,
    })
    isConnected.value = testResult.value.success
  } catch (error) {
    testResult.value = { success: false, message: '测试请求失败' }
    isConnected.value = false
  }

  isTesting.value = false
}

const saveConfig = async () => {
  try {
    await settingsStore.saveConfig(config.value)
    alert('配置保存成功！')
  } catch (error) {
    alert('保存失败')
  }
}

const resetConfig = async () => {
  if (confirm('确定要重置为默认配置吗？')) {
    await settingsStore.resetConfig()
    config.value.api_key = ''
    isConnected.value = false
  }
}

onMounted(async () => {
  await settingsStore.loadProviders()
  await settingsStore.loadCurrentConfig()
})
</script>
