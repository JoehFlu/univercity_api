# 📘 University API — FastAPI + MongoDB

## 🚀 Описание
**University API** — это простое REST-API на **FastAPI**, работающее в Docker и использующее **MongoDB** для хранения данных о студентах, курсах и записях на них.  
Реализован полный **CRUD** для всех сущностей, сидинг тестовых данных и health-check для мониторинга состояния API + интеграция с CastleMock для имитации внешних API.

---

## ⚙️ Стек технологий

- 🐍 **FastAPI** — backend и REST API  
- 🍃 **MongoDB** — база данных  
- 🏰 **CastleMock** — имитация внешних API  
- 🐳 **Docker Compose** — контейнеризация и запуск окружения

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

## 🚀 Установка и запуск
1. Перейди в папку проекта:
   ```bash
   cd ~/univercity_api
   ```

2. Собери и запусти контейнеры:
   ```bash
   docker-compose up --build
   ```

3. Проверить запущенные сервисы:
   ```bash
   docker ps
   ```

---

## 🌐 Доступ к сервисам

| Сервис | URL | Описание |
|--------|-----|-----------|
| **FastAPI Docs** | [http://localhost:8000/docs](http://localhost:8000/docs) | Swagger UI с API |
| **MongoDB** | `mongodb://localhost:27017` | База данных |
| **CastleMock** | [http://localhost:8080/castlemock](http://localhost:8080/castlemock) | Интерфейс для создания моков |

---

## 📚 Основные эндпоинты FastAPI

### 🔧 Вспомогательные эндпоинты

| Метод | Эндпоинт | Описание |
|--------|-----------|-----------|
| `POST` | `/seed` | Сгенерировать тестовые данные |
| `GET` | `/health` | Проверка состояния сервиса |

### 👩‍🎓 Students

| Метод | Эндпоинт | Описание |
|--------|-----------|-----------|
| `GET` | `/students` | Получить всех студентов |
| `POST` | `/students` | Создать нового студента |
| `PUT` | `/students/{id}` | Обновить студента |
| `DELETE` | `/students/{id}` | Удалить студента |

### 📚 Courses

| Метод | Эндпоинт | Описание |
|--------|-----------|-----------|
| `GET` | `/courses` | Получить список курсов |
| `POST` | `/courses` | Добавить курс |
| `PUT` | `/courses/{id}` | Обновить курс |
| `DELETE` | `/courses/{id}` | Удалить курс |

### 📝 Enrollments

| Метод | Эндпоинт | Описание |
|--------|-----------|-----------|
| `GET` | `/enrollments` | Получить все записи |
| `POST` | `/enrollments` | Записать студента на курс |
| `DELETE` | `/enrollments/{id}` | Удалить запись |

---

## 🏰 CastleMock — имитация внешних API

**CastleMock** используется для создания и тестирования фейковых внешних сервисов локально.  
Это позволяет проверять интеграции без подключения к реальным API.

**Интерфейс:**  
👉 [http://localhost:8080/castlemock](http://localhost:8080/castlemock)

### 🌦 Пример мок-ответа
```json
{
  "city": "Berlin",
  "temperature": 18,
  "condition": "Cloudy"
}
```

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
Чтобы данные Mongo и CastleMock не терялись после перезапуска, в `docker-compose.yml` добавны:
```yaml
volumes:
  mongo_data:
  castlemock_data:
```
