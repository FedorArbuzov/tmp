import random

from django.contrib.auth import login, logout

from rest_framework import permissions
from rest_framework import status
from rest_framework import views
from rest_framework.response import Response

from users import serializers
from users.models import Course, StudentInfo, StudentsGroup, Course, Topic, Lesson, Step, Test, Question, UserAnswer
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
        user_answers = UserAnswer.objects.filter(user=request.user, course=course)
        last_user_answer = user_answers.last()

        # Get all the topics for this course
        topics = course.topics.all()

        # Convert the topics to a list of dictionaries
        topics_data = []
        for topic in topics:
            # Get all the lessons for this topic
            lessons = topic.lessons.all()
            topic_steps_total = 0
            topic_steps_complited = 0

            # Convert the lessons to a list of dictionaries
            lessons_data = []
            for lesson in lessons:

                steps_length = lesson.steps.count()
                topic_steps_total += steps_length
                steps_completed_length = user_answers.filter(lesson=lesson).count()
                topic_steps_complited += steps_completed_length
                lesson_data = {
                    'id': lesson.id,
                    'order_number': lesson.order_number,
                    'name': lesson.title,
                    'isOpened': True if steps_completed_length > 0 else False,
                    'isActive': True if last_user_answer.lesson == lesson else False,
                    'total': steps_length,
                    'completed': steps_completed_length,
                    'description': lesson.description,
                }
                lessons_data.append(lesson_data)

            topic_data = {
                'id': topic.id,
                'name': topic.title,
                'isFinished': True if topic_steps_complited == topic_steps_total else False,
                'isStarted': True if topic_steps_complited > 0 else False,
                'percentageCompleted': round(topic_steps_complited / topic_steps_total * 100),
                'lessons': lessons_data,
            }
            topics_data.append(topic_data)

        # Return the course as a JSON response
        return JsonResponse(topics_data, safe=False)


def get_step_test(step, user):
    if not step.test:
        return None
    answer = UserAnswer.objects.filter(user=user, test=step.test).last()
    return {
        'title': step.test.title,
        'description': step.test.description,
        'attempts_number': step.test.attempts_number,
        'num_of_questions': Question.objects.filter(test=step.test).count(),
        'time_spended': answer.time_spended,
        'persent': answer.total_result
    }

def get_step_id_or_none(lesson, order):
    try:
        s = Step.objects.get(lesson=lesson, order_number=order)
        return s.id
    except Step.DoesNotExist:
        return None


def get_step_data(step, user):
    print(step)
    return {
        'previous': get_step_id_or_none(step.lesson, step.order_number - 1),
        'next': get_step_id_or_none(step.lesson, step.order_number + 1),
        'id': step.id,
        'html': None if not step.html else step.html.content,
        'test': get_step_test(step, user)
    }

class LessonStepsView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, lesson_id):
        # Get the lesson object based on the lesson_id parameter
        lesson = Lesson.objects.get(id=lesson_id)
        user_answers = UserAnswer.objects.filter(user=request.user, lesson=lesson)

        # Get all the steps for this lesson
        steps = lesson.steps.all()

        # Convert the steps to a list of dictionaries
        step_data = {}
        for step in steps:
            is_step_done = user_answers.filter(step=step)
            if len(is_step_done) > 0:
                continue
            else:
                step_data = step
                break
            
        if not step_data:
            step_data = step
        current_step = step
        step_data = get_step_data(step_data, request.user)
        if step_data['html']:
            UserAnswer.objects.create(
                user=request.user, 
                course=current_step.lesson.topic.course, 
                topic=current_step.lesson.topic, 
                lesson=current_step.lesson, 
                step=current_step
            )
        # Return the steps as a JSON response
        return JsonResponse(step_data)


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

    