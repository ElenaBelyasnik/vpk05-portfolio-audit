# Telegram AI Bot

Telegram-бот с интеграцией искусственного интеллекта через API GenAPI (модель gpt-5-6-luna).

## Структура проекта

```
vpf02_telegram_ai_bot/
├── .venv/                  # Виртуальное окружение Python
├── .gitignore              # Игнорируемые файлы Git
├── .env.example            # Пример переменных окружения
├── requirements.txt        # Зависимости Python
├── README.md               # Этот файл
├── ProgressOfWork.md       # Ход работ над проектом
├── main.py                 # Точка входа приложения
├── bot/
│   ├── __init__.py
│   ├── bot.py              # Основной класс приложения бота
│   └── router.py           # Роутер (подключение обработчиков)
├── config/
│   ├── __init__.py
│   └── settings.py         # Загрузка переменных окружения
├── handlers/
│   ├── __init__.py
│   └── start.py            # Обработчики команд и сообщений
├── middlewares/
│   └── __init__.py         # Заготовка для мидлваров
└── utils/
    ├── __init__.py
    ├── api_client.py       # Клиент GenAPI через OpenAI
    └── context_manager.py  # Управление контекстом диалогов
```

## Установка

1. Убедитесь, что установлен Python 3.12+.

2. Активируйте виртуальное окружение:

   **Windows (PowerShell):**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   **Linux / macOS:**
   ```bash
   source .venv/bin/activate
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Настройка

1. Создайте файл `.env` из шаблона:
   ```bash
   cp .env.example .env
   ```

2. Откройте `.env` и введите свои значения:
   ```env
   BOT_TOKEN=ваш_токен_бота
   OPENAI_API_KEY=ваш_api_ключ_genapi
   OPENAI_BASE_URL=https://proxy.gen-api.ru/v1
   HTTP_PROXY=socks5://127.0.0.1:10808
   ```

3. Получить токен бота: [BotFather](https://t.me/BotFather) в Telegram.
4. Получить API-ключ GenAPI: [gen-api.ru](https://gen-api.ru/).

## Запуск

```bash
python main.py
```

## Команды бота

| Команда | Описание |
|---|---|
| `/start` | Приветственное сообщение |
| `/reset` | Очистка контекста диалога |

## Влияние температуры на ответы модели

Температура (`temperature`) контролирует креативность ответов модели:
- **Низкая температура (0.1–0.3)** — ответы точные, сжатые, предсказуемые
- **Средняя температура (0.5–0.7)** — баланс между креативностью и точностью
- **Высокая температура (0.8–1.0)** — креативные, развёрнутые, иногда неожиданные ответы

### Результаты тестирования

| Прогон | Модель | Температура | max_tokens | Эффект (креативность/точность) | Использованные токены | Стоимость (примерно) |
|---|---|---|---|---|---|---|
| 1 | gpt-5-6-luna | 0.7 | 1000 | Развёрнутый и креативный ответ — история про Барсика с деталями про Python, команды if/else, приложение для корма | ~400 токенов | 0.10925 ₽ |
| 2 | gpt-5-6-luna | 0.2 | 1000 | Короткий и точный ответ — без «воды», по делу | ~300 токенов | 0.08275 ₽ |

**Вывод:** При температуре 0.7 модель генерирует более развёрнутые и креативные ответы, но использует больше токенов. При температуре 0.2 ответы короче и экономичнее по токенам.

## Зависимости

- `aiogram` — асинхронный фреймворк для Telegram-ботов
- `openai` — клиент для работы с GenAPI (OpenAI-совместимый формат)
- `python-dotenv` — загрузка переменных окружения из `.env`
- `aiohttp-socks` — поддержка SOCKS-прокси для aiohttp
- `httpx[socks]` — поддержка SOCKS-прокси для httpx
- `socksio` — библиотека для SOCKS-прокси

## Решение проблем

### Ошибка: `AttributeError: module 'config' has no attribute 'BOT_TOKEN'`
**Причина:** Python импортировал встроенный модуль `config` вместо нашей папки `config`.
**Решение:** Переименовал `config/config.py` в `config/settings.py`.

### Ошибка: `'Router' object has no attribute 'command'`
**Причина:** В aiogram 3.x нет метода `@router.command()`.
**Решение:** Заменил на `@router.message(Command("..."))`.

### Ошибка: `TelegramNetworkError: Cannot connect to host api.telegram.org:443`
**Причина:** VPN блокировал HTTPS-соединение к Telegram API.
**Решение:** Настроен прокси через Proxifier (SOCKS5, порт 10808) и добавлена переменная `HTTP_PROXY` в `.env`.

### Ошибка: `ModuleNotFoundError: No module named 'aiohttp_socks'`
**Причина:** Для работы прокси в aiogram нужен дополнительный пакет.
**Решение:** Установлен `pip install aiohttp-socks`.

### Ошибка: `ImportError: Using SOCKS proxy, but the 'socksio' package is not installed`
**Причина:** Библиотека httpx требует пакет socksio для SOCKS-прокси.
**Решение:** Установлен `pip install "httpx[socks]"`.

### Ошибка: `TypeError: unsupported operand type(s) for +: 'ClientTimeout' and 'int'`
**Причина:** Параметр `timeout` в `AiohttpSession` должен быть числом (секундами), а не объектом `ClientTimeout`.
**Решение:** Изменил `ClientTimeout(total=30)` на `timeout=30`.

### Ошибка: `Error code: 404 - The route v1/chat/completions could not be found`
**Причина:** Неверный URL GenAPI (`api.gen-api.ru` вместо `proxy.gen-api.ru`).
**Решение:** Обновил `OPENAI_BASE_URL` на `https://proxy.gen-api.ru/v1`.
