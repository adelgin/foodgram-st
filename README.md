# Итоговый проект Foodgram

Foodgram является итоговым проектом для курсов по бэкенд разработке от Яндекса и представляет собой сервис для создания и обмена рецептами.

Автор проекта [Гиниятуллин Адель](https://github.com/adelgin)

### **План по настройке и запуску проекта**

## 1. Клонирование проекта

Для клонирования репозитория в терминале выполните команду:

```
git clone https://github.com/adelgin/foodgram-st
```

## 2. Создание .env файла

В директории `foodgram-st/backend/foodgram` создайте файл .env с таким содержанием:

```
DEBUG=True
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=foodgram_db
POSTGRES_USER=django_user
POSTGRES_PASSWORD=django_password
DB_HOST=db
DB_PORT=5432
```

## 3. Сборка проекта

Перейдите в директорию `foodgram-st/infra` и в консоли введите команду 

```
docker compose up --build
```

Дождитесь пока соберутся все контейнеры и база данных будет готова принимать запросы

## 4. Применение миграций

Находясь в этой же директории выполните команду:

```
docker compose exec backend python manage.py migrate
```

## 5. Создание суперпользователя

Находясь в той же директории выполните команду:

```
docker compose exec backend python manage.py createsuperuser
```

## 6. Внесение тестовых данных

Чтобы внести тестовые данные для проверки функционала в терминале в директории `foodgram-st/infra` необходимо выполнить команду:

```
docker compose exec backend python manage.py loaddata initial_data/ingredients.json initial_data/users.json initial_data/recipes.json
```

## 7. Проверка проекта

Проект будет доступен по ссылке <http://localhost/>

Документация к API будет доступна по ссылке <http://localhost/api/docs/>

Админка проекта будет доступна по ссылке <http://localhost/admin/>

## 8. Удаление проекта

Для остановки контейнеров в директории `foodgram-st/infra` выполните команду:

```
docker compose stop
```

Для удаления контейнеров введите команду:

```
docker compose rm
```

Для удаления хранилищ введите команду:

```
docker volume rm infra_pg_data infra_media_data infra_static_data
```