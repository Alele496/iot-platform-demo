// vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',  // 允许外部访问
    port: 3000
  },
  define: {
    __VUE_PROD_DEVTOOLS__: false,  // 关闭开发工具
    __VUE_OPTIONS_API__: true,      // 启用选项式API
    __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: 'false' // 根据需求设置 true/false	  
  }
})
