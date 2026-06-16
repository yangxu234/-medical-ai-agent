<template>
  <div class="home-container min-h-screen bg-gradient-to-b from-blue-50 to-white">
    <!-- 导航栏 -->
    <nav class="p-4 flex justify-between items-center max-w-6xl mx-auto">
      <div class="flex items-center gap-2">
        <span class="text-2xl">🩺</span>
        <span class="text-xl font-bold text-gray-800">医疗健康咨询助手</span>
      </div>
      <div class="flex gap-4 items-center">
        <router-link to="/settings" class="text-gray-600 hover:text-blue-600">
          模型配置
        </router-link>
        <template v-if="isAuthenticated">
          <span class="text-gray-600 text-sm">{{ user?.name }}</span>
          <button
            @click="handleLogout"
            class="text-gray-600 hover:text-red-600 text-sm"
          >
            退出
          </button>
        </template>
        <template v-else>
          <router-link to="/login" class="text-gray-600 hover:text-blue-600">
            登录
          </router-link>
          <router-link to="/register" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm">
            注册
          </router-link>
        </template>
      </div>
    </nav>

    <!-- 主内容 -->
    <main class="max-w-4xl mx-auto px-4 py-16">
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-800 mb-4">
          AI驱动的健康咨询平台
        </h1>
        <p class="text-xl text-gray-600">
          描述您的症状，获取专业的健康建议和就医指导
        </p>
      </div>

      <!-- 功能卡片 -->
      <div class="grid md:grid-cols-3 gap-6 mb-12">
        <div class="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition-shadow">
          <div class="text-4xl mb-4">🔍</div>
          <h3 class="text-lg font-semibold mb-2">症状分析</h3>
          <p class="text-gray-600">分析您的症状，提供专业的健康建议和可能的原因分析</p>
        </div>
        <div class="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition-shadow">
          <div class="text-4xl mb-4">📋</div>
          <h3 class="text-lg font-semibold mb-2">检查建议</h3>
          <p class="text-gray-600">推荐合适的检查项目和就医科室，避免盲目就医</p>
        </div>
        <div class="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition-shadow">
          <div class="text-4xl mb-4">🏥</div>
          <h3 class="text-lg font-semibold mb-2">就医指导</h3>
          <p class="text-gray-600">引导您正确就医，提供专业的医疗咨询建议</p>
        </div>
      </div>

      <!-- 开始按钮 -->
      <div class="text-center">
        <button
          @click="startConsultation"
          class="bg-blue-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-blue-700 transition-colors shadow-lg"
        >
          开始健康咨询
        </button>
      </div>

      <!-- 免责声明 -->
      <div class="mt-12 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
        <p class="text-yellow-800 text-sm text-center">
          ⚠️ <strong>免责声明</strong>：本平台提供的信息仅供参考，不构成医疗诊断或治疗建议。
          如有健康问题，请及时就医并咨询专业医疗人员。紧急情况请立即拨打急救电话。
        </p>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const { isAuthenticated, user } = storeToRefs(authStore)

const startConsultation = () => {
  if (isAuthenticated.value) {
    router.push('/consultation')
  } else {
    router.push('/login')
  }
}

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}
</script>
