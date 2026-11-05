# База данных homework-2.db

Проект базы данных для хранения рецептов и продуктов с реализацией связи **многие-ко-многим** (many-to-many).

---

## 📁 Расположение

```
C:\SQLite_DB\homework-2.db
```

---

## 📊 Структура базы данных

### Таблицы

| Таблица | Описание |
|---------|----------|
| `products` | Хранит информацию о продуктах питания |
| `recipes` | Хранит информацию о рецептах блюд |
| `recipe_products` | Связующая таблица для связи многие-ко-многим между продуктами и рецептами |

---

## 🏗 DDL-команды

### Таблица `products`

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    unit TEXT NOT NULL,
    description TEXT
);
```

| Колонка | Тип | Описание |
|---------|-----|----------|
| `id` | INTEGER | Первичный ключ, автоинкремент |
| `name` | TEXT | Название продукта (NOT NULL) |
| `unit` | TEXT | Единица измерения (г, мл, шт и т.д.) (NOT NULL) |
| `description` | TEXT | Описание продукта |

---

### Таблица `recipes`

```sql
CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    preparation_time INTEGER,
    servings INTEGER
);
```

| Колонка | Тип | Описание |
|---------|-----|----------|
| `id` | INTEGER | Первичный ключ, автоинкремент |
| `name` | TEXT | Название рецепта (NOT NULL) |
| `description` | TEXT | Описание рецепта |
| `preparation_time` | INTEGER | Время приготовления (минуты) |
| `servings` | INTEGER | Количество порций |

---

### Таблица `recipe_products` (junction table)

```sql
CREATE TABLE recipe_products (
    recipe_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity REAL NOT NULL,
    CONSTRAINT recipe_products_pk PRIMARY KEY (recipe_id, product_id),
    CONSTRAINT recipe_products_recipe_fk 
        FOREIGN KEY (recipe_id) 
        REFERENCES recipes(id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    CONSTRAINT recipe_products_product_fk 
        FOREIGN KEY (product_id) 
        REFERENCES products(id) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE
);
```

| Колонка | Тип | Описание |
|---------|-----|----------|
| `recipe_id` | INTEGER | Внешний ключ на `recipes.id` (NOT NULL) |
| `product_id` | INTEGER | Внешний ключ на `products.id` (NOT NULL) |
| `quantity` | REAL | Количество продукта в рецепте (NOT NULL) |

---

## 🔑 Ключи

### Первичные ключи (Primary Keys)

| Таблица | Первичный ключ | Тип |
|---------|----------------|-----|
| `products` | `id` | Одноколоночный, AUTOINCREMENT |
| `recipes` | `id` | Одноколоночный, AUTOINCREMENT |
| `recipe_products` | `(recipe_id, product_id)` | Составной (composite PK) |

### Внешние ключи (Foreign Keys)

| Таблица | Внешний ключ | Ссылается на | ON DELETE | ON UPDATE |
|---------|--------------|--------------|-----------|-----------|
| `recipe_products.recipe_id` | `recipe_products_recipe_fk` | `recipes(id)` | CASCADE | CASCADE |
| `recipe_products.product_id` | `recipe_products_product_fk` | `products(id)` | RESTRICT | CASCADE |

---

## 🔗 Схема связей

```
┌─────────────┐         ┌───────────────────┐         ┌─────────────┐
│  products   │◄────────│ recipe_products   │────────►│  recipes    │
│             │  FK:    │                   │  FK:    │             │
│  id (PK)    │         │  recipe_id (FK)   │         │  id (PK)    │
│  name       │         │  product_id (FK)  │         │  name       │
│  unit       │         │  quantity         │         │  description│
│  description│         │  PK: (recipe_id,  │         │  prep_time  │
└─────────────┘         │      product_id)  │         │  servings   │
                        └───────────────────┘         └─────────────┘
                        (связь многие-ко-многим)
```

### Пояснение связей

1. **Один рецепт содержит много продуктов** → через `recipe_products.recipe_id`
2. **Один продукт входит во много рецептов** → через `recipe_products.product_id`
3. **Защита данных:**
   - Нельзя удалить продукт, если он используется в рецептах (`ON DELETE RESTRICT`)
   - При удалении рецепта все его связи удаляются автоматически (`ON DELETE CASCADE`)
   - При изменении ID ссылки обновляются автоматически (`ON UPDATE CASCADE`)

---

## 📋 Данные в таблицах

### Таблица `products`

| id | name | unit | description |
|----|------|------|-------------|
| 1 | Мука | г | Пшеничная мука высшего сорта |
| 2 | Сахар | г | Белый сахар-песок |
| 3 | Яйца | шт | Куриные яйца |
| 4 | Молоко | мл | Пастеризованное молоко 3.2% |
| 5 | Сливочное масло | г | Масло сливочное 82.5% |
| 6 | Какао-порошок | г | Натуральный какао-порошок |
| 7 | Разрыхлитель | г | Разрыхлитель для теста |
| 8 | Ванильный сахар | г | Ванильный сахар |

---

### Таблица `recipes`

| id | name | description | preparation_time | servings |
|----|------|-------------|------------------|----------|
| 1 | Бисквитный торт | Классический бисквитный торт с кремом | 60 | 8 |
| 2 | Шоколадное печенье | Хрустящее шоколадное печенье | 30 | 12 |
| 3 | Кекс ванильный | Нежный ванильный кекс | 45 | 10 |

---

### Таблица `recipe_products`

| recipe_id | product_id | quantity |
|-----------|------------|----------|
| 1 | 1 | 200 | (Бисквитный торт → Мука) |
| 1 | 2 | 150 | (Бисквитный торт → Сахар) |
| 1 | 3 | 4 | (Бисквитный торт → Яйца) |
| 1 | 4 | 100 | (Бисквитный торт → Молоко) |
| 1 | 5 | 50 | (Бисквитный торт → Сливочное масло) |
| 2 | 1 | 250 | (Шоколадное печенье → Мука) |
| 2 | 2 | 100 | (Шоколадное печенье → Сахар) |
| 2 | 3 | 2 | (Шоколадное печенье → Яйца) |
| 2 | 5 | 100 | (Шоколадное печенье → Сливочное масло) |
| 2 | 6 | 30 | (Шоколадное печенье → Какао-порошок) |
| 2 | 7 | 5 | (Шоколадное печенье → Разрыхлитель) |
| 3 | 1 | 300 | (Кекс ванильный → Мука) |
| 3 | 2 | 200 | (Кекс ванильный → Сахар) |
| 3 | 3 | 3 | (Кекс ванильный → Яйца) |
| 3 | 4 | 200 | (Кекс ванильный → Молоко) |
| 3 | 5 | 150 | (Кекс ванильный → Сливочное масло) |
| 3 | 8 | 10 | (Кекс ванильный → Ванильный сахар) |
| 3 | 7 | 10 | (Кекс ванильный → Разрыхлитель) |

---

## 📝 Примеры SQL-запросов

### Получить все продукты для рецепта «Бисквитный торт»

```sql
SELECT p.name, rp.quantity, p.unit
FROM recipe_products rp
JOIN products p ON rp.product_id = p.id
JOIN recipes r ON rp.recipe_id = r.id
WHERE r.name = 'Бисквитный торт';
```

### Получить все рецепты, в которых используется «Мука»

```sql
SELECT r.name, rp.quantity, p.unit
FROM recipe_products rp
JOIN recipes r ON rp.recipe_id = r.id
JOIN products p ON rp.product_id = p.id
WHERE p.name = 'Мука';
```

### Подсчитать общее количество продуктов в каждом рецепте

```sql
SELECT r.name, COUNT(rp.product_id) AS product_count
FROM recipes r
LEFT JOIN recipe_products rp ON r.id = rp.recipe_id
GROUP BY r.id;
```

---

## ⚙️ Настройка SQLite

Для работы внешних ключей в SQLite необходимо включить поддержку FK:

```sql
PRAGMA foreign_keys = ON;
```

**Важно:** Эта команда должна выполняться при каждом подключении к базе данных.

---

## 📌 Примечания

- База данных использует **составной первичный ключ** в таблице `recipe_products` для предотвращения дублирования связей
- Реализована **полная целостность данных** через внешние ключи
- Модель готова для использования в веб-приложении или справочнике рецептов
