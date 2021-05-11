# создать образ на основе базового слоя python (там будет ОС и интерпретатор Python)
FROM python:3.8.5

LABEL author='rusich' version=1

# создать директорию /code
RUN mkdir /code

# скопировать всё содержимое директории, в которой лежит докерфайл, в директорию /code
COPY . /code

# делаем рабочую деррикторию
WORKDIR /code

# выполнить команду (как в терминале, с тем же синтаксисом) для установки пакетов из requirements.txt
RUN pip install -r requirements.txt

RUN python manage.py collectstatic --no-input

# при старте контейнера выполнить runserver
CMD python manage.py migrate && --bind 0.0.0.0:8000 api_yamdb.wsgi