# YaMDB - API сервис - База отзывов о фильмах, книгах и музыке
## Описание

Учебный проект

Развернут на сервере тремя докер контейнерами с помощью docker-compose

Описание API доступно по адресу http://yamdb.rusich90.ru/redoc

Для создания были использованы и изучены:

* Python
* Django
* REST API
* PostgreSQL
* Linux
* JWT Token
* smtp gmail
* Gunicorn, NGINX
* Docker, Docker-compose

Возможности:

* Оставлять отзывы и ставить оценки о фильмах, книгах, музыке.
* Комментировать чужие отзывы
* Разные уровни доступа для юзеров, модераторов и админов
* Добавлять произведения, жанры и категории может только администратор

## Установка 
Клонируем репозиторий на локальную машину:

```$ git clone https://github.com/Rusich90/yamdb.git```

Запускаем сборку докера:
 
 ```$ docker-compose up```
 
Для создания админа джанго нужно зайти в контейнер приложения:

```$ docker exec -it <CONTAINER ID> bash```

ID контейнера узнать командой:

```$ docker container ls```

Создать суперюзера:

```$ python manage.py createsuperuser```

API доступен по адресу http://127.0.0.1:80

По инструкции на http://yamdb.rusich90.ru/redoc получаем confarmation-code и token
