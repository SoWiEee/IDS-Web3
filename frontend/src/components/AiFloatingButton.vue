<template>
  <div>
    <!-- 懸浮 AI 按鈕 -->
    <button
      class="fixed bottom-4 left-4 z-50 bg-blue-600 text-white p-4 rounded-full shadow-lg hover:bg-blue-700 transition"
      @click="analyzeLogs"
    >
      🤖 AI 助手
    </button>

    <!-- 側邊 AI 回應面板 -->
    <transition name="slide">
      <div
        v-if="sidebarOpen"
        class="fixed top-0 left-0 h-full w-80 bg-white shadow-lg z-40 p-4 overflow-y-auto"
      >
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold">AI 安全分析</h2>
          <button @click="sidebarOpen = false">❌</button>
        </div>

        <div v-if="loading" class="text-gray-500">分析中，請稍候...</div>
        <div v-else-if="error" class="text-red-500">發生錯誤：{{ error }}</div>
        <div v-else-if="response" class="whitespace-pre-line">{{ response }}</div>
        <div v-else class="text-gray-400">點擊左下角 AI 助手進行安全分析</div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const sidebarOpen = ref(false)
const loading = ref(false)
const response = ref('')
const error = ref('')

const analyzeLogs = async () => {
  sidebarOpen.value = true
  loading.value = true
  error.value = ''
  response.value = ''

  try {
    const res = await axios.get('/api/analyze') // 後端 API endpoint
    response.value = res.data.result
  } catch (err) {
    error.value = err?.response?.data?.message || '無法連接 AI 分析服務'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}
.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
}
</style>
