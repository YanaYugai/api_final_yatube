# api_final

## Описание

Учебный проект. Реализовано API для проекта “yatube” . API доступно
только для авторизованный пользователей за исключением
некоторых запросов(более подробную информацию можно найти
<http://127.0.0.1:8000/redoc/>)

## Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone git@github.com:YanaYugai/api_final_yatube.git
cd yatube_api
```

Cоздать и активировать виртуальное окружение:

python3 -m venv env
source env/bin/activate

Установить зависимости из файла `requirements.txt`:

```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Выполнить миграции:

```bash
python3 manage.py migrate
```

Запустить проект:

```bash
python3 manage.py runserver
```
