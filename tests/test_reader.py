"""
Тесты для модуля reader.py.

Проверяем:
- Чтение одного файла: корректное количество строк.
- Наличие нужных ключей в словарях.
- Корректность значений.
- Чтение нескольких файлов: данные объединяются.
- Обработка ошибки: несуществующий файл.
"""

import pytest

from csv_script.reader import read_csv_files


def test_read_single_file(sample_csv: str):
    """Из одного файла с 6 строками данных должно быть прочитано 6 словарей."""
    data = read_csv_files([sample_csv])
    assert len(data) == 6


def test_row_keys(sample_csv: str):
    """Каждый словарь должен содержать ключи из заголовков CSV."""
    data = read_csv_files([sample_csv])
    # Проверяем наличие ключей, которые используются в отчёте.
    assert "country" in data[0]
    assert "gdp" in data[0]


def test_row_values(sample_csv: str):
    """Значения в словарях должны соответствовать данным в файле."""
    data = read_csv_files([sample_csv])
    # Первая строка файла — United States, 2023, gdp=25462.
    assert data[0]["country"] == "United States"
    # Обратите внимание: значение — строка "25462", а не число.
    # Преобразование в число — ответственность отчёта, не reader'а.
    assert data[0]["gdp"] == "25462"


def test_read_multiple_files(two_csv_files: tuple[str, str]):
    """При чтении двух файлов данные объединяются в один список."""
    file_1, file_2 = two_csv_files
    data = read_csv_files([file_1, file_2])
    # 3 строки из первого файла + 3 строки из второго = 6.
    assert len(data) == 6
    # Проверяем, что данные из обоих файлов присутствуют.
    countries = {row["country"] for row in data}
    assert countries == {"United States", "China"}


def test_file_not_found():
    """При попытке прочитать несуществующий файл — FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        read_csv_files(["no_such_file.csv"])
