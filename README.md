# Portfolio: Сайт-визитка + Telegram-бот

Сайт-портфолио на **Flask** и Telegram-бот на **aiogram 3.x**, использующие единую базу данных — [`projects.json`](projects.json).

Контакты и ссылки централизованно управляются через переменные в файле `.env`.

## Структура проекта

```
├── projects.json          # Единая база данных проектов
├── requirements.txt       # Python-зависимости
├── .env.example           # Шаблон переменных окружения
├── .env                   # Локальные переменные (НЕ коммитить)
├── README.md              # Этот файл
│
├── site/                  # Сайт-визитка (Flask)
│   ├── app.py             # Приложение Flask
│   ├── templates/
│   │   ├── index.html     # Главная страница
│   │   └── project.html   # Страница отдельного проекта
│   └── static/
│       ├── css/
│       │   └── style.css  # Стили (Dusty Rose)
│       └── images/        # Скриншоты проектов
│
└── bot/                   # Telegram-бот (aiogram 3.x)
    └── main.py            # Бот и обработчики команд
```

## Быстрый старт

### 0. Активация виртуального окружения

```bash
# Создание (если ещё нет)
python -m venv .venv

# Активация (Windows)
.venv\Scripts\activate

# Активация (Linux / macOS)
source .venv/bin/activate
```

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка переменных окружения

```bash
# Скопируйте шаблон и подставьте реальные значения
cp .env.example .env
# Отредактируйте .env: токен бота, email, Telegram и т.д.
```

Переменные из `.env` используются и сайтом (Flask), и ботом (aiogram).

### 3. Запуск сайта (Flask)

```bash
# Через Flask CLI
flask --app site/app run --debug

# Или напрямую
python site/app.py
```

Сайт откроется на `http://127.0.0.1:5000`.

### 4. Запуск Telegram-бота

```bash
python bot/main.py
```

Токен бота можно получить через Telegram у [@BotFather](https://t.me/BotFather)
командой `/newbot`.

## Переменные окружения (.env)

| Переменная              | Описание                                     | По умолчанию                        |
|-------------------------|----------------------------------------------|-------------------------------------|
| `BOT_TOKEN`             | Токен Telegram-бота                          | — (обязательно)                     |
| `SITE_URL`              | Адрес сайта для кнопки «Посмотреть на сайте» | `http://127.0.0.1:5000`            |
| `SITE_NAME`             | Имя на сайте                                 | `Елена Белясник`                    |
| `SITE_TITLE`            | Роль / заголовок                             | `Backend Engineer & Vibe Coder`    |
| `CONTACT_EMAIL`         | Email для контактов                          | `elena.belyasnik@yandex.ru`         |
| `CONTACT_TELEGRAM`      | Ник Telegram                                 | `@Belyasnik_Elena`                  |
| `CONTACT_TELEGRAM_URL`  | Ссылка на Telegram                           | `https://t.me/Belyasnik_Elena`      |
| `CONTACT_GITHUB_URL`    | Ссылка на GitHub                             | `https://github.com/ElenaBelyasnik` |
| `CONTACT_GITHUB_NAME`   | Ник на GitHub                                | `ElenaBelyasnik`                    |
| `BOT_LINK`              | Ссылка на Telegram-бота                      | `https://t.me/BelyasnikPortfolioBot`|

## Данные

Все проекты хранятся в [`projects.json`](projects.json) в корне репозитория.
Каждый объект содержит поля:

| Поле           | Тип      | Описание                          |
|----------------|----------|-----------------------------------|
| `id`           | `int`    | Уникальный идентификатор проекта  |
| `title`        | `str`    | Название проекта                  |
| `description`  | `str`    | Полное описание                   |
| `tech`         | `str[]`  | Список технологий                 |
| `github`       | `str`    | Ссылка на GitHub-репозиторий      |
| `image`        | `str`    | Имя файла скриншота (без пути)    |

Скриншоты нужно разместить в `site/static/images/` с именами, совпадающими
со значением поля `image` в `projects.json`.

## Возможности

### Сайт

- Минималистичный дизайн в стиле Apple (шрифт Inter, пыльно-розовая палитра).
- Секции: About Me, Skills, сетка проектов, контакты.
- Страница отдельного проекта с описанием, стеком и ссылками.
- Адаптивная вёрстка (mobile-first).
- Автоматическая проверка существования изображений.
- Все контакты и ссылки управляются через `.env`.

### Бот

- Команда `/start` со списком проектов в inline-клавиатуре (вертикальный).
- При выборе проекта: картинка с диска, описание, стек и кнопки GitHub / сайт.
- Обработка ошибок при отсутствии `projects.json`.
- Загрузка токена из `.env` через `python-dotenv`.
