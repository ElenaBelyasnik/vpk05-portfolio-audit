# SQL Learning Project

Проект для изучения SQL на примере SQLite базы данных.

---

## Структура проекта

```
VPc04_learning/
├── learning.db                 # SQLite база данных
├── sql/
│   └── queries.sql             # SQL-запросы (INSERT, UPDATE, DELETE, SELECT, JOIN)
├── code/
│   ├── seed.py                 # Генератор тестовых данных (Products + Orders)
│   ├── run_queries.py          # Выполнение SQL-запросов из файла
│   └── select_join_examples.py # Примеры SELECT и JOIN (из предыдущих уроков)
├── screenshots/                # Скриншоты результатов (для отчёта)
├── insert_products_explained.md  # Документация по вставке товаров
├── Select_Explained.md         # Документация по SELECT и JOIN
├── update_instruction.md       # Документация по UPDATE
├── sql_insert_guide.md         # Документация по массовому INSERT
└── README.md                   # Этот файл
```

---

## Таблицы базы данных

### Products (товары)

```sql
CREATE TABLE Products (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Description TEXT,
    Category TEXT,
    Price REAL,
    SKU TEXT UNIQUE
);
```

**Категории товаров (релевантные):**

| Категория | Примеры товаров |
|-----------|-----------------|
| Электроника | Смартфон XYZ, Ноутбук Pro, Умные часы |
| Книги | Книга по Python, Книга по SQL, Книга по дизайну |
| Мебель | Офисное кресло, Письменный стол, Диван угловой |
| Спорт и отдых | Беговая дорожка, Велосипед, Гантели |
| Продукты | Яблоки, Бананы, Молоко, Хлеб |
| Бытовая техника | Кофемашина, Холодильник, Стиральная машина |
| Инструменты | Дрель, Набор отвёрток, Молоток |
| Автомобильные | Видеорегистратор, Авточехлы, Компрессор |
| Одежда и аксессуары | Рюкзак, Кепка, Ремень кожаный |
| Для дома | Постельное бельё, Полотенце, Штора |
| Косметика и здоровье | Шампунь, Зубная паста, Крем для лица |

### Orders (заказы)

```sql
CREATE TABLE Orders (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Product_ID INTEGER,
    Quantity INTEGER,
    Order_Date DATE,
    FOREIGN KEY (Product_ID) REFERENCES Products(ID)
);
```

---

## Быстрый старт

### 1. Генерация тестовых данных

```bash
python code/seed.py
```

**Что делает:**
- Создаёт таблицы Products и Orders (если нет)
- Генерирует **105 товаров** с релевантными категориями (>= 100 по заданию)
- Генерирует **150 заказов** (>= 100 по заданию)
- Выводит статистику и **проверку релевантности категорий**

**Пример вывода:**

```
✓ В таблице Products уже есть 105 товаров (минимум 100)
✓ В таблице Orders уже есть 150 заказов

📊 СТАТИСТИКА БАЗЫ ДАННЫХ

📦 Products:
  • Всего товаров: 105
  • Средняя цена: 13750.39 ₽

📋 Orders:
  • Всего заказов: 150

✅ ПРОВЕРКА РЕЛЕВАНТНОСТИ КАТЕГОРИЙ
✅ Смартфон XYZ: Электроника
✅ Книга по Python: Книги
✅ Беговая дорожка: Спорт и отдых
✅ Яблоки: Продукты
✅ Холодильник: Бытовая техника
✅ Офисное кресло: Мебель
✅ Веб-камера HD: Электроника

✅ ВСЕ ТОВАРЫ В ПРАВИЛЬНЫХ КАТЕГОРИЯХ!
```

### 2. Выполнение SQL-запросов

```bash
python code/run_queries.py
```

**Что делает:**
- Читает `sql/queries.sql`
- Выполняет все запросы
- Выводит результаты SELECT-запросов

### 3. Открыть базу в DBeaver

1. Откройте DBeaver
2. Создайте новое соединение → SQLite
3. Выберите файл `learning.db`
4. Перейдите во вкладку "SQL Editor"
5. Откройте `sql/queries.sql` и выполните запросы

---

## Содержимое sql/queries.sql

### Часть 1: Базовые операции

| Тип | Количество | Описание |
|-----|------------|----------|
| INSERT (ручные) | 3 | Вставка товаров "Яблоки", "Бананы", заказа |
| INSERT (массовая) | 1 | Вставка 5 товаров за один запрос |
| UPDATE | 3 | Скидка 10%, исправление цены по SKU, обновление описания |
| DELETE | 1 | Удаление тестовых записей с безопасным WHERE |

### Часть 2: Чтение и анализ

