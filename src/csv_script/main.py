"""
Точка входа в приложение.

Пример запуска:
    python3 main.py --files dataset1.csv dataset2.csv --report average-gdp

Архитектура:
    main.py знает только об интерфейсе отчёта: функция принимает data
    и возвращает (headers, rows). Ему не важно, какой именно отчёт
    вызывается — это определяется параметром --report и реестром.

    Это значит, что main.py вообще не нужно менять при добавлении
    нового отчёта.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

# Добавляем src/ в путь поиска модулей для запуска напрямую
sys.path.insert(0, str(Path(__file__).parent.parent))

from tabulate import tabulate

from csv_script.reader import read_csv_files
from csv_script.reports import get_available_reports, get_report


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Разбор и валидация аргументов командной строки.

    Использует стандартную библиотеку argparse, которая:
    - автоматически генерирует --help,
    - проверяет наличие обязательных аргументов,
    - проверяет, что --report содержит допустимое значение (через choices),
    - при ошибке выводит понятное сообщение и завершает программу с кодом 2.

    Args:
        argv: Список строк-аргументов. Если None, argparse берёт sys.argv[1:].
              Передача argv явно нужна для тестирования — мы можем вызвать
              parse_args(["--files", "a.csv", "--report", "average-gdp"])
              без реального запуска скрипта из командной строки.

    Returns:
        Объект Namespace с атрибутами:
        - files: список строк (пути к файлам).
        - report: строка (имя отчёта).

    Raises:
        SystemExit: При невалидных аргументах (argparse вызывает sys.exit(2)).
    """
    # Создаём парсер. description показывается в начале --help.
    parser = argparse.ArgumentParser(
        description="Generate economic reports from CSV files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # epilog показывается в конце справки - выводим список доступных отчетов
        epilog=f"Available reports: {', '.join(get_available_reports()) or 'none'}",
    )

    # --files: один или несколько путей к CSV-файлам.
    # nargs="+" означает «один или более аргументов». Без этого argparse
    # ожидал бы ровно один файл. Аргументы после --files собираются
    # в список, пока не встретится другой флаг (--report).
    # required=True — аргумент обязательный; без него argparse выдаст ошибку.
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="paths to input CSV files",
    )

    # --report: имя отчёта.
    # choices=get_available_reports() — argparse проверит, что значение
    # входит в список зарегистрированных отчётов. Если пользователь
    # введёт несуществующий отчёт, argparse покажет ошибку вида:
    # "error: argument --report: invalid choice: 'foo'
    #  (choose from 'average-gdp')"
    # Также choices автоматически отображаются в --help.
    parser.add_argument(
        "--report",
        required=True,
        choices=get_available_reports(),
        help="report type to generate",
    )

    # parse_args(argv) разбирает переданный список аргументов
    # (или sys.argv[1:], если argv=None).
    return parser.parse_args(argv)


def main(argv=None):
    """
    Главная функция: координирует весь процесс от аргументов до вывода.

    Порядок действий:
    1. Разбираем аргументы → получаем список файлов и имя отчёта.
    2. По имени отчёта получаем функцию из реестра.
    3. Читаем все CSV-файлы и объединяем данные в один список.
    4. Вызываем функцию отчёта, передав ей данные.
    5. Выводим результат в консоль через tabulate.

    Обработка ошибок:
    - Невалидные аргументы → argparse выведет ошибку и завершит программу.
    - Файл не найден → ловим FileNotFoundError, выводим сообщение в stderr
      и завершаем с кодом 1.
    - Неизвестный отчёт → невозможен, т.к. argparse проверяет choices.

    Args:
        argv: Список аргументов (для тестирования). None = реальные аргументы.
    """

    args = parse_args(argv)

    # получение функции отчёта по имени.
    # Благодаря choices в argparse, сюда дойдёт только валидное имя,
    # поэтому get_report гарантированно найдёт функцию.
    report_func = get_report(args.report)

    try:
        data = read_csv_files(args.files)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        # Любая другая ошибка чтения (права доступа, битый файл и т.д.)
        print(f"Error reading files: {exc}", file=sys.stderr)
        sys.exit(1)

    if not data:
        # Пустые файлы - не ошибка, но предупреждаем пользователя
        print("Warning: No data found in provided files", file=sys.stderr)
        sys.exit(0)  # Код 0 = успех (технически операция выполнена)

    headers, rows = report_func(data)

    print(tabulate(rows, headers=headers, tablefmt="grid", floatfmt=".2f"))


if __name__ == "__main__":
    main()
