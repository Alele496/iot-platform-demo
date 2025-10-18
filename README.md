# IoT Demo Platform (ESP32 + MQTT + TDengine + Flask + Vue)

简体中文 | [English](#english-readme)

---

## 项目简介

本项目为一个简化版的物联网云平台示例，演示了如何通过 ESP32 采集 DHT11 温湿度数据，经 MQTT 传输到后端，存储于 TDengine 数据库，并通过 Flask-SocketIO 实时推送到前端 Vue 可视化界面。

### 技术栈
- 硬件：ESP32 + DHT11
- 通信：MQTT（EMQX）
- 数据库：TDengine
- 后端：Flask + Flask-SocketIO
- 前端：Vue 3 + Vite
- 部署：Docker Compose

---

## 快速开始

### 1. 克隆代码
```bash
git clone https://github.com/Alele496/iot-platform-demo.git
cd iot-demo-docker
```

### 2. 配置环境变量
- 复制 `.env.example` 为 `.env`，填写自己的配置。
- 复制 `backend/config.example.py` 为 `backend/config.py`，填写自己的配置。

### 3. 启动服务
```bash
docker-compose up -d
```

- 后端 Flask 默认监听 5000 端口
- 前端 Vue 默认监听 3000 端口
- EMQX MQTT Broker 默认 1883 端口
- TDengine REST API 默认 6041 端口

### 4. 访问前端
浏览器访问：http://localhost:3000

---

## 目录结构
```
├── backend/            # Flask 后端
├── frontend/           # Vue 前端
├── esp32s3/            # ESP32 设备端代码
├── emqx/               # MQTT Broker 配置
├── tdengine/           # TDengine 配置
├── .env.example        # 环境变量模板
├── docker-compose.yml  # 一键部署
└── README.md           # 项目说明
```

---

## 注意事项
- `.env`、`backend/config.py` 等敏感配置文件已被 `.gitignore` 忽略，请勿上传。
- 推荐仅上传 `.env.example`、`config.example.py` 作为模板。
- 如需生产环境部署，请自行加强安全性。

---

# English README

## Project Overview

This is a simple IoT cloud platform demo. It collects temperature and humidity data from ESP32 + DHT11, sends it via MQTT to a Flask backend, stores it in TDengine, and pushes real-time updates to a Vue frontend via Socket.IO.

### Tech Stack
- Hardware: ESP32 + DHT11
- Communication: MQTT (EMQX)
- Database: TDengine
- Backend: Flask + Flask-SocketIO
- Frontend: Vue 3 + Vite
- Deployment: Docker Compose

---

## Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/Alele496/iot-platform-demo.git
cd iot-demo-docker
```

### 2. Configure environment variables
- Copy `.env.example` to `.env` and fill in your own values.
- Copy `backend/config.example.py` to `backend/config.py` and fill in your credentials.

### 3. Start services
```bash
docker-compose up -d
```

- Backend Flask: port 5000
- Frontend Vue: port 3000
- EMQX MQTT Broker: port 1883
- TDengine REST API: port 6041

### 4. Open the frontend
Visit: http://localhost:3000

---

## Directory Structure
```
├── backend/            # Flask backend
├── frontend/           # Vue frontend
├── esp32s3/            # ESP32 code
├── emqx/               # MQTT broker config
├── tdengine/           # TDengine config
├── .env.example        # Env template
├── docker-compose.yml  # Docker Compose
└── README.md           # Readme
```

---

