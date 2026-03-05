"""
Тесты разбора аргументов
Интеграционные тесты для точки входа

Проверяем:
- Корректный разбор аргументов.
- Ошибки при невалидных аргументах (несуществующий отчёт, отсутствие --files и т.д.).
- Полный цикл: от аргументов до вывода в консоль.
"""

import pytest

from csv_script.main import main, parse_args

# ── Тесты разбора аргументов ─────────────────────────────────────


def test_parse_args_valid():
    """Корректные аргументы разбираются без ошибок."""
    args = parse_args(["--files", "a.csv", "b.csv", "--report", "average-gdp"])
    assert args.files == ["a.csv", "b.csv"]
    assert args.report == "average-gdp"


def test_parse_args_unknown_report():
    """argparse вызывает sys.exit(2) при невалидных аргументах(несуществующий отчёт)."""
    with pytest.raises(SystemExit) as exc_info:
        parse_args(["--files", "a.csv", "--report", "no-such-report"])
    assert exc_info.value.code == 2


def test_parse_args_missing_files():
    """Без --files → ошибка argparse."""
    with pytest.raises(SystemExit) as exc_info:
        parse_args(["--report", "average-gdp"])
    assert exc_info.value.code == 2


def test_parse_args_missing_report():
    """Без --report → ошибка argparse."""
    with pytest.raises(SystemExit) as exc_info:
        parse_args(["--files", "a.csv"])
    assert exc_info.value.code == 2


def test_parse_args_no_args():
    """Вообще без аргументов → ошибка argparse."""
    with pytest.raises(SystemExit) as exc_info:
        parse_args([])
    assert exc_info.value.code == 2


# ── Интеграционные тесты (end-to-end) ────────────────────────────


def test_main_single_file(sample_csv: str, capsys: pytest.CaptureFixture[str]):
    """
    Полный цикл с одним файлом.

    capsys — встроенная фикстура pytest, которая перехватывает вывод
    в stdout/stderr. Это позволяет проверить, что main() напечатал
    ожидаемую таблицу, не вмешиваясь в реальный терминал.
    """
    main(["--files", sample_csv, "--report", "average-gdp"])
    output = capsys.readouterr().out
    # Проверяем, что в выводе есть названия стран и числа.
    assert "United States" in output
    assert "China" in output
    assert "23923.67" in output


def test_main_multiple_files(
    two_csv_files: tuple[str, str], capsys: pytest.CaptureFixture[str]
):
    """Полный цикл с двумя файлами: данные объединяются."""
    file1, file2 = two_csv_files
    main(["--files", file1, file2, "--report", "average-gdp"])
    output = capsys.readouterr().out
    assert "United States" in output
    assert "China" in output


def test_main_nonexistent_file():
    """main ловит FileNotFoundError и вызывает sys.exit(1) при отсутствии файла."""
    with pytest.raises(SystemExit) as exc_info:
        main(["--files", "nonexistent.csv", "--report", "average-gdp"])
    assert exc_info.value.code == 1
