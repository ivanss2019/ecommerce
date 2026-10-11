# Интернет-магазин

Отдельный учебный проект для домашних заданий 14.1 и 14.2.

## Установка

Требуется Python 3.9 или новее и Poetry.

```bash
poetry install --with lint,test
poetry run python main.py
```

При снижении цены пример запрашивает подтверждение: `y` — принять, `n` — отменить.

## Возможности

- `Product`: название, описание, цена, остаток; приватная цена, геттер и сеттер, проверка положительной цены и подтверждение снижения.
- `Product.new_product()`: создание из словаря; необязательный список для объединения дубликатов по имени с суммированием остатков и выбором максимальной цены.
- `Category`: название, описание, приватный список товаров; общие счётчики категорий и товарных позиций, `add_product()`, строковое представление товаров через `products`.
- `load_categories()`: загрузка JSON в объекты категорий и товаров. Пример данных: `data/products.json`.

## Проверки

```bash
poetry run black --check .
poetry run isort --check-only .
poetry run flake8 .
poetry run mypy
poetry run pytest --cov --cov-report=term-missing --cov-report=html --cov-report=xml:coverage.xml
```

Отчёт покрытия: `htmlcov/index.html` и `coverage.xml`.

## GitFlow

`main` — основная ветка, `develop` — ветка разработки; задания выполняются в `feature/*` с Pull Request в `develop`. Настройки IDE `.idea/`, виртуальное окружение и временные файлы исключены через `.gitignore`.
