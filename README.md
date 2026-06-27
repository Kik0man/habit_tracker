# Трекер полезных привычек (Atomic Habits)

Бэкенд SPA-приложения для формирования полезных привычек по методике Джеймса Клира. Позволяет создавать привычки, управлять их выполнением и получать напоминания в Telegram.

## Технологии

- Python, Django, Django REST Framework
- PostgreSQL (или SQLite для тестов)
- Celery + Redis
- JWT-аутентификация
- Telegram Bot API
- Docker, Docker Compose, Nginx
- GitHub Actions (CI/CD)

## Локальный запуск с Docker Compose (рекомендовано)

1. **Клонируйте репозиторий**  
   ```bash
   git clone <your-repo-url>
   cd habits-tracker

2. Создайте файл .env на основе .env.example и заполните его:
`cp .env.example .env`
Отредактируйте .env, указав реальные значения для SECRET_KEY, TELEGRAM_BOT_TOKEN и др.
Примечание: для запуска в Docker значения DB_HOST и REDIS_URL должны указывать на имена сервисов (db, redis).
3. Запустите все сервисы `docker-compose up -d`
4. Примените миграции (обычно выполняются автоматически entrypoint'ом, но можно вручную):
`docker-compose exec web python manage.py migrate`
5. Проверьте работу

API доступно по адресу: http://localhost
Документация Swagger: http://localhost/api/swagger/
Админка: http://localhost/admin/

6. Остановка и очистка
`docker-compose down
docker-compose down -v   # удалить тома (БД, Redis, статику)`

## Локальный запуск без Docker (для разработки)

- Создайте и активируйте виртуальное окружение.
- Установите зависимости: pip install -r requirements.txt.
- Установите и запустите PostgreSQL, Redis локально.
- Создайте .env с настройками (для локального хоста: DB_HOST=localhost, REDIS_URL=redis://localhost:6379/0).
- Выполните миграции: python manage.py migrate.
- Запустите сервер: python manage.py runserver.
- В отдельных терминалах запустите Celery:
`celery -A config worker -l info`
`celery -A config beat -l info`


## Тестирование

Запуск тестов с покрытием: `coverage run --source='habits,tg_bot,config' manage.py test`
`coverage report -m`

### CI/CD и автоматический деплой

Проект настроен на непрерывную интеграцию и доставку с помощью GitHub Actions.


### Настройка удалённого сервера

- Установите на сервере Docker и Docker Compose (плагин).
- Создайте пользователя (например, deploy) и добавьте его в группу docker. 
- Склонируйте репозиторий в /opt/habits-tracker:
`sudo mkdir -p /opt/habits-tracker`
`sudo chown deploy:deploy /opt/habits-tracker`
`git clone <your-repo-url> /opt/habits-tracker`
- Скопируйте файл .env на сервер (с реальными значениями) в /opt/habits-tracker/.env.
- Настройте SSH-доступ: сгенерируйте ключ для GitHub Actions и добавьте публичный ключ в ~/.ssh/authorized_keys пользователя deploy.



## Итоговые изменения

- Добавлен **Dockerfile** для сборки образа Django-приложения.
- **docker-compose.yml** дополнен сервисом `nginx` для раздачи статики и проксирования запросов.
- **entrypoint.sh** теперь выполняет сбор статики (`collectstatic`).
- Создан шаблон **.env.example**.
- Добавлен **GitHub Actions workflow** (`.github/workflows/ci_cd.yml`), который:
  - запускает линтинг и тесты,
  - проверяет сборку образов,
  - автоматически деплоит на сервер при пуше в `main`.
- В **requirements.txt** добавлен `gunicorn`.
- Обновлён **README.md** с подробными инструкциями по локальному запуску, CI/CD и деплою.

После добавления этих файлов в репозиторий проект можно запустить локально командой `docker-compose up -d`, а также настроить автоматический деплой через GitHub Actions.