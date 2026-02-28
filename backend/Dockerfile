# 檔案說明: 建立 FastAPI 開發容器，安裝依賴並啟動應用。
FROM python:3.11-slim
WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt
COPY . /code
