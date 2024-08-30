# Используем официальный образ Python в качестве базового
FROM python:3.10-slim

# Устанавливаем зависимости системы, которые могут понадобиться
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в рабочую директорию контейнера
COPY . .

# Указываем команду, которая будет запускаться при старте контейнера
CMD ["python", "main.py"]
