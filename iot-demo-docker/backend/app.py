# backend/app.py

from flask import Flask, request
import paho.mqtt.client as mqtt
import requests
import time
import json
from config import Config
from flask_cors import CORS
from flask_socketio import SocketIO

import os
import subprocess

# --------------------- 初始化 Flask 和 Socket.IO ---------------------

auth = ('<your_tdengine_user>', '<your_tdengine_password>')
url = "http://tdengine:6041/rest/sql"
payload = "SHOW DATABASES"
response = requests.post(url, data=payload, auth=auth)
print(response.json())

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode='eventlet',
    transports=['websocket'],  # 添加 polling 作为回退方案
    # allow_upgrades=False,       # 禁用协议升级
    logger=True,  # 启用详细日志
    engineio_logger=True,  # 启用 Engine.IO 日志
    ping_timeout=60,            # 增加 ping 超时时间
    ping_interval=30            # 增加 ping 间隔时间
    #max_http_buffer_size=1e8
)

@app.route('/test', methods=['GET'])
def test_push():
    temp, humi = 25.0, 60.0  # 测试数据
    socketio.emit('update', {'temp': temp, 'humi': humi})
    return "Test data sent!"

# 添加连接事件监听
@socketio.on('connect')
def handle_connect():
    print("✅ 客户端已连接:", request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    print("❌ 客户端已断开:", request.sid)

# --------------------- 定义回调函数（必须在前） ---------------------
def on_connect(client, userdata, flags, reason_code, properties):
    """MQTT 连接成功回调"""
    if reason_code == 0:
        print("✅ MQTT Connected!")
        client.subscribe("sensors/dht11")  # 订阅主题
        result, mid = client.subscribe("sensors/dht11")  # 添加返回值日志
        print(f"🔗 订阅状态: {result}, 消息 ID: {mid}")
    else:
        print(f"❌ MQTT 连接失败，错误代码: {reason_code}")

def on_sensor_data(client, userdata, msg):
    """处理 MQTT 消息"""
    try:
        print(f"📩 收到 MQTT 消息: topic={msg.topic}, payload={msg.payload}")
        data = json.loads(msg.payload)
        temp = data.get("temp")
        humi = data.get("humi")
        
        # 参数化 SQL 防止注入
        sql = "INSERT INTO demo.sensors USING demo.sensors TAGS('device1') VALUES (NOW(), %s, %s)"
        response = requests.post(
            app.config["TDENGINE_URL"],
            auth=app.config["TDENGINE_AUTH"],
            data=sql,
            params=(temp, humi)
        )
        response.raise_for_status()
        
        # 推送数据到前端
        print(f"📡 正在推送数据到前端: temp={temp}, humi={humi}")

        socketio.emit("update", {"temp": temp, "humi": humi})
        print(f"📡 推送数据: temp={temp}, humi={humi}")
    except Exception as e:
        print(f"❌ 处理MQTT消息失败: {e}")

# --------------------- 初始化 MQTT 客户端 ---------------------
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_connect = on_connect  # ✅ 此时函数已定义
mqtt_client.on_message = on_sensor_data
mqtt_client.username_pw_set("<your_emqx_user>", "<your_emqx_password>")  # EMQX 认证

#MQTT_BROKER  = emqx
#MQTT_PORT = 1883

# --------------------- 数据库初始化 ---------------------
def init_database():
    max_retries = 10
    for i in range(max_retries):
        try:
            requests.post(
                app.config["TDENGINE_URL"],
                auth=app.config["TDENGINE_AUTH"],
                data="CREATE DATABASE IF NOT EXISTS demo"
            )
            requests.post(
                app.config["TDENGINE_URL"],
                auth=app.config["TDENGINE_AUTH"],
                data="CREATE TABLE IF NOT EXISTS demo.sensors (ts TIMESTAMP, temp FLOAT, humi FLOAT)"
            )
            print("✅ 数据库初始化成功")
            return
        except requests.exceptions.ConnectionError as e:
            print(f"⏳ 等待 TDengine 启动... ({i+1}/{max_retries})")
            time.sleep(5)
    raise RuntimeError("无法连接 TDengine")

@app.route('/test_tdengine', methods=['GET'])
def test_tdengine_connection():
    import requests
    url = Config.TDENGINE_URL
    auth = Config.TDENGINE_AUTH
    payload = "SHOW DATABASES"
    
    try:
        response = requests.post(url, data=payload, auth=auth)
        return response.json()  # 返回TDengine响应
    except Exception as e:
        return {"error": str(e)}, 500


def verify_tdengine_status():
    try:
        print("正在验证 TDengine 数据库状态...")
        # 调用 TDengine CLI
        output = subprocess.check_output("taos -s 'SHOW DATABASES;'", shell=True)
        print("TDengine 数据库状态:")
        print(output.decode())
    except subprocess.CalledProcessError as e:
        print(f"❌ TDengine 验证失败: {e}")

# --------------------- 主程序入口 ---------------------
if __name__ == "__main__":
    with app.app_context():
        init_database()
        # 带重试的 MQTT 连接
        max_retries = 10
        for i in range(max_retries):
            try:
                mqtt_client.connect(
                    host=app.config["MQTT_BROKER"],
                    port=app.config["MQTT_PORT"],
                    keepalive=60
                )
                mqtt_client.loop_start()
                print("✅ MQTT 连接成功")
                break
            except Exception as e:
                print(f"❌ 连接 MQTT 失败 ({i+1}/{max_retries}): {e}")
                time.sleep(5)
        else:
            raise RuntimeError("无法连接 MQTT 服务器")
    
    verify_tdengine_status()
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)