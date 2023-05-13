# Работа с тестами

## Получение информации о тесте:

По методу `/test/10/` можно получить данные о тесте в виде:

```

{
    "result": {
        "id": 10,
        "name": "Test 1",
        "description": "Description 1",
        "questions": [
            {
                "id": 7,
                "text": "Question 1",
                "comment": "Comment 1",
		        "is_correct": null,
		        "multiple": false,
                "order_number": 1,
                "weight": 0,
                "attachment_link": "https://example.com/file1.img",
                "answers": [
                    {
                        "id": 11,
                        "text": "Answer 1",
			            "selected": null,
                        "order_number": 1,
                        "weight": 40,
                        "comment": "Comment 1"
                    },
                    {
                        "id": 12,
                        "text": "Answer 2",
                        "order_number": 2,
			            "selected": null,
                        "weight": -50,
                        "comment": "Comment 2"
                    },
                    {
                        "id": 13,
                        "text": "Answer 3",
                        "order_number": 3,
			            "selected": null,
                        "weight": 60,
                        "comment": "Comment 3"
                    },
                    {
                        "id": 14,
                        "text": "Answer 4",
                        "order_number": 4,
			            "selected": null,
                        "weight": -50,
                        "comment": "Comment 4"
                    }
                ]
            },
            {
                "id": 8,
                "text": "Question 2",
                "comment": "Comment 2",
		        "is_correct": null,
		        "multiple": true,
                "order_number": 2,
                "weight": 0,
                "attachment_link": null,
                "answers": [
                    {
                        "id": 11,
                        "text": "Answer 1",
			            "selected": null,
                        "order_number": 1,
                        "weight": 40,
                        "comment": "Comment 1"
                    },
                    {
                        "id": 12,
                        "text": "Answer 2",
                        "order_number": 2,
			            "selected": null,
                        "weight": -50,
                        "comment": "Comment 2"
                    },
                    {
                        "id": 13,
                        "text": "Answer 3",
                        "order_number": 3,
			            "selected": null,
                        "weight": 60,
                        "comment": "Comment 3"
                    },
                    {
                        "id": 14,
                        "text": "Answer 4",
                        "order_number": 4,
			            "selected": null,
                        "weight": -50,
                        "comment": "Comment 4"
                    }
		        ]
            }
        ]
    }
}
```

Результаты получаем через post запрос

```
{
    "1": ["1", "3"],
    "4": ["6", "1"],
}
```

На бекенде склеиваем это все с данными выше, получаем процент выполнения и сохраняем в базе

