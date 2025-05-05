FastAPI BMI Tracker

Простой REST-API-сервис для учёта и расчёта индекса массы тела (BMI) с аутентификацией, CRUD-операциями и автоматическими тестами.

---

Функциональность

- **Регистрация и вход** пользователей по JWT (JSON Web Token)  
- **CRUD-профиль**: хранение пола и возраста  
- **CRUD-записи BMI**: сохранение параметров `weight`, `height`, автоматический расчёт `bmi` и `category`  
- **Бизнес-логика**: отдельный эндпоинт для расчёта BMI без сохранения в БД  
- **Документация** всех эндпоинтов в Swagger UI и Redoc  
- **Автотесты** на основе `pytest` и `TestClient`

---

Требования

- Python **3.10+**  
- Git (для клонирования репозитория)  
- VS Code или любой другой редактор/IDE  
- Опционально: Docker & Docker Compose для развёртывания PostgreSQL

---
Установка

1. **Клонировать репозиторий**  
   ```bash
   git clone https://github.com/yourname/bmi_app.git
   cd bmi_app

    Создать виртуальное окружение и активировать его

        Windows PowerShell

python -m venv .venv
.\.venv\Scripts\Activate.ps1

macOS/Linux

    python3 -m venv .venv
    source .venv/bin/activate

Установить зависимости

    pip install --upgrade pip
    pip install -r requirements.txt

Настройка окружения

    В корне проекта создайте файл .env со следующими переменными:

DATABASE_URL=sqlite:///./bmi.db
SECRET_KEY=ваш-секретный-ключ
ACCESS_TOKEN_EXPIRE_MINUTES=30

(Опционально) Для работы с PostgreSQL через Docker Compose:

    Создать docker-compose.yml с сервисом db: postgres

    Заменить DATABASE_URL на строку вида
    postgresql://user:pass@localhost:5432/bmi_db

    Запустить:

        docker-compose up -d

Запуск приложения

В активированном окружении выполните:

uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

    Сервер будет доступен по адресу http://127.0.0.1:8000

Документация API

    Swagger UI: http://127.0.0.1:8000/docs

    Redoc: http://127.0.0.1:8000/redoc

Через UI можно просматривать схемы, примеры запросов и пробовать эндпоинты «на лету».
Тестирование

В корне проекта, с активированным .venv, запустите:

pytest -q

Все тесты находятся в app/tests/ и проверяют основные сценарии работы API.
Структура проекта

bmi_app/
+-- app/
¦   +-- main.py           — точка входа приложения
¦   +-- database.py       — настройка SQLAlchemy, init_db()
¦   +-- models.py         — ORM-модели User, Profile, BMIRecord
¦   +-- schemas.py        — Pydantic-схемы для запросов/ответов
¦   +-- auth.py           — JWT-аутентификация и зависимости
¦   +-- routers/
¦   ¦   +-- users.py      — регистрацию и вход
¦   ¦   +-- profiles.py   — CRUD профилей
¦   ¦   +-- records.py    — CRUD записей BMI
¦   ¦   L-- bmi.py        — расчёт BMI-логики
¦   L-- tests/
¦       L-- test_main.py  — автотесты через TestClient
+-- requirements.txt      — список зависимостей
L-- .env                  — переменные окружения (не коммитить)

Полезные команды

    Перезапустить сервер

uvicorn app.main:app --reload

Остановить сервер
Нажать CTRL+C в терминале

Деактивировать окружение

deactivate        # macOS/Linux
.venv\Scripts\Deactivate.ps1  # Windows PowerShell

Запустить тесты

    pytest

Деплой (опционально)

Docker

    Создать Dockerfile (описан в документации проекта).

    Сборка и запуск:

    docker build -t bmi_app .
    docker run -d -p 8000:8000 --env-file .env bmi_app

Gunicorn + Uvicorn Workers

pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

Успешной работы с вашим BMI Tracker API!
