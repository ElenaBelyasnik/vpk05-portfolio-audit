# FastAPI — Тестовый бэкенд

## Описание
Простое тестовое приложение на FastAPI, возвращающее текущее время сервера.

## Запуск

1. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Запустите сервер:
   ```bash
   uvicorn main:app --reload
   ```

 4. Откройте в браузере:
    - [http://127.0.0.1:8000/time](http://127.0.0.1:8000/time)
    - [http://127.0.0.1:8000/date](http://127.0.0.1:8000/date)
    - [http://127.0.0.1:8000/datetime](http://127.0.0.1:8000/datetime)
    - [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) — Swagger UI

## Запуск через Docker

1. Соберите образ:
   ```bash
   docker build -t fastapi-app .
   ```

2. Запустите контейнер:
   ```bash
   docker run -p 8000:8000 fastapi-app
   ```

3. Откройте в браузере:
    - [http://127.0.0.1:8000/time](http://127.0.0.1:8000/time)
    - [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) — Swagger UI

## CI/CD — GitHub Actions

Workflow настроен в `.github/workflows/deploy.yml`. Он состоит из двух джоб:

1. **build-push** — собирает Docker-образ и пушит его в GitHub Container Registry.
2. **deploy** — подключается к серверу по SSH, скачивает образ и разворачивает контейнер.

### Необходимые секреты репозитория

Настройте в **Settings → Secrets and variables → Actions**:

| Секрет | Описание |
|---|---|
| `GITHUB_TOKEN` | Создаётся автоматически GitHub, используется для логина в GHCR. Секрет настраивать не нужно. |
| `SSH_HOST` | IP-адрес или домен сервера |
| `SSH_USERNAME` | Имя пользователя для SSH |
| `SSH_PRIVATE_KEY` | Приватный SSH-ключ (формат `-----BEGIN OPENSSH PRIVATE KEY-----`) |
| `SSH_PORT` | Порт SSH (по умолчанию `22`) |

### Ручной запуск

Можно запустить workflow через **Actions → "Build and Deploy" → Run workflow**.

## Возникшие проблемы и их решение

### 1. Не отправлялся push из-за прав токена
**Проблема:** VS Code использовал токен без прав на изменение файлов в `.github/workflows/`.
**Решение:** создали новый Personal Access Token с правами `repo` и `workflow`.

### 2. Force push не сработал — ветка не сдвинулась
**Проблема:** `git reset --soft` откатил коммит, но изменения остались в staging area. Удалённая ветка осталась на старом коммите.
**Решение:** выполнили `git reset --soft HEAD~1` → `git push --force-with-lease`.

### 3. Git отказывался пушить — локальная и удалённая ветки разошлись
**Проблема:** кто-то сделал push после force push, и Git не мог объединить изменения.
**Решение:** `git pull` → `git push`.

### 4. Контейнер не запускался на сервере — Docker не был установлен
**Проблема:** на сервере не было Docker, поэтому deploy падал.
**Решение:** установили Docker через `apt install -y docker-ce docker-ce-cli containerd.io`.

### 5. Образ не загружался на сервер через `docker pull`
**Проблема:** GHCR хранил образ с именем репозитория в верхнем регистре, но Docker требует только строчные буквы. Тег `latest` не был установлен.
**Решение:** собрали образ локально → `docker save` → скопировали на сервер через `scp` → `docker load` → `docker run`.

### 6. CI/CD не работал — deploy падал
**Проблема:** в workflow `IMAGE_NAME` брался из `${{ github.repository }}` — с заглавными буквами. Docker не мог найти образ из-за регистра.
**Решение:** заменили на строчные буквы: `elena-belyasnik/vpe04-test-github-actions-docker-gitflow`.

### 7. Конфликт имён в Docker
**Проблема:** `ghcr.io/ElenaBelyasnik/...` — Docker требует lowercase. `ghcr.io/elena-belyasnik/...` — Docker ищет образ, но образ в реестре с оригинальным именем.
**Решение:** загрузили образ вручную через `docker save/load`, а в workflow исправили имена на строчные.

### 8. Образ не пушится в GHCR — `owner not found`
**Проблема:** после переименования репозитория пуш в GHCR падал с `denied: not_found: owner not found`.
**Причина:** в workflow использовалось имя владельца `elena-belyasnik` (с дефисом), но GitHub-логин `ElenaBelyasnik` в lowercase — `elenabelyasnik` (без дефиса). GHCR не нашёл такого владельца.
**Решение:** исправили имя во всём workflow на `elenabelyasnik`, удалили старый orphaned-пакет, перезапустили workflow — обе джобы прошли успешно.

### 9. `GITHUB_TOKEN` не мог пушить в GHCR — `permission_denied: write_package`
**Проблема:** после перехода с PAT (`CR_PAT`) на автоматический `GITHUB_TOKEN` пуш падал с `denied: permission_denied: write_package`.
**Причина:** имя образа `ghcr.io/elenabelyasnik/vpe04-app` было привязано к пользователю, а `GITHUB_TOKEN` может пушить только в пакеты, привязанные к репозиторию.
**Решение:** имя образа формируется динамически из `github.repository` в lowercase → `ghcr.io/elenabelyasnik/vpe04-test-github-actions-docker-gitflow:main`. Пакет автоматически привязывается к репозиторию, и `GITHUB_TOKEN` получает право на пуш.
