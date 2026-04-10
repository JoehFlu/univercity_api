# 📘 University API — FastAPI + MongoDB + CastleMock

## 🔎 Описание

**University API** — это простой REST API на FastAPI с MongoDB в Docker.  
В проекте есть CRUD для студентов, курсов и записей на курс, а также `seed`, проверка состояния и несколько мок-эндпоинтов через CastleMock.

---

## ⚙️ Стек технологий

| Технология | Назначение |
|------------|------------|
| 🐍 FastAPI | REST API и backend |
| 🍃 MongoDB | Хранение данных |
| 🏰 CastleMock | Моки внешних API |
| 🐳 Docker Compose | Запуск всего окружения |

---

## 📦 Структура проекта

```text
university_api/
├── Dockerfile
├── docker-compose.yml
├── main.py
├── requirements.txt
├── README.md
└── castlemock_data_persistent/
```

---

## 🚀 Установка и запуск

1. Перейди в папку проекта:
   ```bash
   cd ~/university_api
   ```

2. Собери и запусти контейнеры:
   ```bash
   docker compose up --build
   ```

3. Проверь, что контейнеры запущены:
   ```bash
   docker ps
   ```

---

## 🗑️ Остановка и очистка

```bash
docker compose down
```

Если хочешь удалить данные MongoDB:

```bash
docker compose down -v
```

---

## ⚙️ Требования

| Требование | Примечание |
|------------|------------|
| Docker | Нужен для запуска проекта |
| Docker Compose | Нужен для запуска сервисов |
| Python 3.11+ | Только если запускаешь что-то локально вне Docker |

Проверка:

```bash
docker --version
docker compose version
python3 --version
```

---

## 🌐 Доступ к сервисам

| Сервис | URL | Описание |
|--------|-----|-----------|
| **FastAPI Docs** | [http://localhost:8000/docs](http://localhost:8000/docs) | Swagger UI |
| **MongoDB** | `mongodb://localhost:27017` | База данных |
| **CastleMock** | [http://localhost:8080/castlemock](http://localhost:8080/castlemock) | Интерфейс моков |

---

## 🗂️ Основные эндпоинты FastAPI

### 🔧 Utility

| Метод | Эндпоинт | Описание |
|-------|----------|-----------|
| `POST` | `/seed/` | Заполнить базу тестовыми данными |
| `GET` | `/health` | Проверить состояние API |

### 👩‍🎓 Students

| Метод | Эндпоинт | Описание |
|-------|----------|-----------|
| `GET` | `/students/` | Получить всех студентов |
| `POST` | `/students/` | Создать нового студента |
| `PUT` | `/students/{id}` | Обновить студента |
| `DELETE` | `/students/{id}` | Удалить студента |

### 📚 Courses

| Метод | Эндпоинт | Описание |
|-------|----------|-----------|
| `GET` | `/courses/` | Получить список курсов |
| `POST` | `/courses/` | Добавить курс |
| `PUT` | `/courses/{id}` | Обновить курс |
| `DELETE` | `/courses/{id}` | Удалить курс |

### 📝 Enrollments

| Метод | Эндпоинт | Описание |
|-------|----------|-----------|
| `GET` | `/enrollments/` | Получить все записи |
| `POST` | `/enrollments/` | Записать студента на курс |
| `PUT` | `/enrollments/{id}` | Обновить запись |
| `DELETE` | `/enrollments/{id}` | Удалить запись |

### 🏰 CastleMock

| Метод | Эндпоинт | Описание |
|-------|----------|-----------|
| `GET` | `/external/weather` | Мок погоды |
| `POST` | `/external/auth/login` | Мок логина |
| `PUT` | `/external/user/update` | Мок обновления профиля |

---

## 📌 Коды ответов

| Код | Когда возвращается |
|-----|-------------------|
| `200` | Успешный ответ |
| `400` | Битый `id`, дубликат email или enrollment |
| `404` | Сущность не найдена |
| `422` | Ошибка валидации тела запроса |
| `502` | CastleMock недоступен |

---

## 🏰 CastleMock

CastleMock хранит моки в `castlemock_data_persistent/`, чтобы они не пропадали между перезапусками.

---

## 🧪 Пример запроса

Создание студента:

```bash
curl -X POST "http://localhost:8000/students/" \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","age":21,"email":"alice@example.com"}'
```
