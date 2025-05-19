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
            :items-per-page="10"
            class="elevation-1"
            item-value="id"
          >
            <!-- self-defined header, reserve sorting -->
            <template v-for="header in headers" #[`header.${header.value}`]="{ column }" :key="header.value">
              <span class="text-center text-primary" style="font-weight: bold; font-size: 18px;">
                {{ column.text }}
              </span>
            </template>

            <!-- data table -->
            <template #item="{ item }">
              <tr>
                <td class="text-center">{{ item.event_type }}</td>
                <td class="text-center">{{ item.image }}</td>
                <td class="text-center">{{ item.command_line }}</td>
                <td class="text-center">{{ item.user }}</td>
                <td class="text-center">{{ item.integrity_level }}</td>
                <td class="text-center">{{ item.pid }}</td>
                <td class="text-center">{{ formatTimestamp(item.timestamp) }}</td>
              </tr>
            </template>
          </v-data-table>
        </v-card>
      </v-container>

      <AiButton :logs="logs" />
      <AiDrawer />

    </v-main>
  </v-app>
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
const filteredLogs = ref([])

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
  setInterval(fetchLogs, 2000)
})

function formatTimestamp(ts) {
  const date = new Date(ts * 1000)
  return date.toLocaleString()
}
</script>

<style scoped>
</style>