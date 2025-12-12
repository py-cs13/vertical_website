import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, './src')
    }
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // 后端实际运行在8000端口
        changeOrigin: true
      },
      '/static': {
        target: 'http://localhost:8000', // 后端静态资源代理
        changeOrigin: true
      }
    }
  }
})
