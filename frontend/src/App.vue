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
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const logs = ref([])
const search = ref('')
const selectedEventTypes = ref([])

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

// filter
const filteredLogs = computed(() => {
  return logs.value.filter(log => {
    const matchesSearch = Object.values(log).some(val =>
      String(val).toLowerCase().includes(search.value.toLowerCase())
    )
    const matchesType =
      selectedEventTypes.value.length === 0 ||
      selectedEventTypes.value.includes(log.event_type)

    return matchesSearch && matchesType
  })
})

onMounted(() => {
  const fetchLogs = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/logs')
      logs.value = response.data
    } catch (error) {
      console.error('Error fetching logs:', error)
    }
  }
  fetchLogs()   // initial fetch
  setInterval(fetchLogs, 5000)  // fetch every 5 seconds
})

function formatTimestamp(ts) {
  const date = new Date(ts * 1000)
  return date.toLocaleString()
}
</script>