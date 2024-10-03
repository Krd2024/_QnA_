# Вопрос-Ответ Приложение

Приложение позволяет пользователям задавать вопросы, отвечать на них, взаимодействовать с контентом и профилями других пользователей. Примером для разработки послужил сайт QnA Хабр.

## Возможности приложения

### Вопросы и Ответы
- **Задать вопрос** — любой пользователь может создать вопрос, который будет виден всем.
- **Редактировать вопрос** — после публикации можно отредактировать вопрос.
- **Ответить на вопрос** — возможность написать ответ на вопрос другого пользователя.
- **Редактировать ответ** — изменение ранее опубликованных ответов.
- **Отметить ответ как "решение"** — автор вопроса может выбрать ответ, который решает его вопрос.
- **Лайк/Дизлайк** — возможность ставить или убирать лайки к вопросам и ответам.

### Профиль пользователя (Личный кабинет)
- **Установка фото профиля** — возможность загрузить и изменить аватар.
- **Изменение имени и профессии** — редактирование персональных данных.
- **Просмотр личного кабинета другого пользователя**:
  - Список всех вопросов, заданных пользователем.
  - Список всех ответов, данных пользователем.

### Уведомления
- **Ответы на вопросы** — пользователь получает уведомление, когда кто-то ответил на его вопрос.
- **Лайки на ответ** — уведомление появляется, когда кто-то поставил лайк на ваш ответ.

### Работа с тегами
- **Просмотр всех тегов** — возможность увидеть список всех доступных тегов.
- **Количество вопросов по тегу** — отображается число вопросов, связанных с тегом.
- **Количество подписчиков тега** — отображается, сколько пользователей подписаны на этот тег.
- **Подписаться/Отписаться от тега** — возможность подписаться на интересующие теги или отписаться от них.

## Технические детали

- **База данных**: В приложении зарегистрировано около 1700 пользователей, создано 3000 вопросов и 10000 ответов.
  
## Установка

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/Krd2024/_QnA_.git
2. Создание виртуального окружения
```bash
   python -m venv venv
```
3.Активация виртуального окружения
```bash
   venv\Scripts\activate
```
4. Установка зависимостей проекта
```bash
   pip install -r requirements.txt
```

Конфигурация
Перед запуском приложения необходимо правильно настроить файл settings.py.

**Подключение приложений**


```python
INSTALLED_APPS = [
    "django_redis",  # Поддержка Redis для кэширования
    "debug_toolbar",  # Инструменты отладки в режиме разработки
    "rest_framework",  # Django REST Framework для создания API
]

Middleware
Для отслеживания времени выполнения запросов и отладки в режиме разработки, добавьте следующие промежуточные слои (middleware):
MIDDLEWARE = [
    "qna.middleware.RenderTimeMiddleware",  # Показывает время выполнения каждого запроса
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # Отладочные инструменты
]
Кэширование
Для работы с кэшированием в приложении используется Redis. Убедитесь, что Redis установлен и запущен на локальном сервере. Настройка кэша выглядит следующим образом:

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",  # Локальный Redis сервер
    },
}
Шаблоны
Добавьте процессор контекста для работы с уведомлениями в настройку TEMPLATES:
TEMPLATES = [
    {
        # Другие параметры
        "OPTIONS": {
            "context_processors": [
                # Другие процессоры контекста
                "main.notific_context.context.latest_notific",  # Контекстный процессор для уведомлений
            ],
        },
    },
]
Настройки для отправки писем
Для отправки уведомлений по электронной почте используется SMTP-сервер Yandex. Введите следующие параметры в settings.py:

EMAIL_HOST = "smtp.yandex.ru"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("EMAIL_HOST_USER")  # Получение настроек через переменные окружения
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")

Добавьте соответствующие значения в .env файл:

EMAIL_HOST_USER=your_email@yandex.ru
EMAIL_HOST_PASSWORD=your_password # Яндекс ID -> Безопасность -> Пароли приложений -> Почта
DEFAULT_FROM_EMAIL=your_email@yandex.ru

