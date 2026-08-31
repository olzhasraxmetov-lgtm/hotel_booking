# Hotel Booking API

Backend-приложение для бронирования отелей, реализованное на **FastAPI**. Репозиторий на GitHub: [hotel_booking](https://github.com/olzhasraxmetov-lgtm/hotel_booking).

Проект реализует REST API для управления отелями, номерами, удобствами, бронированиями и пользователями (регистрация, аутентификация по JWT), с кэшированием через Redis, фоновыми задачами через Celery и миграциями БД через Alembic.

## Стек технологий

- **Python 3.12**
- **FastAPI** — веб-фреймворк
- **Uvicorn** — ASGI-сервер
- **SQLAlchemy 2.0 (async)** + **asyncpg** — работа с PostgreSQL
- **Alembic** — миграции базы данных
- **PostgreSQL 16** — основная база данных
- **Redis** — кэширование ответов (`fastapi-cache2`) и брокер сообщений для Celery
- **Celery** — фоновые и периодические задачи (`celery beat`)
- **Pydantic / Pydantic Settings** — валидация данных и конфигурация
- **PyJWT** + **passlib (bcrypt)** — аутентификация по JWT и хэширование паролей
- **Pillow** — обработка изображений (генерация уменьшенных копий)
- **pytest**, **pytest-asyncio**, **pytest-dotenv** — тестирование
- **ruff**, **black** — линтинг и форматирование
- **Docker / Docker Compose** — контейнеризация

## Структура проекта

```
backendCourse/
├── src/
│   ├── api/            # роутеры FastAPI (auth, hotels, rooms, bookings, facilities, images)
│   ├── connectors/      # подключение к Redis
│   ├── exceptions/      # кастомные исключения приложения и HTTP-исключения
│   ├── migrations/       # Alembic-миграции
│   ├── models/          # ORM-модели SQLAlchemy (Hotels, Rooms, Users, Bookings, Facilities)
│   ├── repositories/     # слой доступа к данным (репозитории и мапперы)
│   ├── schemas/          # Pydantic-схемы запросов/ответов
│   ├── services/         # бизнес-логика (auth, hotels, rooms, bookings, facilities, images)
│   ├── static/images/    # загруженные и обработанные изображения
│   ├── tasks/            # Celery-приложение и задачи (в т.ч. ресайз изображений)
│   ├── utils/            # вспомогательные утилиты (DBManager)
│   ├── config.py         # конфигурация приложения (переменные окружения)
│   ├── database.py       # инициализация SQLAlchemy engine/session
│   ├── init.py           # инициализация зависимостей (redis_connector)
│   └── main.py           # точка входа FastAPI-приложения
├── tests/
│   ├── unit_tests/        # юнит-тесты
│   └── integration_tests/ # интеграционные тесты (auth, bookings, hotels, facilities, users)
├── alembic.ini
├── docker-compose.yaml
├── Dockerfile
├── requirements.txt
├── pytest.ini
└── pyproject.toml
```

## Функциональность (API)

### Авторизация и аутентификация — `/auth`
- `POST /auth/register` — регистрация пользователя
- `POST /auth/login` — вход, выдаёт JWT (записывается в cookie `access_token`)
- `GET /auth/me` — получить данные текущего пользователя
- `POST /auth/logout` — выход (удаление cookie)

### Отели — `/hotels`
- `GET /hotels` — список отелей с пагинацией, фильтрами по локации/названию и датам (кэшируется на 10 сек)
- `GET /hotels/{hotel_id}` — получить один отель
- `POST /hotels` — создать отель
- `PUT /hotels/{hotel_id}` — полностью обновить отель
- `PATCH /hotels/{hotel_id}` — частично обновить отель
- `DELETE /hotels/{hotel_id}` — удалить отель

### Номера — `/hotels/{hotel_id}/rooms`
- `GET /` — список номеров отеля с фильтрацией по датам
- `GET /{room_id}` — получить номер (со связанными удобствами)
- `POST /` — создать номер
- `PUT /{room_id}` — полностью обновить номер
- `PATCH /{room_id}` — частично обновить номер
- `DELETE /{room_id}` — удалить номер

### Бронирования — `/bookings`
- `GET /bookings/` — список всех бронирований
- `GET /bookings/me` — бронирования текущего пользователя
- `POST /bookings` — создать бронирование (с проверкой доступности номеров)

### Удобства — `/facilities`
- `GET /facilities` — список удобств (кэшируется на 10 сек)
- `POST /facilities` — создать удобство

### Изображения — `/images`
- `POST /images/` — загрузка изображения; после загрузки в фоне (Celery) генерируются уменьшенные копии в разных размерах

## Модели данных

- **HotelsORM** — отели (`title`, `location`)
- **RoomsORM** — номера отеля (`title`, `description`, `price`, `quantity`), связаны с отелем и удобствами (many-to-many через `RoomsFacilitiesORM`)
- **FacilitiesORM** — удобства номеров
- **UsersORM** — пользователи (`email`, `hashed_password`)
- **BookingsORM** — бронирования (`room_id`, `user_id`, `price`, `date_from`, `date_to`), с вычисляемым свойством `total_cost`

## Фоновые задачи (Celery)

- `resize_and_save_images` — генерация уменьшенных версий загруженных изображений (Pillow)
- `booking_today_check_in` — периодическая задача (каждые 60 секунд, через `celery beat`), находит бронирования с заездом сегодня

## Переменные окружения

Конфигурация читается из файла `.env` (см. `src/config.py`). Необходимые переменные:

```
MODE=                          # TEST | LOCAL | DEV | PROD
DB_HOST=
DB_PORT=
DB_USER=
DB_PASS=
DB_NAME=
REDIS_HOST=
REDIS_PORT=
JWT_SECRET_KEY=
JWT_ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
```

Для тестов используется отдельный файл `.env-test` (подключается через `pytest.ini`).

## Запуск проекта

### Через Docker Compose

В `docker-compose.yaml` описаны сервисы:
- `booking_db` — PostgreSQL 16 (порт `5050:5432`)
- `booking_cache` — Redis 7.4 (порт `7379:6379`)
- `booking_backend_service` — само приложение (порт `2030:8000`), при старте выполняет `alembic upgrade head` и запускает `uvicorn`
- `booking_celery_worker_service` — воркер Celery
- `booking_celery_beat_service` — планировщик периодических задач Celery

Запуск:

```bash
docker compose up --build
```

API будет доступно на `http://localhost:2030`.

### Локально

```bash
pip install -r requirements.txt
alembic upgrade head
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

Для фоновых задач дополнительно потребуется запустить Redis и Celery worker/beat:

```bash
celery --app=src.tasks.celery_app:celery_instance worker -l INFO
celery --app=src.tasks.celery_app:celery_instance beat -l INFO
```

## Миграции базы данных

Миграции управляются через Alembic (`alembic.ini`, `src/migrations/`):

```bash
alembic revision --autogenerate -m "описание миграции"
alembic upgrade head
```

## Тестирование

Тесты находятся в `tests/` и разделены на юнит- и интеграционные:

```bash
pytest
```

Конфигурация pytest (`pytest.ini`) подключает `.env-test` и использует `asyncio_mode = auto`. Интеграционные тесты покрывают auth, hotels, rooms, bookings, facilities, users; в `tests/` также есть мок-данные (`mock_hotels.json`, `mock_rooms.json`).

## Линтинг

Форматирование и линтинг настроены через `ruff` (`pyproject.toml`, `line-length = 100`) и `black`.
