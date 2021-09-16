## Проект «API YAMDB»
### Описание B
API YAMDB на Django REST Framefork. Предоставляет возможность оставлять отзывы на книги, фильмы и другие произведения.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
https://github.com/Nadezhda-Gurova/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
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

### Примеры 

#### Запрос

```http://127.0.0.1:8000/api/v1/titles/{titles_id}/```


#### Ответ
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```
#### Запрос

```http://127.0.0.1:8000/api/v1/categories/```


#### Ответ
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```

