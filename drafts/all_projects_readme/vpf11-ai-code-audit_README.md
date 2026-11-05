# AI Code Audit — рефакторинг и аудит кода

Учебный проект по рефакторингу унаследованного Python-кода: два модуля
(`utils.py` и `api.py`) были написаны «стихийно» и содержали критические
уязвимости — SQL-инъекции, «хеширование» пароля переворотом строки, гонки
потоков, утечки соединений, неверные HTTP-коды и нарушения PEP 8. Оба модуля
переписаны с сохранением исходной бизнес-логики: эндпоинты работают в
параметрах HTTP, функции модулей покрывают самопроверкой `self_test`.

## Структура проекта

```
.
├── api.py               # Flask-приложение: REST API поверх SQLite
├── utils.py             # Работа с БД, пароли, фоновые задачи
├── openapi.yaml         # OpenAPI 3.1.0 документация API
├── requirements.txt     # Зависимости
├── Dockerfile           # Образ контейнера для Flask-приложения
├── .dockerignore        # Файлы, исключаемые из контекста сборки
├── test_endpoints.py    # Скрипт проверки всех эндпоинтов по HTTP
├── README.md            # Этот файл
└── ProgressOfWork.md    # Ход выполнения работ по этапам
```

## Установка

Требуется Python 3.10+.

```bash
pip install -r requirements.txt
```

## Запуск

Запуск Flask-приложения:

```bash
python api.py
```

После запуска сервер доступен на <http://localhost:5000>. База данных
создаётся автоматически: файл `test.db` в корне проекта, схема создаётся при
старте (`init_db()`). Путь к файлу базы можно изменить переменной окружения
`API_DB_PATH` — это единственная переменная окружения, используемая кодом.

Самопроверка утилит (запускается без аргументов):

```bash
python utils.py
```

Вывод при успехе: `self_test passed` (код выхода 0). Проверяются: работа с
БД, нейтральность SQL-инъекций, корректность проверки паролей и отсутствие
гонок потоков при параллельном добавлении пользователей.

## Docker

### Сборка и запуск через Docker

```bash
# Собрать образ
docker build -t vpf11-ai-code-audit .
# Запустить контейнер
docker run --rm -p 5000:5000 vpf11-ai-code-audit
```

> **Примечание:** Если у вас Docker Desktop с драйвером `docker-container` (это стандарт для современных версий), после `docker build` образ может остаться только в кэше сборки, и `docker run` его не найдёт. В этом случае используйте флаг `--load`:
>
> ```bash
> docker build --load -t vpf11-ai-code-audit .
> ```

После запуска приложение доступно на <http://localhost:5000>. Образ построен
на `python:3.11-slim`, работает в `/app`, зависимости ставятся из
`requirements.txt` отдельным слоем (правка кода не вызывает переустановку
Flask).

База данных лежит в томе `/app/data` (путь задаётся `ENV API_DB_PATH`,
значение `/app/data/test.db`). Чтобы файлы базы остались на хосте, монтируйте
каталог или именованный том:

```bash
docker run --rm -p 5000:5000 -v vpf11-data:/app/data vpf11-ai-code-audit
```

Приложение поднимается встроенным CLI Flask
(`flask --app api run --host=0.0.0.0 --port=5000`), а не `python api.py`:
вызов `app.run(debug=True)` в `api.py` не получает параметр `host`, Flask
подставляет `127.0.0.1`, и внутри контейнера порт был бы недоступен с хоста.
CLI использует тот же объект `app` и не требует ни правки кода, ни новых
зависимостей; отладчик Werkzeug в контейнере при этом выключен.

### Проверка эндпоинтов

```bash
# Установить requests (если ещё не установлен)
pip install requests
# Запустить тесты
python test_endpoints.py
```

Скрипт последовательно проверяет все 5 эндпоинтов (`POST /adduser` → 201,
`GET /user/1` → 200, `GET /activate/1` → 200, `GET /slow` → 202,
`GET /wrong` → 500), печатает по каждой проверке метод и URL, код ответа,
тело ответа и вердикт `✅ PASS` / `❌ FAIL`, а в конце выводит сводку
(прошло/упало). Код возврата: `0` — всё прошло, `1` — есть падения.

Сервер к моменту запуска скрипта должен быть поднят (обычный `python api.py`
или контейнер из раздела выше). Адрес переопределяется переменной окружения
`BASE_URL` (по умолчанию `http://localhost:5000`), таймаут запроса —
`REQUEST_TIMEOUT` (по умолчанию 10 секунд):

```bash
BASE_URL=http://127.0.0.1:5000 python test_endpoints.py
```

`requests` — инструмент проверки, а не зависимость приложения
(`requirements.txt` её не содержит).

## Описание эндпоинтов

Ответы всех эндпоинтов — JSON. Флаг `ensure_ascii` не отключён, поэтому
кириллица в ответах экранируется (`\uXXXX`).

### POST /adduser — создать пользователя

Тело запроса — JSON-объект с непустой строкой `name`. Имя вставляется в SQL
только параметрически, поэтому попытка инъекции попадает в БД как обычный
текст и безвредна. Коды ответа: `201` — создан, `400` — не JSON или `name`
отсутствует/пустой.

```bash
curl -X POST http://localhost:5000/adduser -H "Content-Type: application/json" -d "{\"name\": \"Ivan\"}"
```

```json
{"id": 1, "name": "Ivan", "status": "ok"}
```

### GET /user/<id> — получить пользователя

Коды ответа: `200` — найден, `404` — пользователя нет (или `id` не целое:
маршрут объявлен с конвертером `<int:id>`, несовпадающий путь тоже даёт
404).

