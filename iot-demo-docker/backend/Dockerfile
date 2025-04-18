# 使用官方Python镜像
#FROM python:3.9-slim

FROM python:3.9-alpine3.18
# 使用 Alpine 基础镜像

# 安装 Alpine 兼容的包
RUN apk update && \
    apk add --no-cache \
    bind-tools \
    netcat-openbsd \
    curl  

# 安装网络工具（dnsutils、netcat、curl）
#RUN apt-get update && \
#    apt-get install -y dnsutils netcat curl && \
#    rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install -r requirements.txt

# 复制项目文件到容器
COPY . .  

# 启动命令
#CMD ["python", "app.py"]
CMD ["gunicorn", "--worker-class", "eventlet", "-b", "0.0.0.0:5000", "app:app"] 
