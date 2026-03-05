"""
Отчёт «Среднее ВВП по странам» (average-gdp).

Этот модуль содержит единственную функцию average_gdp, которая:
1. Принимает данные (список словарей со строками из CSV).
2. Считает среднее арифметическое ВВП для каждой страны.
3. Сортирует страны по убыванию среднего ВВП.
4. Возвращает заголовки и строки, готовые для вывода через tabulate.

Функция зарегистрирована в реестре под именем "average-gdp" благодаря
декоратору @register. Это значит, что при запуске скрипта с
--report average-gdp будет вызвана именно эта функция.
"""

from typing import Dict, List, Tuple, Union

from .registry import register


# Декоратор @register("average-gdp") делает две вещи:
# 1. Регистрирует функцию в реестре _registry под ключом "average-gdp".
# 2. Возвращает функцию без изменений (не оборачивает её).
# Регистрация происходит в момент импорта модуля (import average_gdp).
@register("average-gdp")
def average_gdp(
    data: List[Dict[str, str]],
) -> Tuple[List[str], List[List[Union[float, int, str]]]]:
    """
    Рассчитать среднее ВВП по странам.

    Пример входных данных (data):
    [
        {"country": "Iran", "gdp": "25462", ...},
        {"country": "United States", "gdp": "23315", ...},
        {"country": "Zeitgeist", "gdp": "17963", ...},
        ...
    ]

    Пример возвращаемого значения:
    headers = ["", "country", "gdp"]
    rows = [
        [1, "United States", 23923.67],
        [2, "China", 17810.33],
        ...
    ]

    Args:
        data: Список словарей. Каждый словарь должен содержать как минимум
              ключи "country" (строка) и "gdp" (строка, приводимая к float).

    Returns:
        Кортеж (headers, rows):
        - headers — список заголовков таблицы (3 элемента).
        - rows — список списков, каждый из которых содержит
          [порядковый_номер, название_страны, среднее_ВВП].
    """

    gdp_sums: Dict[str, float] = {}
    gdp_counts: Dict[str, int] = {}

    # Проверку ключей не делаем так как по условию данные валидны
    for row in data:
        country = row["country"]

        gdp = float(row["gdp"])

        gdp_sums[country] = gdp_sums.get(country, 0.0) + gdp
        gdp_counts[country] = gdp_counts.get(country, 0) + 1

    # Формируем список кортежей (страна, среднее_ВВП).
    results = [
        (country, gdp_sums[country] / gdp_counts[country]) for country in gdp_sums
    ]

    results.sort(key=lambda x: x[1], reverse=True)

    headers = ["", "country", "gdp"]

    rows = [
        [idx, country, round(avg, 2)]
        for idx, (country, avg) in enumerate(results, start=1)
    ]

    return headers, rows
