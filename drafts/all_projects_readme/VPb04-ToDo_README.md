# Система управления задачами (Todo-лист)

Простая система управления задачами на Python с использованием ООП.

## Структура проекта

```
todo_system/
├── __init__.py          # Инициализация пакета, экспорты классов
├── storage/
│   └── __init__.py      # Глобальные словари для хранения объектов
├── task/
│   ├── __init__.py      # Экспорт класса Task
│   └── models.py        # Модель Task
├── project/
│   ├── __init__.py      # Экспорт класса Project
│   └── models.py        # Модель Project
├── user/
│   ├── __init__.py      # Экспорт класса User
│   └── models.py        # Модель User
└── io/
    ├── __init__.py      # Экспорт функций сохранения/загрузки
    └── json_storage.py  # Реализация JSON-хранения

main.py                  # Точка входа, демонстрация работы
todo_data.json           # Файл для сохранения данных
```

## Классы

### Task (Задача)
Базовый элемент системы. Хранит информацию о задаче:
- ID, название, описание
- Статус выполнения
- Приоритет (1-низкий, 2-средний, 3-высокий)
- Даты: создания, выполнения (опционально)
- ID проекта (опционально)

### Project (Проект)
Группирует задачи по темам или целям:
- ID, название, описание
- Список задач проекта
- Методы для работы с задачами и подсчёта прогресса

### User (Пользователь)
Владелец задач и проектов:
- ID, имя
- Списки задач и проектов
- Методы поиска и управления

## Запуск

```bash
python main.py
```

## Использование

```python
from todo_system import Task, Project, User
from todo_system.io import save_to_json, load_from_json

# Создать задачу
task = Task("Купить продукты", "Молоко, хлеб", priority=2)

# Создать проект
project = Project("Работа", "Рабочие задачи")
project.add_task(task.get_task_id())

# Создать пользователя
user = User("Иван")
user.add_task(task.get_task_id())
user.add_project(project.get_project_id())

# Использовать методы
task.mark_as_done()
print(task.get_info())
print(project.get_progress())

# Сохранить данные в JSON
save_to_json("todo_data.json")

# Загрузить данные из JSON
load_from_json("todo_data.json")
```

## Сохранение данных

Данные сохраняются в формате JSON:

- **Функция сохранения:** `save_to_json(filepath)`
- **Функция загрузки:** `load_from_json(filepath)`
- **Файл по умолчанию:** `todo_data.json`

Формат JSON-файла:

```json
{
  "tasks": [
    {
      "task_id": 1,
      "title": "Купить продукты",
      "description": "Молоко, хлеб",
      "is_done": true,
      "due_date": null,
      "created_at": "2026-05-16T23:31:55.566902",
      "priority": 2,
      "project_id": null
    }
  ],
  "projects": [...],
  "users": [...]
}
```
