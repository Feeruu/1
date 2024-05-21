# Используем базовый образ Python
FROM python:3.9-slim

# Устанавливаем переменную окружения, чтобы Python не сохранял кеш-компиляцию
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию
WORKDIR /FeedBackBot

# Копируем файл зависимостей
COPY requirements.txt /FeedBackBot/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . /FeedBackBot/

# Запуск вашего бота
CMD ["python", "main2.py"]