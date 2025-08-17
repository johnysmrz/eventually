import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'
import { join } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  server: {
    proxy: {
      // Proxy /api/* to http://localhost:8080/public/api/*
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: false,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, '/public')
      }
    }
  }
})
