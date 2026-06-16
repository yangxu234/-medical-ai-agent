import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'
import type { User } from '@/types/user'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<User | null>(null)

  const isAuthenticated = computed(() => !!token.value)

  async function login(email: string, password: string) {
    const result = await authApi.login(email, password)
    token.value = result.access_token
    localStorage.setItem('token', result.access_token)
    await loadUser()
  }

  async function register(email: string, name: string, password: string) {
    await authApi.register({ email, name, password })
  }

  async function loadUser() {
    if (!token.value) return
    try {
      user.value = await authApi.getMe()
    } catch {
      logout()
    }
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
  }

  // 初始化时加载用户信息
  if (token.value) {
    loadUser()
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    loadUser,
    logout,
  }
})