```bash
curl http://localhost:5000/user/1
```

```json
{"id": 1, "name": "Ivan"}
```

### GET /activate/<id> и POST /activate/<id> — активировать пользователя

Методы: `GET` и `POST`. Поток-безопасно: общий список защищён
`threading.Lock`, добавление идемпотентно.

```bash
curl http://localhost:5000/activate/1
```

```json
{"active": [1], "status": "ok"}
```

### GET /slow — имитация долгой операции

Отвечает сразу, не блокируя воркер: работа выполняется в отдельном потоке.
Код ответа: `202 Accepted`.

```bash
curl http://localhost:5000/slow
```

```json
{"status": "scheduled"}
```

### GET /wrong — контролируемая обработка ошибки

Внутри гарантированно возникает `ZeroDivisionError`, она перехватывается
(вместо голого `except`) и возвращается с кодом `500`.

```bash
curl http://localhost:5000/wrong
```

```json
{"detail": "division by zero", "msg": "error"}
```

## OpenAPI-документация

Интерфейс API полностью описан в файле `openapi.yaml` в корне проекта — это
спецификация OpenAPI 3.1.0: все 5 эндпоинтов (`/adduser`, `/user/{uid}`,
`/activate/{uid}`, `/slow`, `/wrong`), схемы запросов и ответов
(`components/schemas`), коды ответов и примеры к каждому ответу. Спецификация
синхронизирована с обработчиками в `api.py`.

### Проверка валидности

`pyyaml` и `openapi-spec-validator` — инструменты проверки документации, а не
зависимости приложения (`requirements.txt` их не содержит). Для проверки
выполните в любом окружении:

```bash
pip install pyyaml openapi-spec-validator
python -c "import yaml; from openapi_spec_validator import validate; validate(yaml.safe_load(open('openapi.yaml', encoding='utf-8'))); print('openapi.yaml: VALID OpenAPI 3.1.0')"
```

При успехе команда печатает `openapi.yaml: VALID OpenAPI 3.1.0` и завершается
с кодом 0.

### Импорт в Swagger UI, Postman и Insomnia

- **Swagger UI**: откройте <https://editor.swagger.io> (или локальный
  экземпляр Swagger UI) → меню `File` → `Import file` → выберите
  `openapi.yaml`. Альтернатива для локального Swagger UI — открыть
  `http://localhost:8080/?url=<путь-до-openapi.yaml>`.
- **Postman**: кнопка `Import` → вкладка `File` → перетащите `openapi.yaml`
  → `Import`. Postman создаст коллекцию со всеми запросами автоматически.
- **Insomnia**: `Design` → `Create/Import from File` (или `+` → `Import
  from File`) → выберите `openapi.yaml` → документ с запросами создан.

## Что было исправлено

### utils.py

| Было (уязвимость / дефект)          | Стало                                            |
|-------------------------------------|--------------------------------------------------|
| SQL-инъекции: f-строки в `INSERT`   | Параметризованные запросы (`?` + кортеж)         |
| `def add_user(..., tags=[])`        | Неизменяемый дефолт `None`                       |
| «Хеш» пароля `password[::-1]`       | `hashlib.sha256` с криптографической солью `os.urandom(16)`, формат `user_id:salt:hash` |
| Гонка потоков при `append` в список | Мутации общего списка под `threading.Lock`       |
| `return cursor.lastrowid` (строка)  | `return int(cursor.lastrowid)`                   |
| `is_admin` возвращал `True` при ошибке | Любая ошибка → `False`                        |
| Соединения не закрывались           | Контекстный менеджер `db_connection` (`contextlib.contextmanager`) |
| `open()` без закрытия файла         | Контекстный менеджер `with open(...)`            |
| Фиктивный `self_test` (`assert True`) | Реальные проверки: БД, инъекции, хеши, 8 потоков |
| Неиспользуемый глобальный `CACHE`   | Удалён                                           |
| Глобальный `DB_PATH`                | Параметр `db_path` с дефолтом `test.db`          |
| —                                   | Добавлены: `init_db`, `get_active_users_snapshot`, `run_long_running_task_in_thread` |

### api.py

| Было (уязвимость / дефект)          | Стало                                            |
|-------------------------------------|--------------------------------------------------|
| Глобальные `conn`/`cur`             | Соединение на запрос: `get_db()` через `flask.g`, закрытие в `@app.teardown_appcontext` |
| `INSERT ... VALUES ('%s') % name`   | Параметризованные запросы                        |
| `/user/<user_id>` — строка в SQL    | `<int:id>` + параметрический `SELECT`, 404 при отсутствии |
| Нет валидации тела `/adduser`       | Проверка JSON-объекта и `name`, ответ 400        |
| Неверные коды ответов               | `/adduser` → 201; `/user` → 200/404; `/activate` → 200; `/slow` → 202; `/wrong` → 500 |
| Гонка потоков в `/activate`         | Общий список `_active_users` под `_active_lock`  |
| `/slow` блокировал воркер на 10 с   | Фоновый поток, мгновенный ответ 202              |
| Голый `except` с несуществующей переменной `e` | `except ZeroDivisionError`, ответ 500 с `str(exc)` |
| `init_db` в `@app.before_first_request` (удалён во Flask 2.3+) | Явный вызов `init_db()` при старте |
| Нарушения PEP 8                     | Код приведён к PEP 8, добавлены docstring        |

## Используемые технологии

- Python 3.10+
- Flask (единственная внешняя зависимость, см. `requirements.txt`)
- SQLite (стандартная библиотека `sqlite3`)
- Стандартная библиотека: `hashlib`, `os`, `threading`, `time`, `json`,
  `contextlib`, `typing`
