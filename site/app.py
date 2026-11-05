"""Site-визитка на Flask: портфолио по данным из projects.json.

Приложение читает единую базу данных ``projects.json`` (в корне репозитория)
и рендерит две страницы:

- ``/`` — главная страница (About Me, Skills, сетка проектов, контакты);
- ``/project/<int:project_id>`` — страница отдельного проекта.

Запуск для разработки::

    flask --app site/app run --debug

Либо напрямую::

    python site/app.py
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from flask import Flask, abort, render_template

# Корень репозитория: <root>/site/app.py -> parent.parent == <root>
ROOT_DIR = Path(__file__).resolve().parent.parent
PROJECTS_FILE = ROOT_DIR / "projects.json"

# Изображения в JSON хранятся как "static/images/x.png" относительно сайта,
# физически файл лежит в <root>/site/static/images/.
STATIC_IMAGES_DIR = Path(__file__).resolve().parent / "static" / "images"

# Статичные данные главной страницы (при необходимости отредактируйте здесь).
PROFILE: dict[str, str] = {
    "name": "Елена Белясник",
    "role": "Backend Engineer & Vibe Coder",
    "tagline": "Проектирую и разрабатываю асинхронные сервисы, ботов и LLM-интеграции.",
}

SKILLS: list[str] = ["Python", "FastAPI", "Docker", "Oracle"]

CONTACTS: dict[str, str] = {
    "telegram": "https://t.me/elenabelyasnik",
    "email": "mailto:hello@example.com",
    "github": "https://github.com/ElenaBelyasnik",
}

logger = logging.getLogger(__name__)

app = Flask(__name__)


def _normalize_image_path(raw: str | None) -> str | None:
    """Возвращает url изображения, только если файл реально существует.

    Пути в ``projects.json`` записаны как ``static/images/<file>.png``
    относительно папки ``site``. Проверяем наличие файла на диске, чтобы
    не отдавать битые ссылки; при отсутствии возвращаем ``None``.
    """
    if not raw:
        return None
    relative = raw.removeprefix("static/")  # -> images/<file>.png
    candidate = STATIC_IMAGES_DIR / Path(relative).name
    if candidate.is_file():
        return f"/static/{relative}".replace("\\", "/")
    logger.warning("Файл изображения не найден на диске: %s (пропускаем)", candidate)
    return None


def load_projects() -> list[dict[str, Any]]:
    """Читает и валидирует список проектов из ``projects.json``.

    Raises:
        FileNotFoundError: если файл базы данных отсутствует.
        json.JSONDecodeError: если файл повреждён (не является валидным JSON).
    """
    if not PROJECTS_FILE.is_file():
        raise FileNotFoundError(f"Не найден файл данных: {PROJECTS_FILE}")
    with PROJECTS_FILE.open(encoding="utf-8-sig") as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        raise ValueError("Ожидался JSON-массив проектов на верхнем уровне")

    projects: list[dict[str, Any]] = []
    for index, item in enumerate(data):
        if not isinstance(item, dict):
            logger.warning("Элемент %d не является объектом — пропускаем", index)
            continue
        try:
            project_id = int(item["id"])
        except (KeyError, TypeError, ValueError):
            logger.warning("У элемента %d отсутствует корректный id — пропускаем", index)
            continue
        projects.append(
            {
                "id": project_id,
                "title": str(item.get("title", f"Проект {project_id}")),
                "description": str(item.get("description", "")),
                "tech": [str(t) for t in item.get("tech", []) if t],
                "github": str(item.get("github", "")),
                "image_url": _normalize_image_path(item.get("image")),
            }
        )
    return projects


@app.template_filter("first_line")
def first_line(text: str, limit: int = 140) -> str:
    """Краткое описание для карточки: первая «строка» с ограничением длины."""
    text = " ".join(str(text).split())
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return f"{cut}…"


@app.errorhandler(FileNotFoundError)
@app.errorhandler(json.JSONDecodeError)
@app.errorhandler(ValueError)
def handle_data_error(error: Exception) -> str:
    """Понятная страница ошибки при проблемах с projects.json."""
    logger.exception("Ошибка загрузки данных портфолио")
    return (
        "<h1>Данные недоступны</h1>"
        f"<p>Не удалось загрузить <code>projects.json</code>: {error}</p>"
        '<p><a href="/">На главную</a></p>'
    ), 500


@app.route("/")
def index() -> str:
    """Главная страница: профиль, навыки, сетка проектов, контакты."""
    projects = load_projects()
    return render_template(
        "index.html",
        profile=PROFILE,
        skills=SKILLS,
        contacts=CONTACTS,
        projects=projects,
    )


@app.route("/project/<int:project_id>")
def project_detail(project_id: int) -> str:
    """Страница отдельного проекта по id из projects.json."""
    projects = load_projects()
    project = next((p for p in projects if p["id"] == project_id), None)
    if project is None:
        abort(404, description=f"Проект с id={project_id} не найден в projects.json")
    return render_template(
        "project.html",
        profile=PROFILE,
        contacts=CONTACTS,
        project=project,
    )


@app.errorhandler(404)
def handle_404(error: object) -> str:
    """Страница 404 для несуществующих маршрутов и проектов."""
    return (
        "<h1>Страница не найдена</h1>"
        '<p><a href="/">Вернуться на главную</a></p>'
    ), 404


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(host="127.0.0.1", port=5000, debug=True)
