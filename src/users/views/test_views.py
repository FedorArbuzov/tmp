import random

from rest_framework import views
from rest_framework import permissions
from django.http import JsonResponse


from users.models import Test


def get_test_data(test_id):
    test = Test.objects.get(id=test_id)
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
            'attachment_link': question.attachment_link,
            'options': answers
        })

    


class TaskTestView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, test_id):
        pass

    def get(self, request, test_id):
        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            return JsonResponse({'error': 'Test does not exist'})

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
                'attachment_link': question.attachment_link,
                'options': answers
            })

        if test.shuffle:
            random.shuffle(questions)

        data = {
            'id': test.id,
            'name': test.name,
            'description': test.description,
            'questions': questions
        }

        # Return the step as a JSON response
        return JsonResponse(data)



class CheckTaskTestView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, test_id):
        
        data = request.data
        
        result_score = calculate_test_results(data)
        user = request.user
        course = Course.objects.get(id=data['result']['course'])
        course_topic = Topic.objects.get(id=data['result']['topic'])
        lesson = Lesson.objects.get(id=data['result']['lesson'])
        test = Test.objects.get(id=test_id)

        user_answer, is_created = UserAnswer.objects.get_or_create(user=user, course=course, topic=course_topic, lesson=lesson, test=test)
        user_answer.answers = data

        # добавить логику сохранения максимального значения или последнего
        user_answer.total_result = result_score
        print(user_answer, is_created)

        # Return the step as a JSON response
        return JsonResponse({'status': 'ok'})


class ResultsTaskTestView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, test_id):
        user = request.user
        test = Test.objects.get(id=test_id)

        # Ищем ответы пользователя на заданный тест
        user_answer = UserAnswer.objects.filter(user=user, test=test).first()

        if user_answer:
            # Если ответы найдены, возвращаем их в виде JSON
            return JsonResponse(user_answer.answers)
        else:
            # Если ответы не найдены, возвращаем ошибку
            return JsonResponse({'error': 'Answers not found'})



