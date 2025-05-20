<template>
  <div class="ai-rgb-wrapper" @click="handleClick">
    <v-btn icon class="floating-ai-button" color="blue-accent-3">
      <v-icon>mdi-robot</v-icon>
    </v-btn>
  </div>
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
.ai-rgb-wrapper {
  position: fixed;
  top: 100px;
  right: 40px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
}

.floating-ai-button {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: #3b82f6;
  color: white;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  transition: transform 0.2s ease;
}

.floating-ai-button:hover {
  background-color: #2563eb;
  transform: scale(1.05);
}

.ai-rgb-wrapper::before {
  content: "";
  position: absolute;
  top: -6px;
  left: -6px;
  right: -6px;
  bottom: -6px;
  z-index: -1;
  border-radius: 50%;
  background: conic-gradient(
    red,
    orange,
    yellow,
    green,
    cyan,
    blue,
    violet,
    red
  );
  animation: rotate-rgb 0.7s linear infinite;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.ai-rgb-wrapper:hover::before {
  opacity: 1;
}

@keyframes rotate-rgb {
  0% {
    transform: rotate(0turn);
  }
  100% {
    transform: rotate(1turn);
  }
}
</style>