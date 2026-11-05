# CLI AI Prompt Agent

Консольное приложение для автоматического сравнения двух AI-промптов через API GenAPI (модель gpt-5-6-luna).

## Структура проекта

```
vpf03_cli_ai_agent/
├── .env                  # Переменные окружения (API-ключ, base_url, model)
├── .gitignore            # Игнорируемые файлы Git
├── requirements.txt      # Зависимости Python
├── README.md             # Этот файл
├── ProgressOfWork.md     # Ход работ над проектом
├── prompts.json          # Файл с промптами (ID 1 и 2)
├── main.py               # Точка входа
├── cli/
│   ├── __init__.py
│   ├── menu.py           # Запрос параметров (temperature, max_tokens)
│   ├── api_client.py     # Отправка запросов к AI
│   ├── statistics.py     # Сохранение статистики в JSON
│   └── comparator.py     # Сравнение двух ответов + сохранение в JSON и MD
└── utils/
    ├── __init__.py
    └── color_utils.py    # Цветной вывод (colorama)
```

## Установка

1. Убедитесь, что установлен Python 3.12+.

2. Активируйте виртуальное окружение:

   **Windows (PowerShell):**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Настройка

1. Откройте файл `.env` и введите свои значения:
   ```env
   OPENAI_API_KEY=ваш_api_ключ_genapi
   OPENAI_BASE_URL=https://proxy.gen-api.ru/v1
   OPENAI_MODEL=gpt-5-6-luna
   ```

2. Получить API-ключ GenAPI: [gen-api.ru](https://gen-api.ru/).

## Запуск

```powershell
python main.py
```

## Использование

При запуске программа **автоматически** выполняет:

1. **Запрашивает параметры 1 раз:**
   - **Temperature** (0.0–1.0, по умолчанию 0.2)
   - **Max tokens** (по умолчанию 1000)

2. **Прогоняет оба промпта** (из `prompts.json`):
   - Промпт 1 (`id: 1`) с `test_input`
   - Промпт 2 (`id: 2`) с `test_input` + `example` (few-shot)

3. **Сравнивает ответы** через AI по трём критериям:
   - Соответствие JSON-формату (Да/Нет + пояснение)
   - Полезность шагов (steps) — 1–2 предложения
   - Лаконичность заметок (notes) — 1–2 предложения

4. **Сохраняет результаты** в три файла (перезаписывает при каждом запуске):
   - `ai_query_statistic.json` — статистика обоих промптов
   - `prompt_comparison.json` — результат сравнения в формате JSON
   - `prompt_comparison.md` — результат сравнения в виде таблицы Markdown

5. **Выводит результат** в консоль в структурированном виде.

## Файлы результатов

### ai_query_statistic.json
```json
{
  "timestamp": "2026-08-19T12:00:00",
  "temperature": 0.2,
  "max_tokens": 1000,
  "prompts": [
    {
      "prompt_id": 1,
      "prompt_name": "План утренней зарядки (исходный)",
      "user_question": "...",
      "answer": "...",
      "model": "gpt-5-6-luna",
      "tokens": { "total": 606, "prompt": 82, "completion": 524 }
    },
    ...
  ]
}
```

### prompt_comparison.json
```json
{
  "timestamp": "...",
  "model": "gpt-5-6-luna",
  "temperature": 0.2,
  "max_tokens": 1000,
  "prompt_1_name": "...",
  "prompt_2_name": "...",
  "answer_1": "...",
  "answer_2": "...",
  "comparison": {
    "format_compliance": {
      "prompt_1": "Да",
      "prompt_2": "Да",
      "explanation": "Оба ответа соответствуют формату."
    },
    "steps_usefulness": {
      "prompt_1": "...",
      "prompt_2": "..."
    },
    "notes_conciseness": {
      "prompt_1": "...",
      "prompt_2": "..."
    }
  },
  "conclusion": "..."
}
```

### prompt_comparison.md
```markdown
# Сравнение промптов: ... vs ...

| Критерий | Промпт 1 | Промпт 2 |
|---|---|---|
| Соответствие JSON-формату | Да | Да |
| Полезность шагов (steps) | ... | ... |
| Лаконичность заметок (notes) | ... | ... |

## Итоговый вывод
...
```

## Зависимости

- `openai` — клиент для работы с GenAPI (OpenAI-совместимый формат)
- `python-dotenv` — загрузка переменных окружения из `.env`
- `colorama` — цветной вывод в консоль

## Известные проблемы

### Вывод сравнения

Для корректного отображения в VS Code Terminal вывод сравнения выполнен без цветов.
Остальные части приложения (статистика, ответы) используют цветной вывод.

