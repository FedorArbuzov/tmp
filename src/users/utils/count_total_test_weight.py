

def calculate_test_results(data):
    # Парсим данные из запроса
    questions = data.get('result').get('questions')

    # Считаем результаты теста
    total_weight = 0

    for question_data in questions:
        question_weight = question_data.get('weight')
        answers = question_data.get('options')

        answer_total_weight = 0
        for answer in answers:
            is_selected = answer.get('selected')
            answer_weight = answer.get('weight')

            if is_selected:
                answer_total_weight += answer_weight

        answer_total_weight = answer_total_weight // 100
        question_weight = question_weight * answer_total_weight
        total_weight += question_weight
                
    return round(total_weight, 2)
    