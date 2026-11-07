"""Telegram-бот портфолио на aiogram 3.x.

Читает ``projects.json`` из корня репозитория и демонстрирует каждый проект
через inline-клавиатуру. Изображения бот отправляет, только если файл
физически существует в ``site/static/images/``.

Запуск::

    python bot/main.py
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any, Final

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    Message,
    WebAppInfo,
)
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ---------------------------------------------------------------------------
# Константы
# ---------------------------------------------------------------------------
ROOT_DIR: Final[Path] = Path(__file__).resolve().parent.parent
PROJECTS_FILE: Final[Path] = ROOT_DIR / "projects.json"
STATIC_IMAGES_DIR: Final[Path] = ROOT_DIR / "site" / "static" / "images"

# Значение по умолчанию для SITE_URL (можно переопределить в .env).
DEFAULT_SITE_URL: Final[str] = "http://127.0.0.1:5000"

# ---------------------------------------------------------------------------
# Логирование
# ---------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Загрузка данных
# ---------------------------------------------------------------------------


def _load_projects() -> list[dict[str, Any]]:
    """Читает и валидирует ``projects.json``.

    Raises:
        FileNotFoundError: если файл отсутствует.
        json.JSONDecodeError: если файл повреждён.
    """
    if not PROJECTS_FILE.is_file():
        raise FileNotFoundError(f"Не найден файл данных: {PROJECTS_FILE}")
    with PROJECTS_FILE.open(encoding="utf-8-sig") as fh:
        data: Any = json.load(fh)
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
                "image": str(item.get("image", "")),
            }
        )
    return projects


def _image_path(raw: str | None) -> Path | None:
    """Возвращает абсолютный путь к файлу изображения, если он существует."""
    if not raw:
        return None
    filename: str = Path(raw).name  # e.g. "lead_intake.png"
    candidate: Path = STATIC_IMAGES_DIR / filename
    return candidate if candidate.is_file() else None


def _format_project_message(proj: dict[str, Any]) -> str:
    """Формирует текст сообщения о проекте для Telegram."""
    lines: list[str] = [
        f"📂 {proj['title']}",
        "",
        proj["description"],
        "",
        "🛠 Стек: " + ", ".join(proj["tech"]) if proj["tech"] else "🛠 Стек: не указан",
    ]
    return "\n".join(lines)


def _build_project_keyboard(proj: dict[str, Any]) -> list[list[Any]]:
    """Создаёт inline-клавиатуру с кнопками GitHub и ссылкой на сайт."""
    site_url: str = os.environ.get("SITE_URL", DEFAULT_SITE_URL).rstrip("/")
    builder = InlineKeyboardBuilder()

    if proj.get("github"):
        builder.button(text="🔗 Открыть на GitHub", url=proj["github"])

    builder.button(
        text="🌐 Посмотреть на сайте",
        url=f"{site_url}/project/{proj['id']}",
    )

    return builder.as_markup(resize_keyboard=True)


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
router: Router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """Команда /start: приветствие + список проектов."""
    try:
        projects = _load_projects()
    except (FileNotFoundError, ValueError) as exc:
        await message.answer(f"⚠️ Не удалось загрузить данные: {exc}")
        logger.error("Ошибка загрузки projects.json: %s", exc)
        return

    if not projects:
        await message.answer(
            "📭 Проектов пока нет. Заполните ``projects.json`` и попробуйте снова."
        )
        return

    builder = InlineKeyboardBuilder()
    for proj in projects:
        builder.button(
            text=f"📂 {proj['title']}",
            callback_data=f"project_{proj['id']}",
        )

    builder.adjust(1)  # Каждая кнопка — отдельная строка

    await message.answer(
        "👋 Привет! Я — Бот-портфолио.\n\n"
        "Выберите проект, чтобы увидеть подробности:",
        reply_markup=builder.as_markup(),
    )


@router.callback_query(F.data.startswith("project_"))
async def cb_show_project(callback: CallbackQuery) -> None:
    """Callback-обработчик: показывает детали проекта по ID."""
    data: str = callback.data  # e.g. "project_3"
    try:
        project_id = int(data.split("_", 1)[1])
    except (IndexError, ValueError):
        await callback.answer("Некорректный запрос.", show_alert=True)
        return

    try:
        projects = _load_projects()
    except (FileNotFoundError, ValueError) as exc:
        logger.error("Ошибка загрузки projects.json: %s", exc)
        await callback.answer(
            "⚠️ Не удалось загрузить данные. Попробуйте позже.",
            show_alert=True,
        )
        return

    project = next((p for p in projects if p["id"] == project_id), None)
    if project is None:
        await callback.answer("Проект не найден.", show_alert=True)
        return

    # Отправляем изображение (если есть на диске).
    img = _image_path(project.get("image"))
    if img:
        await callback.message.answer_photo(photo=FSInputFile(str(img)))

    # Текст + inline-кнопки.
    await callback.message.answer(
        text=_format_project_message(project),
        reply_markup=_build_project_keyboard(project),
    )

    await callback.answer()


# ---------------------------------------------------------------------------
# Инициализация и запуск
# ---------------------------------------------------------------------------


def create_dp() -> Dispatcher:
    """Создаёт и настраивает диспетчер с зарегистрированным router."""
    dp: Dispatcher = Dispatcher()
    dp.include_router(router)
    return dp


def main() -> None:
    """Точка входа: загружает .env, запускает бота."""
    load_dotenv(ROOT_DIR / ".env")
    bot_token: str | None = os.environ.get("BOT_TOKEN")
    if not bot_token:
        logger.error(
            "BOT_TOKEN не найден в .env. "
            "Скопируйте .env.example в .env и подставьте токен."
        )
        raise SystemExit(1)

    bot: Bot = Bot(token=bot_token)
    dp: Dispatcher = create_dp()

    logger.info("🚀 Бот портфолио запускается...")
    dp.run_polling(bot, skip_updates=True)


if __name__ == "__main__":
    main()
