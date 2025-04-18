# frontend/Dockerfile
FROM node:18
WORKDIR /app

# 设置国内镜像源
RUN npm config set registry https://registry.npmmirror.com \
    npm config set disturl https://npmmirror.com/dist && \
    npm config set sass_binary_site https://npmmirror.com/mirrors/node-sass && \
    npm config set puppeteer_download_host https://npmmirror.com/mirrors \
    npm config set fetch-retries 5 && \
    npm config set fetch-timeout 300000

# 仅复制包管理文件（利用 Docker 层缓存）
COPY package.json package-lock.json* ./

#COPY ./frontend/local_modules ./node_modules

# 安装依赖（强制清理缓存）
RUN npm cache clean --force \
    && npm install --force --legacy-peer-deps

RUN npm install -g yarn \
    && yarn config set registry https://registry.npmmirror.com \
    && yarn install --force

# 复制源代码
COPY . .

# 构建应用
RUN npm run build

# 启动命令
#CMD ["npm", "start"]
CMD ["npm", "run", "dev"]