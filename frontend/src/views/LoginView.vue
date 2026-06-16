<template>
  <div class="min-h-screen bg-gradient-to-b from-blue-50 to-white flex items-center justify-center px-4">
    <div class="w-full max-w-md">
      <!-- Logo -->
      <div class="text-center mb-8">
        <router-link to="/" class="inline-flex items-center gap-2">
          <span class="text-3xl">🩺</span>
          <span class="text-2xl font-bold text-gray-800">医疗健康咨询助手</span>
        </router-link>
      </div>

      <!-- 登录表单 -->
      <div class="bg-white rounded-xl shadow-lg p-8">
        <h2 class="text-2xl font-bold text-gray-800 mb-6 text-center">登录</h2>

        <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4 text-sm">
          {{ error }}
        </div>

        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">邮箱</label>
            <input
              v-model="form.email"
              type="email"
              required
              placeholder="请输入邮箱"
              class="w-full border border-gray-300 rounded-lg px-4 py-2.5 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">密码</label>
            <input
              v-model="form.password"
              type="password"
              required
              placeholder="请输入密码"
              class="w-full border border-gray-300 rounded-lg px-4 py-2.5 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
            />
          </div>

          <button
            type="submit"
            :disabled="isLoading"
            class="w-full bg-blue-600 text-white py-2.5 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium"
          >
            {{ isLoading ? '登录中...' : '登录' }}
          </button>
        </form>

        <p class="text-center text-gray-600 mt-6 text-sm">
          还没有账号？
          <router-link to="/register" class="text-blue-600 hover:text-blue-700 font-medium">
            立即注册
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  email: '',
  password: '',
})

const isLoading = ref(false)
const error = ref('')

const handleLogin = async () => {
  isLoading.value = true
  error.value = ''

  try {
    await authStore.login(form.value.email, form.value.password)
    router.push('/consultation')
  } catch (err: any) {
    error.value = err.response?.data?.detail || '登录失败，请检查邮箱和密码'
  } finally {
    isLoading.value = false
  }
}
</script>
