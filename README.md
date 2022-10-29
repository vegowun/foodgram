### Foodgram

Проект "продуктовый помощник".
Сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на
публикации других авторов. А также создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

### Установка. Как запустить backend проекта:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/gevolx/foodgram-project-react.git
```

```
cd backend
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Запуск frontend проекта:

```
cd frontend
npm install
npm run build
npm start
```

### Примеры запросов к API:

Список ингредиентов.

```
GET http://127.0.0.1:8000/api/ingredients/
```

Добавить рецепт в список покупок.

```
POST http://127.0.0.1:8000/api/recipes/{id}/shopping_cart/
```

Скачать список покупок.

```
GET http://127.0.0.1:8000/api/recipes/download_shopping_cart/
```

Полный перечень запросов к API можно получить по эндпоинту /redoc

```
http://localhost/api/docs
```

### Проект развернут и доступен на сервере - http://51.250.23.122

### Процесс деплоя

В директории infra необходимо создать .env файл

### Наполнение .env файла

```angular2html
SECRET_KEY=
DEBUG=False
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
DB_HOST=db
DB_PORT=5432
PATH_JSON_INGREDIENTS=/app/data/ingredients.json
```

### Запуск приложения в контейнерах

Находясь в директории infra необходимо выполнить команду

```
docker-compose up -d --build
```

После успешного запуска контейнеров необходимо создать супер пользователя

```
docker-compose exec backend python manage.py createsuperuser
```
