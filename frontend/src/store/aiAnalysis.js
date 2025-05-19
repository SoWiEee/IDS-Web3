import { defineStore } from 'pinia'
import axios from 'axios'

export const useAIAnalysisStore = defineStore('aiAnalysis', {
  state: () => ({
    drawer: false,
    loading: false,
    response: '',
    error: '',
  }),
  actions: {
    async trigger(logs) {
      this.drawer = true
      this.loading = true
      this.response = ''
      this.error = ''

      try {
        const res = await axios.post('http://localhost:5000/api/analyze', {
          logs: logs.slice(-30)
        }, { timeout: 20000 })
        this.response = res.data.result
      } catch (err) {
        this.error = err?.response?.data?.message || 'AI 分析失敗'
      } finally {
        this.loading = false
      }
    },
    close() {
      this.drawer = false
    }
  }
})
