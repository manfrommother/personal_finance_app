# Personal Finance App

Personal Finance App - это API для управления личными финансами, разработанное с использованием FastAPI и SQLAlchemy.

## Особенности

- Управление пользователями (регистрация, аутентификация)
- Отслеживание транзакций (доходы и расходы)
- Категоризация транзакций
- Управление бюджетом
- Генерация финансовых отчетов

## Требования

- Python 3.7+
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn (для запуска сервера)

## Установка

1. Клонируйте репозиторий:
   ```
   git clone https://github.com/your-username/personal-finance-app.git
   cd personal-finance-app
   ```

2. Создайте виртуальное окружение и активируйте его:
   ```
   python -m venv venv
   source venv/bin/activate  # На Windows используйте `venv\Scripts\activate`
   ```

3. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```

## Настройка базы данных

По умолчанию приложение использует SQLite. Вы можете изменить настройки базы данных в файле `personal_finance_app/app/database.py`.

## Запуск приложения

1. Перейдите в директорию проекта:
   ```
   cd personal_finance_app
   ```

2. Запустите сервер:
   ```
   uvicorn app.main:app --reload
   ```

Приложение будет доступно по адресу `http://127.0.0.1:8000`.

## API документация

После запуска приложения, вы можете получить доступ к автоматически сгенерированной документации API:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Структура проекта

```
personal_finance_app/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── crud.py
│
├── tests/
│   └── test_main.py
│
├── requirements.txt
└── README.md
```
