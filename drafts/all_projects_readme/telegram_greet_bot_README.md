# Telegram Greet Bot

Telegram-бот на aiogram, который приветствует пользователей по имени.

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Получите токен бота через [@BotFather](https://t.me/BotFather) в Telegram.

3. Установите токен в переменную окружения:

**Windows (PowerShell):**
```powershell
$env:TELEGRAM_BOT_TOKEN="ваш_токен"
```

**Windows (CMD):**
```cmd
set TELEGRAM_BOT_TOKEN=ваш_токен
```

**macOS/Linux:**
```bash
export TELEGRAM_BOT_TOKEN="ваш_токен"
```

Или замените в `bot.py`:
```python
BOT_TOKEN = "ваш_токен_здесь"
```

## Запуск

```bash
python bot.py
```

## Использование

1. Найдите бота в Telegram по имени
2. Отправьте `/start` для приветствия
3. Напишите своё имя — бот ответит приветствием
4. Бот работает бесконечно до остановки через Ctrl+C
