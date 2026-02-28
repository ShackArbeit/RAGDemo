# 檔案說明: 建立 Next.js 開發容器，安裝依賴並複製專案。
FROM node:20-alpine
WORKDIR /app
COPY package.json /app/package.json
RUN npm install
COPY . /app
