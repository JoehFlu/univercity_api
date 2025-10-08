# 📘 University API — FastAPI + MongoDB

## 🚀 Описание
**University API** — это простое REST-API на **FastAPI**, работающее в Docker и использующее **MongoDB** для хранения данных о студентах, курсах и записях на них.  
Реализован полный **CRUD** для всех сущностей, а также сидинг тестовых данных и health-check для мониторинга состояния API.

---

## 📦 Структура проекта
```
univercity_api/
├── Dockerfile
├── docker-compose.yml
├── main.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Требования
Перед запуском убедись, что установлено:
- Docker >= 27.0
- Docker Compose >= 1.29
- Python >= 3.12 (если хочешь запускать локально без Docker)
- WSL2 (если на Windows)

Проверка:
```bash
docker --version
docker-compose --version
python3 --version
```

---

## 🧩 Установка и запуск
1. Перейди в папку проекта:
   ```bash
   cd ~/univercity_api
   ```

2. Собери и запусти контейнеры:
   ```bash
   docker-compose up --build
   ```

3. После успешного запуска сервер будет доступен по адресу:
   👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧠 API эндпоинты

| Метод | Эндпоинт | Описание |
|-------|-----------|-----------|
| **POST** | `/students/` | Создать студента |
| **GET** | `/students/` | Получить список студентов |
| **PUT** | `/students/{id}` | Обновить данные студента |
| **DELETE** | `/students/{id}` | Удалить студента и связанные записи |
| **POST** | `/courses/` | Создать курс |
| **GET** | `/courses/` | Получить список курсов |
| **PUT** | `/courses/{id}` | Обновить курс |
| **DELETE** | `/courses/{id}` | Удалить курс и связанные записи |
| **POST** | `/enrollments/` | Добавить запись о зачислении |
| **GET** | `/enrollments/` | Получить список записей |
| **PUT** | `/enrollments/{id}` | Обновить запись |
| **DELETE** | `/enrollments/{id}` | Удалить запись |
| **POST** | `/seed/` | Заполнить БД тестовыми данными |
| **GET** | `/health` | Проверить состояние API (статус `ok`) |

---

## 🔄 Примеры запросов

### Создание студента
```bash
curl -X POST "http://localhost:8000/students/" -H "Content-Type: application/json" -d '{"name": "Alice", "age": 21, "email": "alice@example.com"}'
```

### Обновление студента
```bash
curl -X PUT "http://localhost:8000/students/68e5a4bfc48eb29e7c491b3b" -H "Content-Type: application/json" -d '{"name": "New Name", "age": 25, "email": "new@example.com"}'
```

**Ответ:**
```json
{
  "id": "68e5a4bfc48eb29e7c491b3b",
  "name": "New Name",
  "age": 25,
  "email": "new@example.com"
}
```

### Удаление студента
```bash
curl -X DELETE "http://localhost:8000/students/68e5a4bfc48eb29e7c491b3b"
```

**Ответ:**
```json
{
  "status": "deleted",
  "entity": "student",
  "id": "68e5a4bfc48eb29e7c491b3b"
}
```

---

## 🧪 Сидинг тестовых данных
Создаёт случайные данные (5 студентов, 3 курса и зачисления между ними):
```bash
curl -X POST "http://localhost:8000/seed/"
```

---

## 🩺 Проверка состояния
```bash
curl http://localhost:8000/health
```
**Ответ:**
```json
{"status": "ok"}
```
---

## 🗑️ Остановка и очистка контейнеров
```bash
docker-compose down
```

Если хочешь очистить данные MongoDB:
```bash
docker-compose down -v
```

---

## 💾 Персистентность данных (опционально)
Чтобы данные Mongo не терялись после перезапуска, в `docker-compose.yml` добавь:
```yaml
volumes:
  mongo_data:
```

и подключи его:
```yaml
services:
  mongo:
    volumes:
      - mongo_data:/data/db
```

---

## 📜 Лицензия
MIT License © 2025
