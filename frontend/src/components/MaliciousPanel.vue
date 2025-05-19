<template>
  <v-container>
    <v-card class="mt-5" outlined>
      <v-card-title class="text-error">
        <v-icon class="mr-2">mdi-virus</v-icon>
        Malicious Detection Panel
      </v-card-title>

      <!-- Filter Area -->
      <v-row class="pa-4" dense>
        <v-col cols="12" sm="6" md="4">
          <v-text-field
            v-model="search"
            label="模糊搜尋"
            prepend-icon="mdi-magnify"
            clearable
          />
        </v-col>

        <v-col cols="12" sm="6" md="4">
          <v-select
            v-model="selectedEventTypes"
            :items="eventTypeOptions"
            label="事件類型篩選"
            multiple
            clearable
          />
        </v-col>
      </v-row>

      <v-data-table :items="logs" :items-per-page="10" class="elevation-1">
        <template #headers>
          <tr>
            <th v-for="header in headers" :key="header.value" class="text-center text-primary" style="font-weight: bold; font-size: 18px;">
              {{ header.text }}
            </th>
          </tr>
        </template>

        <template #item="{ item }">
          <tr>
            <td class="text-center">{{ item.event_type }}</td>
            <td class="text-center">{{ item.image }}</td>
            <td class="text-center">{{ item.command_line }}</td>
            <td class="text-center">{{ item.detail }}</td>
            <td class="text-center">{{ item.pid }}</td>
            <td class="text-center">{{ item.user }}</td>
            <td class="text-center">{{ formatTimestamp(item.timestamp) }}</td>
          </tr>
        </template>
      </v-data-table>
    </v-card>

    <v-btn
      color="blue-accent-3"
      dark
      fab
      class="floating-ai-button"
      @click="triggerAI"
    >
      <v-icon>mdi-robot</v-icon>
    </v-btn>

    <v-navigation-drawer v-model="drawer" right temporary>
      <v-card>
        <v-card-title>🧠 AI 分析結果</v-card-title>
        <v-card-text>
          <div v-if="loading">
            <v-progress-circular indeterminate color="primary" />
            <p class="mt-2">AI 正在分析中，請稍候...</p>
          </div>
          <div v-else-if="response">
            <p style="white-space: pre-wrap;">{{ response }}</p>
          </div>
          <div v-else-if="error">
            <v-alert type="error">{{ error }}</v-alert>
          </div>
        </v-card-text>
      </v-card>
    </v-navigation-drawer>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const logs = ref([])

const headers = [
  { text: 'Technique', value: 'event_type', sortable: true },
  { text: 'Process Image', value: 'image', sortable: true },
  { text: 'Command Line', value: 'command_line', sortable: true },
  { text: 'Description', value: 'detail', sortable: true },
  { text: 'PID', value: 'pid', sortable: true },
  { text: 'User', value: 'user', sortable: true },
  { text: 'Timestamp', value: 'timestamp', sortable: true },
]

const drawer = ref(false)
const response = ref('')
const loading = ref(false)
const error = ref('')

onMounted(() => {
  const fetchLogs = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/malicious')
      logs.value = response.data
    } catch (e) {
      console.error('Error fetching logs:', e)
    }
  }
  fetchLogs()
  setInterval(fetchLogs, 2000)
})

function formatTimestamp(ts) {
  const date = new Date(ts * 1000)
  return date.toLocaleString()
}

const triggerAI = async () => {
  drawer.value = true
  response.value = ''
  loading.value = true
  error.value = ''

  try {
    const recentLogs = logs.value.slice(-30)
    const res = await axios.post('http://localhost:5000/api/analyze', {
      logs: recentLogs
    }, { timeout: 20000 })
    response.value = res.data.result
  } catch (err) {
    error.value = err?.response?.data?.message || 'AI 分析失敗'
  } finally {
    loading.value = false
  }
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