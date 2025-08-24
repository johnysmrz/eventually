import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from "path"

console.info(path.resolve(__dirname, 'src/components/ui'))

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: [
      { find: '@ui', replacement: path.resolve(__dirname, 'src/components/ui') },
      { find: '@', replacement: path.resolve(__dirname, 'src') }
    ]
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: false,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, '/public')
      }
    }
  }
})
