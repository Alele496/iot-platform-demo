<!-- frontend/src/views/Dashboard.vue -->
<template>
  <el-card>
    <el-statistic :value="temperature" suffix="℃" title="当前温度" />
    <el-statistic :value="humidity" suffix="%" title="当前湿度" />
  </el-card>
</template>

<script>
import { io } from 'socket.io-client';

export default {
  data() {
    return {
      temperature: 0,
      humidity: 0,
      socket: null
    }
  },
  mounted() {
    // 自动适配本地或生产环境，且路径与后端一致
    const socketUrl = 'http://localhost:5000';
    this.socket = io(socketUrl, {
      transports: ['websocket'],
      path: '/socket.io',
      reconnection: true,
      reconnectionAttempts: 5,
      timeout: 20000,
      withCredentials: true
    });
    this.socket.on('connect', () => {
      console.log('Socket.IO 已连接');
    });
    this.socket.on('update', (data) => {
      this.temperature = data.temp;
      this.humidity = data.humi;
      console.log('收到的数据:', data);
    });
    this.socket.on('connect_error', (err) => {
      console.error('Socket.IO 连接失败:', err);
    });
    this.socket.on('disconnect', () => {
      console.warn('⚠️ WebSocket 已断开');
    });
  },
  beforeDestroy() {
    if (this.socket) {
      this.socket.disconnect();
    }
  }
}
</script>
