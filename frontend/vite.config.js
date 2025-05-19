import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'
import path from 'path'

export default defineConfig({
  root: __dirname,  // frontend = root
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),  // @ = src
    },
  },
  plugins: [
    vue(),
    vuetify(),
  ],
})
