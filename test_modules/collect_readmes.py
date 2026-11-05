#!/usr/bin/env python3
"""
Скрипт для рекурсивного сбора всех README.md файлов из директории C:\projects.

Каждый найденный файл копируется в drafts/all_projects_readme с переименованием,
добавляющим имя родительской папки проекта, чтобы избежать конфликтов имён.
"""

import os
import shutil
import sys
from pathlib import Path
from typing import Tuple

# Константы
SOURCE_DIR = Path(r"C:\projects")
# Корень проекта — parent.parent от test_modules
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "drafts" / "all_projects_readme"

# Папки, которые нужно игнорировать при обходе (начинаются с точки)
IGNORED_PREFIXES = (".",)


def is_ignored(directory: Path) -> bool:
    """Проверяет, начинается ли имя директории с точки."""
    return directory.name.startswith(IGNORED_PREFIXES)


def generate_output_name(source_path: Path) -> Path:
    """
    Генерирует новое имя файла, добавляя имя родительской папки.

    Например: C:/projects/VP-01-bot/README.md -> VP-01-bot_README.md
    """
    parent_name = source_path.parent.name
    return Path(f"{parent_name}_{source_path.name}")


def collect_readmes(source_dir: Path, output_dir: Path) -> Tuple[int, int]:
    """Основная логика сбора README-файлов."""
    # Создаём целевую директорию
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"[INFO] Целевая директория: {output_dir}")

    copied_count = 0
    error_count = 0

    for root_dir, dirs, files in os.walk(str(source_dir)):
        root_path = Path(root_dir)
        # Фильтруем dirs на месте, чтобы не заходить в игнорируемые папки
        dirs[:] = [d for d in dirs if not is_ignored(Path(d))]

        for filename in files:
            if filename.lower() != "readme.md":
                continue

            source_path = root_path / filename
            output_filename = generate_output_name(source_path)
            dest_path = output_dir / output_filename

            try:
                shutil.copy2(source_path, dest_path)
                print(f"[OK]   {source_path} -> {dest_path}")
                copied_count += 1
            except PermissionError as e:
                print(f"[WARN] Нет доступа к файлу: {source_path} - {e}")
                error_count += 1
            except OSError as e:
                print(f"[ERR]  Ошибка при копировании {source_path} - {e}")
                error_count += 1

    # Итоговая статистика
    print(f"\n{'=' * 60}")
    print(f"ИТОГО: скопировано {copied_count}, ошибок {error_count}")
    print(f"{'=' * 60}")

    return copied_count, error_count


def main() -> None:
    """Точка входа в скрипт."""
    if not SOURCE_DIR.exists():
        print(f"[ERR] Исходная директория не существует: {SOURCE_DIR}")
        sys.exit(1)

    print(f"[INFO] Поиск README.md файлов в: {SOURCE_DIR}")
    print()

    copied, errors = collect_readmes(SOURCE_DIR, OUTPUT_DIR)

    if errors > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
