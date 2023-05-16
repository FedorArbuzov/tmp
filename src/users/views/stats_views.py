from rest_framework import views
from rest_framework import permissions
from django.http import JsonResponse

from django.db.models import Avg


from users.models import UserAnswer, Course, Topic, Lesson, Step, StudentsGroup

def get_course_users(course):
    # Получаем все группы, связанные с курсом
    groups = course.studentsgroup_set.all()

    # Получаем всех пользователей, связанных со всеми группами
    users = []
    for group in groups:
        users += list(group.users.all())

    # Возвращаем список всех пользователей
    return users


def get_user_courses(user):
    # Найти все группы, связанные с пользователем
    groups = StudentsGroup.objects.filter(users=user)

    # Создать пустой список для хранения программ
    courses = []

    # Пройти по всем группам и добавить все связанные с ними программы в список
    for group in groups:
        courses.extend(group.courses.all())

    courses = set(courses)
    return courses    


def get_data_course_user(user, course):
    steps = Step.objects.filter(lesson__topic__course=course).exclude(test=None).values_list('id', flat=True)
    user_answers = UserAnswer.objects.filter(step__in=steps, user=user)
    user_answers_avg = user_answers.aggregate(Avg('total_result'))['total_result__avg']
    return {
        'title': course.title,
        'description': course.description,
        'completed_tests': user_answers.count(),
        'total_tests': steps.count(),
        'avg': round(user_answers_avg) if user_answers_avg else 0
    }

def get_stats_for_course(course_id, user):
    course = Course.objects.get(id=course_id)
    topics = course.topics.all()

    # Получаем среднее значение поля total_result для каждого топика
    average_total_result_by_topic = {}
    for topic in topics:
        user_answers = UserAnswer.objects.filter(topic=topic).exclude(test=None)
        current_user_answers = UserAnswer.objects.filter(topic=topic, user=user).exclude(test=None)
        average_total_result_by_topic[topic] = {
            'total_avg': user_answers.aggregate(Avg('total_result'))['total_result__avg'],
            'avg': current_user_answers.aggregate(Avg('total_result'))['total_result__avg']
        }

    # Возвращаем результат
    return average_total_result_by_topic

class StatsView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        courses = get_user_courses(user)
        results = []
        for course in courses:
            result = get_data_course_user(user, course)
            results.append(result)

        return JsonResponse(results, safe=False)


class StatsDetailView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        model_type = request.GET.get('model_type')
        model_id = request.GET.get('model_type')
        user = request.user
        courses = get_user_courses(user)
        results = []
        for course in courses:
            users = get_course_users(course)
            user_results = {}
            course_avg = 0
            for course_user in users:
                user_stats = get_data_course_user(course_user, course)
                course_avg += user_stats['avg']
                if course_user == user:
                    user_results = user_stats

            user_results['total_avg'] = round(course_avg / len(users))     
            results.append(user_results)
        
        return JsonResponse(results, safe=False)
