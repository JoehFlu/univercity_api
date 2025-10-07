# 📘 University API — FastAPI + MongoDB

## 🚀 Описание
**University API** — это простое REST-API на **FastAPI**, работающее в Docker и использующее **MongoDB** для хранения данных о студентах, курсах и записях на них.  
Есть эндпоинты для CRUD-операций и автогенерации тестовых данных через `/seed/`.

---

## 📦 Структура проекта
```
univercity_api/
├── Dockerfile
├── docker-compose.yml
├── main.py
└── requirements.txt
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
| **POST** | `/courses/` | Создать курс |
| **GET** | `/courses/` | Получить список курсов |
| **POST** | `/enrollments/` | Записать студента на курс |
| **GET** | `/enrollments/` | Получить список записей |
| **POST** | `/seed/` | Заполнить БД тестовыми данными |

---

## 🧰 Пример запроса
**Создание студента**
```bash
curl -X POST "http://localhost:8000/students/" -H "Content-Type: application/json" -d '{"name": "Alice", "age": 21, "email": "alice@example.com"}'
```

**Результат:**
```json
{
  "id": "6710b4f8f8e88a1d5a6b9c90",
  "name": "Alice",
  "age": 21,
  "email": "alice@example.com"
}
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
