from django.contrib.auth import login, logout

from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import views
from rest_framework.response import Response

from users import serializers
from users.models import StudentInfo, StudentsGroup, Program
from django.views import View
from users.models import Course, CourseTopic, Lesson

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

class ProfileProgramsView(views.APIView):

    def get(self, request):
        user = request.user
        
        # Найти все группы, связанные с пользователем
        groups = StudentsGroup.objects.filter(users=user)

        # Создать пустой список для хранения программ
        programs = []

        # Пройти по всем группам и добавить все связанные с ними программы в список
        for group in groups:
            programs.extend(group.programs.all())

        programs = set(programs)

        # Вернуть список программ
        serializer = serializers.ProgramSerializer(programs, many=True)
        return Response(serializer.data)



class ProgramInfoView(views.APIView):

    def get_all_subprograms(self, program):
        subprograms = program.subprogram.all()
        for subprogram in subprograms:
            subprograms |= self.get_all_subprograms(subprogram)
        return subprograms
    

    def get(self, request):
        program = Program.objects.get(id=1)
        all_subprograms = self.get_all_subprograms(program)
        subprograms = []
        subprograms.append({
            'program': program,
            'all_subprograms': all_subprograms,
        })

        return subprograms


class CourseDataView(View):
    def get(self, request, *args, **kwargs):
        # Get all courses
        courses = Course.objects.all()

        # Create a list to store course data
        course_data = []

        # Loop through each course and add its data to the list
        for course in courses:
            course_topics = []

            # Loop through each topic for the course and add its data to the list
            for topic in course.topics.all():
                topic_lessons = []

                # Loop through each lesson for the topic and add its data to the list
                for lesson in topic.lessons.all():
                    lesson_data = {
                        'title': lesson.title,
                        'description': lesson.description,
                        'video_url': lesson.video_url,
                    }
                    topic_lessons.append(lesson_data)

                topic_data = {
                    'title': topic.title,
                    'description': topic.description,
                    'image': topic.image,
                    'lessons': topic_lessons,
                }
                course_topics.append(topic_data)

            course_data.append({
                'title': course.title,
                'description': course.description,
                'image': course.image,
                'topics': course_topics,
            })

        # Return course data as JSON response
        return JsonResponse({'courses': course_data})

