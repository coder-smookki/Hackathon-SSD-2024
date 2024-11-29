# Используем официальный образ Node.js
FROM node:20-alpine

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем package.json и yarn.lock в контейнер
COPY webapp/frontend/package*.json webapp/frontend/yarn.lock ./

# Устанавливаем зависимости с помощью yarn (предустановлен)
RUN yarn

# Копируем содержимое фронтенд-приложения в контейнер
COPY webapp/frontend .

# Указываем порт, который будет использоваться
EXPOSE 1234

# Запускаем приложение в режиме разработки
CMD ["yarn", "dev", "--host", "0.0.0.0", "--port", "1234"]
