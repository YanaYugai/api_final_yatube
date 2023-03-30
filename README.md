# api_final
# Телеграм_бот для отслеживания статуса домашней работы

## Описание

Учебный проект. Реализовано Api для проекта yatube. API длступно 
только для авторизованный пользователей за исключением 
некоторых запросов(более подробную информацию можно найти 
http://127.0.0.1:8000/redoc/)

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

git clone git@github.com:YanaYugai/api_final_yatube.git
cd yatube_api

Cоздать и активировать виртуальное окружение:

python3 -m venv env
source env/bin/activate

Установить зависимости из файла requirements.txt:

python3 -m pip install --upgrade pip
pip install -r requirements.txt

Выполнить миграции:

python3 manage.py migrate

Запустить проект:

python3 manage.py runserver
