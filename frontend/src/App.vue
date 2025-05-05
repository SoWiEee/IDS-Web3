<template>
  <v-app>
    <v-main>
      <v-container>
        <v-card class="mt-5" outlined>
          <v-card-title>
            <v-icon class="mr-2">mdi-shield-alert</v-icon>
            Security Event Logs
          </v-card-title>
          <v-data-table
            :headers="headers"
            :items="logs"
            class="elevation-1"
          >
            <template #item.timestamp="{ item }">
              {{ formatTimestamp(item.timestamp) }}
            </template>
          </v-data-table>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const logs = ref([])

const headers = [
  { text: 'Event Type', value: 'event_type' },
  { text: 'Timestamp', value: 'timestamp' },
  { text: 'Image Path', value: 'image' },
  { text: 'Command Line', value: 'command_line' },
  { text: 'PID', value: 'pid' },
  { text: 'User', value: 'user' },
  { text: 'Integrity Level', value: 'integrity_level' },
]

const fetchLogs = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/logs')
    logs.value = response.data
  } catch (error) {
    console.error('[X] Error fetching logs:', error)
  }
}

const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp * 1000)
  return date.toLocaleString()
}

onMounted(() => {
  fetchLogs()
  setInterval(fetchLogs, 5000)  // update per 5 secs
});

</script>