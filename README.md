# backend

### Ветки
- main - основная ветка.
- develop - ветка разработки, сюда сливаем все fix, features и т.д.

### Как развернуть у себя

Вам нужен будет установленый Git и Python 3. Последовательность шагов следующая.

Клонируем репозиторий:
```
git clone https://github.com/by-the-ticket-take-the-ride/backend/
```

Переключаемся на ветку разработки:
```
git checkout develop
```
Создаем виртуальное окружение:
```
python -m venv venv
```

Активируем виртуальное окружение:
```
source venv/Scripts/activate
```

Устанавливаем зависимости:
```
pip install -r requirements.txt
```

Создаем миграции:
```
python manage.py makemigrations api
```
```
python manage.py makemigrations events
```

Выполняем миграции:
```
python manage.py migrate
```

Есть возможность загрузки фикстур - данных о городах и типах мероприятий. Для этого нужно выполнить команды:
Загрузить данные о городах из json:
```
python manage.py import_data --write_cities_json
```
Загрузить данные о городах из csv:
```
python manage.py import_data --write_cities_csv
```
Прочитать данные о городах:
```
python manage.py import_data --read_cities
```

Загрузить данные о типах мероприятий:
```
python manage.py import_data --write_types
```

Прочитать данные о типах мероприятий:
```
python manage.py import_data --read_types
```

Запускаем сервер разработчика:
```
python manage.py runserver
```

При успешном запуске в консоли должно появиться следующее:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
August 11, 2023 - 09:28:47
Django version 4.2.1, using settings 'wiki.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

Документация доступна по ссылке:
```
http://127.0.0.1:8000/api/docs
```

Чтобы остановить работу сервера разработчика, нажмине Ctrl+C.
