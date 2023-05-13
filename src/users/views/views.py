import random

from django.contrib.auth import login, logout

from rest_framework import permissions
from rest_framework import status
from rest_framework import views
from rest_framework.response import Response

from users import serializers
from users.models import Course, StudentInfo, StudentsGroup, Course, Topic, Lesson, Step, Test, UserAnswer
from users.utils.count_total_test_weight import calculate_test_results

from django.http import JsonResponse

from rest_framework_simplejwt.tokens import RefreshToken


class LoginView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = serializers.LoginSerializer(data=self.request.data, context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class LogoutView(views.APIView):

    def post(self, request, format=None):
        logout(request)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class ProfileCoursesView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        
        # Найти все группы, связанные с пользователем
        groups = StudentsGroup.objects.filter(users=user)

        # Создать пустой список для хранения программ
        courses = []

        # Пройти по всем группам и добавить все связанные с ними программы в список
        for group in groups:
            courses.extend(group.courses.all())

        courses = set(courses)

        # Вернуть список программ
        serializer = serializers.CourseSerializer(courses, many=True)
        return Response(serializer.data)


class CourseDetailView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, course_id):
        # Get the course object based on the course_id parameter
        course = Course.objects.get(id=course_id)

        # Get all the topics for this course
        topics = course.topics.all()

        # Convert the topics to a list of dictionaries
        topics_data = []
        for topic in topics:
            # Get all the lessons for this topic
            lessons = topic.lessons.all()

            # Convert the lessons to a list of dictionaries
            lessons_data = []
            for lesson in lessons:

                lesson_data = {
                    'id': lesson.id,
                    'title': lesson.title,
                    'total': 5,
                    'completed': 5,
                    'description': lesson.description,
                }
                lessons_data.append(lesson_data)

            topic_data = {
                'id': topic.id,
                'title': topic.title,
                'description': topic.description,
                'image': topic.image,
                'total': 5,
                'completed': 5,
                'lessons': lessons_data,
            }
            topics_data.append(topic_data)

        # Convert the course to a dictionary
        course_data = {
            'id': course.id,
            'title': course.title,
            'description': course.description,
            'total': 5,
            'completed': 5,
            'image': course.image,
            'topics': topics_data,
        }

        # Return the course as a JSON response
        return JsonResponse({'course': course_data})


class LessonStepsView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, lesson_id):
        # Get the lesson object based on the lesson_id parameter
        lesson = Lesson.objects.get(id=lesson_id)

        # Get all the steps for this lesson
        steps = lesson.steps.all()

        # Convert the steps to a list of dictionaries
        steps_data = []
        for step in steps:
            step_data = {
                'id': step.id,
                'title': step.name,
            }
            steps_data.append(step_data)

        # Return the steps as a JSON response
        return JsonResponse({'steps': steps_data})


class StepDetailView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, step_id):
        # Get the step object based on the step_id parameter
        step = Step.objects.get(id=step_id)

        # Get the test for this step, if it exists
        test = step.test
        test_data = None
        if test:
            test_data = {
                'id': test.id,
            }

        # Get the HTML page for this step, if it exists
        html_page = step.html
        html_page_data = None
        if html_page:
            html_page_data = {
                'id': html_page.id,
            }

        # Convert the step to a dictionary
        step_data = {
            'id': step.id,
            'name': step.name,
            'test': test_data,
            'html_page': html_page_data,
        }

        # Return the step as a JSON response
        return JsonResponse({'step': step_data})


class TaskTestView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

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


# добавить метод получения статистик по всем разделам



class StatsView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request):
        section_type = request.GET["section_type"]
        section_id = request.GET["section_id"]
        if section_type == 'course':
            return JsonResponse({'results': {
                'stats': [{
                    'title': 'Русский язык',
                    'passed': 12,
                    'total': 20,
                    'average_score': 80,
                    'group_score': 95
                }],
            }})
        elif section_type == 'lesson':
            return JsonResponse({'results': {
                'stats': [{
                    'title': 'Тест методы изучения биологии',
                    'average_score': 80,
                    'group_score': 95,
                    'attempts': 1,
                    'date': '06.04.23',
                    'time': '02:03:00'
                }],
            }})

    