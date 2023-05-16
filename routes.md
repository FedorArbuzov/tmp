# Методы

## Залогиниться

POST http://px-dev-backend.platonics.ru:8080/login/

ЗАПРОС
```
{
    "username": "user1",
    "password": "password1"
}
```

ОТВЕТ

```
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4NDMxOTE5MCwiaWF0IjoxNjg0MjMyNzkwLCJqdGkiOiJhMjQ2OGI3YmQ3ZWI0MThkOGIyOGY5MmJkNWZmOTc1NSIsInVzZXJfaWQiOjJ9.rs4IgqECznxYcp6ZZSY2qvG3xaM2R4vT0rhoWetrgHA",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkyODcyNzkwLCJpYXQiOjE2ODQyMzI3OTAsImp0aSI6ImNhZjcwOTcxMWI4NDQ0ODZhOGY4NzU5Y2NiODQ2MmRkIiwidXNlcl9pZCI6Mn0.q08vbWo-SEwAGjmus3MBBQIy1mt8MdcdQ6szNH-dM-k"
}

```
## Получить все курсы пользователя

GET http://px-dev-backend.platonics.ru:8080/profile/courses/

ОТВЕТ

```
[
    {
        "title": "Python for Beginners",
        "id": 1
    }
]
```

массив из курсов с title и id

id берем и подставляем в следующий запрос

## Получить роадмап по курсу для пользователя

GET http://px-dev-backend.platonics.ru:8080/courses/1/

ОТВЕТ

```
[
    {
        "id": 1,
        "name": "Python Basics",
        "isFinished": false,
        "isStarted": true,
        "percentageCompleted": 60,
        "lessons": [
            {
                "id": 1,
                "order_number": 0,
                "name": "Introduction to Python",
                "isOpened": true,
                "isActive": true,
                "total": 3,
                "completed": 3,
                "description": "Learn about Python and the Python interpreter"
            },
            {
                "id": 2,
                "order_number": 1,
                "name": "Variables and Data Types",
                "isOpened": false,
                "isActive": false,
                "total": 2,
                "completed": 0,
                "description": "Learn how to use variables and data types in Python"
            }
        ]
    },
    {
        "id": 2,
        "name": "Functions and Loops",
        "isFinished": false,
        "isStarted": false,
        "percentageCompleted": 0,
        "lessons": [
            {
                "id": 3,
                "order_number": 0,
                "name": "Introduction to Python",
                "isOpened": false,
                "isActive": false,
                "total": 3,
                "completed": 0,
                "description": "Learn about Python and the Python interpreter"
            },
            {
                "id": 4,
                "order_number": 1,
                "name": "Variables and Data Types",
                "isOpened": false,
                "isActive": false,
                "total": 2,
                "completed": 0,
                "description": "Learn how to use variables and data types in Python"
            }
        ]
    }
]
```

## Провалиться в урок из роадмапа

Тут нужно взять id урока из роадмапа и подставить в запрос

GET http://px-dev-backend.platonics.ru:8080/lessons/1/

```
{
    "previous": 2,
    "next": null,
    "id": 3,
    "html": null,
    "test": {
        "title": "Test 1",
        "id": 1,
        "description": "Description 1",
        "attempts_number": 3,
        "attempts_number_used": 1,
        "num_of_questions": 2,
        "time_spended": 15,
        "perсent": 50
    }
}
```

в полях previous и next лежат id предыдущего и следущего step, если хочется ходить по разным пунктам урока, то их нужно подложит в следующий запрос

## Получить конкретный шаг урока

GET http://px-dev-backend.platonics.ru:8080/steps/1/

```
{
    "previous": null,
    "next": 2,
    "id": 1,
    "html": "<p>intro python</p>",
    "test": null
}
```

Если в шаге тест, то можно провалиться в тест по id теста

## Открыть тест

GET http://px-dev-backend.platonics.ru:8080/test/1/

```

```



