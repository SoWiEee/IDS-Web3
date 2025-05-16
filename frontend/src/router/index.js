import { createRouter, createWebHistory } from 'vue-router'
import MainPanel from '../components/MainPanel.vue'
import MaliciousPanel from '../components/MaliciousPanel.vue'

const routes = [
  { path: '/', name: 'Main', component: MainPanel },
  { path: '/malicious', name: 'MaliciousRecord', component: MaliciousPanel }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
