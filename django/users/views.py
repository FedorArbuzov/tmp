from django.contrib.auth import login, logout

from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import views
from rest_framework.response import Response

from users import serializers
from users.models import StudentInfo, StudentsGroup
from django.views import View
from users.models import Course

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.http import JsonResponse

from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta


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


class ProfileView(generics.RetrieveAPIView):
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user

class ProfileCoursesView(views.APIView):

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


class CourseDetailView(View):
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
                    'description': lesson.description,
                }
                lessons_data.append(lesson_data)

            topic_data = {
                'id': topic.id,
                'title': topic.title,
                'description': topic.description,
                'image': topic.image,
                'lessons': lessons_data,
            }
            topics_data.append(topic_data)

        # Convert the course to a dictionary
        course_data = {
            'id': course.id,
            'title': course.title,
            'description': course.description,
            'image': course.image,
            'topics': topics_data,
        }

        # Return the course as a JSON response
        return JsonResponse({'course': course_data})

