# Python Test App

Тестовое Flask-приложение для проверки Docker-контейнеров.

## Эндпоинты

| Путь | Описание |
|---|---|
| `/` | Главная страница с общей информацией |
| `/health` | Проверка здоровья приложения |
| `/info` | Информация о системе |
| `/multiply/<a>/<b>` | Умножение двух чисел |
| `/divide/<a>/<b>` | Деление двух чисел |

## Фронтенд

Страница с блоками для каждого эндпоинта:

- Каждый эндпоинт — отдельный блок с путём, кнопкой «Проверить» и полем результата
- При нажатии «Проверить» результат отображается в поле блока в формате JSON
- Кнопка блокируется на время запроса
- Время последнего обновления показывается внизу страницы

## Быстрый старт

### Запуск контейнеров

```bash
# Запуск (образы скачаются с Docker Hub)
docker-compose up -d

# Проверка
docker-compose ps

# Остановка
docker-compose down
```

Фронтенд: [http://localhost](http://localhost)
Бэкенд API: [http://localhost:5000](http://localhost:5000)

Подробная инструкция: [DOCKER_INSTRUCTION.md](DOCKER_INSTRUCTION.md).

## Запуск на другом компьютере

1. Установите **Docker Desktop** с https://www.docker.com/products/docker-desktop/
2. Создайте файл `docker-compose.yml` (см. [DOCKER_INSTRUCTION.md](DOCKER_INSTRUCTION.md))
3. Выполните: `docker-compose up -d`
4. Откройте http://localhost

Ничего больше настраивать не нужно — образы уже загружены на Docker Hub.

## Структура

| Файл | Назначение |
|---|---|
| `app.py` | Flask-приложение |
| `requirements.txt` | Зависимости Python |
| `Dockerfile` | Описание образа |
| `DOCKER_INSTRUCTION.md` | Инструкция по сборке и запуску |
| `test_app.py` | Скрипт тестирования эндпоинтов |
| `screenshots/` | Папка для скриншотов |
