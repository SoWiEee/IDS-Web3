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

      <v-data-table
        :headers="headers"
        :items="filteredLogs"
        :items-per-page="10"
        class="elevation-1"
        item-value="id"
      >
        <template v-for="header in headers" #[`header.${header.value}`]="{ column }" :key="header.value">
          <span class="text-center text-primary" style="font-weight: bold; font-size: 18px;">
            {{ column.text }}
          </span>
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

    <AiButton :logs="logs" />
    <AiDrawer />
  </v-container>
</template>

<script setup>
import AiButton from '@/components/AiButton.vue'
import AiDrawer from '@/components/AiDrawer.vue'
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import Fuse from 'fuse.js'

const logs = ref([])
const search = ref('')
const selectedEventTypes = ref([])

const eventTypeOptions = ['Logon', 'DLL Injection', 'Registry']

const headers = [
  { text: 'Technique', value: 'event_type', sortable: true },
  { text: 'Process Image', value: 'image', sortable: true },
  { text: 'Command Line', value: 'command_line', sortable: true },
  { text: 'Description', value: 'detail', sortable: true },
  { text: 'PID', value: 'pid', sortable: true },
  { text: 'User', value: 'user', sortable: true },
  { text: 'Timestamp', value: 'timestamp', sortable: true },
]

const fuseOptions = {
  keys: ['event_type', 'image', 'command_line', 'detail', 'user'],
  threshold: 0.3,
}
let fuse = null

watch(logs, (newLogs) => {
  fuse = new Fuse(newLogs, fuseOptions)
})

const filteredLogs = computed(() => {
  let result = logs.value

  if (search.value && fuse) {
    result = fuse.search(search.value).map(res => res.item)
  }

  if (selectedEventTypes.value.length > 0) {
    result = result.filter(item => selectedEventTypes.value.includes(item.event_type))
  }

  return result
})

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
</script>

<style scoped>
</style>
