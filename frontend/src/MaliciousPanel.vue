<template>
    <v-container>
        <v-card class="mt-5 bg-surface" outlined>
            <v-card-title class="text-red-darken-2">
                <v-icon class="mr-2">mdi-bug</v-icon>
                    Malicious Detection Panel
            </v-card-title>
  
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
                        v-model="selectedTags"
                        :items="tagOptions"
                        label="惡意類型篩選"
                        multiple
                        clearable
                    />
                </v-col>
            </v-row>
  
            <v-data-table
                :headers="headers"
                :items="filteredData"
                :items-per-page="10"
                class="elevation-1"
            >
                <template #item.timestamp="{ item }">
                    <span class="text-secondary">{{ formatTimestamp(item.timestamp) }}</span>
                </template>
                <template #item.tag="{ item }">
                    <span class="text-red font-weight-bold">{{ item.tag }}</span>
                    </template>
            </v-data-table>
        </v-card>
    </v-container>
</template>
  
<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import Fuse from 'fuse.js'
  
const logs = ref([])
const search = ref('')
const selectedTags = ref([])
const filteredData = ref([])
  
const headers = [
    { text: '行為類型', value: 'tag', sortable: true },
    { text: '描述', value: 'description', sortable: true },
    { text: '目標處理程序', value: 'target_pid', sortable: true },
    { text: '來源處理程序', value: 'source_pid', sortable: true },
    { text: '時間戳記', value: 'timestamp', sortable: true },
]
  
const tagOptions = computed(() => {
    const set = new Set(logs.value.map(l => l.tag))
    return Array.from(set)
})

let fuse = null

const updateFiltered = () => {
    let temp = logs.value
  
    if (selectedTags.value.length > 0) {
      temp = temp.filter(log => selectedTags.value.includes(log.tag))
    }
  
    if (search.value.trim() !== '' && fuse) {
      const fuseResults = fuse.search(search.value.trim())
      temp = fuseResults.map(result => result.item)
    }
  
    filteredData.value = temp
}
  
watch(logs, () => {
    fuse = new Fuse(logs.value, {
        keys: ['tag', 'description', 'target_pid', 'source_pid'],
        threshold: 0.4,
    })
    updateFiltered()
})
  
watch([search, selectedTags], updateFiltered)
  
onMounted(() => {
    const fetchLogs = async () => {
        try {
            const response = await axios.get('http://localhost:5000/api/malicious')
            logs.value = response.data
        } catch (err) {
            console.error('Error fetching malicious logs:', err)
        }
    }
  
    fetchLogs()
    setInterval(fetchLogs, 5000)
})
  
function formatTimestamp(ts) {
    const date = new Date(ts * 1000)
    return date.toLocaleString()
}

</script>  