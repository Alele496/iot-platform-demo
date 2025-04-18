import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';
import { Card, Row, Col, Statistic, Alert } from 'antd';
import { ThermometerOutlined, WaterOutlined } from '@ant-design/icons';
import './App.css';

const socket = io('http://localhost:5000');

function App() {
  const [sensorData, setSensorData] = useState({
    temp: null,
    humi: null,
    device_id: null,
    timestamp: null
  });
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const [error, setError] = useState(null);

  useEffect(() => {
    socket.on('connect', () => {
      setConnectionStatus('connected');
      setError(null);
    });

    socket.on('disconnect', () => {
      setConnectionStatus('disconnected');
    });

    socket.on('connection_response', (data) => {
      console.log('Connection response:', data);
    });

    socket.on('sensor_data', (data) => {
      setSensorData(data);
    });

    socket.on('error', (error) => {
      setError(error.message);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  return (
    <div className="app-container">
      <h1>物联网温湿度监控系统</h1>
      
      {error && (
        <Alert
          message="连接错误"
          description={error}
          type="error"
          showIcon
          style={{ marginBottom: '20px' }}
        />
      )}

      <Row gutter={[16, 16]}>
        <Col span={12}>
          <Card title="温度数据">
            <Statistic
              title="当前温度"
              value={sensorData.temp}
              precision={1}
              suffix="°C"
              prefix={<ThermometerOutlined />}
            />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="湿度数据">
            <Statistic
              title="当前湿度"
              value={sensorData.humi}
              precision={1}
              suffix="%"
              prefix={<WaterOutlined />}
            />
          </Card>
        </Col>
      </Row>

      <Card title="设备信息" style={{ marginTop: '20px' }}>
        <p>设备ID: {sensorData.device_id || '未连接'}</p>
        <p>最后更新时间: {sensorData.timestamp ? new Date(sensorData.timestamp).toLocaleString() : '未连接'}</p>
        <p>连接状态: <span className={connectionStatus}>{connectionStatus === 'connected' ? '已连接' : '未连接'}</span></p>
      </Card>
    </div>
  );
}

export default App; 