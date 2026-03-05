"""
Пакет отчётов (reports).

Этот файл __init__.py выполняется при первом импорте пакета reports.
Его главная задача — импортировать все модули отчётов, чтобы декораторы
@register внутри них сработали и функции попали в реестр.

Порядок действий при запуске скрипта:
1. main.py делает from reports import get_report.
   Это загружает пакет reports → выполняется этот __init__.py.
2. Здесь мы импортируем average_gdp → Python загружает файл average_gdp.py.
3. При загрузке average_gdp.py срабатывает декоратор @register("average-gdp"),
   который записывает функцию в словарь _registry.
4. Теперь get_report("average-gdp") может найти эту функцию.

Чтобы добавить новый отчёт:
1. Создать файл reports/my_report.py с функцией, обёрнутой в @register("my-report").
2. Добавить сюда строку: from . import my_report
Всё. Новый отчёт автоматически появится в --help и будет доступен через --report.

noqa: F401 — подавляет предупреждение линтера о «неиспользуемом импорте».
Мы не вызываем average_gdp напрямую, но импорт нужен для побочного эффекта —
регистрации функции в реестре.
"""

from . import average_gdp  # noqa: F401
from .registry import get_available_reports, get_report

# __all__ определяет, что экспортируется при "from reports import *"
# публичный API модуля
__all__ = [
    "get_report",
    "get_available_reports",
]
