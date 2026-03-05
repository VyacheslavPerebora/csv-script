"""
Тесты для реестра отчётов (reports/registry.py).

Проверяем:
- Декоратор @register корректно записывает функцию в реестр.
- get_report возвращает зарегистрированную функцию.
- get_report выбрасывает ValueError для несуществующего отчёта.
- average-gdp присутствует в списке доступных отчётов.
"""

import pytest

from csv_script.reports.registry import (
    _registry,
    get_available_reports,
    get_report,
    register,
)


def test_register_and_retrieve():
    """
    Проверяем, что @register записывает функцию и get_report её возвращает.

    Используем имя с префиксом "_test-", чтобы не конфликтовать
    с реальными отчётами. В конце удаляем запись из реестра,
    чтобы тест не влиял на другие тесты (изоляция).
    """

    @register("_test-dummy")
    def dummy(data):
        return [], []

    # get_report должен вернуть тот же самый объект функции.
    assert get_report("_test-dummy") is dummy

    # Очистка: убираем тестовый отчёт из реестра.
    del _registry["_test-dummy"]


def test_get_unknown_report():
    """При запросе незарегистрированного отчёта — ValueError."""
    with pytest.raises(ValueError, match="Unknown report"):
        get_report("does-not-exist")


def test_available_reports_contains_average_gdp():
    """
    Проверяем, что после импорта пакета reports отчёт 'average-gdp'
    зарегистрирован и доступен.
    """
    assert "average-gdp" in get_available_reports()
