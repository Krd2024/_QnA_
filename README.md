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

# Технические детали:
  
## Установка

1.Склонируйте репозиторий:
   ```bash
   git clone https://github.com/Krd2024/_QnA_.git
```
2.Создание виртуального окружения
```bash
   python -m venv venv
```
3.Активация виртуального окружения
```bash
   venv\Scripts\activate
```
4.Установка зависимостей проекта
```bash
   pip install -r requirements.txt
```
5.Применение миграций базы данных
```bash
python manage.py migrate
```

**Подключение приложений**

Сосдать файл .env
Добавьте соответствующие значения в .env файл:
```python
EMAIL_HOST_USER=your_email@yandex.ru
EMAIL_HOST_PASSWORD=your_password # Зайти в свой Яндекс ID -> Безопасность -> Пароли приложений -> Почта -> прописать пароль для сторонних пиложений
DEFAULT_FROM_EMAIL=your_email@yandex.ru
```
