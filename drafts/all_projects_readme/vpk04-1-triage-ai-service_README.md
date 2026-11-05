# Triage AI Service

MVP-сервис на FastAPI для предварительной обработки (триажа) клиентских
обращений: приём обращения по API, определение категории и подготовка
черновика ответа.

## Текущее состояние (этап 2)

- Реализован эндпоинт `POST /triage` с полной валидацией входных данных (Pydantic).
- LLM, база данных и лимитирование запросов **не подключены** — используются
  заглушки (будут добавлены на следующих этапах).

## Запуск

```bash
# 1. Создать и активировать виртуальное окружение
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Создать .env из образца и заполнить ключи
copy .env.example .env       # Windows
# cp .env.example .env       # Linux/macOS

# 4. Запустить сервис
uvicorn main:app --reload
```

## Проверка

- Swagger UI: http://localhost:8000/docs
- Примеры HTTP-запросов: `tests/test_requests.http`

## Пример запроса

```json
POST /triage
{
  "text": "Не приходит счёт за услуги",
  "channel": "email",
  "client_id": "client-001"
}
```

## Пример ответа

```json
{
  "category": "other",
  "draft_reply": "Обращение получено, обрабатывается.",
  "confidence": "low",
  "escalate": true
}
```
