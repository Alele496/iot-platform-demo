workers = 1
worker_class = "eventlet"
timeout = 300  # 超时时间设为 300 秒
keepalive = 10  # 保持连接活跃
bind = "0.0.0.0:5000"  # 强制绑定到5000端口
