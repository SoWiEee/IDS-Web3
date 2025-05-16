import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'vuetify/styles'
import vuetify from './vuetify'
import '@mdi/font/css/materialdesignicons.css'


createApp(App).use(vuetify).use(router).mount('#app')