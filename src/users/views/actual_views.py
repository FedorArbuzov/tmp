from rest_framework import views
from rest_framework import permissions
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q, Count


from users.models import Test, Topic, StudentsGroup, UserAnswer


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


class ActualView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        current_date = timezone.now().date()
        topic_id = request.GET.get('topic_id')
        if topic_id is not None:
            # если есть топик в параметрах то получаем актуальные только по нему
            topics = Topic.objects.filter(id=topic_id)
            query = Q(step__lesson__topic__in=topics)    
        else:
            # если топика нет, то достаем все задачи из курсов пользователя
            courses = get_user_courses(request.user)
            query = Q(step__lesson__topic__course__in=courses)
        tests = Test.objects.filter(Q(end_date__gte=current_date) & query).order_by('end_date')
        user_answers = UserAnswer.objects.filter(test__in=tests)
        results = []
        for test in tests:
            results.append({
                'id': test.id,
                'title': test.title,
                'description': test.description,
                'left_days': (test.end_date - current_date).days,
                'left_attempts': 4
            })
        return JsonResponse(results, safe=False)


class ActualCoursesView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        courses = get_user_courses(request.user)
        current_date = timezone.now().date()
        results = []
        for course in courses:
            tests = Test.objects.filter(Q(end_date__gte=current_date) & 
                Q(step__lesson__topic__course_id__in=[course])).order_by('end_date')
            course_results = []
            for test in tests:
                course_results.append({
                    'id': test.id,
                    'title': test.title,
                    'description': test.description,
                    'left_days': (test.end_date - current_date).days,
                    'left_attempts': 4
                })
            results.append({
                'id': course.id,
                'title': course.title,
                'tasks': course_results
            })
        
        return JsonResponse(results, safe=False)