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
                "isCompleted": true,
                "totalTasks": 3,
                "completedTasks": 3,
                "description": "Learn about Python and the Python interpreter"
            },
            {
                "id": 2,
                "order_number": 1,
                "name": "Variables and Data Types",
                "isOpened": false,
                "isActive": false,
                "isCompleted": false,
                "totalTasks": 2,
                "completedTasks": 0,
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
                "isCompleted": false,
                "totalTasks": 3,
                "completedTasks": 0,
                "description": "Learn about Python and the Python interpreter"
            },
            {
                "id": 4,
                "order_number": 1,
                "name": "Variables and Data Types",
                "isOpened": false,
                "isActive": false,
                "isCompleted": false,
                "totalTasks": 2,
                "completedTasks": 0,
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
{
    "id": 1,
    "name": "Test 1",
    "description": "Description 1",
    "questions": [
        {
            "id": 1,
            "text": "Question 1",
            "comment": "Comment 1",
            "order_number": 0,
            "weight": 50,
            "media": "https://example.com/file1.pdf",
            "multiple": false,
            "options": [
                {
                    "id": 1,
                    "text": "Answer 1",
                    "order_number": 0,
                    "selected": null,
                    "weight": 40,
                    "comment": "Comment 1"
                },
                {
                    "id": 2,
                    "text": "Answer 2",
                    "order_number": 1,
                    "selected": null,
                    "weight": -50,
                    "comment": "Comment 2"
                },
                {
                    "id": 3,
                    "text": "Answer 3",
                    "order_number": 2,
                    "selected": null,
                    "weight": 60,
                    "comment": "Comment 3"
                },
                {
                    "id": 4,
                    "text": "Answer 4",
                    "order_number": 3,
                    "selected": null,
                    "weight": -50,
                    "comment": "Comment 4"
                }
            ],
            "is_correct": null
        },
        {
            "id": 2,
            "text": "Question 2",
            "comment": "Comment 2",
            "order_number": 1,
            "weight": 50,
            "media": null,
            "multiple": true,
            "options": [
                {
                    "id": 5,
                    "text": "Answer 5",
                    "order_number": 0,
                    "selected": null,
                    "weight": 30,
                    "comment": "Comment 1"
                },
                {
                    "id": 6,
                    "text": "Answer 6",
                    "order_number": 1,
                    "selected": null,
                    "weight": -20,
                    "comment": "Comment 2"
                },
                {
                    "id": 7,
                    "text": "Answer 7",
                    "order_number": 2,
                    "selected": null,
                    "weight": 70,
                    "comment": "Comment 3"
                },
                {
                    "id": 8,
                    "text": "Answer 8",
                    "order_number": 3,
                    "selected": null,
                    "weight": -80,
                    "comment": "Comment 4"
                }
            ],
            "is_correct": null
        }
    ]
}
```

Этот метод отдает данные для отрисовки теста


## Отправить ответ

GET http://px-dev-backend.platonics.ru:8080/test/check/1/

```
{
    "time_spended": 15,
    "questions": {
        "1": ["1", "3"],
        "2": ["2", "4"]
    }
}
```

Здесь time_spended время в секундах, questions - набор из ответов на вопросы

## Посмотреть решения теста

GET http://px-dev-backend.platonics.ru:8080/test/results/1/

```
[
    {
        "id": 1,
        "text": "Question 1",
        "media": "https://example.com/file1.pdf",
        "weight": 50,
        "result": "Частично правильный",
        "comment": "Comment 1",
        "options": [
            {
                "id": 1,
                "text": "Answer 1",
                "weight": 40,
                "comment": "Comment 1",
                "selected": true,
                "order_number": 0
            },
            {
                "id": 2,
                "text": "Answer 2",
                "weight": -50,
                "comment": "Comment 2",
                "selected": null,
                "order_number": 1
            },
            {
                "id": 3,
                "text": "Answer 3",
                "weight": 60,
                "comment": "Comment 3",
                "selected": true,
                "order_number": 2
            },
            {
                "id": 4,
                "text": "Answer 4",
                "weight": -50,
                "comment": "Comment 4",
                "selected": null,
                "order_number": 3
            }
        ],
        "multiple": false,
        "is_correct": true,
        "order_number": 0
    },
    {
        "id": 2,
        "text": "Question 2",
        "media": null,
        "weight": 50,
        "comment": "Comment 2",
        "options": [
            {
                "id": 5,
                "text": "Answer 5",
                "weight": 30,
                "comment": "Comment 1",
                "selected": null,
                "order_number": 0
            },
            {
                "id": 6,
                "text": "Answer 6",
                "weight": -20,
                "comment": "Comment 2",
                "selected": null,
                "order_number": 1
            },
            {
                "id": 7,
                "text": "Answer 7",
                "weight": 70,
                "comment": "Comment 3",
                "selected": null,
                "order_number": 2
            },
            {
                "id": 8,
                "text": "Answer 8",
                "weight": -80,
                "comment": "Comment 4",
                "selected": null,
                "order_number": 3
            }
        ],
        "multiple": true,
        "is_correct": false,
        "order_number": 1
    }
]
```

## Получение бредкрампосов

GET http://px-dev-backend.platonics.ru:8080/breadcrumbs?model_type=step&model_id=1

```
[
    {
        "title": "Python for Beginners",
        "id": 1,
        "type": "course"
    },
    {
        "title": "Python Basics",
        "id": 1,
        "type": "topic"
    },
    {
        "title": "Introduction to Python",
        "id": 1,
        "type": "lesson"
    },
    {
        "title": "Declaring variables 1",
        "id": 1,
        "type": "step"
    }
]
```

## Получение всех актуальных

GET http://px-dev-backend.platonics.ru:8080/profile/actual/

```
[
    {
        "id": 2,
        "title": "Test 1",
        "left_days": 109,
        "left_attempts": 4
    },
    {
        "id": 1,
        "title": "Test 1",
        "left_days": 111,
        "left_attempts": 4
    }
]
```

Тут массив из актуальных заданий: получаем сколько осталось дней, сколько осталось попыток, id теста, и его название

## Получение базовой статистики на главной

GET http://px-dev-backend.platonics.ru:8080/profile/stats_short/

```
[
    {
        "title": "Python for Beginners",
        "description": "Learn Python programming from scratch",
        "completed_tests": 1,
        "total_tests": 4,
        "avg": 50
    }
]
```

Получаем массив объектов, где каждый массив это отдельный курс с числом сделанных тестов, всего тестов и среднего процента по тестам 

## Получение информации о пользователе

GET http://px-dev-backend.platonics.ru:8080/profile/

```
{
    "avatar": null,
    "phone": "333-33-33",
    "mail": "mail1@example.com",
    "date_birth": "2000-01-01",
    "responsible_1": {
        "full_name": "Responsible1 FIO",
        "phone": "111-11-11",
        "mail": "responsible1@example.com"
    },
    "responsible_2": {
        "full_name": "Responsible2 FIO",
        "phone": "222-22-22",
        "mail": "responsible2@example.com"
    }
}
```


## Измениение/Добавление аватара

POST http://px-dev-backend.platonics.ru:8080/profile/avatar/

```
{
    "file": "...",
    "file_name": "avatar.png"
}
```

## Удаление аватара

DELETE http://px-dev-backend.platonics.ru:8080/profile/avatar/

## Получение продвинутой статистики

GET http://px-dev-backend.platonics.ru:8080/profile/stats_detail/

```
[
    {
        "title": "Python for Beginners",
        "description": "Learn Python programming from scratch",
        "completed_tests": 3,
        "total_tests": 4,
        "avg": 67,
        "total_avg": 34
    }
]
```

Тут еще добавляется паравметр total_avg - среднее по ресурсу


## Получение уроков для темы

GET http://px-dev-backend.platonics.ru:8080/topic/1/

```
[
    {
        "id": 1,
        "order_number": 0,
        "name": "Introduction to Python",
        "isOpened": true,
        "isActive": true,
        "isCompleted": false,
        "totalTasks": 3,
        "completedTasks": 6,
        "description": "Learn about Python and the Python interpreter"
    },
    {
        "id": 2,
        "order_number": 1,
        "name": "Variables and Data Types",
        "isOpened": false,
        "isActive": false,
        "isCompleted": false,
        "totalTasks": 2,
        "completedTasks": 0,
        "description": "Learn how to use variables and data types in Python"
    }
]
```

## Получение актуальных по теме 

GET http://px-dev-backend.platonics.ru:8080/profile/actual/?topic_id=1

```
[
    {
        "id": 2,
        "title": "Test 1",
        "left_days": 109,
        "left_attempts": 4
    },
    {
        "id": 1,
        "title": "Test 1",
        "left_days": 111,
        "left_attempts": 4
    }
]
```

Чтобы получить актуальные по теме нужно передать topic_id get параметром


## Получение продвинутой статистики по курсу

GET http://px-dev-backend.platonics.ru:8080/profile/stats_detail/?course_id=1

```
[
    {
        "title": "Python for Beginners",
        "description": "Learn Python programming from scratch",
        "completed_tests": 3,
        "total_tests": 4,
        "avg": 67,
        "total_avg": 34
    }
]
```


## Получение продвинутой статистики по теме

GET http://px-dev-backend.platonics.ru:8080/profile/stats_detail/?topic_id=1

```
[
    {
        "title": "Python for Beginners",
        "description": "Learn Python programming from scratch",
        "completed_tests": 3,
        "total_tests": 4,
        "avg": 67,
        "total_avg": 34
    }
]
```


## Получение продвинутой статистики по уроку/теме/курсу

GET http://px-dev-backend.platonics.ru:8080/profile/stats_detail/?lesson_id=1

```
[
    {
        "title": "Test 1",
        "id": 1,
        "user_percent": 55,
        "group_percent": 40,
        "date": "06.04.2023",
        "time": "02:30:00",
        "attempts": 2
    },
    {
        "title": "Test 1",
        "id": 2,
        "user_percent": 55,
        "group_percent": 40,
        "date": "06.04.2023",
        "time": "02:30:00",
        "attempts": 2
    },
    {
        "title": "Test 1",
        "id": 3,
        "user_percent": 55,
        "group_percent": 40,
        "date": "06.04.2023",
        "time": "02:30:00",
        "attempts": 2
    },
    {
        "title": "Test 1",
        "id": 4,
        "user_percent": 55,
        "group_percent": 40,
        "date": "06.04.2023",
        "time": "02:30:00",
        "attempts": 2
    }
]
```

## Получение выполненных тестов по теме

GET http://px-dev-backend.platonics.ru:8080/topic/1/tests

```
[
    {
        "title": "Test 1",
        "percent": 50,
        "allowed_attempts": 3,
        "left_days": 4,
        "used_attempts": 3
    }
]
```
