import random

from rest_framework import views
from rest_framework import permissions
from django.http import JsonResponse


from users.models import Test, Course, Topic, Lesson, UserAnswer


def get_test_data(test):
    questions = []
    for question in test.question_set.all():
        answers = []
        for answer in question.answer_set.all():
            answers.append({
                'id': answer.id,
                'text': answer.text,
                'order_number': answer.order_number,
                'selected': None,
                'weight': answer.weight,
                'comment': answer.comment
            })
        questions.append({
            'id': question.id,
            'text': question.text,
            'comment': question.comment,
            'order_number': question.order_number,
            'weight': question.weight,
            'media': None if not question.attachment_link else question.attachment_link,
            'multiple': question.multiple,
            'options': answers,
            'is_correct': None
        })
    
    return questions


def calculate_test_results(data, questions):
    # Парсим данные из запроса
    # Считаем результаты теста
    total_weight = 0

    for question_data in questions:
        question_weight = question_data.get('weight')
        answers = question_data.get('options')
        user_answers = data[str(question_data['id'])]

        answer_total_weight = 0
        for answer in answers:
            answer_weight = answer.get('weight')

            if str(answer['id']) in user_answers:
                answer_total_weight += answer_weight
                answer['selected'] = True
        answer_total_weight = answer_total_weight // 100
        if answer_total_weight > 0:
            question_data['is_correct'] = True
        else: 
            question_data['is_correct'] = False
            answer_total_weight = 0
        question_weight = question_weight * answer_total_weight
        total_weight += question_weight
                
    return round(total_weight), questions


class TaskTestView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, test_id):
        pass

    def get(self, request, test_id):
        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            return JsonResponse({'error': 'Test does not exist'})

        questions = get_test_data(test)

        if test.shuffle:
            questions = random.shuffle(questions)

        data = {
            'id': test.id,
            'name': test.title,
            'description': test.description,
            'questions': questions
        }

        # Return the step as a JSON response
        return JsonResponse(data)


class CheckTaskTestView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, test_id):
        
        data = request.data

        test = Test.objects.get(id=test_id)
        questions = get_test_data(test)

        result_score, questions_data = calculate_test_results(data['questions'], questions)
        user = request.user

        step = test.step
        lesson = step.lesson
        topic = lesson.topic
        course = topic.course

        user_answer = UserAnswer.objects.create(user=user, course=course, topic=topic, lesson=lesson, step=step, test=test)
        user_answer.answers = questions_data

        # добавить логику сохранения максимального значения или последнего
        user_answer.total_result = result_score
        user_answer.time_spended = data['time_spended']
        user_answer.save()
        print(user_answer)

        # Return the step as a JSON response
        return JsonResponse({'status': 'ok'})


class ResultsTaskTestView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, test_id):
        user = request.user
        test = Test.objects.get(id=test_id)

        # Ищем ответы пользователя на заданный тест
        user_answer = UserAnswer.objects.filter(user=user, test=test).last()

        if user_answer:
            # Если ответы найдены, возвращаем их в виде JSON
            return JsonResponse(user_answer.answers, safe=False)
        else:
            # Если ответы не найдены, возвращаем ошибку
            return JsonResponse({'error': 'Answers not found'})



