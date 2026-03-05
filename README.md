# CSV Script

Приложение для генерации экономических отчётов из CSV-файлов.

## Описание

Проект предоставляет расширяемую систему для обработки CSV-файлов с экономическими данными и генерации различных отчётов. Архитектура основана на реестре отчётов, что позволяет легко добавлять новые типы отчётов без изменения основного кода.

## Установка

```bash
# Установка зависимостей через poetry
poetry install

```

## Использование

```bash
python src/csv_script/main.py --files dataset1.csv dataset2.csv --report average-gdp
```

### Пример вывода

![Пример запуска](docs/images/example_run.png)

### Параметры

- `--files` - один или несколько путей к CSV-файлам (обязательный)
- `--report` - тип отчёта для генерации (обязательный)

## Структура проекта

```
csv_script/
├── src/csv_script/
│   ├── main.py          # Точка входа
│   ├── reader.py        # Чтение CSV-файлов
│   └── reports/         # Модули отчётов
├── tests/               # Тесты
├── docs/
│   └── images/          # Скриншот запуска скрипта
├── .gitignore           # Исключения для Git
├── pytest.ini           # Конфигурация pytest
├── pyproject.toml       # Зависимости и настройки
└── README.md            # Документация
```

## Зависимости

- Python >= 3.12
- pytest >= 9.0.2
- tabulate >= 0.9.0

## Разработка

```bash
# Запуск тестов
pytest

# Запуск тестов с покрытием кода
pytest --cov=src/csv_script --cov-report=html

# Линтинг
ruff check .

# Автоматическое исправление
ruff check --fix .
```

### Конфигурация

- `pytest.ini` - настройки pytest и coverage
- `.gitignore` - исключения для Git
- `pyproject.toml` - зависимости и настройки проекта

## Автор

ra (kulttura.hardware@gmail.com)
