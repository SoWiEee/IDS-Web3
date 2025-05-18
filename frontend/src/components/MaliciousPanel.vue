<template>
  <v-container>
    <v-card class="mt-5" outlined>
      <v-card-title class="text-error">
        <v-icon class="mr-2">mdi-virus</v-icon>
        Malicious Detection Panel
      </v-card-title>
      <v-data-table
        :headers="headers"
        :items="logs"
        class="elevation-1"
      />
    </v-card>
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

onMounted(() => {
  const fetchLogs = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/malicious')
      logs.value = response.data
    } catch (e) {
      console.error('Error fetching logs:', e)
    }
  }
  fetchLogs()   // initial fetch
  setInterval(fetchLogs, 3000)  // fetch every 3 seconds
})

</script>