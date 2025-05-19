<template>
  <v-navigation-drawer v-model="ai.drawer" right temporary>
    <v-card>
      <v-card-title>🧠 AI 分析結果</v-card-title>
      <v-card-text>
        <div v-if="ai.loading">
          <v-progress-circular indeterminate color="primary" />
          <p class="mt-2">AI 正在分析中，請稍候...</p>
        </div>
        <div v-else-if="ai.response">
          <p style="white-space: pre-wrap;">{{ ai.response }}</p>
        </div>
        <div v-else-if="ai.error">
          <v-alert type="error">{{ ai.error }}</v-alert>
        </div>
      </v-card-text>
    </v-card>
  </v-navigation-drawer>
</template>

<script setup>
import { useAIAnalysisStore } from '@/store/aiAnalysis'

const ai = useAIAnalysisStore()
</script>