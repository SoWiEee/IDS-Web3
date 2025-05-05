<template>
  <v-app>
    <v-main>
      <v-container>
        <v-card class="mt-5 bg-surface" outlined>
          <v-card-title class="text-primary">
            <v-icon class="mr-2">mdi-shield-alert</v-icon>
            Security Event Logs
          </v-card-title>
          <v-data-table
            :headers="headers"
            :items="logs"
            class="elevation-1 border border-primary"
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

<script>
import { ref, onMounted } from "vue";

export default {
  setup() {
    const headers = ref([
      { text: 'Event Type', align: 'start', key: 'event_type' },
      { text: 'Image', align: 'start', key: 'image' },
      { text: 'Command Line', align: 'start', key: 'command_line' },
      { text: 'PID', align: 'start', key: 'pid' },
      { text: 'User', align: 'start', key: 'user' },
      { text: 'Integrity Level', align: 'start', key: 'integrity_level' },
      { text: 'Timestamp', align: 'start', key: 'timestamp' }
    ]);
    
    const logs = ref([]);

    const formatTimestamp = (timestamp) => {
      const date = new Date(timestamp * 1000);
      return date.toLocaleString();
    };

    const fetchLogs = async () => {
      try {
        const response = await fetch("http://localhost:5000/api/logs");
        const data = await response.json();
        logs.value = data;
      } catch (error) {
        console.error("Error fetching logs:", error);
      }
    };

    onMounted(() => {
      setInterval(() => {
        fetchLogs();
      }, 5000);
    });

    return {
      headers,
      logs,
      formatTimestamp,
    };
  }
};
</script>