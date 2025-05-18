<template>
  <v-app>
    <v-main>
      <v-container>
        <v-card class="mt-5 bg-surface" outlined>
          <v-card-title class="text-primary">
            <v-icon class="mr-2">mdi-shield-alert</v-icon>
            Security Event Logs
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

          <!-- Table -->
          <v-data-table
            :headers="headers"
            :items="filteredLogs"
            class="elevation-1"
            :search="''"
            :items-per-page="10"
          >
            <template #item.timestamp="{ item }">
              <span class="text-secondary">{{ formatTimestamp(item.timestamp) }}</span>
            </template>
            <template #item.event_type="{ item }">
              <span class="text-primary font-weight-bold">{{ item.event_type }}</span>
            </template>
          </v-data-table>
        </v-card>
      </v-container>

      <!-- 🔵 AI 懸浮按鈕（固定在右上角） -->
      <v-btn
        color="deep-purple accent-4"
        dark
        fab
        class="floating-ai-button"
        @click="triggerAI"
      >
        <v-icon>mdi-robot</v-icon>
      </v-btn>

      <!-- 🔵 側邊抽屜 -->
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
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import Fuse from 'fuse.js'

const logs = ref([])
const search = ref('')
const selectedEventTypes = ref([])
const filteredLogs = ref([])
const drawer = ref(false)
const response = ref('')
const loading = ref(false)
const error = ref('')

const headers = [
  { text: 'Event Type', value: 'event_type', sortable: true },
  { text: 'Image', value: 'image', sortable: true },
  { text: 'Command Line', value: 'command_line', sortable: true },
  { text: 'User', value: 'user', sortable: true },
  { text: 'Integrity Level', value: 'integrity_level', sortable: true },
  { text: 'PID', value: 'pid', sortable: true },
  { text: 'Timestamp', value: 'timestamp', sortable: true },
]

const eventTypeOptions = computed(() => {
  const set = new Set(logs.value.map(l => l.event_type))
  return Array.from(set)
})

let fuse = null

const updateFilteredLogs = () => {
  let temp = logs.value

  if (selectedEventTypes.value.length > 0) {
    temp = temp.filter(log => selectedEventTypes.value.includes(log.event_type))
  }

  if (search.value.trim() !== '' && fuse) {
    const fuseResults = fuse.search(search.value.trim())
    temp = fuseResults.map(result => result.item)
  }

  filteredLogs.value = temp
}

watch(logs, () => {
  fuse = new Fuse(logs.value, {
    keys: ['event_type', 'image', 'command_line', 'user', 'integrity_level', 'pid', 'timestamp'],
    threshold: 0.6,
  })
  updateFilteredLogs()
})

watch([search, selectedEventTypes], updateFilteredLogs)

onMounted(() => {
  const fetchLogs = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/logs')
      logs.value = response.data
    } catch (error) {
      console.error('Error fetching logs:', error)
    }
  }
  fetchLogs()
  setInterval(fetchLogs, 3000)
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
    const res = await axios.post('http://localhost:5000/api/analyze', {
      logs: filteredLogs.value
    })
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
