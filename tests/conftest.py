"""
Общие фикстуры (fixtures) для тестов.

Фикстуры — это функции, которые pytest автоматически вызывает
перед каждым тестом, если тест запрашивает их по имени аргумента.
Файл conftest.py — специальный: pytest загружает его автоматически,
и фикстуры из него доступны во всех тестовых файлах каталога.

Здесь мы определяем:
- SAMPLE_ROWS: тестовые данные (6 строк: 3 для US, 3 для China).
- sample_csv: фикстура, создающая один временный CSV-файл.
- two_csv_files: фикстура, создающая два временных CSV-файла.

Временные файлы создаются через встроенную фикстуру tmp_path,
которая предоставляет уникальную временную директорию для каждого теста.
После завершения теста pytest автоматически удаляет эту директорию.
"""

import csv

import pytest

# Заголовки CSV-файла. Совпадают с реальным форматом входных данных.
FIELDNAMES = [
    "country",
    "year",
    "gdp",
    "gdp_growth",
    "inflation",
    "unemployment",
    "population",
    "continent",
]

# Тестовые данные:
# Значения взяты из реальных данных задания, чтобы можно было проверить
# корректность вычислений (среднее ВВП US = (25462+23315+22994)/3 = 23923.67).
SAMPLE_ROWS = [
    {
        "country": "United States",
        "year": "2023",
        "gdp": "25462",
        "gdp_growth": "2.1",
        "inflation": "3.4",
        "unemployment": "3.7",
        "population": "339",
        "continent": "North America",
    },
    {
        "country": "United States",
        "year": "2022",
        "gdp": "23315",
        "gdp_growth": "2.1",
        "inflation": "8.0",
        "unemployment": "3.6",
        "population": "338",
        "continent": "North America",
    },
    {
        "country": "United States",
        "year": "2021",
        "gdp": "22994",
        "gdp_growth": "5.9",
        "inflation": "4.7",
        "unemployment": "5.3",
        "population": "337",
        "continent": "North America",
    },
    {
        "country": "China",
        "year": "2023",
        "gdp": "17963",
        "gdp_growth": "5.2",
        "inflation": "2.5",
        "unemployment": "5.2",
        "population": "1425",
        "continent": "Asia",
    },
    {
        "country": "China",
        "year": "2022",
        "gdp": "17734",
        "gdp_growth": "3.0",
        "inflation": "2.0",
        "unemployment": "5.6",
        "population": "1423",
        "continent": "Asia",
    },
    {
        "country": "China",
        "year": "2021",
        "gdp": "17734",
        "gdp_growth": "8.4",
        "inflation": "1.0",
        "unemployment": "5.1",
        "population": "1420",
        "continent": "Asia",
    },
]


def _write_csv(path, rows):
    """
    Вспомогательная функция: записывает список словарей в CSV-файл.

    Используется фикстурами для создания тестовых файлов.
    Функция приватная (начинается с _), потому что предназначена
    только для использования внутри этого модуля.

    Args:
        path: Путь к файлу (объект pathlib.Path или строка).
        rows: Список словарей для записи.
    """
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDNAMES)
        # Записываем строку заголовков: country,year,gdp,...
        writer.writeheader()
        # Записываем все строки данных.
        writer.writerows(rows)


@pytest.fixture()
def sample_csv(tmp_path):
    """
    Фикстура: создаёт один CSV-файл со всеми 6 тестовыми строками.

    tmp_path — встроенная фикстура pytest, предоставляющая уникальную
    временную директорию (pathlib.Path). Файл будет удалён после теста.

    Returns:
        Строка с путём к созданному CSV-файлу.
    """
    path = tmp_path / "data.csv"
    _write_csv(path, SAMPLE_ROWS)
    # Возвращаем str, потому что open() и argparse работают со строками.
    return str(path)


@pytest.fixture()
def two_csv_files(tmp_path):
    """
    Фикстура: создаёт два отдельных CSV-файла.
    - Первый файл содержит данные US (3 строки).
    - Второй файл содержит данные China (3 строки).

    Используется для тестирования объединения данных из нескольких файлов.

    Returns:
        Кортеж из двух строк (путь_к_файлу_1, путь_к_файлу_2).
    """
    file_1 = tmp_path / "us.csv"
    file_2 = tmp_path / "china.csv"
    # SAMPLE_ROWS[:3] — первые 3 элемента (US).
    # SAMPLE_ROWS[3:] — последние 3 элемента (China).
    _write_csv(file_1, SAMPLE_ROWS[:3])
    _write_csv(file_2, SAMPLE_ROWS[3:])
    return str(file_1), str(file_2)
