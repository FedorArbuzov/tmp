
from rest_framework import permissions
from rest_framework import views

from django.http import JsonResponse

from users.models import Topic, Lesson, Step, Test


def topic_breadcrumbs(id):
    topic = Topic.objects.get(id=id)
    course = topic.course
    result = []
    result.append({'title': course.title, 'id': course.id, 'type': 'course'})
    result.append({'title': topic.title, 'id': topic.id, 'type': 'topic'})
    return result


def lesson_breadcrumbs(id):
    lesson = Lesson.objects.get(id=id)
    previous_breadcrumbs = topic_breadcrumbs(lesson.topic.id)
    previous_breadcrumbs.append({'title': lesson.title, 'id': lesson.id, 'type': 'lesson'})
    return previous_breadcrumbs


def step_breadcrumbs(id):
    step = Step.objects.get(id=id)
    previous_breadcrumbs = lesson_breadcrumbs(step.lesson.id)
    previous_breadcrumbs.append({'title': step.title, 'id': step.id, 'type': 'step'})
    return previous_breadcrumbs

def test_breadcrumbs(id):
    test = Test.objects.get(id=id)    
    previous_breadcrumbs = step_breadcrumbs(test.step.id)
    previous_breadcrumbs.append({'title': test.title, 'id': test.id, 'type': 'step'})
    return previous_breadcrumbs


breadcrumbs = {
    'test': test_breadcrumbs,
    'step': step_breadcrumbs,
    'lesson': lesson_breadcrumbs,
    'topic': topic_breadcrumbs,
}

class BreadcrumbsView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    
    def get(self, request):
        model_type = request.GET.get('model_type')
        model_id = request.GET.get('model_id')

        return JsonResponse(breadcrumbs[model_type](model_id), safe=False)