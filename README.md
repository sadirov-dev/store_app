# FastAPI Store API

Простой учебный backend-проект интернет-магазина на FastAPI.

## Описание

Проект показывает базовую структуру backend API для магазина:

- регистрация и login пользователя
- JWT авторизация
- CRUD для категорий
- CRUD для товаров
- корзина пользователя
- создание заказов из корзины
- Swagger документация

Проект специально сделан без сложной архитектуры, чтобы код было легче читать студенту.

## Технологии

- Python 3.11+
- FastAPI
- SQLAlchemy
- SQLite
- Alembic
- JWT

## Структура папок

```text
fastapi-store/
├── alembic/
├── store_app/
│   ├── api/
│   │   ├── auth.py
│   │   ├── cart.py
│   │   ├── categories.py
│   │   ├── dependencies.py
│   │   ├── orders.py
│   │   └── products.py
│   ├── database/
│   │   ├── db.py
│   │   ├── models.py
│   │   └── schemas.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── cart_service.py
│   │   ├── category_service.py
│   │   ├── order_service.py
│   │   └── product_service.py
│   └── config.py
├── .env.example
├── .gitignore
├── alembic.ini
├── main.py
├── README.md
└── requirements.txt
```

## Установка

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## .env пример

Создай файл `.env` и добавь:

```env
DATABASE_URL=sqlite:///./store.db
SECRET_KEY=change-this-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=60
ALGORITHM=HS256
```

## Запуск проекта

```bash
uvicorn main:app --reload
```

После запуска API будет доступен по адресу:

- `http://127.0.0.1:8000`

## Запуск через Docker

Сборка и запуск:

```bash
docker compose up --build
```

Остановка контейнеров:

```bash
docker compose down
```

После запуска API будет доступен по адресу:

- `http://127.0.0.1:8000`

## Миграции

Создание миграции:

```bash
alembic revision --autogenerate -m "initial"
```

Применение миграций:

```bash
alembic upgrade head
```

## Swagger

Swagger UI:

- `http://127.0.0.1:8000/docs`

ReDoc:

- `http://127.0.0.1:8000/redoc`

## Основные endpoints

### Auth

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`

### Categories

- `POST /api/categories`
- `GET /api/categories`
- `GET /api/categories/{id}`
- `PUT /api/categories/{id}`
- `DELETE /api/categories/{id}`

### Products

- `POST /api/products`
- `GET /api/products`
- `GET /api/products/{id}`
- `PUT /api/products/{id}`
- `DELETE /api/products/{id}`

Фильтры товаров:

- `search`
- `category_id`
- `min_price`
- `max_price`

### Cart

- `POST /api/cart/add`
- `GET /api/cart`
- `PATCH /api/cart/{item_id}`
- `DELETE /api/cart/{item_id}`
- `DELETE /api/cart/clear`

### Orders

- `POST /api/orders`
- `GET /api/orders`
- `GET /api/orders/{id}`

## Подготовка к GitHub

Если git еще не инициализирован:

```bash
git init
git add .
git commit -m "Initial FastAPI Store API"
```

Если хочешь отправить проект на GitHub:

```bash
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git branch -M main
git push -u origin main
```

## Простая инструкция AWS EC2 deploy

1. Подключиться к серверу по SSH.
2. Установить Python, `venv` и `git`.
3. Склонировать репозиторий:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd fastapi-store
```

4. Создать и активировать виртуальное окружение:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

5. Установить зависимости:

```bash
pip install -r requirements.txt
```

6. Создать `.env`.
7. Применить миграции:

```bash
alembic upgrade head
```

8. Запустить проект:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

9. Открыть порт `8000` в Security Group или использовать Nginx как reverse proxy.
