<template>
  <v-btn color="blue-accent-3" dark fab class="floating-ai-button" @click="handleClick">
    <v-icon>mdi-robot</v-icon>
  </v-btn>
</template>

<script setup>
import { useAIAnalysisStore } from '@/store/aiAnalysis'
import { toRef } from 'vue'

const props = defineProps({ logs: Array })
const logs = toRef(props, 'logs')

const aiStore = useAIAnalysisStore()

const handleClick = () => {
  aiStore.trigger(logs.value)
}
</script>

<style scoped>
.floating-ai-button {
  position: fixed;
  top: 80px;
  right: 30px;
  z-index: 9999;
}
</style>