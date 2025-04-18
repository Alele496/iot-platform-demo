<template>
  <el-card class="dashboard-card">
    <template #header>
      <div class="card-header">
        <el-icon><Opportunity /></el-icon>
        <span>实时温湿度监控</span>
      </div>
    </template>
    <div class="sensor-data">
      <el-statistic :value="temperature" suffix="°C" title="温度" />
      <el-statistic :value="humi" suffix="%" title="湿度" />
    </div>
  </el-card>
</template>

<script>
import { io } from 'socket.io-client';

//const isHttps = window.location.protocol === 'https:';
//const socketUrl = isHttps 


export default {
  data() {
    return {
      temperature: 0,
      humi: 0,
      socket: null
    };
  },
  mounted() {

    //const socketUrl = process.env.VITE_WS_URL || 'http://127.0.0.1:5000';
    //const socketUrl = import.meta.env.VITE_WS_URL || 'http://127.0.0.1:5000';
    const socketUrl = 'http://localhost:5000'; // 动态获取 WebSocket URL
    //const socketUrl = 'http://172.18.0.5:5000/socket.io';

    this.socket = io(socketUrl, {
      transports: ['websocket'],
      path: '/socket.io',
      //query: { EIO: "4" },
      reconnectionAttempts: 5,
      reconnection: true, // 启用重连
      timeout: 20000, // 设置超时时间为 20 秒
      reconnectionDelay: 5000, // 设置重试延迟
      secure: window.location.protocol === 'https:',
      //upgrade: false, 
      withCredentials: true,   //允许跨域
      rejectUnauthorized: false
  });


    this.socket.on('connect', () => {
        console.log('Socket.IO 已连接');
    });

    this.socket.on('update', (data) => {
    this.temperature = data.temp;
    this.humi = data.humi;
    console.log('收到的数据:', data);
    });

    this.socket.on('connect_error', (err) => {
      console.error('Socket.IO 连接失败:', err);
    });

    // 检查 WebSocket 是否断开
    this.socket.on('disconnect', () => {
      console.warn('⚠️ WebSocket 已断开');
    });
  },
  beforeDestroy() {
    // 组件销毁前断开 Socket.IO 连接
    if (this.socket) {
      this.socket.disconnect();
    }
  }
  
}

</script>

<style scoped>
.sensor-data {
  display: flex;
  gap: 20px;
}
</style>
