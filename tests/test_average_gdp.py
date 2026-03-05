"""
Тесты для отчёта average-gdp.

Проверяем:
- Корректные заголовки.
- Пустые данные → пустой отчёт.
- Одна страна, одна запись → среднее = само значение.
- Несколько записей → правильное среднее арифметическое.
- Сортировка по убыванию.
- Нумерация строк начинается с 1.
- Округление до 2 знаков.
- Реалистичные данные из задания дают ожидаемые числа.
"""

from csv_script.reports.average_gdp import average_gdp


def test_headers():
    """Заголовки всегда одинаковые, независимо от данных."""
    headers, _ = average_gdp([])
    assert headers == ["", "country", "gdp"]


def test_empty_data():
    """Если данных нет, таблица пустая."""
    _, rows = average_gdp([])
    assert rows == []


def test_single_country_single_row():
    """Одна запись — среднее равно самому значению."""
    data = [{"country": "A", "gdp": "100"}]
    _, rows = average_gdp(data)
    assert len(rows) == 1
    # [номер, страна, среднее_ВВП]
    assert rows[0] == [1, "A", 100.0]


def test_average_calculation():
    """Проверяем арифметику: (100 + 200 + 300) / 3 = 200.0."""
    data = [
        {"country": "A", "gdp": "100"},
        {"country": "A", "gdp": "200"},
        {"country": "A", "gdp": "300"},
    ]
    _, rows = average_gdp(data)
    assert rows[0][2] == 200.0


def test_sorted_descending():
    """Страны должны быть отсортированы по среднему ВВП от большего к меньшему."""
    data = [
        {"country": "Low", "gdp": "10"},
        {"country": "High", "gdp": "1000"},
        {"country": "Mid", "gdp": "500"},
    ]
    _, rows = average_gdp(data)
    countries = [r[1] for r in rows]
    assert countries == ["High", "Mid", "Low"]


def test_row_indices_start_at_one():
    """Порядковые номера строк должны начинаться с 1."""
    data = [
        {"country": "C", "gdp": "1"},
        {"country": "B", "gdp": "2"},
        {"country": "A", "gdp": "3"},
    ]
    _, rows = average_gdp(data)
    indices = [r[0] for r in rows]
    # 3 страны → номера 1, 2, 3 (отсортированы по ВВП: A=3, B=2, C=1).
    assert indices == [1, 2, 3]


def test_rounding():
    """Результат должен быть округлён до 2 знаков после запятой."""
    data = [
        {"country": "X", "gdp": "90"},
        {"country": "X", "gdp": "99"},
        {"country": "X", "gdp": "109"},
    ]
    _, rows = average_gdp(data)
    assert rows[0][2] == 99.33


def test_realistic_data():
    """
    Проверяем на реальных данных из задания.
    Ожидаемые значения:
    - United States: (25462 + 23315 + 22994) / 3 = 23923.67
    - China: (17963 + 17734 + 17734) / 3 = 17810.33
    - Japan: (4230 + 4235 + 4936) / 3 = 4467.00
    - Germany: (4086 + 4072 + 4257) / 3 = 4138.33
    """
    data = [
        {"country": "United States", "gdp": "25462"},
        {"country": "United States", "gdp": "23315"},
        {"country": "United States", "gdp": "22994"},
        {"country": "China", "gdp": "17963"},
        {"country": "China", "gdp": "17734"},
        {"country": "China", "gdp": "17734"},
        {"country": "Japan", "gdp": "4230"},
        {"country": "Japan", "gdp": "4235"},
        {"country": "Japan", "gdp": "4936"},
        {"country": "Germany", "gdp": "4086"},
        {"country": "Germany", "gdp": "4072"},
        {"country": "Germany", "gdp": "4257"},
    ]
    _, rows = average_gdp(data)

    # Проверяем порядок (по убыванию) и значения.
    assert rows[0][1] == "United States"
    assert rows[0][2] == 23923.67

    assert rows[1][1] == "China"
    assert rows[1][2] == 17810.33

    assert rows[2][1] == "Japan"
    assert rows[2][2] == 4467.0

    assert rows[3][1] == "Germany"
    assert rows[3][2] == 4138.33