| Запрос | Описание |
|--------|----------|
| SELECT + WHERE + ORDER BY + LIMIT | Топ-10 по цене, топ-5 по категории |
| Агрегация + GROUP BY + HAVING | Статистика по категориям (COUNT(*) > 5) |
| LIKE (case-insensitive) | Поиск через UPPER(column) LIKE 'ABC%' |
| Примечание: UPPER() в SQLite работает только с ASCII | Для русского языка используйте `Name LIKE 'Б%'` |
| JOIN | Заказы с названиями товаров, сумма по категориям |

### Часть 3: Безопасность

| Пример | Описание |
|--------|----------|
| ❌ Небезопасная конкатенация | Демонстрация SQL-инъекции |
| ✅ Параметризованный запрос | Использование `?` placeholders |

---

## Примеры запросов

### INSERT: Массовая вставка

```sql
INSERT INTO Products (Name, Description, Category, Price, SKU)
VALUES 
    ('Молоко', 'Свежее молоко 3.2%, 1 л', 'Продукты', 89.90, 'ART-99997-C'),
    ('Хлеб', 'Белый хлеб, 400 г', 'Продукты', 45.00, 'ART-99996-D'),
    ('Сыр', 'Твёрдый сыр, 200 г', 'Продукты', 250.00, 'ART-99995-A');
```

### UPDATE: Скидка категории

```sql
UPDATE Products
SET Price = ROUND(Price * 0.90, 2)
WHERE Category = 'Продукты';
```

### SELECT: Агрегация с GROUP BY и HAVING

```sql
SELECT 
    Category,
    COUNT(*) AS product_count,
    ROUND(AVG(Price), 2) AS avg_price
FROM Products
GROUP BY Category
HAVING COUNT(*) > 5;
```

### SELECT: Поиск через UPPER (case-insensitive)

```sql
SELECT Name, Price, Category
FROM Products
WHERE UPPER(Name) LIKE 'Б%';
```

### JOIN: Заказы с товарами и суммой по категориям

```sql
SELECT 
    p.Category,
    COUNT(o.ID) AS total_orders,
    SUM(o.Quantity) AS total_items_sold,
    ROUND(SUM(o.Quantity * p.Price), 2) AS total_revenue
FROM Orders o
JOIN Products p ON o.Product_ID = p.ID
GROUP BY p.Category
ORDER BY total_revenue DESC;
```

### Безопасность: Параметризованный запрос (Python)

```python
# ❌ НЕБЕЗОПАСНО (SQL-инъекция):
user_input = "1 OR 1=1"
query = f"SELECT * FROM Products WHERE ID = {user_input}"

# ✅ БЕЗОПАСНО (параметризованный):
cursor.execute("SELECT * FROM Products WHERE ID = ?", (user_input,))
```

---

## Статистика базы данных

После выполнения `seed.py`:

| Таблица | Количество записей | Статус |
|---------|-------------------|--------|
| Products | **105 товаров** | ✅ >= 100 |
| Orders | **150 заказов** | ✅ >= 100 |

**Категории товаров:**
- Электроника: 20 товаров
- Спорт и отдых: 20 товаров
- Продукты: 20 товаров
- Мебель: 15 товаров
- Книги: 15 товаров
- Бытовая техника: 15 товаров

---

## Документация

| Файл | Описание |
|------|----------|
| `insert_products_explained.md` | Вставка данных (INSERT) с примерами |
| `Select_Explained.md` | Полное руководство по SELECT и JOIN |
| `update_instruction.md` | Инструкция по оператору UPDATE |
| `sql_insert_guide.md` | Массовая вставка данных |

---

## Выполнение задания

### Требования:

- [x] Таблицы Products и Orders созданы и заполнены
- [x] Products содержит **105 товаров** (>= 100)
- [x] Orders содержит **150 заказов** (>= 100)
- [x] Все товары имеют **релевантные категории** (проверено)
- [x] `sql/queries.sql` содержит все требуемые запросы
- [x] 3 ручных INSERT + 1 массовая вставка
- [x] 3 UPDATE с WHERE (скидка, правка цены по SKU)
- [x] 1 DELETE с безопасным WHERE
- [x] SELECT с WHERE + ORDER BY + LIMIT
- [x] Агрегация с GROUP BY + HAVING
- [x] LIKE через UPPER(column) LIKE 'ABC%'
- [x] JOIN: сводная выборка заказов с товарами и суммой по категориям
- [x] Демонстрация безопасности (небезопасная vs параметризованная конкатенация)
- [x] `code/seed.py` для генерации данных
- [x] `insert_products_explained.md` документация
- [x] Папки `/sql`, `/screenshots`, `/code` созданы

---

## Полезные команды

```bash
# Генерация данных
python code/seed.py

# Выполнение SQL-запросов
python code/run_queries.py

# Проверка количества записей
python -c "import sqlite3; c=sqlite3.connect('learning.db'); print('Products:', c.execute('SELECT COUNT(*) FROM Products').fetchone()[0]); print('Orders:', c.execute('SELECT COUNT(*) FROM Orders').fetchone()[0])"
```

---

## Автор

NLP-Core-Team SQL Learning Project
